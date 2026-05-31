# Timeline

A vertical timeline of events.

## Usage

```django
{% include "components/timeline.html" %}
    <div class="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
        <div class="flex items-center justify-center w-10 h-10 rounded-full border border-background bg-muted text-muted-foreground shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2">
            <svg class="fill-current" viewBox="0 0 16 16"><path d="M8 0a8 8 0 1 0 8 8 8.009 8.009 0 0 0-8-8Zm0 14a6 6 0 1 1 6-6 6.007 6.007 0 0 1-6 6Z"/><circle cx="8" cy="8" r="3"/></svg>
        </div>
        <div class="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-4 rounded border bg-card shadow">
            <time class="font-bold text-primary">May 2024</time>
            <div class="text-muted-foreground">Djinn Registry Launched</div>
        </div>
    </div>
{% endinclude %}
```
