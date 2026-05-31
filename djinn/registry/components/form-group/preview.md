# Form Group

A wrapper for form fields with labels, inputs, and error messages.

## Usage

```django
{% include "components/form-group.html" with label="Email" name="email" error="Invalid email address" %}
    {% include "components/input.html" with name="email" type="email" %}
{% endinclude %}
```
