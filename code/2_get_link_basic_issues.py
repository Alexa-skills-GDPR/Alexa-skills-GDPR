import os
import csv
from tqdm import tqdm
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0

### get basic link problems

def get_skill_link_without_empty(countries):
    skills = {}
    for country in countries:
        with open('skills_' + country + '.csv') as f:
            reader = csv.reader(f)
            skills[country] = {}
            skill_nubmer = 0
            for row in reader:
                skill_nubmer = skill_nubmer + 1
                if row[9] == '':
                    continue
                skills[country][row[0]] = row[9]
            print(country, skill_nubmer, 'skills', len(skills[country]), 'skills with a privacy policy')
    return skills


# Detect broken links or get failed skills
def get_broken(skills):
    broken_words = ['404', '403', 'not exist', 'not found', 'not accssed', 'can\'t be reached', 'no longer available', 'server is down']
    for country in skills:
        broken1_page_not_found = []
        broken2_get_failed = []
        pdf_failed = []
        private_error = []
        for skill in skills[country]:
            try:
                content = open(country + '_txt_google_sentences/' + skill + '.txt').read().lower()
            except:
                broken2_get_failed.append(skill)
                continue
            if len(content) == 0:
                pdf_failed.append(skill)
                continue
            if any (word in content for word in broken_words):
                broken1_page_not_found.append(skill)
                continue
            if 'not private' in content:
                private_error.append(skill)
                continue
        print(country, len(broken1_page_not_found + broken2_get_failed), 'page not found')


# Get duplicate links in each country
def get_duplicate(skills):
    for country in skills:
        links = [skills[country][skill] for skill in skills[country] if skills[country][skill] != '']
        k = 0
        for skill in skills[country]:
            if links.count(skills[country][skill]) == 1:
                k = k + 1
        print(country, len(links), len(links) - k, 1 - k/len(links))



def get_privacy_policy_languages(countries):
    for country in countries:
        skills = os.listdir(country + '_txt/')
        languages = {}
        for skill in tqdm(skills):
            content = open(country + '_txt/' + skill).read()
            try:
                language = detect(content)
            except:
                continue
            if language in languages:
                languages[language] = languages[language] + 1
            else:
                languages[language] = 1
        sorted_languages = sorted(languages.items(), key=lambda kv: kv[1], reverse = True)
        print(country, len(skills), sorted_languages)


def get_privacy_policy_length(countries):
    for country in countries:
        skills = os.listdir(country + '_txt_google_sentences/')
        country_sentences = 0
        country_words = 0
        for skill in tqdm(skills):
            if '.txt' not in skill:
                continue
            sentences = open(country + '_txt_google_sentences/' + skill).read().split('\n')
            words = sum([len(line.split()) for line in sentences])
            country_sentences = country_sentences + len(sentences)
            country_words = country_words + words
        print(country, len(skills), country_sentences, country_words)


def main():

    countries = ['BR', 'FR', 'GE', 'IT', 'JA', 'ME', 'SP', 'UK', 'US']

    skills = get_skill_link_without_empty(countries)

    get_broken(skills)

    get_duplicate(skills)

    get_privacy_policy_languages(countries)

    get_privacy_policy_length(countries)



if __name__ == "__main__":
	main()