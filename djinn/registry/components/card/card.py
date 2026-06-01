from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.inclusion_tag('components/card.html')
def djinn_card(
    variant="default",
    title=None,
    description=None,
    footer=None,
    slot=None,
    class_name="",
    **attrs
):
    """
    Djinn Card component tag.
    Usage: {% djinn_card title="Card Title" description="Card Description" %}
    """
    variants = {
        "default": "rounded-lg border bg-card text-card-foreground shadow-sm",
        "bordered": "rounded-lg border-2 bg-card text-card-foreground",
        "elevated": "rounded-lg border bg-card text-card-foreground shadow-lg",
    }

    variant_class = variants.get(variant, variants["default"])
    final_classes = f"{variant_class} {class_name}"

    # Process extra attributes
    attr_string = ""
    for key, value in attrs.items():
        attr_string += f' {key.replace("_", "-")}="{value}"'

    return {
        "class": final_classes.strip(),
        "attrs": mark_safe(attr_string),
        "title": title,
        "description": description,
        "footer": footer,
        "slot": slot,
    }
