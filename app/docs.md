## Custom input label

By default the label will be the key name itself.
If you want to change it, set the key name and value in `field_labels` in [context_form.py](document/context_form.py)

## Custom input result transformation

If you want process a context value before landing on the template, you can catch the respective key in function `render_partial_html` in [html.py](document/lib/html.py)

If you also want to hide it from `ContextForm` fields, add the key name to `custom_form_keys` in [context_form.py](document/context_form.py)

## Add custom context inputs

Catch the desired key in function `get_input_field` in [context_form.py](document/context_form.py)
This will prevent from rendering as a regular input.


## Add value to render Context

Add the value to function `get_base_context` in [context.py](document/lib/context.py)
