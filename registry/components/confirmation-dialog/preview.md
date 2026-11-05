# Confirmation Dialog

A simpler confirmation dialog for non-destructive actions.

## Usage

```django
{% include "components/confirmation-dialog.html" with id="confirm-save" title="Save Changes?" action_label="Save" %}
    <p>Are you sure you want to save these changes?</p>
{% endinclude %}
```
