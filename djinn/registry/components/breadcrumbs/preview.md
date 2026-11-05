# Breadcrumbs

Navigation path indicator.

## Usage

```django
{% include "components/breadcrumbs.html" %}
    <li class="inline-flex items-center gap-1.5">
        <a class="transition-colors hover:text-foreground" href="/">Home</a>
    </li>
    <li role="presentation" aria-hidden="true" class="[&>svg]:size-3.5">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>
    </li>
    <li class="inline-flex items-center gap-1.5 font-normal text-foreground">
        Components
    </li>
{% endinclude %}
```
