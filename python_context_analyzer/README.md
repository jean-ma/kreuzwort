# Context Analyzer

Calculate the context of words. Hopefully it will help to decide which word should be learn together and which words should be put together to make a crossword.

## Definition of a context

Here the context of a word W is defined as the three words preceeding W + the three words following it. That is: a window of six words centered on W.

## Result

The algorithm has been applied to the german text "Die Verwandlung" the result can be seen in `result_for_die_verwandlung.txt`.

It doesn't seem useful. The context are mostly made of words with one single occurence. This makes it difficult to consider them as a usual context.

Improvement could be obtained through
- increasing the window size,
- using a larger text or many texts
- trying word embeddings

# Run
You need to install python [[link](https://www.python.org/downloads/)] and pipenv [[link](https://pipenv.pypa.io/en/latest/)]

Then in command line
```commandline
pipenv run python simple_context_analyzer.py
```
