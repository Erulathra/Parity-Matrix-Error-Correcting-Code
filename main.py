from read_file import read_and_encode, read_and_decode

# INFO
# Plik wejściowy musi mieć nazwę "plik.txt"
# Plik wyjściowy po zakodowaniu ma nazwę "encoded.txt";
#   Taka sama nazwa jest zarezerwowana dla pliku wejściowego dla poprawienia i odkodowania
# Plik wyjściowy po zdekodowaniu ma nazwę "fixed.txt"
def main():
    try:
        user = str(input("Choose whether you want to encode (e), or decode (d) file"))
        if user == 'e':
            read_and_encode()

        elif user == 'd':
            read_and_decode()
    except:
        print("Something goes wrong")


if __name__ == "__main__":
    main()
