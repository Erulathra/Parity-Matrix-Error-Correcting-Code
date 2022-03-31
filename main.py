from read_file import read_and_encode, read_and_decode

# INFO
# Initial input file must have name "plik.txt"
# Output file after encoding is named "encoded.txt";
#   The same name is reserved as input file for correcting and decoding
# Output file after decoding is named "fixed.txt"
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
