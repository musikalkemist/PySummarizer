# PySummarizer
PySummarizer is a python library that allows you to perform automatic text summarization using word frequency and sentence position.

# Usage
Import the PySummarizer class:
```python
   from pysummarizer.summarizer import PySummarizer
```
Instantiate a PySummarizer object and use the 'summarize' method to produce a summary:  
```python
   text = "This is the text you want to summarize..."
   ps = PySummarizer() 
   summary = ps.summarize(text) 
```
Optionally, you can specify the max length of the summary in no. of words passing it as the second argument of 'summarize' (default max length = 150 words): 
```python
   ...
   # create a summary which is at most 100 words long  
   summary = ps.summarize(text, 100) 
```


# Installation
To install PySummarizer, use the following code:
```
   $ pip install pysummarizer
```
# Dependencies
You need to have the NLTK library installed to use PySummarizer.
