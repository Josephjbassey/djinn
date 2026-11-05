from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()


def format_html_attrs(attrs):
    attr_list = []
    for key, attr_value in attrs.items():
        attr_list.append(f'{key.replace("_", "-")}="{escape(str(attr_value))}"')
    return mark_safe(" ".join(attr_list))


@register.inclusion_tag('components/modal.html')
def djinn_modal(
    id="modal",
    title="",
    description="",
    footer=None,
    class_name="",
    **attrs
):
    """
    Djinn Modal component tag.

    Usage: {% djinn_modal id="my-modal" title="Title" %}
           {% djinn_modal id="my-modal" title="Title" description="Description" %}

    To open the modal from a button, use djinn_modal_trigger:
    {% djinn_modal_trigger "my-modal" label="Open Modal" %}
    """
    return {
        "id": id,
        "title": title,
        "description": description,
        "footer": footer,
        "class": class_name,
        "attrs": format_html_attrs(attrs),
    }


@register.simple_tag
def djinn_modal_trigger(modal_id, label="Open", class_name="", **attrs):
    """
    Render a button that opens a modal via CustomEvent.

    Usage: {% djinn_modal_trigger "my-modal" label="Edit User" %}
    """
    escaped_attrs = format_html_attrs(attrs)
    escaped_label = escape(str(label))
    click_handler = (
        'dispatchEvent(new CustomEvent("open-modal", '
        '{ detail: { id: "' + modal_id + '" } }))'
    )
    return mark_safe(
        '<button type="button" '
        '@click="' + click_handler + '" '
        'class="' + escape(str(class_name)) + '" ' + escaped_attrs + ">"
        + escaped_label +
        "</button>"
    )
