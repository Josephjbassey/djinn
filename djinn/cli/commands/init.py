import click
import os
from djinn.core.config import Config, DEFAULT_CONFIG

@click.command()
@click.option("--yes", "-y", is_flag=True, help="Skip interactive prompts and use defaults.")
@click.option("--defaults", is_flag=True, help="Skip interactive prompts and use defaults.")
@click.option("--force", "-f", is_flag=True, help="Force overwrite of existing configuration.")
@click.option("--cwd", "-c", default=".", help="The working directory. Defaults to the current directory.")
@click.option("--framework", default="django", help="Target framework (e.g. django, flask, fastapi).")
@click.option("--engine", default="django", help="Template engine (e.g. django, jinja).")
@click.option("--style", default="default", help="Component style (e.g. default, new-york).")
@click.option("--color", default="zinc", help="Base color (e.g. slate, zinc).")
@click.option("--radius", default="0.5rem", help="Border radius (e.g. 0, 0.3rem, 0.5rem).")
@click.option("--no-css-variables", is_flag=True, help="Do not use CSS variables for theming.")
def init(yes, defaults, force, cwd, framework, engine, style, color, radius, no_css_variables):
    """Initialize Djinn in the current project."""
    
    if cwd != ".":
        os.chdir(cwd)

    if framework == "django" and not os.path.exists("manage.py"):
        click.secho("Warning: manage.py not found. Are you in a Django project root?", fg="yellow")

    if not force and Config.load():
        if not click.confirm("Djinn is already initialized. Overwrite existing configuration?", default=False):
            return

    if yes or defaults:
        config_data = DEFAULT_CONFIG.copy()
        config_data["style"] = style
        if no_css_variables:
            config_data["tailwind"]["cssVariables"] = False
            
        config = Config(**config_data)
        config.save()
        if not no_css_variables:
            _install_base_css(radius=radius, force=force)
        _install_tailwind_config(force=force)
        _install_base_utils(config.aliases["utils"], force=force)
        click.echo(f"Initialized djinn.json with defaults.")
        return

    # Interactive prompts
    style_choice = click.prompt("Which style would you like to use?", default=style)
    color_choice = click.prompt("Which color would you like to use as base color?", default=color)
    css_variables = not no_css_variables and click.confirm("Do you want to use CSS variables for colors?", default=True)

    css_path = click.prompt("Where is your global CSS file?", default=DEFAULT_CONFIG["tailwind"]["css"])
    tailwind_config = click.prompt("Where is your tailwind.config.js located?", default=DEFAULT_CONFIG["tailwind"]["config"])
    
    components_path = click.prompt(f"Configure the import alias for components:", default=DEFAULT_CONFIG["aliases"]["components"])
    utils_path = click.prompt("Configure the import alias for utils:", default=DEFAULT_CONFIG["aliases"]["utils"])

    config_data = {
        "registry_url": DEFAULT_CONFIG["registry_url"],
        "style": style_choice,
        "tailwind": {
            "config": tailwind_config,
            "css": css_path,
            "cssVariables": css_variables
        },
        "aliases": {
            "components": components_path,
            "utils": utils_path
        },
        "registries": DEFAULT_CONFIG["registries"]
    }

    config = Config(**config_data)
    config.save()
    if css_variables:
        _install_base_css(css_path, radius=radius, force=force)
    _install_tailwind_config(tailwind_config, force=force)
    _install_base_utils(utils_path, force=force)

    click.echo("\nDjinn initialized successfully!")
    click.echo(f"Config saved to djinn.json")

def _install_base_utils(path="templatetags", force=False):
    import os
    os.makedirs(path, exist_ok=True)
    
    init_path = os.path.join(path, "__init__.py")
    if not os.path.exists(init_path):
        with open(init_path, "w") as f:
            f.write("")
            
    tags_path = os.path.join(path, "djinn_tags.py")
    if not os.path.exists(tags_path) or force:
        with open(tags_path, "w") as f:
            f.write("""from django import template
try:
    from tailwind_merge import TailwindMerge
    tw_merge = TailwindMerge().merge
except ImportError:
    tw_merge = lambda *args: " ".join(args)

register = template.Library()

@register.simple_tag
def cn(*args):
    \"\"\"
    Merges tailwind classes intelligently.
    Usage: {% cn "base-class" dynamic_class %}
    \"\"\"
    classes = [str(arg) for arg in args if arg]
    return tw_merge(*classes)
""")
        click.echo(f"Installed base utilities to {tags_path}")

def _install_base_css(path="static/css/djinn.css", radius="0.5rem", force=False):
    import os
    dirname = os.path.dirname(path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
        
    css_content = """@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;

    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
 
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
 
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
 
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
 
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
 
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
 
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;

    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
 
    --radius: 0.5rem;
  }
 
  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
 
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
 
    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;
 
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;
 
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
 
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
 
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
 
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
 
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 212.7 26.8% 83.9%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}
"""
    css_content = css_content.replace("--radius: 0.5rem;", f"--radius: {radius};")

    if not os.path.exists(path) or force:
        with open(path, "w") as f:
            f.write(css_content)
    else:
        with open(path, "r") as f:
            existing = f.read()
            
        if "--radius" not in existing:
            # Smart append - strip the tailwind base imports from our default if they exist
            append_content = css_content
            if "@tailwind base;" in existing:
                append_content = append_content.replace("@tailwind base;\n@tailwind components;\n@tailwind utilities;\n", "")
            
            with open(path, "a") as f:
                f.write("\n" + append_content)
            click.echo(f"Appended base CSS variables to {path}")

def _install_tailwind_config(path="tailwind.config.js", force=False):
    import os
    
    default_config = """/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./**/templates/**/*.html",
    "./templatetags/**/*.py",
  ],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
  plugins: [],
}
"""
    if not os.path.exists(path) or force:
        with open(path, "w") as f:
            f.write(default_config)
    else:
        click.echo(f"Warning: {path} already exists. Please manually ensure your content array includes:")
        click.echo('  "./templates/**/*.html",\n  "./**/templates/**/*.html",\n  "./templatetags/**/*.py"')
        click.echo("and that your theme is extended with Djinn CSS variables.")
