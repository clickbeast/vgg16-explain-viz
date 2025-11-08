# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Matrix(Component):
    """A Matrix component.


Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- hoverColor (string; optional):
    The color of the layer when hovering over it.

- selectedColor (string; optional):
    The color of the layer when selected.

- selectedLayer (number; optional):
    The layer that needs to be selected."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, selectedLayer=Component.UNDEFINED, hoverColor=Component.UNDEFINED, selectedColor=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'hoverColor', 'selectedColor', 'selectedLayer']
        self._type = 'Matrix'
        self._namespace = 'ssp_matrix'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'hoverColor', 'selectedColor', 'selectedLayer']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Matrix, self).__init__(**args)
