# Report

Automatically generated report, used to check model precision and help in handheld reviews.
### Results
#### Extracted JSON 1


`
```json
{
    "birthDate": "14-05-2014",
    "contact": {
        "relationship": {
            "properties": {
                "coding": {
                    "type": "object"
                },
                "type": "object"
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
            "system": {
                "type": "string"
            },
            "value": "null"
        }
    },
    "extension": {
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
        },
        "required": [
            "relationship",
            "telecom"
        ],
        "type": "object"
    },
    "gender": "male",
    "id": "PatientHulafe",
    "identifier": [
        {
            "system": "http://hl7.eu/fhir/ig/pcsp/sid/pat-id-hulafe",
            "value": "04969377"
        }
    ],
    "type": "array"
}
```
`


#### Data found in text


SOAP note example for counselors
Subjective
David states that he continues to experience cravings for heroin. He desperately wants to drop out of his methadone program and revert to what he was doing. David is motivated to stay sober by his daughter and states that he is "sober but still experiencing terrible withdrawals." He stated that [he] "dreams about heroin all the time and constantly wakes in the night drenched in sweat."

Objective
David arrived promptly for his appointment, completing his patient information sheet in the waiting room while exhibiting a pleasant demeanor during the session. He displayed no signs of intoxication.

While David still exhibits heightened arousal and some distractibility, his ability to focus has improved. This was evident during his sustained engagement in a fifteen-minute discussion about his partner and his capacity for self-reflection. Additionally, David demonstrated a marked improvement in personal hygiene and self-care. His recent physical exam also revealed a weight gain of 3 pounds.

Assessment
David demonstrates encouraging progress in his treatment journey. He actively utilizes coping mechanisms, ranging from control techniques to exercises, resulting in a decrease in his cravings, dropping from "constant" to "a few times an hour." This signifies his active engagement and positive response to treatment.

However, it is crucial to acknowledge that David still experiences regular cravings, indicative of his ongoing struggle. Coupled with his history of five years of heroin use, it underscores the need for further support. David would benefit from acquiring and implementing additional coping skills to consolidate his gains and progress toward sustainable recovery.

Therefore, considering both his current progress and the underlying factors related to his substance use, David would likely benefit from the addition of Cognitive Behavioral Therapy (CBT) alongside his current methadone treatment. Integrating CBT can equip him with valuable tools for managing triggers, challenging negative thoughts, and developing healthy coping mechanisms, ultimately enhancing his long-term recovery potential.

Plan
David has received a significant amount of psychoeducation within his therapy sessions. The therapist will begin to use dialectical behavioral therapy techniques to address David's emotional dysregulation. David also agreed to continue to hold family therapy sessions with his wife. Staff will continue to monitor David regularly in the interest of patient care and his past medical history.

#### Original Text


SOAP note example for counselors
Subjective
David states that he continues to experience cravings for heroin. He desperately wants to drop out of his methadone program and revert to what he was doing. David is motivated to stay sober by his daughter and states that he is "sober but still experiencing terrible withdrawals." He stated that [he] "dreams about heroin all the time and constantly wakes in the night drenched in sweat."

Objective
David arrived promptly for his appointment, completing his patient information sheet in the waiting room while exhibiting a pleasant demeanor during the session. He displayed no signs of intoxication.

While David still exhibits heightened arousal and some distractibility, his ability to focus has improved. This was evident during his sustained engagement in a fifteen-minute discussion about his partner and his capacity for self-reflection. Additionally, David demonstrated a marked improvement in personal hygiene and self-care. His recent physical exam also revealed a weight gain of 3 pounds.

Assessment
David demonstrates encouraging progress in his treatment journey. He actively utilizes coping mechanisms, ranging from control techniques to exercises, resulting in a decrease in his cravings, dropping from "constant" to "a few times an hour." This signifies his active engagement and positive response to treatment.

However, it is crucial to acknowledge that David still experiences regular cravings, indicative of his ongoing struggle. Coupled with his history of five years of heroin use, it underscores the need for further support. David would benefit from acquiring and implementing additional coping skills to consolidate his gains and progress toward sustainable recovery.

Therefore, considering both his current progress and the underlying factors related to his substance use, David would likely benefit from the addition of Cognitive Behavioral Therapy (CBT) alongside his current methadone treatment. Integrating CBT can equip him with valuable tools for managing triggers, challenging negative thoughts, and developing healthy coping mechanisms, ultimately enhancing his long-term recovery potential.

Plan
David has received a significant amount of psychoeducation within his therapy sessions. The therapist will begin to use dialectical behavioral therapy techniques to address David's emotional dysregulation. David also agreed to continue to hold family therapy sessions with his wife. Staff will continue to monitor David regularly in the interest of patient care and his past medical history.


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
| telecom_items_value | null |
| birthDate | 14-05-2014 |
| contact_relationship_properties_coding_type | object |
| contact_relationship_properties_type | object |
| contact_relationship_required_0 | coding |
| contact_relationship_type | object |
| contact_type | array |
| telecom_items_system_type | string |
| extension_url_type | string |
| extension_valueAddress_properties_city_type | string |
| extension_valueAddress_properties_country_type | string |
| extension_valueAddress_properties_postalCode_type | string |
| extension_valueAddress_required_1 | country |
| extension_valueAddress_required_2 | postalCode |
| extension_valueAddress_type | object |
| extension_required_0 | relationship |
| extension_required_1 | telecom |
| extension_type | object |
| gender | male |
| id | PatientHulafe |
| identifier_0_system | http://hl7.eu/fhir/ig/pcsp/sid/pat-id-hulafe |
| identifier_0_value | 04969377 |
| type | array |

##### Configuration

- [x] Validation
- [ ] Model Prompt Dynamic Memory
- [x] Report
### Usage
Data information about the execution of the model and the endpoint
#### Model usage

| Date       | Prompt Tokens  | Completion Tokens | Total Tokens | Model ID | Total time | Model Load time | LM Total Duration |
| ---------- | -------------- | ----------------- | ------------ | -------- | -------- |------------- | ----------------- |
| 2025-04-12 | 1471 | 368 | 1839 | gemma3:1b | 47.511 | 0.120s | 47.499s |

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

