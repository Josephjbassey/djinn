from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()

def format_html_attrs(attrs):
    attr_list = []
    for key, attr_value in attrs.items():
        attr_list.append(f'{key.replace("_", "-")}="{escape(str(attr_value))}"')
    return mark_safe(" ".join(attr_list))

@register.inclusion_tag('components/icon-button.html')
def djinn_icon_button(class_name="", **attrs):
    """
    Djinn Icon-button component tag.
    """
    return {
        "class": class_name,
        "attrs": format_html_attrs(attrs),
    }
