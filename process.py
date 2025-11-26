import re

def get_uncommon_words(text_file_path="/home/herman/Descargas/persuasion.txt", common_word_list_file="/home/herman/Descargas/google-10000-english-usa.txt"):
    """
    Extracts uncommon words from a text based on a provided list of common words.

    Args:
        text (str): The input text.
        common_word_list_file (str, optional): Path to a file containing common words,
                                              one word per line. Defaults to "common_words.txt".

    Returns:
        list: A list of uncommon words found in the text.
    """
    try:
        with open(common_word_list_file, 'r') as f:
            common_words = set(word.strip() for word in f)
    except FileNotFoundError:
        print(f"Error: Common word list file '{common_word_list_file}' not found.")
        return []
    
    try:
        with open(text_file_path, 'r', encoding='utf-8') as f_text:
            text = f_text.read()
    except FileNotFoundError:
        print(f"Error: Text file '{text_file_path}' not found.")
        return []
    except Exception as e:
        print(f"Error reading text file '{text_file_path}': {e}")
        return []

    text = text.lower()
    words = re.findall(r'\b\w+\b', text)  # Tokenize and keep only alphanumeric words

    uncommon_words = {word for word in words if word not in common_words}
    return uncommon_words

uncommon_words = get_uncommon_words()
print(len(uncommon_words))
print(uncommon_words)