from django import template
from django.template.base import token_kwargs
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

class ButtonNode(template.Node):
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
        
        # Evaluate cva
        final_class = button_cva(**resolved_kwargs)
        
        # Separate extra attributes
        known_args = ["variant", "size", "class", "class_name", "type", "disabled", "loading", "icon_left", "icon_right", "label"]
        attrs = {k: v for k, v in resolved_kwargs.items() if k not in known_args}
        
        # Render body
        slot = self.nodelist.render(context) if self.nodelist else ""
        
        t = context.template.engine.get_template('components/button.html')
        new_context = context.new({
            'class': final_class,
            'slot': slot,
            'attrs': attrs,
            **resolved_kwargs
        })
        return t.render(new_context)

@register.tag('djinn_button')
def djinn_button(parser, token):
    bits = token.split_contents()
    kwargs = token_kwargs(bits[1:], parser)
    nodelist = parser.parse(('enddjinn_button',))
    parser.delete_first_token()
    return ButtonNode(nodelist, kwargs)
