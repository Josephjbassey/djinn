---
name: djinn-use
description: "Use when working with djinn-ui CLI (init, add, list, diff, upgrade, remove, doctor, mcp). Teaches AI agents how to scaffold Tailwind components into Django projects, manage the component registry, and run the MCP server. Trigger terms: djinn, djinn-ui, shadcn, components, Django templates, add component, init, registry, MCP server."
license: MIT
metadata:
  author: https://github.com/josephjbassey/djinn
  version: "1.0.0"
  domain: backend
  triggers: djinn, djinn-ui, shadcn, components, Django templates, add component, init, registry, MCP server
  role: specialist
  scope: implementation
  output-format: code
  related-skills: django-expert, web-design-guidelines, popular-web-designs
  hermes:
    tags: [djinn, djinn-ui, shadcn, components, Django, templates, CLI, registry, MCP]
    related_skills: django-expert, web-design-guidelines, popular-web-designs
---

# Djinn Use

AI-agent guide for using djinn-ui — the shadcn/ui-style CLI that scaffolds Tailwind CSS components directly into Django templates. Zero runtime dependency; components are your code.

## When to Use This Skill

- Running `djinn init`, `djinn add`, `djinn list`, `djinn view`, `djinn diff`, `djinn upgrade`, `djinn remove`, `djinn doctor`, or `djinn mcp`
- Adding a shadcn-style component to a Django project (button, card, modal, alert, data-table, hero-section, etc.)
- Managing the Djinn component registry (bundled or custom namespaces)
- Running the Djinn MCP server over stdio or HTTP/SSE for remote agents
- Troubleshooting Djinn installation or component conflicts

## Core Workflow

1. **Install Djinn** — `pip install djinn-ui` (or `pip install -e /path/to/djinn` for local development)
2. **Initialize** — `djinn init --defaults --force` creates `djinn.json`, `tailwind.config.js`, `static/css/djinn.css`, `theme/templatetags/djinn_tags.py`, and `templates/components/`
3. **Add components** — `djinn add <name> --force` installs `<name>.html` to `templates/components/` and `djinn_<name>.py` to `theme/templatetags/`
4. **Render in templates** — `{% load djinn_tags %}` then `{% include 'components/button.html' %}` or `{% djinn_button variant="default" label="Click me" %}`
5. **Diff/upgrade/remove** — `djinn diff <name>` checks for drift; `djinn upgrade <name> --force` syncs; `djinn remove <name> --force` uninstalls
6. **Doctor** — `djinn doctor` verifies config, tailwind config, CSS path, cn tag, components dir

## Djinn CLI Commands

| Command | Purpose |
|---------|---------|
| `djinn init --defaults --force` | Initialize Djinn in a Django project |
| `djinn add <component> [--force]` | Install a component from the registry |
| `djinn list [query]` | List/search available components |
| `djinn view <component>` | View raw source without installing |
| `djinn diff <component>` | Compare registry vs installed version |
| `djinn upgrade <component> [--force]` | Upgrade to latest registry version |
| `djinn remove <component> [--force]` | Uninstall component files |
| `djinn doctor` | Check project setup for common issues |
| `djinn mcp [--http --host HOST --port PORT]` | Start MCP server (stdio default, HTTP/SSE optional) |

## Component Structure

Each component has two files:

**`templates/components/<name>.html`** — Django template with `{{ class }}`, `{{ slot|safe }}`, `{{ attrs|safe }}`, and component-specific variables (e.g. `{{ label }}`, `{{ variant }}`, `{{ title }}`).

**`theme/templatetags/djinn_<name>.py`** — Django template tag using `@register.inclusion_tag` or `@register.tag`. Components using CVA (Class Variance Authority) declare `cva(...)` with variants and default_variants, then render via `final_class = <name>_cva(**resolved_kwargs)`.

**Template tag registration pattern:**

```python
from django import template
from django.template.base import token_kwargs
from djinn.core.cva import cva

register = template.Library()

<button>_cva = cva(
    base="...",
    variants={"variant": {"default": "...", "destructive": "..."}},
    default_variants={"variant": "default", "size": "default"}
)

class <Button>Node(template.Node):
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
        final_class = <button>_cva(**resolved_kwargs)
        known_args = ["variant", "size", "class", "class_name", ...]
        attrs = {k: v for k, v in resolved_kwargs.items() if k not in known_args}
        slot = self.nodelist.render(context) if self.nodelist else ""
        t = context.template.engine.get_template('components/<name>.html')
        new_context = context.new({
            'class': final_class,
            'slot': slot,
            'attrs': attrs,
            **resolved_kwargs
        })
        return t.render(new_context)

@register.tag('djinn_<name>')
def djinn_<name>(parser, token):
    bits = token.split_contents()
    kwargs = token_kwargs(bits[1:], parser)
    nodelist = parser.parse(('enddjinn_<name>',))
    parser.delete_first_token()
    return <Button>Node(nodelist, kwargs)
```

