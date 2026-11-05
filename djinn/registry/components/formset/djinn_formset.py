from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()


def format_html_attrs(attrs):
    attr_list = []
    for key, attr_value in attrs.items():
        attr_list.append(f'{key.replace("_", "-")}="{escape(str(attr_value))}"')
    return mark_safe(" ".join(attr_list))


@register.inclusion_tag('components/formset.html')
def djinn_formset(
    formset=None,
    class_name="",
    can_add=True,
    **attrs
):
    """
    Djinn FormSet component tag.

    Renders a Django formset with management form, each form's fields,
    optional delete checkboxes, and Alpine.js-powered dynamic add/remove.

    Usage: {% djinn_formset formset=formset %}
           {% djinn_formset formset=formset class_name="max-w-xl mx-auto" can_add=True %}
           {% djinn_formset formset=formset can_add=False %}

    The template expects the formset to have been created with
    django.forms.formsets.formset_factory() and passed to the template
    context. Empty form rendering uses formset.empty_form.

    Security: {{ management_form }} and form fields are rendered with |safe
    because they come from Django's own form rendering, which is already
    escaped. User-controlled slot content should not be passed here.
    """
    if formset is None:
        return {
            "formset": None,
            "class": "",
            "can_add": False,
            "attrs": "",
        }

    return {
        "formset": formset,
        "class": class_name,
        "can_add": can_add,
        "attrs": format_html_attrs(attrs),
    }
