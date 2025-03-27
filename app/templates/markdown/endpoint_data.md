
#### Endpoint information
Information about the execution of KeFHIR server endpoint

##### Description: 
{{ endpoint_description | default('N/A') }}

##### Table info

| Endpoint path | Target Model ulr  | Model name | Context Window |
| ---------- | -------------- | ----------------- | ------------ |
| {{ endpoint_url | default('N/A') }} | {{ target_url | default('N/A') }} | {{ model_name | default('N/A') }} | {{context_window | default('N/A') }} |

{% if additional_prompt %}
##### Additional Prompt
{{additional_prompt}}
{% endif %}
{% if request %}
##### Request Information
{{request}}

{% endif %}
