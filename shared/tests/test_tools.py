from unittest import TestCase

from expects import (
    equal,
    expect,
)

from shared.tools import (
    hf_clean_text,
    tokenize,
)


class ToolsTestCase(TestCase):

    def test_it_cleans_multiple_spaces(self):
        text = 'multiple   spaces'

        cleaned_text = hf_clean_text(text)

        expect(cleaned_text).to(equal('multiple spaces'))

    def test_it_removes_new_lines(self):
        text = 'new \n  line'

        cleaned_text = hf_clean_text(text)

        expect(cleaned_text).to(equal('new line'))

    def test_it_removes_tabs(self):
        text = 'text \t with tabs'

        cleaned_text = hf_clean_text(text)

        expect(cleaned_text).to(equal('text with tabs'))

    def test_it_cleans_hack_forums_tags(self):
        text = (
            '$2/hour ***img***[https://i.imgur.com/qnh55.png]***img*** site '
            'any ***link***https://i.imgur.com***link*** link to any site '
        )

        cleaned_text = hf_clean_text(text)

        expect(cleaned_text).to(equal(
            '$2/hour site any link to any site'
        ))

    def test_it_gets_a_lower_case_words_list_from_a_string(self):
        text1 = '$2/hour  site any  link to any site '
        text2 = '๖predator hosting | UPTIME | cheap | fast | Hosting'
        text3 = 'free irc vps Doser FREE!! for all members!!!!!!!!!!!!!!!!!!'
        text4 = '☆▄▀▄▀darkDDoSer login $15☆▀▄▀▄☆ title! darkddoser $15, on site for $25.'

        words1 = tokenize(text1)
        words2 = tokenize(text2)
        words3 = tokenize(text3)
        words4 = tokenize(text4)

        expect(words1).to(equal([
            '$2', 'hour', 'site', 'any', 'link', 'to', 'any', 'site',
        ]))
        expect(words2).to(equal([
            'predator', 'hosting', 'uptime', 'cheap', 'fast', 'hosting',
        ]))
        expect(words3).to(equal([
            'free', 'irc', 'vps', 'doser', 'free', 'for', 'all', 'members',
        ]))
        expect(words4).to(equal([
            'darkddoser', 'login', '$15', 'title', 'darkddoser', '$15', 'on', 'site', 'for', '$25',
        ]))
