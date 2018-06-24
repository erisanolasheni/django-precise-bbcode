# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import django
import pytest


@pytest.mark.skipif(django.VERSION < (1, 8),
                    reason="requires django>=1.8")
@pytest.mark.django_db
class TestBbcodeJinja2Tags(object):
    BBCODE_FILTER_EXPRESSIONS_TESTS = (
        (
            '{{ "[b]hello world![/b]"|bbcode }}',
            '<strong>hello world!</strong>',
        ),
        (
            '{{ "[b]Write some bbcodes![/b] The [i]current[/i] text was generated by using the '
            'bbcode filter..."|bbcode }}',
            '<strong>Write some bbcodes!</strong> The <em>current</em> text was generated by using '
            'the bbcode filter...',
        ),
    )

    BBCODE_TAG_EXPRESSIONS_TESTS = (
        (
            '{{ bbcode("This [b]one[/b] was generated using the [i][color=green]bbcode[/color][/i] '
            'template tag.") }}',
            'This <strong>one</strong> was generated using the <em><span style="color:green;">'
            'bbcode</span></em> template tag.',
        ),
        (
            '{% set renderedvar = bbcode("Hello [u]world![/u]") %}'
            '{{ renderedvar }}',
            'Hello <u>world!</u>',
        ),
        (
            "{{ bbcode('[i]a \"small\" test[/i]') }}",
            "<em>a &quot;small&quot; test</em>",
        )
    )

    def setup_method(self, method):
        from django.template import engines
        self.engine = engines['jinja2']

    def test_provide_a_functional_bbcode_filter(self):
        # Run & check
        for template_content, expected_html_text in self.BBCODE_FILTER_EXPRESSIONS_TESTS:
            t = self.engine.from_string(template_content)
            rendered = t.render({})
            assert rendered == expected_html_text

    def test_provide_a_functional_bbcode_tag(self):
        # Run & check
        for template_content, expected_html_text in self.BBCODE_TAG_EXPRESSIONS_TESTS:
            t = self.engine.from_string(template_content)
            rendered = t.render({})
            assert rendered == expected_html_text
