# Toast

A push notification component (requires Alpine.js).

## Usage

```django
{% include "components/toast.html" %}

<!-- To trigger -->
<button @click="$dispatch('toast', { message: 'Action completed!', type: 'success' })">Show Toast</button>
```
