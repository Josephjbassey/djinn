# Metric Grid

A pre-configured grid for dashboard metrics.

## Usage

```django
{% include "components/metric-grid.html" %}
    {% include "components/stats-card.html" with label="Active Users" value="1,234" %}
    {% include "components/stats-card.html" with label="Sales" value="2,000" %}
    {% include "components/stats-card.html" with label="New Orders" value="45" %}
    {% include "components/stats-card.html" with label="Server Load" value="12%" %}
{% endinclude %}
```
