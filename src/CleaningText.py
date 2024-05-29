import string, re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# class untuk pembersihan dan pengelolaan data 
class CleaningText:

    # membersihkan special string
    def remove_special(self, text)-> string :
        # remove tab, new line, ans back slice
        text = text.replace('\\t'," ").replace('\\n'," ").replace('\\u'," ").replace('\\',"")
        # remove non ASCII (emoticon, chinese word, .etc)
        text = text.encode('ascii', 'replace').decode('ascii')
        # remove mention, link, hashtag
        text = ' '.join(re.sub("([@#][A-Za-z]+.-)|(\w+:\/\/\S+.-)"," ", text).split())
        # remove incomplete URL
        return text.replace("http://", " ").replace("https://", " ")
    
    # remove punctuation
    def remove_punctuation(self, text)-> string:
        return text.translate(str.maketrans("","",string.punctuation))
    
    # remove whitespace leading & trailing
    def remove_whitespace_LT(self, text)-> string:
        return text.strip()
    
    # remove multiple whitespace into single whitespace
    def remove_whitespace_multiple(self, text)-> string:
        return re.sub('\s+',' ',text)
    
    # remove single char
    def remove_single_char(self, text)-> string:
        return re.sub(r"\b[a-zA-Z]\b", "", text)
    
    # Remove regular numbers
    def remove_number(self, text)->str :
        return re.sub(r'\b\d+\b', '', text)
    
    # membersihkan stemmer kata
    def remove_stemmer_word(self, text)-> str:
        # create stemmer
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()

        return stemmer.stem(text)

    def remove_romawi_number(self, text):
    # Define the regex pattern for Roman numerals in lowercase and uppercase
        roman_numeral_pattern = r'\b[mdclxvi]+\b'
        
        # Use re.sub to replace Roman numerals with an empty string
        cleaned_text = re.sub(roman_numeral_pattern, '', text)
        
        # Remove any extra whitespace created by the removal
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
        
        return cleaned_text
    
    def remove_stopwords(self, text)-> str:

        # Tokenize the text
        words = word_tokenize(text)

        # Remove stopwords from the tokenized words
        filtered_words = [word for word in words if word.lower() not in set(stopwords.words('indonesian'))]

        # Join the filtered words back into a string
        return ' '.join(filtered_words)
        
    
    # membersihkan semuanya
    def remove_all(self, text):
        text = self.remove_special(text)
        text = self.remove_punctuation(text)
        text = self.remove_whitespace_LT(text)
        text = self.remove_single_char(text)
        text = self.remove_number(text)

        text = self.remove_romawi_number(self.text_to_lower(text))

        text = self.remove_whitespace_multiple(text)

        # remove stemmer word
        text = self.remove_stemmer_word(text)

        text = self.remove_stopwords(text)

        return text
    
    # mengubah teks ke lower case
    def text_to_lower(self, text)-> str:
        return text.lower()
        