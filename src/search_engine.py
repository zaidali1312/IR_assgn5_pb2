import math
from collections import defaultdict
import os


def load_documents(data_dir):
    """
    Load all text files from the given directory and return a list of file contents.
    """
    documents = []
    file_names = []
    
    for file_name in os.listdir(data_dir):
        if file_name.endswith(".txt"):  # Only process .txt files
            file_path = os.path.join(data_dir, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                documents.append(file.read())
                file_names.append(file_name)
    
    return documents, file_names


class SearchEngine:
    def __init__(self):
        self.documents = []
        self.file_names = []
        self.inverted_index = defaultdict(list)
        self.doc_lengths = {}
        self.avgdl = 0
        self.N = 0
        
    def preprocess(self, text):
        """
        Tokenization, stopword removal, and optional stemming/lemmatization.
        """
        return text.lower().split()  # Simple tokenization
    
    def build_index(self, data_dir):
        """
        Build an inverted index from files in the given directory.
        """
        self.documents, self.file_names = load_documents(data_dir)
        self.N = len(self.documents)
        total_length = 0
        
        for doc_id, doc in enumerate(self.documents):
            terms = self.preprocess(doc)
            self.doc_lengths[doc_id] = len(terms)
            total_length += len(terms)
            
            term_freqs = defaultdict(int)
            for term in terms:
                term_freqs[term] += 1
            
            for term, freq in term_freqs.items():
                self.inverted_index[term].append((doc_id, freq))
        
        self.avgdl = total_length / self.N

    def idf(self, term):
        """
        Compute the Inverse Document Frequency (IDF) for a term.
        """
        df = len(self.inverted_index.get(term, []))
        return math.log((self.N - df + 0.5) / (df + 0.5) + 1)
    
    def bm25(self, query, k1=1.5, b=0.75):
        """
        Compute BM25 scores for all documents given a query.
        """
        query_terms = self.preprocess(query)
        scores = defaultdict(float)
        
        for term in query_terms:
            idf = self.idf(term)
            for doc_id, freq in self.inverted_index.get(term, []):
                doc_length = self.doc_lengths[doc_id]
                score = idf * (freq * (k1 + 1)) / (freq + k1 * (1 - b + b * (doc_length / self.avgdl)))
                scores[doc_id] += score
        
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    def search(self, query, top_k=10):
        """
        Search for a query and return the top-k results with file names.
        """
        ranked_docs = self.bm25(query)
        return [(self.file_names[doc_id], score) for doc_id, score in ranked_docs[:top_k]]
