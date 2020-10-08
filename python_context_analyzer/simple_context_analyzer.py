import spacy

from text_sample import die_verwandlung

# The context of a word is defined as the 3 words that preceed it + 3 words that follow it
#
# calculate a context for each word of the text received as input
#
CONTEXT_SIZE = 3


class TokenArray:
    def __init__(self, token_array):
        self.token_array = token_array

    def get_text_at(self, index):
        return self.token_array[index].lemma_

    def get_token_at(self, index):
        return self.token_array[index]

    def get_len(self):
        return len(self.token_array)


def get_word_to_context(text_to_analyze):
    # context is a mapping of word -> context
    # example: [
    #   überwunden: [('Spiel', 1), ('verfallen', 1), ('war', 1), ('hatte', 1), ('sich', 1)],
    #   überzeugt: [('und', 2), ('mußte', 1), ('gehalten', 1), ('beruhigt', 1), ('schließlich', 1)],
    #   übrig: [('nichts', 2), ('doch', 1), ('anderes', 1), ('denn', 1), ('er', 1)],
    #   übrigen: [('Im', 3), ('der', 2), ('verlassen', 1), ('haben', 1), ('wird', 1)],
    #   übrigens: [('er', 3), ('war', 2), ('hinausfliegen', 1), ('Wer', 1), ('weiß', 1)],
    #   ]
    context = dict()
    nlp = spacy.load('de_core_news_md')
    text_array = TokenArray([token for token in nlp(text_to_analyze) if not token.is_stop and token.is_alpha])
    text_size = text_array.get_len()

    for iterator in range(0, text_size):
        local_context = get_local_context(text_array, iterator)
        merge_in_larger_context(context, local_context, text_array.get_text_at(iterator))

    return context


def get_local_context(text_array: TokenArray, iterator):
    """
    example:
        ['', '', '']
    """
    text_size = text_array.get_len()
    word = text_array.get_text_at(iterator)
    context_start = max(0, iterator - CONTEXT_SIZE)
    context_end = min(text_size, iterator + CONTEXT_SIZE)
    word_context = dict()

    for i in range(context_start, context_end):
        neighbor_word = text_array.get_text_at(i)
        if neighbor_word != word:
            local_context = {word: {neighbor_word: 1}}
            word_context = merge_in_larger_context(word_context, local_context, word)

    return word_context


def merge_in_larger_context(larger_context, local_context, word):
    """ 
    example:
        larger_context = {'word1': {'a': 2, 'c': 3, 'e':1}}
        local_context = {'word1': {'a': 1, 'b': 2, 'e':1}}
        word = 'word1'

        return {'word1': {'a': 3, 'b': 2, 'c': 3, 'e':2}}
    """
    larger_neighbor = larger_context.get(word, dict())
    local_neighbor = local_context.get(word, dict())

    for neighbor_key in local_neighbor:
        larger_neighbor_value = larger_neighbor.get(neighbor_key, 0)
        local_neighbor_value = local_neighbor.get(neighbor_key)
        larger_neighbor[neighbor_key] = larger_neighbor_value + local_neighbor_value

    larger_context[word] = larger_neighbor

    return larger_context


#
# Pretty print methods
#
def pretty_print(all_contexts):
    for key in sorted(all_contexts.keys()):
        sorted_context = sort_by_frequency(all_contexts[key])
        print(key + ': ' + str(sorted_context[0:5]))


def sort_by_frequency(single_context):
    return sorted(single_context.items(), key=lambda x: x[1], reverse=True)


def pretty_print_to_file(all_contexts):
    f = open('result_for_die_verwandlung.txt', 'w')
    for key in sorted(all_contexts.keys()):
        sorted_context = sort_by_frequency(all_contexts[key])
        print(key + ': ' + str(sorted_context[0:5]), file=f)

    f.close()


#
# Main method
#
if __name__ == '__main__':
    all_contexts = get_word_to_context(die_verwandlung)
    pretty_print(all_contexts)
    # pretty_print_to_file(all_contexts)
