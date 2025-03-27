### JSON Format info

#### Validation
{% if validation is none %}
JSON `not parsed` with Validation Schema
{% elif validation %}
JSON is `Valid`
{% else %}
JSON is `not valid`
{% endif %}

#### Schema
JSON schema used to validation.
```json
{{ schema }}
```
