import re
from text_sample import die_verwandlung

# The context of a word is defined as the 3 words that preceed it + 3 words that follow it
#
# calculate a context for each word of the text received as input
#
CONTEXT_SIZE = 3
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
    text_array = get_text_as_array_of_words(text_to_analyze)
    text_size = len(text_array)

    for iterator in range(0, text_size):
        word = text_array[iterator]
        local_context = get_local_context(text_array, iterator)
        merge_in_larger_context(context, local_context, word)

    return context

def get_text_as_array_of_words(text_to_split: str):
    """
    example:
        from
        \"""
        Franz Kafka:
        DIE VERWANDLUNG
        I.
        ALS Gregor Samsa eines Morgens aus unruhigen
        \"""
        to
        ['Franz', 'Kafka', 'DIE', 'VERWANDLUNG', 'I', 'ALS', 'Gregor', 'Samsa', 'eines',
        'Morgens', 'aus', 'unruhigen']
    """
    pattern = re.compile('\w+')
    return re.findall(pattern, text_to_split)

def get_local_context(text_array, iterator):
    """
    example:
        ['', '', '']
    """
    text_size = len(text_array)
    word = text_array[iterator]
    context_start = max(0, iterator - CONTEXT_SIZE)
    context_end = min(text_size, iterator + CONTEXT_SIZE)
    word_context = dict()

    for i in range(context_start, context_end):
        neighbor_word = text_array[i]
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
    f = open('result.txt', 'w')
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
