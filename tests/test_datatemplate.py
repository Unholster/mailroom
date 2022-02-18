from mailroom.datatemplate import DataTemplate


def test_dicttemplates():
    dt = DataTemplate({
        'foo': '{{foo}}',
        'nested': {
            'bar': 'This is {{bar}}'
        },
        'list': [
            '{{foo}}', '{{bar}}', 'GROO'
        ]
    })

    dr = dt.render(foo='FOO', bar='BAR')

    assert dr == {
        'foo': 'FOO',
        'nested': {'bar': 'This is BAR'},
        'list': ['FOO', 'BAR', 'GROO'],
    }
