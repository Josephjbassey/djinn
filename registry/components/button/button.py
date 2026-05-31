def get_button_classes(variant="primary", size="md", class_name=""):
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

    return f"{base} {variants.get(variant, variants['primary'])} {sizes.get(size, sizes['md'])} {class_name}"

def subtract(value, arg):
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return value
