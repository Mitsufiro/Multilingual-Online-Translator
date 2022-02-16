from bs4 import BeautifulSoup
import requests
import argparse

print("Hello, you're welcome to the translator. Translator supports:")
languages = {'all': 'all',
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
[print(key + '.', value, ) for key, value in languages.items() if languages[key] != '0']
your_language = languages[input('Type the number of your language:')]
# parser = argparse.ArgumentParser(description='Type the number of your language:')
# parser.add_argument('your_language')
translate_to = languages[
    input("Type the number of a language you want to translate to or '0' to translate to all languages:")]

word = input('Type the word you want to translate:')
headers = {'User-Agent': 'Mozilla/5.0'}
word_file = open(f'{word}.txt', 'w', encoding="utf-8")
if translate_to == 'all':
    for i in range(1, 14):
        i = str(i)
        if languages[i] == your_language:
            continue
        else:
            translate_to = languages[i]
            req = requests.get(
                f'https://context.reverso.net/translation/{your_language.lower()}-{translate_to.lower()}/{word}',
                headers=headers)
            if req.status_code == 200:
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
                print(req.status_code)
else:
    req = requests.get(f'https://context.reverso.net/translation/{your_language.lower()}-{translate_to.lower()}/{word}',
                       headers=headers)
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
        print(f'{translate_to} Example:')
        print(f'{translate_to} Example:', file=word_file)
        examples = [i.text.strip() for i in examples]
        examples = [(examples[i] + '\n' + examples[i + 1]) for i in range(0, len(examples), 2)]
        print(*examples, sep='\n', end='')
        print(*examples, sep='\n', file=word_file)
    else:
        print(req.status_code)
word_file.close()
