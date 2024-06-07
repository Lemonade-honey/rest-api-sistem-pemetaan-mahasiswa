class StaticMatakuliah:
    matakuliah = {
        "211810811" : "Praktikum Dasar Pemrograman", # 1
        "211810331" : "Dasar Sistem Komputer",
        "211820430" : "Arsitektur Komputer",
        "211830641" : "Statistika Informatika", # 3
        "211830431" : "Pemrograman Berorientasi Objek", # 3

        "211860831" : "Sistem Informasi Geografis",
        "211860120" : "Manajemen Proyek Teknologi Informasi", # 5
        "211861331" : "Pengembangan Aplikasi Game", # 6

        # data sains
        "211810531" : "Logika Informatika", # 1
        "211820230" : "Algoritma Pemrograman", # 2
        "211840831" : "Strategi Algoritma", # 4
        "211850831" : "Penambangan Data/Data Mining",
        "211850420" : "Teori Bahasa Otomata",
        "211861231" : "Pemrosesan Bahasa Alami", # 6

        # sistem cerdas
        "211840531" : "Kecerdasan Buatan", # 4
        "211861131" : "Deep Learning", # 6
        "211861531" : "Pengelihatan Komputer", # 6
        "211861431" : "Pengenalan Pola", # 6

        # ui/ux class
        "211861031" : "Visualisasi Data", # 6
        "211860431" : "Teknologi Multimedia", # 6
        "211840231" : "Grafika Komputer", # 4

        # progammer
        "211820731" : "Pemrograman Web", # 2
        "211850731" : "Pemrograman Web Dinamis", # 5
        "211860731" : "Rekayasa Web", # 6
        # progammer
        "211850131" : "Keamanan Komputer", # 5
        "211860631" : "Kriptografi", # 6
        "211850531" : "Forensik Digital",
        "211850231" : "Pemrograman Mobile",

    }

    # mapping matakuliah
    label = {
        # sistem cerdas class
        "sistem cerdas" : [
            "211840531",
            "211861131",
            "211861531",
            "211861431"
        ],

        "data sains": [
            "211850831",
            "211810531",
            "211820230",
            "211840831",
            "211850420",
            "211861231",
        ],

        # ui/ux class
        "ui/ux" : [
            "211861031",
            "211860431",
            "211840231",
        ],

        # progammer class
        "progammer" : [
            "211820731",
            "211850731",
            "211860731",
            "211850131",
            "211860631",
            "211850531",
            "211850231",
        ]
    }

    ranah = {
        "1" : [
            "211810531",
            "211810811"
        ],

        "2" : [
            "211820230",
            "211820731"
        ],

        "3" : [
            "211830641",
            "211830431"
        ],

        "4" : [
            "211840831",
            "211840231",
            "211840531"
        ],

        "5" : [
            "211860120",
            "211850131",
            "211850731"
        ],

        "6" : [
            "211861231",
            "211861331",
            "211860631",
            "211861131",
            "211861531",
            "211861431",
            "211861031",
            "211860431",
            "211860731"
        ],

        "7" : [

        ],

        "8" : [

        ]
    }

    nilai = {
        "A" : 10,
        "A-": 9,
        "B+" : 8, # high end
        "B" : 7,
        "B-" : 6,
        "C+" : 5, # middle end
        "C" : 4,
        "C-" : 3,
        "D+" : 2,
        "D" : 1,
        "D-" : 0,
        "E": 0
    }

    badge = {
        'web progammer' : [
            "211820731",
            "211850731",
            "211860731"
        ],

        'mobile progammer' : [
            "211850231"
        ],

        'cyber crime analysis' : [
            "211850531"
        ],

        'data mining' : [
            "211850831"
        ],

        'fundamental progamming': [
            "211810811",
            "211830641",
            "211830431",
            "211810531",
            "211820230",
            "211840831"
        ],

        'machine learning progammer' : [
            "211840531",
            "211861131"
        ],

        'basic computer knowladge': [
            "211810331",
            "211820430"
        ]
    }