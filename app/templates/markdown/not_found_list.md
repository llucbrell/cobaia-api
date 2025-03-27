
{% if words_not_found %}
#### Decoupled Concepts

| Concept Key  | Value         |
| ------------ | ------------- |
{%- for word in words_not_found %}
| {{ word.key | safe }} | {{ (word.value | safe) if word.value is not none else "null" }} |
{%- endfor %}
{% endif %}
