# Modal

A standard modal dialog (requires Alpine.js).

## Usage

```django
{% include "components/modal.html" with id="my-modal" title="Edit profile" description="Make changes to your profile here. Click save when you're done." %}
    <div class="grid gap-4 py-4">
        <!-- Content -->
    </div>
    {% slot "footer" %}
        <button @click="$dispatch('close-modal', {id: 'my-modal'})">Save changes</button>
    {% endslot %}
{% endinclude %}

<!-- To Open -->
<button @click="$dispatch('open-modal', {id: 'my-modal'})">Open Modal</button>
```
