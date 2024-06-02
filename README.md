# REST API CLASSIFICATION KNN
Rest API Aplication, created by 
```
daffa alif murtaja
daffa2000018160@webmail.uad.ac.id
```

## Desc Project
sebuah aplikasi untuk mengklasifikasikan text menjadi 4 kategori yaitu, sistem cerdas, progammer, ui/ux dan data sains, berdasarkan sebuah dokumen yang akan dibaca oleh aplikasi


## Command CLI
1. Server CLI
    * start server development
        ```
        fastapi dev main.py
        ```
        pastikan `main.py` berada di bawah root project

    * start server production
        ```
        fastapi run
        ```

2. Symlik Folder
    * Digunakan jika menggunakan alur **berbagi storage**, tidak untuk upload file ke project classification
    * pastikan menggunakan `cmd run as admin`
    * menghubungkan folder upload file di laravel ke classification service,
    pastikan pada project classificasai tidak ada folder `Storage`, jika ada dihapus terlebih dahulu
        ```cmd
        mklink /J "disk:(root project)\skripsi-model\Storage\" "disk:(root project)\skripsi-web-model\storage\app\public\"
        ```

        contoh full implementasi
        ```cmd
        mklink /J "F:\00.Project\0.Skripsi\skripsi-project\skripsi-model\Storage\" "F:\00.Project\0.Skripsi\skripsi-project\skripsi-web-model\storage\app\public\"
        ```

## Route

1. Upload File
    ```
    /upload-file
    ```
    * `request` berupa file
    * pada file upload, hanya boleh diperbolehkan `.pdf`
    * return `responsenya` merupakan nama folder, berupa 7 digit nomer acak
    * file hasil upload ditaruh di folder storages


2. Delete File
    ```
    /delete-file
    ```
    * `request` berupa sebuah `body`, dan isinya harus hanya sebuah `angka nama folder`
    * akan menghapus sesuai dengan nama folder yang ada di body request
    * return `responsenya` berupa bool `True`