{% for post in posts %}
# {{ post.posting_datetime_string.strftime("%d.%m.%Y") }}: {{ post.subject }}

{{ post.content }}

Тэги: **{{ post.tags }}**
{% endfor %}
