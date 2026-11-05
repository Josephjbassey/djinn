from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()


def format_html_attrs(attrs):
    attr_list = []
    for key, attr_value in attrs.items():
        attr_list.append(f'{key.replace("_", "-")}="{escape(str(attr_value))}"')
    return mark_safe(" ".join(attr_list))


@register.inclusion_tag('components/pagination.html')
def djinn_pagination(
    page_obj=None,
    class_name="",
    **attrs
):
    """
    Djinn Pagination component tag.

    Renders an accessible pagination control using Django's Paginator page_obj.
    Supports HTMX for partial page updates (hx-get/hx-target) but works without
    HTMX as plain form links can be added manually.

    Usage: {% djinn_pagination page_obj=page_obj %}
           {% djinn_pagination page_obj=page_obj class_name="max-w-xl mx-auto" %}

    Requires Django's Paginator page_obj in context. Renders Previous/Next
    buttons, ellipsis for skipped pages, and the current page highlighted.

    Accessibility: Uses <nav aria-label="Pagination">, aria-label on all
    buttons, and disabled states on boundary buttons when at first/last page.
    """
    if page_obj is None:
        return {
            "page_obj": None,
            "class": "",
            "attrs": "",
        }

    return {
        "page_obj": page_obj,
        "class": class_name,
        "attrs": format_html_attrs(attrs),
    }
