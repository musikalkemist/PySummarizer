# coding: utf-8
""" 
(c) Valerio Velardo, velardovalerio@gmail.com, April 2015
    
This file contains the PySummarize class, which creates a summary for a text 
using word frequency and sentence position. PySummarize has a single public 
method (i.e, 'summarize') responsible for generating a summary:
Input 'summarize': 
    text to be summarised (string)
    max length summary in no. of words (int). Optional parameter (default=150) 
Output 'summarize':
    summary (string)
"""

import operator
from math import log
from string import punctuation
from collections import defaultdict
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
     
     
class PySummarizer:    
    def __init__(self, min_cut=0.1, max_cut=0.9, max_redundancy=0.4):
        """ Initialize a Summarizer object"""
        
        self._min_cut = min_cut
        self._max_cut = max_cut 
        self._stopwords = set(stopwords.words('english') + list(punctuation))
        self._max_redundancy = max_redundancy
        
    def summarize(self, text, max_words=150):
        """ Provide summary made up of more salient sentences for a text. 
            Input: text (str), max words for summary (int) (optional).
            Output: summary (str)."""
        
        self._max_words = max_words
        text = unicode(text, errors='ignore')
        self._word_sents = self._preprocess(text)
        self._ranking = self._rank_sentences()
        summary = self._choose_sentences()
        return summary
        
    def _preprocess(self, text):
        """ Return a list of lists. Each list is a preprocessed sentence of 
            text in bag-of-words format."""
        
        stemmer = PorterStemmer()
        self._sents = sent_tokenize(text)
        # tokenize sentences
        word_sents = [word_tokenize(sent.lower()) for sent in self._sents]
        # remove stop-words and stem words
        word_sents = [[stemmer.stem(word) for word in sent if 
            word not in self._stopwords] for sent in word_sents]
        return word_sents
    
    def _compute_frequency(self, word_sents):
        """ Compute frequency of words in text. Return dictionary of the type
            word: frequency."""
        
        frequency = defaultdict(int)
        for sent in word_sents:
            for word in sent:
                frequency[word] += 1
        # frequencies normalization and fitering
        max_freq = float(max(frequency.values()))
        for word in frequency.keys():
          frequency[word] = frequency[word]/max_freq
          if self._min_cut <= frequency[word] <= self._max_cut:
            del frequency[word]
        return frequency
        
    def _rank_sentences(self):
        """ Rank sentences based on relevane. Return dictionary of the type 
            sentence id: score."""
        
        frequency = self._compute_frequency(self._word_sents)
        score = defaultdict(int)
        no_sents = float(len(self._word_sents))
        for i,sent in enumerate(self._word_sents):
          for word in sent:
            if word in frequency:
              score[i] += frequency[word] * (no_sents - i + 1) / no_sents
        ranking = sorted(score.items(), key=operator.itemgetter(1))
        ranking.reverse()
        return ranking
                 
    def _choose_sentences(self):
        """ Select the sentences that make up the summary, based on their 
            ranking."""
            
        summary = ""
        sents_id_chosen = []
        for i in range(len(self._sents)):
            summary_check = summary
            sent_id = self._ranking[i][0]
            summary_check += self._sents[sent_id]
            if len(summary_check.split()) >= self._max_words:
                break
            else:
                # check for redundancy of new sentence
                if i == 0:
                    summary += self._sents[sent_id]
                    sents_id_chosen.append(sent_id)
                elif i > 0 and self._redundancy_ok(i, sents_id_chosen):
                    summary += self._sents[sent_id]
                    sents_id_chosen.append(sent_id)
                else:
                    continue
        return summary        
        
    def _redundancy_ok(self, no_iterations, sents_id_chosen):
        """ Check if sentence is too similar to previous sentences in 
            summary, using Jaccard similarity."""
            
        sent_to_check = set(self._word_sents[self._ranking[no_iterations][0]])
        redundancy_ok = True
        for n in range(len(sents_id_chosen)):
            sent_in_summary = set(self._word_sents[sents_id_chosen[n]])
            jaccard_similarity = (len(sent_to_check & sent_in_summary) / 
                float(len(sent_to_check | sent_in_summary)))
            if jaccard_similarity > self._max_redundancy:
                    redundancy_ok = False
                    break
        return redundancy_ok
                
    



        
        
        
        
