# Djinn

**Djinn is a shadcn-style component system for Django.**

It lets developers visually build, install, and own UI components directly inside their Django projects using a simple CLI.

---

## ✨ Philosophy

Djinn is NOT a UI framework.

Djinn is a **source-code delivery system**.

Once a component is installed, it belongs to your project — fully editable, fully owned.

---

## ⚡ Features

* CLI-based component installation
* Registry-driven architecture
* Copy-paste ownership model (like shadcn/ui)
* Django-native templates
* TailwindCSS-based styling
* Alpine.js / HTMX support
* Versioned components
* Diff and update system

---

## 📦 Installation (CLI)

```bash
pip install django-djinn
```

---

## 🚀 Quick Start

Initialize Djinn in your Django project:

```bash
djinn init
```

Add a component:

```bash
djinn add button
```

---

## 🧩 Example Component Usage

```django
{% include "components/button.html" %}
```

---

## 📁 Registry System

Djinn components are stored in a remote registry:

* Each component is versioned
* Includes templates, logic, and metadata
* CLI fetches and installs directly into your project

---

## 🏗 Architecture

```
Registry → CLI → Django Project
```

No runtime dependency.
No locked library.
You own the code.

---

## 🔮 Roadmap

* Visual Component Builder (Djinn Canvas)
* AI component generator
* Component marketplace
* Figma import
* Team registries

---

## 🤝 Contribution

We welcome contributions to:

* Registry components
* CLI improvements
* Documentation
