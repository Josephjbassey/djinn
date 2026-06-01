from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.inclusion_tag('components/input.html')
def djinn_input(
    label=None,
    placeholder="",
    error=None,
    help_text=None,
    type="text",
    name=None,
    id=None,
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
    base = "flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"

    if error:
        base += " border-destructive"

    final_classes = f"{base} {class_name}"

    # Process extra attributes
    attr_string = ""
    for key, value in attrs.items():
        attr_string += f' {key.replace("_", "-")}="{value}"'

    return {
        "label": label,
        "placeholder": placeholder,
        "error": error,
        "help_text": help_text,
        "type": type,
        "name": name,
        "id": id or name,
        "value": value,
        "disabled": disabled,
        "required": required,
        "class": final_classes.strip(),
        "attrs": mark_safe(attr_string),
    }
