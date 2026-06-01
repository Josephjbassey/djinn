from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.inclusion_tag('components/button.html')
def djinn_button(
    variant="primary",
    size="md",
    disabled=False,
    loading=False,
    label=None,
    class_name="",
    type="button",
    icon_left=None,
    icon_right=None,
    **attrs
):
    """
    Djinn Button component tag.
    Usage: {% djinn_button variant="outline" label="Cancel" %}
    """
    base = "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50"

    variants = {
        "primary": "bg-primary text-primary-foreground hover:bg-primary/90",
        "secondary": "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        "destructive": "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        "outline": "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        "ghost": "hover:bg-accent hover:text-accent-foreground",
        "link": "text-primary underline-offset-4 hover:underline",
    }

    sizes = {
        "sm": "h-9 rounded-md px-3",
        "md": "h-10 px-4 py-2",
        "lg": "h-11 rounded-md px-8",
        "icon": "h-10 w-10",
    }

    variant_class = variants.get(variant, variants["primary"])
    size_class = sizes.get(size, sizes["md"])

    final_classes = f"{base} {variant_class} {size_class} {class_name}"

    # Process extra attributes (convert underscore to hyphen)
    attr_string = ""
    for key, value in attrs.items():
        attr_string += f' {key.replace("_", "-")}="{value}"'

    return {
        "type": type,
        "disabled": disabled or loading,
        "class": final_classes.strip(),
        "attrs": mark_safe(attr_string),
        "label": label,
        "icon_left": icon_left,
        "icon_right": icon_right,
        "loading": loading,
    }
