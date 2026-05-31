# Pricing Card

A card for displaying subscription plans or product pricing.

## Usage

```django
{% include "components/pricing-card.html" with name="Pro" price="9" featured=True %}
    {% slot "features" %}
        <li class="flex items-center"><svg>...</svg> Unlimited Projects</li>
        <li class="flex items-center"><svg>...</svg> Priority Support</li>
    {% endslot %}
{% endinclude %}
```
