from bs4 import BeautifulSoup
import requests
import argparse
import sys


class Error404(Exception):
    def __init__(self, text):
        self.txt = text


languages = {'All': '0',
             'Arabic': 'Arabic',
             'German': 'German',
             'English': 'English',
             'Spanish': 'Spanish',
             'French': 'French',
             'Hebrew': 'Hebrew',
             'Japanese': 'Japanese',
             'Dutch': 'Dutch',
             'Polish': 'Polish',
             'Portuguese': 'Portuguese',
             'Romanian': 'Romanian',
             'Russian': 'Russian',
             'Turkish': 'Turkish'}

parser = argparse.ArgumentParser(description='Type the number of your language:')
parser.add_argument('your_language', type=str)
parser.add_argument('translate_to', type=str)
parser.add_argument('word', type=str)
args = parser.parse_args()

try:
    your_language = languages[args.your_language.capitalize()]
except KeyError:
    print(f"Sorry, the program doesn't support {args.your_language}")
    sys.exit()

try:
    translate_to = languages[args.translate_to.capitalize()]
except KeyError:
    print(f"Sorry, the program doesn't support {args.translate_to}")
    sys.exit()

word = args.word

headers = {'User-Agent': 'Mozilla/5.0'}
word_file = open(f'{word}.txt', 'w', encoding="utf-8")
if translate_to == '0':
    for i in languages:
        if languages[i] == your_language or languages[i] == '0':
            continue
        else:
            translate_to = languages[i]
            try:
                req = requests.get(
                    f'https://context.reverso.net/translation/{your_language.lower()}-{translate_to.lower()}/{word}',
                    headers=headers)
            except requests.exceptions.ConnectionError:
                sys.exit('Something wrong with your internet connection')
            try:
                assert req.status_code == 200
            except AssertionError:
                print(f'Sorry, unable to find {word}')
                sys.exit()
            print()
            print(f'{translate_to} Translations:')
            print(f'{translate_to} Translations:', file=word_file)
            soup = BeautifulSoup(req.content, 'html.parser')
            translation_words = soup.find_all('a', class_='translation')
            translation_words = [i.text.strip() for i in translation_words]
            examples = soup.find('section', id='examples-content').find_all('span', class_='text')
            print(translation_words[1] + '\n')
            print(translation_words[1] + '\n', file=word_file)
            print(f'{translate_to} Example:')
            print(f'{translate_to} Example:', file=word_file)
            examples = [i.text.strip() for i in examples]
            examples = [(examples[i] + '\n' + examples[i + 1]) for i in range(0, len(examples), 2)]
            print(*examples[:1], '\n')
            print(*examples[:1], '\n\n', file=word_file)
else:
    try:
        req = requests.get(
            f'https://context.reverso.net/translation/{your_language.lower()}-{translate_to.lower()}/{word}',
            headers=headers)
    except requests.exceptions.ConnectionError:
        sys.exit('Something wrong with your internet connection')
    try:
        assert req.status_code == 200
    except AssertionError:
        print(f'Sorry, unable to find {word}')
        sys.exit()
    if req.status_code == 200:
        print()
        print(f'{translate_to} Translations:')
        print(f'{translate_to} Translations:', file=word_file)
        soup = BeautifulSoup(req.content, 'html.parser')
        translation_words = soup.find_all('a', class_='translation')
        translation_words = [i.text.strip() for i in translation_words]
        examples = soup.find('section', id='examples-content').find_all('span', class_='text')
        print(*translation_words[1:], sep='\n')
        print(*translation_words[1:], sep='\n', end='\n\n', file=word_file)
        print()
        print(f'{translate_to} Examples:')
        print(f'{translate_to} Examples:', file=word_file)
        examples = [i.text.strip() for i in examples]
        examples = [(examples[i] + '\n' + examples[i + 1]) for i in range(0, len(examples), 2)]
        print(*examples, sep='\n\n', end='')
        print(*examples, sep='\n\n', file=word_file)
    else:
        sys.exit(f'Sorry, unable to find {word}')
word_file.close()
