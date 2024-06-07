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