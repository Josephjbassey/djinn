from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
from djinn.core.cva import cva

register = template.Library()

button_cva = cva(
    base="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
    variants={
        "variant": {
            "default": "bg-primary text-primary-foreground hover:bg-primary/90",
            "destructive": "bg-destructive text-destructive-foreground hover:bg-destructive/90",
            "outline": "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
            "secondary": "bg-secondary text-secondary-foreground hover:bg-secondary/80",
            "ghost": "hover:bg-accent hover:text-accent-foreground",
            "link": "text-primary underline-offset-4 hover:underline",
        },
        "size": {
            "default": "h-10 px-4 py-2",
            "sm": "h-9 rounded-md px-3",
            "lg": "h-11 rounded-md px-8",
            "icon": "h-10 w-10",
        }
    },
    default_variants={
        "variant": "default",
        "size": "default"
    }
)


def format_html_attrs(attrs):
    attr_list = []
    for key, attr_value in attrs.items():
        attr_list.append(f'{key.replace("_", "-")}="{escape(str(attr_value))}"')
    return mark_safe(" ".join(attr_list))


@register.inclusion_tag('components/button.html')
def djinn_button(
    variant="default",
    size="default",
    class_name="",
    type="button",
    disabled=False,
    loading=False,
    icon_left=None,
    icon_right=None,
    label=None,
    aria_label=None,
    aria_pressed=False,
    **attrs
):
    """
    Djinn Button component tag.
    Usage: {% djinn_button variant="destructive" size="lg" label="Delete" aria_label="Delete item" %}
    """
    final_class = button_cva(variant=variant, size=size, class_=class_name)
    return {
        "class": final_class,
        "type": type,
        "disabled": disabled,
        "loading": loading,
        "icon_left": icon_left,
        "icon_right": icon_right,
        "label": label,
        "aria_label": aria_label,
        "aria_pressed": aria_pressed,
        "attrs": format_html_attrs(attrs),
    }
