class KNNClassification:
    def __init__(self, model, vectorizer) -> None:
        self.knn_model = model
        self.vectorizer = vectorizer

    def predict_label(self, text: str)-> tuple:
        # Membuat dan menyesuaikan TfidfVectorizer dengan data latih
        text_tfidf = self.vectorizer.transform([text])

        # Lakukan prediksi
        predicted_label = self.knn_model.predict(text_tfidf)
        predicted_proba = self.knn_model.predict_proba(text_tfidf)

        # return dan ubah tipe data
        return int(predicted_label[0]), predicted_proba[0].tolist()
    
    # translate label to text
    def label_to_text(self, label)-> str :
        if label == 0 :
            return 'data sain'
        elif label == 1 :
            return 'progammer'
        elif label == 2 :
            return 'sistem cerdas'
        elif label == 3 :
            return 'ui/ux'
        else:
            return 'tidak ada label terdaftar'
        
    def probabilitas_score_labels(self, probabilitas: list)-> dict:
        # nama kunci untuk tiap indeks
        keys = ["data sain", "progammer", "sistem cerdas", "ui/ux"]

        return {keys[i]: probabilitas[i] * 100 for i in range(len(probabilitas))}