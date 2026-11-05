<div align="center">
  <img src="https://raw.githubusercontent.com/Josephjbassey/djinn/main/assets/logo.jpg" alt="Djinn UI Logo" width="250"/>
</div>

# Djinn UI
### The First True shadcn/ui Equivalent for the Django Monolith.

[![PyPI version](https://img.shields.io/pypi/v/djinn-ui.svg)](https://pypi.org/project/djinn-ui/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Stop wasting weeks building UI components from scratch or fighting rigid frontend frameworks. **Djinn UI** is a CLI-driven component registry that delivers beautifully styled, accessible, and responsive Tailwind CSS components directly into your Django templates.

No vendor lock-in. No heavy JS frameworks. No locked pip libraries. Just clean, native Django code that **you own completely**.

---

## 🚀 The Paradigm Shift

Modern frontend ecosystems (React, Next.js) have premium, plug-and-play component delivery systems like `shadcn/ui`. Meanwhile, Django developers have been left choosing between heavy runtime packages with custom template syntax, or locked third-party packages that are impossible to customize without brutal CSS overrides.

Djinn UI brings the **copy-paste ownership model** to the Python world. It isn't a runtime dependency. It is a scaffolding engine.

### How it compares:

| Feature | Locked Pip Packages | Heavy Runtime Tools | Djinn UI |
| :--- | :--- | :--- | :--- |
| **Delivery Model** | Distributed via `pip` | Complex Server Logic | **CLI Scaffolding** |
| **Runtime Overhead**| Low (but rigid) | High (Custom engines) | **Zero (Native Django)** |
| **Customization** | Painful CSS overrides | Limited by library API | **100% Free (It's your code)** |
| **AI Workflows** | Hidden from LLMs | Hard for AI to reason | **Built-in MCP Server** |

---

## 🎨 The Web Builder & Canvas

Djinn isn't just a CLI—it is a visual component ecosystem. Djinn UI ships with a fully interactive local **Drag & Drop Canvas Builder** and Component Explorer. 

- **Interactive Canvas**: Drag and drop Djinn components visually to build full layouts, then instantly copy the generated, production-ready Django template code.
- **Custom Namespaces (`@internal/`)**: Create and host your own private design systems for your team or agency. Use `djinn add @internal/dashboard-card` to pull components securely.
- **Preset Sharing**: Instantly share complex, pre-configured component layouts with your team using short-links (`/c/xyz123`).

---

## 🤖 Built for the Agentic Era

Djinn UI is the only Django component registry designed from the ground up for AI-assisted workflows (**vibecoding**). 

It ships with a built-in **Model Context Protocol (MCP) Server**. When you connect it to AI agents like **Cursor** or **Claude**, your assistant can natively read, understand, and scaffold your custom UI setup. 

> **Example Prompt for Cursor:** 
> *"Use my Djinn components to build a beautiful SaaS billing dashboard page with a 3-tier pricing breakdown."*

---

## 📦 Installation & Usage

Get up and running in less than 60 seconds.

### 1. Install the CLI via PyPI
```bash
pip install djinn-ui
```

### 2. Initialize Djinn in your Django Project
```bash
djinn init
```
*This configures your components directory and ensures compatibility with your Tailwind CSS setup.*

### 3. Add a Component
Want a clean, fully-styled dashboard layout or a functional modal? Just call the Djinn:

> *(Insert a fast-paced GIF here showing `djinn add dashboard` alongside the rendered browser output!)*

```bash
djinn add dashboard
```
*The raw, clean HTML (and any optional Alpine.js interactions) is instantly dropped right into your project's local templates directory.*

### 4. Render Natively
Use standard, vanilla Django `{% include %}` tags out of the box:

```html
{% include 'components/ui/dashboard.html' %}
```

---

## 🧩 Tech Stack Philosophy

Djinn UI is built for developers who believe in the power and simplicity of the clean monolith. It pairs perfectly with:

* **Django** (Native templating, no complex SPA decoupled overhead)
* **Tailwind CSS** (Utility-first styling, easily configured via `tailwind-merge` utility tag `{% cn %}`)
* **HTMX & Alpine.js** (For crisp, lightweight, SPA-like reactivity without leaving your Python ecosystem)

---

## 🗺️ Roadmap & Ecosystem

- [x] Core CLI Architecture & Core Scaffolding Engine
- [x] Built-in MCP Server for AI/LLM context injection
- [x] Foundational UI blocks (Buttons, Inputs, Modals, Cards)
- [x] Visual Drag & Drop Component Canvas 
- [x] Custom Namespace Routing for Private Design Systems
- [ ] Premium "Djinn Pro" block expansion (SaaS landing pages, complex charts, data tables)
- [ ] Multi-variant theme generator

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.
