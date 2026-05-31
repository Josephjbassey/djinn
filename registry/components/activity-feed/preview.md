# Activity Feed

A list of recent activities/events.

## Usage

```django
{% include "components/activity-feed.html" %}
    <div class="flex items-center gap-4">
        {% include "components/avatar.html" with fallback="JD" %}
        <div class="space-y-1">
            <p class="text-sm font-medium">John Doe created a new project</p>
            <p class="text-xs text-muted-foreground">2 hours ago</p>
        </div>
    </div>
{% endinclude %}
```
