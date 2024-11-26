import unittest

from solution import sum_two


class TestStrictDecorator(unittest.TestCase):

    def test_valid_types(self):
        result = sum_two(1, 2)
        self.assertEqual(result, 3)

    def test_invalid_first_argument(self):
        with self.assertRaises(TypeError) as context:
            sum_two(1.2, 2)

        self.assertIsInstance(context.exception, TypeError)

    def test_invalid_second_argument(self):
        with self.assertRaises(TypeError) as context:
            sum_two(1, 2.2)
        self.assertIsInstance(context.exception, TypeError)

    def test_invalid_both_arguments(self):
        with self.assertRaises(TypeError) as context:
            sum_two('1', '2')
        self.assertIsInstance(context.exception, TypeError)


if __name__ == "__main__":
    unittest.main()
