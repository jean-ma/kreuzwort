import unittest
from simple_context_analyzer import merge_in_larger_context, get_text_as_array_of_words, get_local_context, sort_by_frequency

class TestSimpleContextAnalyzer(unittest.TestCase):
    
    def test_merge_in_larger_context(self):
        larger_context = {'word1': {'a': 2, 'c': 3, 'e':1}}
        local_context = {'word1': {'a': 1, 'b': 2, 'e':1}}
        word = 'word1'
        actual_result = merge_in_larger_context(larger_context, local_context, word)
        expected_result = {'word1': {'a': 3, 'b': 2, 'c': 3, 'e':2}}

        self.assertEqual(actual_result, expected_result)

    def test_get_text_as_array_of_words(self):
        text_to_split = """

        Franz Kafka:
        DIE VERWANDLUNG
        I.
        ALS Gregor Samsa eines Morgens aus unruhigen
        """
        actual = get_text_as_array_of_words(text_to_split)
        expected = ['Franz', 'Kafka', 'DIE', 'VERWANDLUNG', 'I', 'ALS', 'Gregor', 'Samsa', 'eines',
        'Morgens', 'aus', 'unruhigen']
        self.assertEqual(actual, expected)
    
    def test_get_local_context(self):
        text_array = ['Franz', 'Kafka', 'DIE', 'VERWANDLUNG', 'I', 'ALS', 'Gregor', 'Samsa', 'eines',
        'Morgens', 'aus', 'unruhigen']

        actual = get_local_context(text_array, 3)
        expected = {'VERWANDLUNG': {'Franz': 1, 'Kafka': 1, 'DIE': 1, 'I': 1, 'ALS': 1}}

        self.assertEqual(actual, expected)
    
    def test_sort_by_frequency(self):
        single_context_to_sort = {'Franz': 1, 'Kafka': 1, 'DIE': 5, 'I': 2, 'ALS': 3}
        actual = sort_by_frequency(single_context_to_sort)
        expected = [('DIE', 5), ('ALS', 3), ('I', 2), ('Franz', 1), ('Kafka', 1)]

        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
