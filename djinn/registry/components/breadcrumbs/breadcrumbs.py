from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()

def format_html_attrs(attrs):
    attr_list = []
    for key, attr_value in attrs.items():
        attr_list.append(f'{key.replace("_", "-")}="{escape(str(attr_value))}"')
    return mark_safe(" ".join(attr_list))

@register.inclusion_tag('components/breadcrumbs.html')
def djinn_breadcrumbs(class_name="", **attrs):
    """
    Djinn Breadcrumbs component tag.
    """
    return {
        "class": class_name,
        "attrs": format_html_attrs(attrs),
    }
