DayOne Audio Summarizer
=======================

This is a simple utility to process transcriptions from DayOne audio entries into Markdown, complete with a summary of
the transcriptions. [`punctuator`](https://pypi.org/project/punctuator/) is used to infer punctuation, and
the TextRank implementation from [`gensim`](https://radimrehurek.com/gensim/) is used for (extractive) text summarization.

## Setup (Requires Python 3.7)
* `pip install -r requirements.txt`
* `pip install -e .`

## Usage
* `doas <dayone-json-export>.zip <output-path>`