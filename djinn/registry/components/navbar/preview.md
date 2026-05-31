# Navbar

A responsive navigation bar.

## Usage

```django
{% include "components/navbar.html" with brand_name="My App" %}
    <a href="/features">Features</a>
    <a href="/pricing">Pricing</a>
    {% slot "right_slot" %}
        <button>Login</button>
    {% endslot %}
{% endinclude %}
```
