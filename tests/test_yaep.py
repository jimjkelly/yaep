import os
import io
from unittest import TestCase
from .utils import monkey_patch
import yaep


class TestStrToBool(TestCase):
    def run_cases(self, test_cases, boolean_map=None):
        for string, expected in test_cases:
            try:
                assert(yaep.utils.str_to_bool(string, boolean_map) == expected)
            except AssertionError:
                print 'Error testing {} - expected {}, but got {}'.format(
                    string,
                    str(expected),
                    str(yaep.utils.str_to_bool(string))
                )
                raise

    def test_bools(self):
        test_cases = [
            ('True', True),
            ('true', True),
            ('tRue', True),
            ('1', True),
            ('False', False),
            ('false', False),
            ('faLse', False),
            ('0', False)
        ]

        self.run_cases(test_cases)

    def test_nonbool_str(self):
        test_cases = [
            ('Pony', 'Pony'),
            (u'Pony', u'Pony')
        ]

        self.run_cases(test_cases)

    def test_nonstr(self):
        self.assertRaises(AttributeError, yaep.utils.str_to_bool, 1)

    def test_custom_boolmap(self):
        test_cases = [
            ('True', True),
            ('true', True),
            ('tRue', True),
            ('1', True),
            ('Pony', True)
        ]

        self.run_cases(test_cases, boolean_map={
            True: ['True', '1', 'Pony']
        })


class TestEnv(TestCase):
    def test_not_in_env(self):
        assert(yaep.env('FOOA') is None)

    def test_default(self):
        assert(yaep.env('FOOB', 'bar') == 'bar')

    def test_sticky(self):
        assert(os.getenv('FOOC') is None)
        yaep.env('FOOC', 'bar', sticky=True)
        assert(os.getenv('FOOC') == 'bar')

    def test_convert_boolean(self):
        yaep.env('FOOD', 'True', sticky=True)
        assert(yaep.env('FOOD') is True)
        assert(yaep.env('FOOD', convert_booleans=False) == 'True')

    def test_raise_unset_exception(self):
        with self.assertRaises(yaep.exceptions.UnsetException):
            yaep.env('BEER', default=yaep.exceptions.UnsetException)


class TestPopulateEnv(TestCase):
    def test_populate_env(self):
        env_file = io.BytesIO('foo = bar\nbaz = biz\nBOO = FAR')
        with monkey_patch(yaep.yaep, 'open', lambda fn: env_file):
            yaep.yaep.populate_env()
            assert(yaep.env('foo') == 'bar')
            assert(yaep.env('baz') == 'biz')
            assert(yaep.env('BOO') == 'FAR')
