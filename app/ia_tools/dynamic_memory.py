from app.ia_tools.tokenizer import TokenizerWrapper
from app.ia_tools.prompt_builder import SimplePrompt, DynamicPrompt
from app.ia_tools.text_divider import TextDivider
from app.ia_tools.chat_service import ModelCommunication
import json
from jsonfinder import jsonfinder

class DynamicMemoryEngine:
    def __init__(self, endpoint, error_log_path="error_log.txt"):
        self.endpoint = endpoint
        """
        Ejecuta el request del modelo usando la memoria dinámica de prompt
        :param error_log_path: La ruta donde se guardarán los errores de validación.
        """
        self.min_prompt_tokens = 500
        self.min_prompt_tokens_for_text = 100
        
        self.security_tokens_space = 500
        self.offset = 0.1
        self.error_log_path = error_log_path
        self.total_text_tokens = 0
        self.kf_error = None
        self.endpoint = endpoint
        self.text = None
        self.tokenizer = TokenizerWrapper(error_log_path=self.error_log_path)
        self.initial_promt = None
        self.repeat_prompt = None
        self.prompter = DynamicPrompt()
        self.cumulative_usage = []
        self.additional_prompt = endpoint.additional_prompt
        
 

    def set_context_memory(self, text):
        """
        Establece la memoria dinámica, contando y dividiendo el texto en tokens
        :param text: el texto a parsear.
        """
        self.text = text
        self.set_min_prompt_tokens()
        print(self.min_prompt_tokens)
        # Verificar si 'context_window' existe y no está vacío
        if self.endpoint.model_context_window & self.endpoint.model_context_window > self.min_prompt_tokens:
                tokens =self.tokenizer.tokenize(text)
                # Contar el número de tokens
                num_tokens = self.tokenizer.count_tokens(tokens)
                # establecemos variables para reutilizarlas después en la ejecución
                self.total_text_tokens = num_tokens
                self.max_prompt_tokens = self.min_prompt_tokens + self.schema_tokens
                self.remaining_prompt_tokens = self.endpoint.model_context_window - self.max_prompt_tokens
                self.tokens_for_text = self.remaining_prompt_tokens - self.schema_tokens
                if self.tokens_for_text < self.min_prompt_tokens_for_text:
                    self.kf_error = f"Model Context Window out of bounds, please push up the context window size or change the model, now you have {self.tokens_for_text} tokens availables for parsing text. try to push up to at least {self.min_prompt_tokens_for_text}"
        else:
            msg = f"If Dynamic Memory is activated, the Context Window must be set at least {self.min_prompt_tokens} tokens"
            print(msg)
            self.kf_error = msg
            return 
    
    def run(self):
        slicer = TextDivider()
        partes = slicer.token_slice(self.text, self.tokens_for_text, self.offset)
        #for i, parte in enumerate(partes):
        #    print(f"Parte {i+1}:\n{parte}\n")
        prompter = DynamicPrompt()
        chatsvc = ModelCommunication(endpoint=self.endpoint, error_log_path=self.error_log_path)

        dynamic_mem_data = {}
        self.last_response = ""
        for part, index in enumerate(partes):
            if index == 0:
                prompt= prompter.get_initial_prompt(schema=self.endpoint.schema, text=self.text, extra_prompt=self.additional_prompt)
            else:
                prompt= prompter.get_reptition_prompt(schema=self.endpoint.schema, json_object=dynamic_mem_data, text=self.text , extra_prompt=self.additional_prompt)
            model_response = chatsvc.send_to_model(prompt) 

            if "message" in model_response:
                model_response = model_response["message"]
            # Extraer objetos JSON del texto
            extracted_json = list(jsonfinder(model_response))
            # Filtrar solo los elementos que contienen objetos JSON (donde el tercer valor no es None)
            json_objects = [item[2] for item in extracted_json if item[2] is not None]
            for json_obj in json_objects:
                dynamic_mem_data = json_obj

            usage = chatsvc.get_usage()
            usage["delay"] = chatsvc.get_response_time()
            self.cumulative_usage.append(usage)
            self.last_response = model_response
        return {"status": "ok", "message": self.last_response}

    def get_usage(self):
        return self.cumulative_usage

    def set_min_prompt_tokens(self):
        additional_prompt = getattr(self.endpoint, 'additional_prompt', '')
        repetition_prompt = self.prompter.get_reptition_prompt(
            schema=self.endpoint.schema, 
            text="", 
            json_object=self.endpoint.schema, 
            extra_prompt=additional_prompt  # Pasar el valor predeterminado si no existe
        )

        #print(repetition_prompt)
        tokens_template_init = self.tokenizer.tokenize(repetition_prompt)
        
        #print(tokens_template_init)
        
        schema = getattr(self.endpoint, 'schema', '')
        if schema:
            schema_size = self.tokenizer.tokenize(repetition_prompt)
            
        else:
             schema = ""

        schema_tokens = self.tokenizer.tokenize(schema)
        self.schema_tokens = self.tokenizer.count_tokens(schema_tokens)
        self.min_prompt_tokens = self.tokenizer.count_tokens(tokens_template_init)
    
    def get_errors(self):
        print(self.kf_error)
        return self.kf_error