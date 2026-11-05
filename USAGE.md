# Djinn UI — Component Usage Guide

This document covers the djinn-ui component system: forms, formsets, pagination, modals, buttons, inputs, and selects. It also covers the security model, registry system, and how to create private components.

---

## 1. Installation

```bash
pip install djinn-ui
djinn init --force
djinn add button input select modal form form_field formset pagination --force
```

---

## 2. Form Components

### `djinn_form` — Render a complete Django form

Wraps a `django.forms.Form` with CSRF token, non-field errors, and field iteration.

**Template:**
```html
{% load djinn_form %}
{% djinn_form form=registration_form method="post" action="/register/" %}
    {% djinn_button variant="primary" type="submit" label="Create Account" %}
{% enddjinn_form %}
```

**Parameters:**
| Parameter | Default | Description |
|-----------|---------|-------------|
| `form` | Required | Django `Form` or `ModelForm` instance |
| `method` | `"post"` | HTTP method |
| `action` | `""` | Form action URL |
| `class` | `""` | Extra CSS classes on `<form>` |
| `id` | `""` | HTML `id` attribute |

**Security:** `{{ fields\|safe }}` renders pre-rendered Django widget HTML (already escaped by Django). `{{ slot\|safe }}` renders the block content between the tags. Do not pass user-controlled content into `slot`.

---

### `djinn_form_field` — Render a single form field

Renders a Django `BoundField` with label, errors, and help text.

**Template:**
```html
{% load djinn_form_field %}
{% djinn_form_field field=form.email label_class="mb-2" class_name="mb-4" %}
```

**Parameters:**
| Parameter | Default | Description |
|-----------|---------|-------------|
| `field` | Required | Django `BoundField` |
| `label_class` | `""` | Extra classes on `<label>` |
| `class_name` | `""` | Extra classes on wrapper div |
| `field_id` | `""` | Override the `id` attribute |

**Accessibility:** Each field renders with:
- `<label for="...">` associated with the input `id`
- `aria-required="true"` on required fields
- `aria-invalid="true"` and `role="alert"` on fields with errors
- `aria-describedby` linking to help text when present

---

## 3. FormSet Component

### `djinn_formset` — Render a Django formset with dynamic add/remove

Renders a `django.forms.formsets.BaseFormSet` with management form, per-form fields, delete checkboxes, and Alpine.js-powered dynamic add/remove.

**Template:**
```html
{% load djinn_formset %}
{% djinn_formset formset=item_formset can_add=True %}
```

**Python view:**
```python
from django.forms.formsets import formset_factory
from .forms import ItemForm

ItemFormSet = formset_factory(ItemForm, extra=1, can_delete=True)

def my_view(request):
    if request.method == "POST":
        formset = ItemFormSet(request.POST)
        if formset.is_valid():
            # Process forms...
            pass
    else:
        formset = ItemFormSet()
    return render(request, "template.html", {"formset": formset})
```

**Parameters:**
| Parameter | Default | Description |
|-----------|---------|-------------|
| `formset` | Required | Django formset instance |
| `class_name` | `""` | Extra CSS classes |
| `can_add` | `True` | Show "Add another" button |

**Dynamic behavior:**
- Click "Add another" to clone the empty form via Alpine.js
- Click "Remove" to mark a form for deletion (checkbox checked, row hidden)
- The management form's `TOTAL_FORMS` count updates automatically

**Accessibility:**
- Remove buttons have `aria-label="Remove this form"`
- Add button has `aria-label="Add another item"`
- Delete checkboxes are properly labeled

---

## 4. Pagination Component

### `djinn_pagination` — Accessible pagination control

Renders Previous/Next buttons, page numbers with ellipsis, and current page highlight.

**Template:**
```html
{% load djinn_pagination %}
{% djinn_pagination page_obj=page_obj %}
```

**HTMX support:** Buttons include `hx-get` and `hx-target` attributes for partial page updates. Set `hx-target` to your content container's ID.

**Parameters:**
| Parameter | Default | Description |
|-----------|---------|-------------|
| `page_obj` | Required | Django Paginator `page_obj` |
| `class_name` | `""` | Extra CSS classes |

**Accessibility:**
- `<nav aria-label="Pagination">` landmark
- `aria-label` on all buttons (Previous page, Next page, Page N)
- Disabled state (visual + semantic) on boundary buttons

---

## 5. Modal Component

### `djinn_modal` — Accessible dialog with focus management

Renders a modal dialog with ARIA attributes, focus trapping, and return focus.

**Template:**
```html
{% load djinn_modal djinn_modal_trigger %}
{% djinn_modal_trigger "user-modal" label="Edit User" variant="primary" %}

{% djinn_modal id="user-modal" title="Edit User" description="Update your profile information" %}
    <form method="post">
        {% csrf_token %}
        {% djinn_form_field field=form.name %}
        {% djinn_button variant="primary" type="submit" label="Save" %}
    </form>
{% enddjinn_modal %}
```

