import os
import csv
import time
import spacy
import trafilatura
from tqdm import tqdm
from selenium import webdriver
from googletrans import Translator
from webdriver_manager.chrome import ChromeDriverManager

translator = Translator()
nlp = spacy.load("en_core_web_sm")


# Read skill privacy policy links of all countries
def get_country_skills(countries):
    skills = {}
    for country in countries:
        with open('skills_' + country + '.csv') as f:
            reader = csv.reader(f)
            skills[country] = {}
            for row in reader:
                skills[country][row[0]] = row[9]
    return skills


# Use chrome webdriver to download html and pdf files
# Get privacy policy pages with webdriver can enable the javascript
def scrapy_data(country, skills, done):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    for skill in tqdm(skills):
        if skill + '.html' in done or skill + '.pdf' in done:
            continue
        if skills[skill] == '':
            continue
        if skills[skill].endswith('.pdf'):
            x = os.system('curl -L "' + skills[skill] + '" >' + country + '/' + skill + '.pdf')
        try:
            driver.set_page_load_timeout(10)
            try:
                driver.get(skills[skill])
                time.sleep(5)
                content = driver.page_source#.encode('utf-8')
                with open(country + '/' + skill + '.html', 'w') as f:
                    x = f.write(content)
            except:
                continue
        except:
            continue
    driver.close()


# Download privacy policy of all countries
def download_with_webdriver(skills):
    x = os.system('mkdir US')
    for country in skills:
        # Don't download all US skills but only skills exist in other countries
        if country == 'US':
            continue
        print(country)
        x = os.system('mkdir ' + country)
        done = os.listdir(country)
        # Download all skills in other countries
        scrapy_data(country, skills[country], done)
        # Since almost all skills in US and UK are same, so don't collect US/UK overlap
        if country == 'UK':
            continue
        # For each country, download skills existing in US
        overlap_skills = {}
        for skill in skills[country]:
            if skill in skills['US']:
                overlap_skills[skill] = skills['US'][skill]
        done = os.listdir('US/')
        scrapy_data('US', overlap_skills, done)


# Policylint will keep head content and this library only keeps the main content
def html_to_txt(countries):
    for country in countries:
        print(country + ' html to txt')
        x = os.system('mkdir ' + country + '_txt')
        skills = os.listdir(country)
        done = os.listdir(country + '_txt/')
        for skill in tqdm(skills):
            if skill[:10] + '.txt' in done:
                continue
            time.sleep(0.01)
            if skill.endswith('.pdf'):
                x = os.system('pdftotext ' + country + '/' + skill + ' ' + country + '_txt/' + skill[:-4] + '.txt > /dev/null 2>&1')
            else:
                downloaded = trafilatura.load_html(open(country + '/' + skill).read())
                content = trafilatura.extract(downloaded)
                if content == None:
                    continue
                with open(country + '_txt/' + skill[:-5] + '.txt', 'w') as f:
                    x = f.write(content)


# translate each skill: other languages into english
def translate_content(language, country_content):
    country_content_translated = ''
    content_to_translate = []
    sentence_to_translate = ''
    # If privacy policy is too long, split it into several parts
    for sentence in country_content:
        sentence_to_translate = sentence_to_translate + '\n' + sentence
        # The length limitation for Google is 5000
        if len(sentence_to_translate) > 5000:
            content_to_translate.append(sentence_to_translate)
            sentence_to_translate = ''
    content_to_translate.append(sentence_to_translate)
    for sentence_to_translate in content_to_translate:
        try:
            # Use the Google translation API for translation
            country_content_translated = country_content_translated + '\n' + translator.translate(sentence_to_translate, src = language).text.lower()
        except:
            country_content_translated = country_content_translated + ''
    return country_content_translated


# Translate all countries: other languages into english
def translate_with_google(countries, translation_type):
    languages = {'US': 'en', 'UK': 'en', 'GE': 'de', 'SP': 'es', 'IT': 'it', 'FR': 'fr', 'JA': 'ja', 'ME': 'es', 'BR': 'pt'}
    for country in countries:
        print(country + ' to english')
        # For US and UK, don't translate them but only copy to folder with same format name
        if country == 'US' or country == 'UK':
            try:
                x = os.system('cp -r ' + country + '_txt ' + ' ' + country + '_txt_' + translation_type)
            except:
                x = 0
            continue
        x = os.system('mkdir ' + country + '_txt_' + translation_type)
        skills = os.listdir(country + '_txt/')
        done = os.listdir(country + '_txt_' + translation_type)
        # Read and translate each skill that haven't been translated
        for skill in tqdm(skills):
            if skill in done:
                continue
            language = languages[country]
            country_content = open(country + '_txt/' + skill).read().split('\n')
            country_content_translated = translate_content(language, country_content)
            with open(country + '_txt_' +  + translation_type + '/' + skill, 'w') as f:
                    x = f.write(country_content_translated + '\n')


# Use nlp to split paragraphes into sentences
def txt_to_sentences(countries, translation_type):
    for country in countries:
        x = os.system('mkdir ' + country + '_txt_' + translation_type + '_sentences')
        print(country + ' txt to sentences')
        skills = os.listdir(country + '_txt_' + translation_type)
        done = os.listdir(country + '_txt_' + translation_type + '_sentences/')
        for skill in tqdm(skills):
            if skill in done:
                continue
            time.sleep(0.05)
            with open(country + '_txt_' + translation_type + '/' + skill) as f:
                content = f.read()
            with open(country + '_txt_' + translation_type + '_sentences/' + skill, 'w') as f:
                try:
                    # If text isn't too long, process it once
                    doc = nlp(content)
                    for sent in doc.sents:
                        x = f.write(sent.text + '\n')
                except:
                    # If text is too long, read each line and process it
                    for line in content.split('\n'):
                        doc = nlp(line)
                        for sent in doc.sents:
                            x = f.write(sent.text + '\n')


# Remove empty lines or lines with only symbols
def remove_blank(countries, translation_type):
    for country in countries:
        print(country + ' remove blank')
        skills = os.listdir(country + '_txt_' + translation_type + '_sentences/')
        for skill in tqdm(skills):
            with open(country + '_txt_' + translation_type + '_sentences/' + skill) as f:
                content = f.read().split('\n')
            new_content = []
            for line in content:
                # If length of line is less than 5, it is not possible to contain a data practice
                if len(line) < 5:
                    continue
                new_content.append(line)
            # Write sentences into files
            with open(country + '_txt_' + translation_type + '_sentences/' + skill, 'w') as f:
                for line in new_content:
                    x = f.write(line + '\n')


def main():

    countries = ['BR', 'FR', 'GE', 'IT', 'JA', 'ME', 'SP', 'UK', 'US']

    skills = get_country_skills(countries)

    download_with_webdriver(skills)      # First scrapy US skills that exist in other countries

    download_with_webdriver(skills)      # Do it twice because some pages download failed

    html_to_txt(countries)

    translation_type = 'google'         # Translation type will influence later folder name

    translate_with_google(countries, translation_type)

    txt_to_sentences(countries, translation_type)

    remove_blank(countries, translation_type)


if __name__ == "__main__":
    main()

