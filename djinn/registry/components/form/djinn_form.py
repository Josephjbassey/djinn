from django import template
from django.template.base import token_kwargs
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()


def format_html_attrs(attrs):
    attr_list = []
    for key, attr_value in attrs.items():
        attr_list.append(f'{key.replace("_", "-")}="{escape(str(attr_value))}"')
    return mark_safe(" ".join(attr_list))


KNOWN_FORM_ARGS = {
    "form", "method", "action", "class", "class_name", "id",
    "csrf_token", "non_field_errors", "fields", "slot",
}


class FormNode(template.Node):
    def __init__(self, nodelist, kwargs):
        self.nodelist = nodelist
        self.kwargs = kwargs

    def render(self, context):
        resolved_kwargs = {}
        for k, v in self.kwargs.items():
            try:
                resolved_kwargs[k] = v.resolve(context)
            except template.VariableDoesNotExist:
                resolved_kwargs[k] = ""

        form = resolved_kwargs.get("form")
        if form is None or not hasattr(form, "fields"):
            return ""

        # CSRF token from context
        csrf_token = context.get("csrf_token", "")

        # Non-field errors
        non_field_errors = form.non_field_errors() if hasattr(form, "non_field_errors") else []

        # Render each field using form_field template
        field_html_parts = []
        for bound_field in form:
            field_ctx = context.new({"field": bound_field})
            t = context.template.engine.get_template('components/form_field.html')
            field_rendered = t.render(field_ctx)
            field_html_parts.append(field_rendered)

        fields_html = "\n".join(field_html_parts)

        # Render slot content (submit button, etc.)
        slot = self.nodelist.render(context) if self.nodelist else ""

        # Only pass extra attributes (not known form args) to the form tag
        extra_attrs = {
            k: v for k, v in resolved_kwargs.items()
            if k not in KNOWN_FORM_ARGS
        }

        t = context.template.engine.get_template('components/form.html')
        new_context = context.new({
            "form": form,
            "csrf_token": csrf_token,
            "non_field_errors": non_field_errors,
            "fields": fields_html,
            "slot": slot,
            "method": resolved_kwargs.get("method", "post"),
            "action": resolved_kwargs.get("action", ""),
            "class": resolved_kwargs.get("class", ""),
            "id": resolved_kwargs.get("id", ""),
            "attrs": format_html_attrs(extra_attrs),
        })
        return t.render(new_context)


@register.tag('djinn_form')
def djinn_form(parser, token):
    bits = token.split_contents()
    kwargs = token_kwargs(bits[1:], parser)
    nodelist = parser.parse(('enddjinn_form',))
    parser.delete_first_token()
    return FormNode(nodelist, kwargs)
