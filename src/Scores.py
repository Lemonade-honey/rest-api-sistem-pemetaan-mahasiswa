from .Support import ArraySupport
from static import StaticMatakuliah

class TranskipScores:

    def label_transkip_nilai(self, transkip_nilai: dict):
        data = list()

        for kode, nilai in transkip_nilai.items():
            label = ArraySupport().find_key_by_value(StaticMatakuliah.label, kode)

        #     hanya yang berlabel
            if label:
                data.append({label : ArraySupport().find_value(StaticMatakuliah.nilai, nilai)})

        # menggabungkan key yang sama
        data = ArraySupport().combined_same_key(data)

        # menjumlahkan value score dengan key yang sama
        score_sum = ArraySupport().sum_values_by_keys(data)

        return score_sum

    # get score transkip
    def point_of_transkip_nilai(self, last_row_transkip_nilai: list)-> int:
        
        last_data = last_row_transkip_nilai.pop()

        return last_data

    # mengisi label yang tidak ada
    def fill_empty_labels(self, label_transkip: dict)-> dict:

        for label in StaticMatakuliah.label:
            if label not in label_transkip:
                label_transkip[label] = 0

        return label_transkip
    
class AchievementTranskip:

    # mendapatkan pencapaina apa saja pada nilai transkip
    def badge_achievement_transkip(self, transkip_nilai: dict)-> dict:

        # mengubah nilai huruf menjadi angka
        for kode, nilai in transkip_nilai.items():
            transkip_nilai[kode] = ArraySupport().find_value(StaticMatakuliah.nilai, nilai)

        achievement = dict()
        # ambil keysnya, kode matkulnya saja
        transkip_kode = set(transkip_nilai.keys())

        for badge, kode in StaticMatakuliah.badge.items():
            if set(kode).issubset(transkip_kode):
                
                # total gabungan nilai untuk tiap badge
                total_sum = sum(value for key, value in transkip_nilai.items() if key in kode)

                achievement[badge] = self.level_badge_achievement(int((total_sum / len(kode)) * 10))
        
        return achievement
    
    # memberikan level pada badge sesuai dengan avg score yang diberikan
    def level_badge_achievement(self, avg_score: int)-> int:
        
        if avg_score >= 90:
            return 2
        
        elif avg_score >= 85 and avg_score < 90:
            return 1
        
        else:
            return 0