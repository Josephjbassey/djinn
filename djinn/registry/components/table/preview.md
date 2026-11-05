# Table

Styled table components.

## Usage

```django
{% include "components/table.html" %}
    <thead class="[&_tr]:border-b">
        <tr class="border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted">
            <th class="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Invoice</th>
            <th class="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Status</th>
            <th class="h-12 px-4 text-right align-middle font-medium text-muted-foreground">Amount</th>
        </tr>
    </thead>
    <tbody class="[&_tr:last-child]:border-0">
        <tr class="border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted">
            <td class="p-4 align-middle font-medium">INV001</td>
            <td class="p-4 align-middle">Paid</td>
            <td class="p-4 align-middle text-right">50.00</td>
        </tr>
    </tbody>
{% endinclude %}
```
