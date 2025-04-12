# Report

Automatically generated report, used to check model precision and help in handheld reviews.
### Results
#### Extracted JSON 1


`
```json
{
    "resourceType": "Patient",
    "id": "PatientHulafe",
    "meta": {
        "profile": [
            "http://hl7.eu/fhir/ig/ig/pcsp/StructureDefinition/Patient-eu-pcsp"
        ]
    },
    "identifier": [
        {
            "system": "http://hl7.eu/fhir/ig/ig/pcsp/sid/pat-id-hulafe"
        },
        {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/CoreLabel",
                    "code": "pat",
                    "display": "Patient"
                }
            ]
        }
    ],
    "name": [
        {
            "family": "Blasco",
            "given": [
                "Manuel"
            ]
        }
    ],
    "gender": "male",
    "birthDate": "14-05-2014",
    "telecom": null,
    "type": [
        "array"
    ],
    "extension": [
        {
            "url": "http://hl7.org/fhir/StructureDefinition/patient-appointment",
            "value": "http://example.org"
        }
    ],
    "note": "David is experiencing increased anxiety and distraction, which has improved. He is seeking support to address his cravings and return to his previous routine. Therapy continues to be essential for fostering long-term recovery and mitigating relapse risk.  The TCC integration will provide valuable tools to enhance his coping mechanisms and increase his self-efficacy."
}
```
`


#### Data found in text


Ejemplo de nota SOAP para consejeros
Subjetivo
David afirma que sigue teniendo antojos de heroína. Quiere desesperadamente abandonar su programa de metadona y volver a lo que estaba haciendo. Su hija lo motiva a mantenerse sobrio y afirma que está «sobrio, pero que sigue teniendo una terrible abstinencia». Afirmó que «sueña con la heroína todo el tiempo y se despierta constantemente por la noche empapado de sudor».

Objetivo
David llegó puntualmente a su cita, completando su hoja de información para el paciente en la sala de espera y exhibiendo una actitud agradable durante la sesión. No mostró signos de intoxicación.

Si bien David todavía muestra una mayor excitación y cierta capacidad de distracción, su capacidad de concentración ha mejorado. Esto se hizo evidente durante su participación sostenida en una conversación de quince minutos sobre su pareja y su capacidad de autorreflexión. Además, David demostró una mejora notable en la higiene personal y el cuidado personal. Su examen físico reciente también reveló un aumento de peso de 3 libras.

Evaluación
David demuestra un progreso alentador en su proceso de tratamiento. Utiliza activamente mecanismos de afrontamiento, que van desde técnicas de control hasta ejercicios, lo que reduce sus antojos, que pasan de «constantes» a «unas pocas veces por hora». Esto significa su compromiso activo y su respuesta positiva al tratamiento.

Sin embargo, es crucial reconocer que David todavía tiene antojos regulares, lo que indica su lucha continua. Esto, sumado a su historial de cinco años de consumo de heroína, subraya la necesidad de recibir más apoyo. Para consolidar sus logros y avanzar hacia una recuperación sostenible, David se beneficiaría si adquiriera e implementara habilidades de afrontamiento adicionales.

Por lo tanto, teniendo en cuenta tanto su progreso actual como los factores subyacentes relacionados con su consumo de sustancias, es probable que David se beneficie de la adición de la terapia cognitivo-conductual (TCC) junto con su tratamiento actual con metadona. La integración de la terapia cognitiva conductual puede proporcionarle herramientas valiosas para controlar los factores desencadenantes, desafiar los pensamientos negativos y desarrollar mecanismos de afrontamiento saludables y, en última instancia, mejorar su potencial de recuperación a largo plazo.

Planear
David ha recibido una cantidad significativa de psicoeducación durante su sesión de terapia. El terapeuta comenzará a utilizar técnicas de terapia conductual dialéctica para abordar la desregulación emocional de David. David también accedió a seguir realizando sesiones de terapia familiar con su esposa. El personal continuará monitoreando a David con regularidad en aras de la atención del paciente y de su historial médico anterior.

#### Original Text


Ejemplo de nota SOAP para consejeros
Subjetivo
David afirma que sigue teniendo antojos de heroína. Quiere desesperadamente abandonar su programa de metadona y volver a lo que estaba haciendo. Su hija lo motiva a mantenerse sobrio y afirma que está «sobrio, pero que sigue teniendo una terrible abstinencia». Afirmó que «sueña con la heroína todo el tiempo y se despierta constantemente por la noche empapado de sudor».

