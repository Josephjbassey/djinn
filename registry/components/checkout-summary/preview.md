# Checkout Summary

A summary of items and totals for checkout.

## Usage

```django
{% include "components/checkout-summary.html" with subtotal="20.00" shipping="Free" total="20.00" %}
    {% slot "items" %}
        <div class="flex justify-between"><span>Product 1</span><span>0.00</span></div>
        <div class="flex justify-between"><span>Product 2</span><span>0.00</span></div>
    {% endslot %}
{% endinclude %}
```
