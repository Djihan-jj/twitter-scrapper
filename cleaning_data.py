from pathlib import Path
import glob

used_chars = list("abcdefghijklmnopqrstuvwxyz ")

def clean_data(source_file_name):
    # Define all file directories
    source_file = open(f"data/raw/{source_file_name}", encoding="utf8")
    list_of_words_file = open(f"data/dictionary/{source_file_name[0:-4]}-kamus.csv","w+", encoding="utf8")
    destination_file = open(f"data/case_folding/{source_file_name[0:-4]}-case_folding.csv","w+", encoding="utf8")

    # Read all lines in source file
    lines = source_file.readlines()

    # This is used for storing words that used in all tweets
    list_of_words = []

    # Iterate each line 
    for line in lines:
        
        # This is for cleaning data
        line = line.lower()
        for char in line:
            if (char not in used_chars):
                line = line.replace(char, "")
                
        # Add list of words
        list_of_words.extend(line.split())
        # print(list_of_words)

        # Write/save it to destination file
        destination_file.writelines(line)

    # Convert set of list_of_words to list to make it all unique
    list_of_words = list(set(list_of_words))
    list_of_words.sort()

    length_of_words = len(list_of_words)
    print(f"Jumlah kata ada kamus {source_file_name}: {length_of_words}")

    # Join list to string
    list_of_words_string = " ".join(list_of_words)

    # Write it to a file
    list_of_words_file.writelines(list_of_words_string)

if __name__ == '__main__':

    for filename in glob.glob("data/raw/*.csv"):
        clean_data(filename[9:])

    # print(list(used_chars))