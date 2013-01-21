from birdcage import (Phrase,
                      Text)
import unittest

class TestText(unittest.TestCase):
    # lens, select, cur_text, cur_len, next_len, select_next

    def test_create_unicode_text_object(self):
        self.assertEqual(sorted(Text(111,22,3,555555).items), \
            [u'111', u'22', u'3', u'555555'])
        self.assertEqual(Text(111,22,3,555555).cur_len, 1)

    def test_create_trim_text_object(self):
        self.assertEqual(Text('message', trim=True).items, \
            [u'message'])
        self.assertEqual(Text('message', trim=True).cur_text(), \
            u'message')
        self.assertEqual(Text('message', trim=True, trim_length=10).cur_len, \
            7)
        self.assertEqual(Text('message', trim=True, trim_length=5, \
            trim_delim='.').cur_len, 7)

    def test_iterate_text_object(self):
        text_object = Text('a','bb','ccc','dddd')
        self.assertEqual(text_object.cur_text(), 'a')
        self.assertEqual(text_object.selected, 0)
        self.assertEqual(text_object.cur_len, 1)
        self.assertEqual(text_object.next_len, 2)

        text_object.select_next()
        self.assertEqual(text_object.cur_text(), 'bb')
        self.assertEqual(text_object.selected, 1)
        self.assertEqual(text_object.cur_len, 2)
        self.assertEqual(text_object.next_len, 3)

        text_object.select_next()
        self.assertEqual(text_object.cur_text(), 'ccc')
        self.assertEqual(text_object.selected, 2)
        self.assertEqual(text_object.cur_len, 3)
        self.assertEqual(text_object.next_len, 4)

        text_object.select_next()
        self.assertEqual(text_object.cur_text(), 'dddd')
        self.assertEqual(text_object.selected, 3)
        self.assertEqual(text_object.cur_len, 4)
        self.assertEqual(text_object.next_len, None)

        with self.assertRaises(IndexError):
            text_object.select_next()

    def test_select_text_object(self):
        text_object = Text('a','bb','ccc','dddd')

        text_object.select(0)
        self.assertEqual(text_object.cur_text(), 'a')

        text_object.select(1)
        self.assertEqual(text_object.cur_text(), 'bb')

        text_object.select(2)
        self.assertEqual(text_object.cur_text(), 'ccc')

        text_object.select(3)
        self.assertEqual(text_object.cur_text(), 'dddd')

        with self.assertRaises(IndexError):
            text_object.select(4)
        with self.assertRaises(IndexError):
            text_object.select(-1)

    def test_lens_text_object(self):
        self.assertEqual(Text('a','bb','ccc','dddd').lens, [1, 2, 3, 4])
        self.assertEqual(Text(1, 22, 333, 4444).lens, [1, 2, 3, 4])

class TestPhrase(unittest.TestCase):
    def setUp(self):
        self.text_a = Text('a', 'aa')
        self.text_b = Text('b', 'bb')
        self.text_trim = Text('longer message', trim=True, min_length=5)
        self.text_long_trim = Text('this is a much longer message', \
            trim=True)

    def test_phrase_object(self):
        self.assertEqual(Phrase(self.text_a,self.text_b).generate(), \
            u'aa bb')
        self.assertEqual(Phrase(self.text_a,self.text_trim).generate(), \
            u'aa longer message')

    def test_phrase_delim_object(self):
        self.assertEqual(Phrase(self.text_a,self.text_b). \
            generate(delimiter=', '), u'aa, bb')
        self.assertEqual(Phrase(self.text_a,self.text_trim). \
            generate(delimiter=', '), u'aa, longer message')
   
    def test_phrase_length_object(self):
        self.assertEqual(Phrase(self.text_a,self.text_b). \
            generate(length=50), u'aa bb')
        self.assertEqual(Phrase(self.text_a,self.text_trim). \
            generate(length=50), u'aa longer message')

        self.assertEqual(Phrase(self.text_a,self.text_b). \
            generate(length=10), u'aa bb')
        self.assertEqual(Phrase(self.text_a, self.text_trim). \
            generate(length=10), u'a longe...')

        self.assertEqual(Phrase(self.text_a, self.text_long_trim). \
            generate(length=50), u'aa this is a much longer message')

    def test_phrase_example(self):
        text_a = Text('one hour, fourty-five minutes', '1 hour, 45 minutes', \
            '1h45m', '1:45')
        text_b = Text('until armageddon strikes the earth', trim=True)
        self.assertEqual(Phrase(text_a, text_b). \
            generate(length=40), u'1h45m until armageddon strikes the ea...')
