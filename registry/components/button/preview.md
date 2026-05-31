# Button

A versatile button component with multiple variants and states.

## Usage

```django
{% include "components/button.html" with label="Click Me" variant="primary" %}
```

## Variants

- `primary` (default)
- `secondary`
- `outline`
- `ghost`
- `destructive`
- `link`

## Sizes

- `sm`
- `md` (default)
- `lg`
- `icon`

## Props

- `label`: Text to display
- `variant`: Style variant
- `size`: Size of the button
- `disabled`: Boolean to disable the button
- `icon_left`: HTML for icon on the left
- `icon_right`: HTML for icon on the right
- `type`: HTML button type (default: 'button')
- `class`: Extra CSS classes
