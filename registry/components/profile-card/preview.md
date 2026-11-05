# Profile Card

A card for user profiles with avatar and info.

## Usage

```django
{% include "components/profile-card.html" with name="Jules" role="Senior Engineer" avatar_url="https://github.com/shadcn.png" %}
    <button class="text-xs border px-2 py-1 rounded">Message</button>
    <button class="text-xs bg-primary text-primary-foreground px-2 py-1 rounded">Follow</button>
{% endinclude %}
```
