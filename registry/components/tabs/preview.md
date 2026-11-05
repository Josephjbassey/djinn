# Tabs

Accessible tabbed content (requires Alpine.js).

## Usage

```django
{% include "components/tabs.html" active="account" %}
    {% slot "triggers" %}
        <button
            @click="activeTab = 'account'"
            :class="activeTab === 'account' ? 'bg-background text-foreground shadow-sm' : ''"
            class="inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50"
        >
            Account
        </button>
        <button
            @click="activeTab = 'password'"
            :class="activeTab === 'password' ? 'bg-background text-foreground shadow-sm' : ''"
            class="inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50"
        >
            Password
        </button>
    {% endslot %}

    <div x-show="activeTab === 'account'">Account settings content</div>
    <div x-show="activeTab === 'password'">Password settings content</div>
{% endinclude %}
```