Objetivo
David llegó puntualmente a su cita, completando su hoja de información para el paciente en la sala de espera y exhibiendo una actitud agradable durante la sesión. No mostró signos de intoxicación.

Si bien David todavía muestra una mayor excitación y cierta capacidad de distracción, su capacidad de concentración ha mejorado. Esto se hizo evidente durante su participación sostenida en una conversación de quince minutos sobre su pareja y su capacidad de autorreflexión. Además, David demostró una mejora notable en la higiene personal y el cuidado personal. Su examen físico reciente también reveló un aumento de peso de 3 libras.

Evaluación
David demuestra un progreso alentador en su proceso de tratamiento. Utiliza activamente mecanismos de afrontamiento, que van desde técnicas de control hasta ejercicios, lo que reduce sus antojos, que pasan de «constantes» a «unas pocas veces por hora». Esto significa su compromiso activo y su respuesta positiva al tratamiento.

Sin embargo, es crucial reconocer que David todavía tiene antojos regulares, lo que indica su lucha continua. Esto, sumado a su historial de cinco años de consumo de heroína, subraya la necesidad de recibir más apoyo. Para consolidar sus logros y avanzar hacia una recuperación sostenible, David se beneficiaría si adquiriera e implementara habilidades de afrontamiento adicionales.

Por lo tanto, teniendo en cuenta tanto su progreso actual como los factores subyacentes relacionados con su consumo de sustancias, es probable que David se beneficie de la adición de la terapia cognitivo-conductual (TCC) junto con su tratamiento actual con metadona. La integración de la terapia cognitiva conductual puede proporcionarle herramientas valiosas para controlar los factores desencadenantes, desafiar los pensamientos negativos y desarrollar mecanismos de afrontamiento saludables y, en última instancia, mejorar su potencial de recuperación a largo plazo.

Planear
David ha recibido una cantidad significativa de psicoeducación durante su sesión de terapia. El terapeuta comenzará a utilizar técnicas de terapia conductual dialéctica para abordar la desregulación emocional de David. David también accedió a seguir realizando sesiones de terapia familiar con su esposa. El personal continuará monitoreando a David con regularidad en aras de la atención del paciente y de su historial médico anterior.


### JSON Format info

#### Validation

JSON is `not valid`


#### Schema
JSON schema used to validation.
```json
{
    "properties": {
        "birthDate": {
            "type": "string"
        },
        "contact": {
            "items": {
                "properties": {
                    "relationship": {
                        "items": {
                            "properties": {
                                "coding": {
                                    "items": {
                                        "properties": {
                                            "code": {
                                                "type": "string"
                                            },
                                            "display": {
                                                "type": "string"
                                            },
                                            "system": {
                                                "type": "string"
                                            }
                                        },
                                        "required": [
                                            "code",
                                            "display",
                                            "system"
                                        ],
                                        "type": "object"
                                    },
                                    "type": "array"
                                }
                            },
                            "required": [
                                "coding"
                            ],
                            "type": "object"
                        },
                        "type": "array"
                    },
                    "telecom": {
                        "items": {
                            "properties": {
                                "system": {
                                    "type": "string"
                                },
                                "value": {
                                    "type": "string"
                                }
                            },
                            "required": [
                                "system",
                                "value"
                            ],
                            "type": "object"
                        },
                        "type": "array"
                    }
                },
                "required": [
                    "relationship",
                    "telecom"
                ],
                "type": "object"
            },
            "type": "array"
        },
        "extension": {
            "items": {
                "properties": {
                    "url": {
                        "type": "string"
                    },
                    "valueAddress": {
                        "properties": {
                            "city": {
                                "type": "string"
                            },
                            "country": {
                                "type": "string"
                            },
                            "postalCode": {
                                "type": "string"
                            }
                        },
                        "required": [
                            "city",
                            "country",
                            "postalCode"
                        ],
                        "type": "object"
                    }
                },
                "required": [
                    "url",
                    "valueAddress"
                ],
                "type": "object"
            },
            "type": "array"
        },
        "gender": {
            "type": "string"
        },
        "id": {
            "type": "string"
        },
        "identifier": {
            "items": {
                "properties": {
                    "system": {
                        "type": "string"
                    },
                    "value": {
                        "type": "string"
                    }
                },
                "required": [
                    "system",
                    "value"
                ],
                "type": "object"
            },
            "type": "array"
        },
        "meta": {
            "properties": {
                "profile": {
                    "items": {
                        "type": "string"
                    },
                    "type": "array"
                }
            },
            "required": [
                "profile"
            ],
            "type": "object"
        },
        "name": {
            "items": {
                "properties": {
                    "family": {
                        "type": "string"
                    },
                    "given": {
                        "items": {
                            "type": "string"
                        },
                        "type": "array"
                    }
                },
                "required": [
                    "family",
                    "given"
                ],
                "type": "object"
            },
            "type": "array"
        },
        "resourceType": {
            "type": "string"
        },
        "text": {
            "properties": {
                "div": {
                    "type": "string"
                },
                "status": {
                    "type": "string"
                }
            },
            "required": [
                "div",
                "status"
            ],
            "type": "object"
        }
    },
    "required": [
        "birthDate",
        "gender",
        "id",
        "identifier",
        "meta",
        "name",
        "resourceType"
    ],
    "type": "object"
}
```



