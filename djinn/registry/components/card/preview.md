# Card

A container for content with header, body, and footer.

## Usage

```django
{% include "components/card.html" with title="Create project" description="Deploy your new project in one-click." %}
    <p>Card content goes here.</p>
    {% slot "footer" %}
        <button class="bg-primary text-primary-foreground px-4 py-2 rounded">Deploy</button>
    {% endslot %}
{% endinclude %}
```
