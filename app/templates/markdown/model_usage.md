{% if usage_list %}
### Usage
Data information about the execution of the model and the endpoint
#### Model usage

| Date       | Prompt Tokens  | Completion Tokens | Total Tokens | Model ID | Total time | Model Load time | LM Total Duration |
| ---------- | -------------- | ----------------- | ------------ | -------- | -------- |------------- | ----------------- |
{%- for usage in usage_list %}
| {{ usage.date | default('N/A') }} | {{ usage.prompt_tokens | default('N/A') }} | {{ usage.completion_tokens | default('N/A') }} | {{ usage.total_tokens | default('N/A') }} | {{ usage.model_id_name | default('N/A') | safe }} | {{ usage.delay | default('N/A') }} | {{ usage.load_duration | default('N/A') }} | {{ usage.total_duration | default('N/A') }} |
{%- endfor %}
{% endif %}
