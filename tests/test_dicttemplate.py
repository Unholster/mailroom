from mailroom.dicttemplate import DictTemplate


def test_dicttemplates():
    dt = DictTemplate({
        'foo': '{{foo}}',
        'nested': {
            'bar': 'This is {{bar}}'
        }
    })

    dr = dt.render(foo='FOO', bar='BAR')

    assert dr == {'foo': 'FOO', 'nested': {'bar': 'This is BAR'}}
