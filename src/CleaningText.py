import string, re

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
    
    # membersihkan semuanya
    def remove_all(self, text):
        text = self.remove_special(text)
        text = self.remove_punctuation(text)
        text = self.remove_whitespace_LT(text)
        text = self.remove_single_char(text)
        text = self.remove_whitespace_multiple(text)

        return text
        