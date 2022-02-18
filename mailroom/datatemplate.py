from jinja2 import Template
from typing import Union


TEMPLATABLE = Union[str, list, dict]


class DataTemplate:
    '''A templated data structure that is instatiated
    from a string, list or dictionary whose values are interpreted as
    Jinja2 template strings.
    The resulting DataTemplate can then be rendered into a dict with
    variables replaced
    '''

    def __init__(self, source: TEMPLATABLE):
        self.template = _templatize(source)

    def render(self, **kwargs) -> dict:
        '''Creates a dictionary based by replacing provided variables into each
        template in the DictTemplate'''

        if isinstance(self.template, list):
            return [v.render(**kwargs) for v in self.template]

        if isinstance(self.template, dict):
            return {k: v.render(**kwargs) for k, v in self.template.items()}

        if isinstance(self.template, Template):
            return self.template.render(**kwargs)

        raise ValueError(f'Internal template invalid: {self.template}')


def _templatize(source: TEMPLATABLE):
    '''Converts a source dictionary of strings into a
    corresponding dictionary of templates'''

    if isinstance(source, dict):
        return {
            key: DataTemplate(value)
            for key, value in source.items()
        }

    if isinstance(source, list):
        return [
            DataTemplate(value) for value in source
        ]

    if isinstance(source, str):
        return Template(source)

    raise ValueError(f'Non-templatizable data: {source}')