## Component Registry

- `djinn/registry/index.json` — lightweight manifest: `name`, `type`, `path` references only (no embedded file content)
- `djinn/registry/components/<name>/registry.json` — full component data: `name`, `dependencies`, `registryDependencies`, `files` (list of `{name, dir, content}`), `type`
- To add a new component: create both files, then `djinn add <name> --force` installs it

## CVA (Class Variance Authority)

`cva(base, variants, default_variants)` merges Tailwind classes with `tailwind-merge` dedup:
- `base` — always-applied classes
- `variants` — variant name → {value → class string}
- `default_variants` — variant name → default value
- `class` kwarg — extra merged classes (use `**{"class": "..."}` since `class` is a Python keyword)
- Unknown variant values are ignored (not defaulted); defaults apply only when omitted

## MCP Server

**Stdio (default):** `djinn mcp` — for local agents like Cursor/Claude Code
**HTTP/SSE:** `djinn mcp --http --host 0.0.0.0 --port 8000` — for remote agents via Tailscale Funnel

Tools:
- `get_project_info` — project style, registry URL, aliases
- `search_components` — list/search components
- `add_component` — install a component

## Django Template Usage

```html
{% load djinn_tags %}

{% include "components/button.html" with class="my-btn" %}

{% djinn_button variant="destructive" label="Delete" class="w-auto" %}

{% djinn_card variant="elevated" title="Card Title" %}
    {{ slot content }}
{% enddjinn_card %}
```

## MUST DO

- Set `PYTHONPATH=.` when running local package code — the venv won't import the local `djinn` directory without it
- Install package dependencies before running tests — missing `tailwind-merge` breaks test collection
- `class` is a Python keyword — use `**{"class": "..."}` when calling `cva()` or template tags
- Read every page of a file before `write_file`; use `patch` for targeted edits
- When adding components, update BOTH `registry/components/<name>/registry.json` AND `registry/index.json`
- `init` installs CSS to `config_data["tailwind"]["css"]`, not a hardcoded default
- `init` creates the components directory (`os.makedirs(config.get_template_path(), exist_ok=True)`)
- `upgrade` diffs before installing; only `--force` if differences exist
- `remove` uninstalls tracked files listed in the component's registry.json
- `doctor` checks config-driven paths; exit non-zero on any failure
- MCP server version string must match package version (`0.1.11`)

## MUST NOT DO

- Call `Registry(config)` with a string URL — it expects a `Config` object
- Assume `ComponentMetadata.files` is a dict keyed by `file_type` — it's a list of file dicts
- Call `_install_base_css()` with a hardcoded path instead of the config's `tailwind.css` value
- Assume `index.json` contains embedded component `files` content — it's references only
- Store secrets in `settings.py` or `djinn.json`
- Use `DEBUG=True` in production

## Output Templates

When adding a new djinn component:

```json
{
  "name": "<name>",
  "dependencies": [],
  "registryDependencies": [],
  "files": [
    {
      "name": "<name>.html",
      "dir": "templates/components",
      "content": "<div class=\"{{ class }}\">{{ slot|safe }}</div>"
    },
    {
      "name": "djinn_<name>.py",
      "dir": "templatetags",
      "content": "from django import template\nfrom django.template.base import token_kwargs\nfrom djinn.core.cva import cva\n..."
    }
  ],
  "type": "components:ui"
}
```

When using a component in a Django template:

```html
{% load djinn_tags %}
{% djinn_button variant="default" size="lg" label="Click me" class="w-auto" %}
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `djinn diff` crashes on every call | Fixed in v0.1.11 — reinstall; `Registry` now takes `Config` object |
| `doctor` reports CSS missing | `init` now installs CSS to configured path; re-run `djinn init --force` |
| `djinn add` says file exists | Use `--force` to overwrite |
| Component not found | Check `registry/index.json` and `registry/components/<name>/registry.json` both exist |
| MCP server version mismatch | Fixed — `server_version` now matches package `0.1.11` |

## Related Skills

- **django-expert** — Django models, ORM, DRF serializers, viewsets, permissions
- **web-design-guidelines** — Web Interface Guidelines compliance for UI review
- **popular-web-designs** — Design tokens from Linear, Vercel, Stripe, etc.
