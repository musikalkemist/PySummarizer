# PySummarize
PySummarize is a python library that performs automatic text summarization using word frequency and sentence position.

Import the class PySummarize:
```python
   from PySummarize import PySummarize
```
Instantiate a PySummarize object and Use the 'summarize' method to produce a summary. Optionally, you can specify the max length of the summary in no. of words, passing it as the second argument of 'summarize'. The default max length is 150 words. 
```python
   text = "This is the text you want to summarize..."
   ps = PySummarize()
   # create a summary which is at most 100 words long  
   summary = ps.summarize(text, 100) 
```

# Installation


