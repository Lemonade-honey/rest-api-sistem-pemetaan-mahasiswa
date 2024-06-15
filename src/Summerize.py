import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Summerize:

    def tokenize_sentance(self, text:str):
        return nltk.sent_tokenize(text)
    
    def vectorize_sentences(self, sentences):
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(sentences)
        return vectors

    # Perhitungan Cosine Similarity
    def calculate_cosine_similarity(self, vectors):
        similarity_matrix = cosine_similarity(vectors)
        return similarity_matrix
    
    # memberikan bobot rank pada text
    def rank_sentences(self, similarity_matrix):
        sentence_scores = similarity_matrix.sum(axis=1)
        ranked_sentences = [sentence for sentence in np.argsort(sentence_scores)[::-1]]
        return ranked_sentences
    
    def extract_summary(self, sentences, ranked_sentences, num_sentences):
        summary = []
        for idx in ranked_sentences[:num_sentences]:
            summary.append(sentences[idx])
        return ' '.join(summary)
    
    def summarize_text(self, text, num_sentences=3)-> str:
        sentences = self.tokenize_sentance(text)
        vectors = self.vectorize_sentences(sentences)
        similarity_matrix = self.calculate_cosine_similarity(vectors)
        ranked_sentences = self.rank_sentences(similarity_matrix)
        summary = self.extract_summary(sentences, ranked_sentences, num_sentences)

        return summary