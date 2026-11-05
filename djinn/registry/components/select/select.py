from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()


def format_html_attrs(attrs):
    attr_list = []
    for key, attr_value in attrs.items():
        attr_list.append(f'{key.replace("_", "-")}="{escape(str(attr_value))}"')
    return mark_safe(" ".join(attr_list))


@register.inclusion_tag('components/select.html')
def djinn_select(
    label=None,
    placeholder="",
    error=None,
    help_text=None,
    name=None,
    select_id=None,
    disabled=False,
    required=False,
    class_name="",
    **attrs
):
    """
    Djinn Select component tag.
    """
    return {
        "label": label,
        "placeholder": placeholder,
        "error": error,
        "help_text": help_text,
        "name": name,
        "id": select_id or name,
        "disabled": disabled,
        "required": required,
        "class": class_name,
        "attrs": format_html_attrs(attrs),
    }
