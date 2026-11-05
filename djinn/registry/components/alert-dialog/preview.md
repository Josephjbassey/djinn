# Alert Dialog

A modal dialog for important alerts or destructive actions.

## Usage

```django
{% include "components/alert-dialog.html" with id="confirm-delete" title="Delete account?" description="This will permanently delete your account and remove your data from our servers." action_label="Delete Account" %}
```
