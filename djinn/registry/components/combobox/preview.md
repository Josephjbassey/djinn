# Combobox

A searchable select component (requires Alpine.js).

## Usage

```django
{% include "components/combobox.html" with name="framework" placeholder="Select framework..." %}
    <div
        @click="selected = 'Django'; open = false"
        class="relative flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none hover:bg-accent hover:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50"
    >
        Django
    </div>
    <div
        @click="selected = 'Flask'; open = false"
        class="relative flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none hover:bg-accent hover:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50"
    >
        Flask
    </div>
{% endinclude %}
```
