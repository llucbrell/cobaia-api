from flask import request, jsonify
from ..models import Token, Endpoint, Role
from app.ia_tools.json_validator import JSONValidator
from app.ia_tools.html_jinja_ai_tools import JinjaHtmlTools
from app.ia_tools.chat_service import ModelCommunication
from app.ia_tools.markdown_reporter import MarkdownReporter
from app.ia_tools.dynamic_memory import DynamicMemoryEngine
from app.ia_tools.prompt_builder import SimplePrompt, DynamicPrompt
import json
from jsonfinder import jsonfinder


class EngineBuilder:
    def __init__(self, error_log_path="error_log.txt"):
        """
        Inicializa el motor de conversión de texto desestructurado a FHIR/json
        :param error_log_path: La ruta donde se guardarán los errores de validación.
        """
        self.error_log_path = error_log_path

    def run(self, endpoint, req_data):
        configs = {}
        jinjatools = JinjaHtmlTools()
        usage = None
        model_id_name = None
        # Inicializar el wrapper del tokenizador, con un archivo de log personalizado
        text = req_data.get("messages", [{}])[0].get("text", "")
        model_response = {
            "status": "initial"
            }


        chatsvc = ModelCommunication(endpoint=endpoint, error_log_path=self.error_log_path)
        json_schema = json.loads(endpoint.schema)
        # Si activamos la memoria ejecutamos
        if req_data.get("dynamicPromptModelMemory"):
            configs["memory"] = True
            dyn_engine = DynamicMemoryEngine(endpoint)
            dyn_engine.set_context_memory(text=text)
            err = dyn_engine.get_errors()
            if err is not None and len(err) > 0:  # Asegurarte de que err no sea None antes de usar len()
                return jsonify(kf_error=err)
            model_response = dyn_engine.run() 
            usage = dyn_engine.get_usage()
            num_tokens = None
        else:
            configs["memory"] = False
            prompter = SimplePrompt()
            prompt= prompter.get_simple_prompt(schema=json_schema, text=text, extra_prompt=endpoint.additional_prompt)
            model_response = chatsvc.send_to_model(prompt)
            simple_usage = chatsvc.get_usage()
            simple_usage["delay"] = chatsvc.get_response_time()
            usage = [simple_usage]
            num_tokens = None

        if model_response["status"] == "error":
            errmsg =model_response["message"]
            msg = f"Error with the model:\n{errmsg}"
            print(msg)
            json_data = None 
            return jsonify(kf_error=msg)

        configs["validation"] = False
        if req_data.get("validation"):
            configs["validation"] = True
            try:
                json_data_for_validation = model_response
            except json.JSONDecodeError as e:
                msg = f"Error parsing JSON, the model commit mistakes generating json file, try it again: {e}"
                print(msg)
                json_data = None 
                return jsonify(kf_error=msg)


            # Verificar si 'endpoint.schema' existe y no está vacío
            if endpoint.schema and isinstance(endpoint.schema, (str, dict)) and endpoint.schema != "":
                # Ahora comprobamos si el JSON no está vacío
                schema_data = json.loads(endpoint.schema) if isinstance(endpoint.schema, str) else endpoint.schema
                if schema_data:
                    print("JSON object it's not empty")
                    schema = endpoint.schema
                    # Inicializar el validador con un archivo de log personalizado
                    print("Data received for validation:")
                    print(json_data_for_validation)
                    
                    validator = JSONValidator(error_log_path=self.error_log_path)
                    if json_data_for_validation.get('status') == "success" or json_data_for_validation.get('status') == "ok":
                        extracted_json_for_validation = jsonfinder(json_data_for_validation.get('message'))
                        print("EXTRACTED")
                        #print(extracted_json_for_validation.get('message'))
                        is_valid = validator.validate_json(extracted_json_for_validation, json_schema)
                    else:
                        # Validar el JSON contra el esquema
                        is_valid = validator.validate_json(json_data_for_validation, json_schema)
                    print("JSONDATA")
                    print(json_data_for_validation)
                    print("JSONSCHEMA")
                    print(json_schema)
                    if is_valid:
                        print("El JSON es válido.")
                    else:
                        print("El JSON es inválido. Revisa los logs para más detalles.")
                else:
                    msg = "JSON object can't be an empty object"
                    print(msg)
                    return jsonify(kf_error=msg)
            else:
                msg = "JSON schema it's empty"
                print(msg)
                return jsonify(kf_error=msg)
 

            


        else:
            is_valid = None




        # Convertir el diccionario a JSON ojo, si el texto es muy largo esto puede ralentizar y bloquear el 
        #json_data = json.dumps(processed, default=list)  # Convertir sets a listas
        if "status" in model_response:
            sts = model_response["status"]
            if sts == "initial":
                return jsonify(error=f"Connection with model not stablished, something wrong happen. Please talk with the support I.T, not byt chat ;-)", type="text")
        
        report_response = None
        # Extraer objetos JSON del texto
        
        if "message" in model_response:
            model_response = model_response["message"]

        
        
            extracted_json = list(jsonfinder(model_response))
            # Filtrar solo los elementos que contienen objetos JSON (donde el tercer valor no es None)
            json_objects = [item[2] for item in extracted_json if item[2] is not None]

            print("REQ")
            print("REQ")
            print("REQ")
        
            print(extracted_json)
            print(json_objects)
            for json_obj in json_objects:
                # Generación del informe markdown
                report = MarkdownReporter( text=text, endpoint=endpoint)
                if req_data.get("reportMarkdown") == True:
                    print("EN REPORT GENERATION")
                    print("EN REPORT GENERATION")
                    print("EN REPORT GENERATION")
                    print("EN REPORT GENERATION")
                    print(str(usage))
                    configs["report"] = True
                    report.add_to_report(text=text, model_response=model_response, json_data=json_obj, is_valid=is_valid)

                report.mark_text_keys(text=text, json_array=json_objects)
            if usage:
                report.add_model_usage(usage=usage)
            print("CONFIGS")
            print(configs)
            report.add_kf_validation(validation=is_valid)
            report.add_kf_config(configs=configs)
            report.add_original_text(text=text)
            report_text = report.get_report()
            report_response = {
                "md": report_text
            }


        #for obj in extracted_json:
        #    print(obj)
        json_objects = "{}"
        

        return jsonify(kf_text=f"{model_response}", kf_type="text", kf_num_tokens=f"{num_tokens}", kf_is_valid=is_valid, kf_report=report_response, kf_json=json_objects)