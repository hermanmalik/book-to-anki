# book-to-anki script

This script turns book vocab into anki cards. Might be useful to dump in a book before you read it, idk.
I thought about putting in epub and pdf support. I'll probably end up doing that when the need arises for me.

Here is an example of how to use it from the shell:
```
$ python3 book-to-anki.py test-readme.txt
Parsing test-readme.txt using wordlist(s) at wordlists and cache at cache.txt...
Available wordlists:
(1) 20k.txt with 24 words
(2) google-10000-english-usa.txt with 38 words
> 1
Moving on to adding words to cards and cache. At any point type 'f' to add all remaining words.
Add 'amphetype'? (y/n/f) > y
Add 'appended'? (y/n/f) > n
Add 'badwords'? (y/n/f) > 
Add 'cheerfulstoic'? (y/n/f) > 
Add 'corpora'? (y/n/f) > y
Add 'datacenters'? (y/n/f) > f
Adding 19 remaining words...
Finished adding 9 total cards. All done!
$
```

It uses dictionaryapi.dev to get definitions. There are also some flags you can use to control the script behavior,
```
parser.add_argument("-l", "--word-list", default="wordlists", help="Word list path or folder")
parser.add_argument("-c", "--cache", default="cache.txt", help="Cache path")
parser.add_argument("-f", "--force-confirm", action="store_true", help="Add all words without confirming")
parser.add_argument("-o", "--output", help="Output file path")
```

```
book-to-anki/
│
├── book-to-anki.py
├── wordlists/
│   ├── customList1.txt
│   ├── customList2.txt
│   ├── customList3.txt
│   └── customList4.txt
├── bookName.txt
├── cache.txt
└── bookNameAnkiCards.txt (produced by the script)
```

Once you have the output file, you can go to Anki and import the cards either as basic, or basic with reversed, or any other note type with two fields.