#### Decoupled Concepts

| Concept Key  | Value         |
| ------------ | ------------- |
| telecom | null |
| resourceType | Patient |
| id | PatientHulafe |
| meta_profile_0 | http://hl7.eu/fhir/ig/ig/pcsp/StructureDefinition/Patient-eu-pcsp |
| identifier_0_system | http://hl7.eu/fhir/ig/ig/pcsp/sid/pat-id-hulafe |
| identifier_1_coding_0_system | http://terminology.hl7.org/CodeSystem/CoreLabel |
| identifier_1_coding_0_code | pat |
| identifier_1_coding_0_display | Patient |
| name_0_family | Blasco |
| name_0_given_0 | Manuel |
| gender | male |
| birthDate | 14-05-2014 |
| type_0 | array |
| extension_0_url | http://hl7.org/fhir/StructureDefinition/patient-appointment |
| extension_0_value | http://example.org |
| note | David is experiencing increased anxiety and distraction, which has improved. He is seeking support to address his cravings and return to his previous routine. Therapy continues to be essential for fostering long-term recovery and mitigating relapse risk.  The TCC integration will provide valuable tools to enhance his coping mechanisms and increase his self-efficacy. |

##### Configuration

- [x] Validation
- [ ] Model Prompt Dynamic Memory
- [x] Report
### Usage
Data information about the execution of the model and the endpoint
#### Model usage

| Date       | Prompt Tokens  | Completion Tokens | Total Tokens | Model ID | Total time | Model Load time | LM Total Duration |
| ---------- | -------------- | ----------------- | ------------ | -------- | -------- |------------- | ----------------- |
| 2025-04-12 | 1581 | 571 | 2152 | gemma3:1b | 58.621 | 4.264s | 58.542s |

#### Endpoint information
Information about the execution of KeFHIR server endpoint

##### Description: 
N/A

##### Table info

| Endpoint path | Target Model ulr  | Model name | Context Window |
| ---------- | -------------- | ----------------- | ------------ |
| patient | http://127.0.0.1:11434/api/generate | gemma3:1b | None |


##### Additional Prompt
Take in account that resourceType is allways Patient, id is the uuid given by the user to send to the fhir server, meta.profile is allways required and is allways the same, identifier is the business identifier or SIP from La Fe, spanish names has multiple posibilities, single or composed given names (like María or Jose Antonio) and two surnames, so name must have both, given and family, if patient has more than one given name, use it, and for family name include onlye the first surname. Finally for gender, only have 2 options, male and female. 
Here you have an example
{
  "resourceType" : "Patient",
  "id" : "PatientHulafe",
  "meta" : {
    "profile" : ["http://hl7.eu/fhir/ig/pcsp/StructureDefinition/Patient-eu-pcsp"]
  },
  "identifier" : [{
    "system" : "http://hl7.eu/fhir/ig/pcsp/sid/pat-id-hulafe",
    "value" : "04969377"
  }],
  "name" : [{
    "family" : "Blasco",
    "given" : ["Manuel"]
  }],
  "gender" : "male",
  "birthDate" : "14-05-2014",
} If you don't find any of the data from the user input don't include that in the json output. Very important, don't sorround the json 


##### Request Information
{
    "url": "{{url}}",
    "payload": {
         "model": "{{model_name}}",
        "prompt": "{{prompt}}",
        "stream": false
    },
    "headers": {
        "Content-Type": "application/json"
    }
}

