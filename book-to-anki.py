#################### SPEC ####################

# want this script to take the text of a book (either txt or epub, MAYBE pdf if not too difficult) and convert it to anki cards for unknown vocab

# should utilize a cache for words already ankified, one word per line

# should have reference files for top 5k / 10k / 15k / 20k english words, but can take in a wordlist with one word per line

# usage should be:
# > python book-to-anki.py bookTitle.txt [-l wordList or path to folder containing wordlists] [-c path/to/cache] [-f (to not confirm)]
# Parsing bookTitle.txt using default wordlists and default cache at cachePath...
# (1) Use 3450 words not in top5000English.txt
# (2) Use 1504 words not in top10000English.txt
# (3) Use 129 words not in top15000English.txt
# (4) Use 94 words not in top20000English.txt
# > 5
# 5 is not an option, please select from available word lists
# > 4
# Moving on to adding words to cards and cache. At any point type 'f' to add all remaining words. 
# Add 'brillig'? (y/n)
# > y
# Add 'osteoporosis'? (y/n)
# > f
# Adding 93 remaining words...
# Finished adding 94 total words to cards and cache. All done!

# should use a dictionary API to get definitions, add the cards as the type "Basic (and Reversed)" with one side being the word and the other side being the definition

#################### CODE ####################

import argparse
import re
import os
import requests

parser = argparse.ArgumentParser()

def load_wordlist(wordlist_path):
    """
    Loads wordlist(s) from a file or a folder. If a directory is passed, all text files are loaded as separate lists.
    
    Args:
        wordlist_path (str): Path to a wordlist file or folder.
        
    Returns:
        dict: A dictionary with filenames or indices as keys and sets of words as values.
    """
    try:
        # check if directory of wordlists...
        if os.path.isdir(wordlist_path):
            lists = {}
            for file in sorted(os.listdir(wordlist_path)):
                file_path = os.path.join(wordlist_path, file)
                if file_path.endswith('.txt'):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lists[file] = set(word.strip().lower() for word in f)
            return lists
        # ...or single wordlist file
        else:
            with open(wordlist_path, 'r', encoding='utf-8') as f:
                return {wordlist_path: set(word.strip().lower() for word in f)}
    except FileNotFoundError as e:
        print(f"Error: Word list file or path '{wordlist_path}' not found.")
        raise e

def load_cache(cache_path):
    try:
        with open(cache_path, 'r', encoding='utf-8') as f:
            return set(line.strip().lower() for line in f)
    except FileNotFoundError as e:
      print(f"Error: Cache file '{cache_path}' not found.")
      raise e
  
def load_text(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read().lower()
    except Exception as e:
      print(f"Error loading text from '{path}'.")
      raise e

def tokenize(text):
    # todo do the lowercasing here for words at the start of a sentence, and discard proper nouns
    return re.findall(r'\b[a-z]+\b', text)


def get_definition(word):
    try:
        res = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}", timeout=5)
        data = res.json()
        if isinstance(data, list) and 'meanings' in data[0]:
            defs = []
            for meaning in data[0]['meanings']:
                for defn in meaning['definitions']:
                    defs.append(defn['definition'])
            return '; '.join(defs[:2])  # limit to 2 definitions
        else:
            return "No definition found."
    except Exception:
        return "Definition lookup failed."

def save_card(word, definition, output_path):
    with open(output_path, 'a', encoding='utf-8') as f:
        word = word.replace('"', '""')
        definition = definition.replace('"', '""')
        f.write(f"\"{word}\";\"{definition}\"\n")

def save_to_cache(word, cache_path):
    with open(cache_path, 'a') as f:
        f.write(f"{word}\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("book", help="Path to the book text file")
    parser.add_argument("-l", "--word-list", default="wordlists", help="Word list path or folder")
    parser.add_argument("-c", "--cache", default="cache.txt", help="Cache path")
    parser.add_argument("-f", "--force-confirm", action="store_true", help="Add all words without confirming")
    parser.add_argument("-o", "--output", help="Output file path")
    args = parser.parse_args()

    book_path = args.book
    wordlist_path = args.word_list
    cache_path = args.cache
    force_confirm = args.force_confirm
    if args.output:
        output_path = args.output
    else:
        base_name = os.path.splitext(os.path.basename(book_path))[0]
        output_path = f"{base_name}AnkiCards.txt"

    print(f"Parsing {book_path} using wordlist(s) at {wordlist_path} and cache at {cache_path}...")

    text = load_text(book_path)
    words = set(tokenize(text))
    cache = load_cache(cache_path)

    wordlists = load_wordlist(wordlist_path)

    candidates_by_wordlist = {}

    for list_name, common_words in wordlists.items():
        uncommon = words - common_words  # Uncommon words are those in book, but not in wordlist
        filtered = sorted(uncommon - cache)
        candidates_by_wordlist[list_name] = filtered

    print("Available wordlists:")
    for i, list_name in enumerate(wordlists.keys(), start=1):
        print(f"({i}) {list_name} with {len(candidates_by_wordlist[list_name])} words")

    selection = None
    while selection not in map(str, range(1, len(wordlists) + 1)):
        selection = input("> ")
        if selection not in map(str, range(1, len(wordlists) + 1)):
            print("Invalid selection, try again.")

    selected_wordlist = list(wordlists.keys())[int(selection) - 1]
    selected_words = candidates_by_wordlist[selected_wordlist]

    print("Moving on to adding words to cards and cache. At any point type 'f' to add all remaining words.")

    count = 0
    i = 0
    while i < len(selected_words):
        word = selected_words[i]
        save_to_cache(word, cache_path)

        # Ask for confirmation if not in force mode
        if not force_confirm:
            ans = input(f"Add '{word}'? (y/n/f) > ").strip().lower()
            if ans == 'y':
                pass
            elif ans == 'f':
                force_confirm = True
                print(f"Adding {len(selected_words) - i} remaining words...")
            else:
                i += 1
                continue

        defn = get_definition(word)
        if defn and defn != "No definition found." and defn != "Definition lookup failed.":
            save_card(word, defn, output_path)
            count += 1

        i += 1

    print(f"Finished adding {count} total cards. All done!")

if __name__ == "__main__":
    main()
