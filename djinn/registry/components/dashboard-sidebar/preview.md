# Dashboard Sidebar

A more complex sidebar for dashboards with grouping and nested items.

## Usage

```django
{% include "components/dashboard-sidebar.html" with brand_name="CyberAdmin" %}
    <a href="#" class="flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:text-primary bg-muted">
        <svg>...</svg> Dashboard
    </a>
    <a href="#" class="flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:text-primary">
        <svg>...</svg> Orders
    </a>
{% endinclude %}
```
