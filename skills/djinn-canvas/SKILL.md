---
name: djinn-canvas
description: "Use when building the Drag & Drop Canvas Builder for djinn-ui — a visual tool that lets users drag and drop Djinn components to generate Django template code. Trigger terms: canvas, drag and drop, visual builder, Django templates, component canvas, djinn canvas builder."
license: MIT
metadata:
  author: https://github.com/josephjbassey/djinn
  version: "1.0.0"
  domain: frontend
  triggers: canvas, drag and drop, visual builder, Django templates, component canvas, djinn canvas builder, canvas builder
  role: specialist
  scope: implementation
  output-format: code
  related-skills: djinn-use, django-expert, web-design-guidelines, popular-web-designs
  hermes:
    tags: [canvas, drag-and-drop, visual-builder, Django, templates, djinn-ui, shadcn]
    related_skills: djinn-use, django-expert, web-design-guidelines, popular-web-designs
---

# Djinn Canvas Builder

AI-agent guide for building and using the Djinn Canvas Builder — a drag-and-drop visual tool that lets users compose Djinn UI components into Django templates and export ready-to-use template code.

## When to Use This Skill

- Building the Drag & Drop Canvas Builder for djinn-ui
- Creating visual component composition tools for Django templates
- Generating `{% include %}` and `{% djinn_* %}` template code from visual layouts
- Exporting canvas layouts as Django-ready template files

## Core Workflow

1. **Canvas setup** — Create a single-file HTML artifact with drag-and-drop canvas, component palette, and code preview
2. **Component library** — Load Djinn components from the registry (button, card, modal, alert, data-table, hero-section, etc.) with their variant schemas
3. **Drag and drop** — Users drag components from palette onto canvas; each dropped component renders a live preview
4. **Configure variants** — Side panel lets users select variant values (variant, size, etc.) for each component instance
5. **Generate code** — Canvas outputs complete Django template with `{% load djinn_tags %}`, `{% include %}`, and `{% djinn_* %}` tags
6. **Copy/export** — One-click copy of generated template code to clipboard

## Canvas Architecture

```
Canvas Builder (single HTML file)
├── Palette (left) — Component list with thumbnails and variant info
├── Canvas (center) — Drop zone with live-rendered component instances
├── Inspector (right) — Variant controls for selected component
└── Code preview (bottom) — Generated Django template code
```

## Component Palette

Each palette entry shows:
- Component name and description
- Thumbnail preview
- Available variants (from cva schema)
- Drag handle

## Component Instance

Each canvas instance includes:
- Component tag (`{% djinn_button %}`, `{% djinn_card %}`, etc.)
- Variant values (variant, size, etc.)
- Slot content (for components with children)
- Extra CSS class
- Delete handle

## Generated Template Code

The canvas outputs:

```html
{% load djinn_tags %}

{% djinn_hero_section variant="default" size="default" label="Get Started" %}
    <p>Hero section content</p>
{% enddjinn_hero_section %}

{% djinn_button variant="primary" label="Primary Button" class="w-auto" %}

{% djinn_card variant="elevated" title="Card Title" %}
    <p>Card content</p>
{% enddjinn_card %}
```

## MUST DO

- Single-file HTML artifact (no external dependencies beyond Tailwind CDN and Alpine.js)
- Load component schemas from djinn registry (variant names, default values, boolean props, text props)
- Live preview renders with actual Tailwind classes applied
- Variant selector updates preview in real time
- Generated code uses correct `{% djinn_<name> %}` tag syntax with proper opening/closing tags
- Slot content supported for components with children (card, modal, etc.)
- Copy-to-clipboard for generated code
- Component instances can be deleted, reordered, and configured
- Responsive layout works on desktop and tablet

## MUST NOT DO

- Don't require build step (no npm, no webpack)
- Don't require backend (pure HTML/JS)
- Don't assume specific component set — load from registry dynamically
- Don't hardcode variant values — read from component schema
- Don't generate invalid Django template syntax (unclosed tags, wrong attribute names)

## Output Templates

Canvas artifact structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Djinn Canvas Builder</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <style>/* custom canvas styles */</style>
</head>
<body x-data="canvasBuilder()">
    <!-- Palette, Canvas, Inspector, Code Preview -->
</body>
</html>
```

## Related Skills

- **djinn-use** — How to use djinn CLI and components in Django
- **django-expert** — Django models, ORM, templates
- **web-design-guidelines** — Web Interface Guidelines compliance
- **popular-web-designs** — Design tokens from Linear, Vercel, Stripe, etc.
