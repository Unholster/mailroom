from jinja2 import Template


class DictTemplate:
    '''A dict template
    Is instantiated with a dictionary whose values are interpreted as
    Jinja2 template strings.
    The resulting DictTemplate can then be rendered into a dict with
    variables replaced
    '''

    def __init__(self, source: dict):
        self.templates = _templatize(source)

    def render(self, **kwargs) -> dict:
        '''Creates a dictionary based by replacing provided variables into each
        template in the DictTemplate'''
        target = dict()

        for key, template in self.templates.items():
            target[key] = template.render(**kwargs)

        return target


def _templatize(source: dict):
    '''Converts a source dictionary of strings into a
    corresponding dictionary of templates'''
    target = dict()
    for key, value in source.items():
        if isinstance(value, dict):
            target[key] = DictTemplate(value)
        else:
            target[key] = Template(value)
    return target