**Parameters:**
| Parameter | Default | Description |
|-----------|---------|-------------|
| `id` | `"modal"` | Unique modal identifier |
| `title` | `""` | Dialog title |
| `description` | `""` | Dialog description |
| `footer` | `None` | Footer content (buttons, etc.) |
| `class_name` | `""` | Extra CSS classes |

**Accessibility:**
- `role="dialog"`, `aria-modal="true"`
- `aria-labelledby` / `aria-describedby`
- Focus moves into dialog on open, returns to trigger on close
- Tab key is trapped within the dialog
- Escape key closes the dialog
- Close button has `aria-label="Close dialog"`

### `djinn_modal_trigger` — Button that opens a modal

Renders a button that dispatches a `open-modal` CustomEvent.

**Template:**
```html
{% djinn_modal_trigger "user-modal" label="Edit User" class_name="btn-primary" %}
```

**Parameters:**
| Parameter | Default | Description |
|-----------|---------|-------------|
| `modal_id` | Required | ID of the target modal |
| `label` | `"Open"` | Button text |
| `class_name` | `""` | Extra CSS classes |

---

## 6. Button, Input, Select Components

All three use the `@register.inclusion_tag` pattern with `format_html_attrs` for safe attribute rendering.

### `djinn_button`
```html
{% djinn_button variant="destructive" size="lg" label="Delete" aria_label="Delete item" aria_pressed=False %}
```

### `djinn_input`
```html
{% djinn_input label="Email" type="email" name="email" error="Invalid email" help_text="We'll never share your email." %}
```

### `djinn_select`
```html
{% djinn_select label="Country" name="country" error="Required" %}
    <option value="us">United States</option>
    <option value="ca">Canada</option>
{% enddjinn_select %}
```

---

## 7. Security Model — The `\|safe` Boundary

Two component templates use `\|safe` deliberately:

| Component | Template | Why `\|safe` is safe |
|-----------|----------|---------------------|
| `form` | `{{ fields\|safe }}` | Pre-rendered Django widget HTML (already escaped by Django) |
| `form` | `{{ slot\|safe }}` | Block content between tags (developer-controlled) |

**All other component templates have zero `\|safe` usage.** User-controlled content (labels, slot content in button/modal, etc.) is rendered through Django's auto-escaping.

**Rule:** Never pass user-controlled HTML into `slot` or `footer` parameters without escaping it first.

---

## 8. Registry System

### How it works

Each component is defined in `registry.json`:

```json
{
  "name": "button",
  "dependencies": [],
  "registryDependencies": [],
  "files": [
    {
      "name": "button.html",
      "dir": "templates/components",
      "content": "..."
    },
    {
      "name": "djinn_button.py",
      "dir": "templatetags",
      "content": "..."
    }
  ],
  "type": "components:ui"
}
```

- `registry.json` is the **source of truth**. Standalone `.html` and `.py` files on disk are documentation only.
- `dependencies` is **ignored** by the installer. Use `registryDependencies` for install ordering.
- The `files` list is a list of dicts, not a dict keyed by type.

### Creating private components (`@internal/` namespace)

1. Create your own registry:
   ```json
   {
     "name": "my-dashboard-card",
     "dependencies": [],
     "registryDependencies": [],
     "files": [
       {
         "name": "dashboard-card.html",
         "dir": "templates/components",
         "content": "..."
       },
       {
         "name": "djinn_dashboard_card.py",
         "dir": "templatetags",
         "content": "..."
       }
     ],
     "type": "components:ui"
   }
   ```

2. Add to your `djinn.json`:
   ```json
   {
     "registries": {
       "@internal": "http://your-private-registry/components/{name}/registry.json"
     }
   }
   ```

3. Install: `djinn add @internal/dashboard-card`

### Component file naming

- Templatetag files must be named `djinn_<name>.py` (underscore, not hyphen)
- HTML files must be named `<name>.html`
- The installer creates `__init__.py` in templatetags directories automatically

---

## 9. CLI Commands

| Command | Description |
|---------|-------------|
| `djinn init` | Initialize djinn.json config |
| `djinn add <component>` | Install a component |
| `djinn list` | List available components |
| `djinn diff <component>` | Compare registry vs local version |
| `djinn upgrade <component>` | Upgrade a component (prompts before overwriting) |
| `djinn upgrade --all` | Upgrade all installed components |
| `djinn upgrade --diff <component>` | Preview changes without applying |
| `djinn upgrade --backup <component>` | Create backups before overwriting |
| `djinn upgrade --force <component>` | Upgrade without prompting |
| `djinn remove <component>` | Remove a component |
| `djinn doctor` | Check project setup for issues |
| `djinn mcp` | Start MCP server for AI agent integration |

---

## 10. Migration Path

djinn-ui uses **copy-paste ownership**: components are copied into your project's `templates/components/` and `templatetags/` directories. You own every line. If upstream stalls:

1. Stop running `djinn add` for production deploys
2. Maintain your `templates/components/` and `templatetags/` directories yourself
3. The cost of abandoning djinn-ui is zero — there's no runtime dependency to unwind

---
