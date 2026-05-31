# Accordion

Collapsible content panels (requires Alpine.js).

## Usage

```django
{% include "components/accordion.html" %}
    <div x-data="{ id: 1 }" class="border-b">
        <button
            @click="active = (active === id ? null : id)"
            class="flex flex-1 items-center justify-between py-4 font-medium transition-all hover:underline"
        >
            Is it accessible?
            <svg :class="active === id ? 'rotate-180' : ''" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4 shrink-0 transition-transform duration-200"><path d="m6 9 6 6 6-6"/></svg>
        </button>
        <div x-show="active === id" x-collapse class="overflow-hidden text-sm transition-all p-4">
            Yes. It adheres to the WAI-ARIA design pattern.
        </div>
    </div>
{% endinclude %}
```
