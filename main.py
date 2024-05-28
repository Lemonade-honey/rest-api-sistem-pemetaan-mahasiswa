from src import CleaningText

def main():
    text = "ini text  yang harus a dibersihkan *kan"
    
    cleaning = CleaningText()

    bersih = cleaning.remove_all(text)

    print(bersih)

if __name__ == "__main__":
    main()