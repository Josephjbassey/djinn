from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()

def format_html_attrs(attrs):
    attr_list = []
    for key, attr_value in attrs.items():
        attr_list.append(f'{key.replace("_", "-")}="{escape(str(attr_value))}"')
    return mark_safe(" ".join(attr_list))

@register.inclusion_tag('components/input.html')
def djinn_input(
    label=None,
    placeholder="",
    error=None,
    help_text=None,
    input_type="text",
    name=None,
    input_id=None,
    value="",
    disabled=False,
    required=False,
    class_name="",
    **attrs
):
    """
    Djinn Input component tag.
    Usage: {% djinn_input label="Email" type="email" placeholder="you@example.com" %}
    """
    return {
        "label": label,
        "placeholder": placeholder,
        "error": error,
        "help_text": help_text,
        "type": input_type,
        "name": name,
        "id": input_id or name,
        "value": value,
        "disabled": disabled,
        "required": required,
        "class": class_name,
        "attrs": format_html_attrs(attrs),
    }
