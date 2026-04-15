from birdcage import Phrase, Text
import unittest


class TestText(unittest.TestCase):

    def test_create_text_object(self):
        self.assertEqual(sorted(Text(111, 22, 3, 555555).items),
                         ['111', '22', '3', '555555'])
        self.assertEqual(Text(111, 22, 3, 555555).cur_len, 1)

    def test_create_trim_text_object(self):
        self.assertEqual(Text('message', trim=True).items,
                         ['message'])
        self.assertEqual(Text('message', trim=True).cur_text(),
                         'message')
        self.assertEqual(Text('message', trim=True, trim_length=10).cur_len,
                         7)
        self.assertEqual(Text('message', trim=True, trim_length=5,
                              trim_delim='.').cur_len, 7)

    def test_iterate_text_object(self):
        text_object = Text('a', 'bb', 'ccc', 'dddd')
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
        text_object = Text('a', 'bb', 'ccc', 'dddd')

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
        self.assertEqual(Text('a', 'bb', 'ccc', 'dddd').lens, [1, 2, 3, 4])
        self.assertEqual(Text(1, 22, 333, 4444).lens, [1, 2, 3, 4])

    def test_custom_trim_delim(self):
        t = Text('a long message here', trim=True, trim_delim='…')
        result = t.cur_text(trim_length=10)
        self.assertTrue(result.endswith('…'))
        self.assertLessEqual(len(result), 10)

        t2 = Text('a long message here', trim=True, trim_delim='..')
        result2 = t2.cur_text(trim_length=10)
        self.assertTrue(result2.endswith('..'))
        self.assertLessEqual(len(result2), 10)


class TestPhrase(unittest.TestCase):
    def setUp(self):
        self.text_a = Text('a', 'aa')
        self.text_b = Text('b', 'bb')
        self.text_trim = Text('longer message', trim=True, min_length=5)
        self.text_long_trim = Text('this is a much longer message',
                                   trim=True)

    def test_non_trim_length(self):
        test_phrase = Phrase(self.text_a, self.text_b)
        self.assertEqual(test_phrase._non_trim_length(), 2)

    def test_phrase_object(self):
        self.assertEqual(Phrase(self.text_a, self.text_b).generate(),
                         'aa bb')
        self.assertEqual(Phrase(self.text_a, self.text_trim).generate(),
                         'aa longer message')

    def test_phrase_delim_object(self):
        self.assertEqual(
            Phrase(self.text_a, self.text_b).generate(delimiter=', '),
            'aa, bb')
        self.assertEqual(
            Phrase(self.text_a, self.text_trim).generate(delimiter=', '),
            'aa, longer message')

    def test_phrase_length_object(self):
        self.assertEqual(
            Phrase(self.text_a, self.text_b).generate(length=50),
            'aa bb')
        self.assertEqual(
            Phrase(self.text_a, self.text_trim).generate(length=50),
            'aa longer message')

        self.assertEqual(
            Phrase(self.text_a, self.text_b).generate(length=10),
            'aa bb')
        self.assertEqual(
            Phrase(self.text_a, self.text_trim).generate(length=10),
            'a longe...')

        self.assertEqual(
            Phrase(self.text_a, self.text_long_trim).generate(length=50),
            'aa this is a much longer message')

        with self.assertRaises(ValueError):
            Phrase(self.text_a, self.text_b).generate(length=1)

    def test_phrase_example(self):
        text_a = Text('one hour, fourty-five minutes',
                       '1 hour, 45 minutes', '1h45m', '1:45')
        text_b = Text('until armageddon strikes the earth', trim=True)
        self.assertEqual(
            Phrase(text_a, text_b).generate(length=40),
            '1h45m until armageddon strikes the earth')

        text_a = Text('one hour, fourty-five minutes',
                       '1 hour, 45 minutes', '1h45m', '1:45')
        text_b = Text('until armageddon strikes the earth', trim=True)
        self.assertEqual(
            Phrase(text_a, text_b).generate(length=30),
            '1h45m until armageddon stri...')

        text_a = Text('one hour, fourty-five minutes',
                       '1 hour, 45 minutes', '1h45m', '1:45')
        text_c = Text('until armageddon strikes the earth',
                       min_length=22, trim=True)
        self.assertEqual(
            Phrase(text_a, text_c).generate(length=30),
            '1:45 until armageddon strik...')

    def test_generate_idempotent(self):
        text_a = Text('one hour, fourty-five minutes',
                       '1 hour, 45 minutes', '1h45m', '1:45')
        text_b = Text('until armageddon strikes the earth', trim=True)
        phrase = Phrase(text_a, text_b)

        result1 = phrase.generate(length=40)
        result2 = phrase.generate(length=40)
        self.assertEqual(result1, result2)

        result3 = phrase.generate(length=30)
        result4 = phrase.generate(length=30)
        self.assertEqual(result3, result4)

    def test_single_text(self):
        text = Text('hello', 'hi')
        self.assertEqual(Phrase(text).generate(), 'hello')
        self.assertEqual(Phrase(text).generate(length=3), 'hi')

    def test_single_trimmable_text(self):
        text = Text('hello world', trim=True, min_length=3)
        result = Phrase(text).generate(length=8)
        self.assertEqual(result, 'hello...')
        self.assertLessEqual(len(result), 8)

    def test_no_trimmable_with_length(self):
        text_a = Text('a', 'aa')
        text_b = Text('b', 'bb')
        result = Phrase(text_a, text_b).generate(length=4)
        self.assertEqual(result, 'aa b')

    def test_all_trimmable(self):
        text_a = Text('hello world', trim=True)
        text_b = Text('goodbye world', trim=True)
        result = Phrase(text_a, text_b).generate(length=50)
        self.assertEqual(result, 'hello world goodbye world')
