import os
import csv
import spacy
from tqdm import tqdm
from sklearn import metrics

nlp = spacy.load("en_core_web_sm")


def get_country_skills_without_empty(countries):
    skills = {}
    for country in countries:
        with open('skills_' + country + '.csv') as f:
            reader = csv.reader(f)
            skills[country] = {}
            for row in reader:
                if row[9] == '':
                    continue
                skills[country][row[0]] = row[9]
    return skills


def get_similarity(line1, line2, US_content, country_content):
    similarity = 0
    if line1 == 0:
        similarity = similarity + US_content[line1].similarity(country_content[line2])
        similarity = similarity + US_content[line1].similarity(country_content[line2])
        similarity = similarity + US_content[line1 + 1].similarity(country_content[line2 + 1])
    elif line1 == len(US_content) - 1:
        similarity = similarity + US_content[line1].similarity(country_content[line2])
        similarity = similarity + US_content[line1].similarity(country_content[line2])
        similarity = similarity + US_content[line1 - 1].similarity(country_content[line2 - 1])
    else:
        similarity = similarity + US_content[line1 - 1].similarity(country_content[line2 - 1])
        similarity = similarity + US_content[line1].similarity(country_content[line2])
        similarity = similarity + US_content[line1 + 1].similarity(country_content[line2 + 1])
    return similarity


# try to put three sentence together and calculate similarity?
# short sentence with different translation may cause huge difference, like contact details and contact information
def get_similar_sentence(US_content, country_content):
    threshold = 2.5
    predict = {}
    for line1 in range(0, len(US_content)):
        for number in range(0, len(US_content)):
            try:
                line2 = line1 - number
                similarity = get_similarity(line1, line2, US_content, country_content)
                if similarity > threshold:
                    #predict[line1 -1] = line2 - 1
                    predict[line1] = line2
                    #predict[line1 + 1] = line2 + 1
                    break
                line2 = line1 + number
                similarity = get_similarity(line1, line2, US_content, country_content)
                if similarity > threshold:
                    #predict[line1 -1] = line2 - 1
                    predict[line1] = line2
                    #predict[line1 + 1] = line2 + 1
                    break
            except:
                continue
    return predict


def get_sentence_between_similar_sentence(predict):
    predict2 = {}
    keys = list(predict.keys())
    for number in range(0, len(keys) - 1):
        this_line = keys[number]
        next_line = keys[number + 1]
        if next_line - this_line == predict[next_line] - predict[this_line]:
            for line in range(1, next_line - this_line):
                predict2[this_line + line] = predict[this_line] + line
    return predict2


def align_sentence(US_content, country_content):
    # find simiar sentence, requires three sentences all similar (similarity((a1,b1,c1),(a2,b2,c2)) > 2.5)
    predict = get_similar_sentence(US_content, country_content)
    # find sentences between two same sentences with same length (if 4 => 10, 8 => 14, then 5,6,7 are aligned)
    predict2 = get_sentence_between_similar_sentence(predict) 
    # put them together
    for i in predict2:
        predict[i] = predict2[i]
    return predict


def get_skills_with_all_languages(skills):
    skills_in_all_countries = []
    skills_in_all_countries = set(skills['US'])
    for country in skills:
        skills_in_all_countries = skills_in_all_countries & set(skills[country])
    skills_with_all_languages = []
    for skill_id in skills_in_all_countries:
        links = []
        for country in skills:
            links.append(skills[country][skill_id])
        if len(set(links)) > 5:                         # 6 languages: en, fr, ge, it, es, pt
            skills_with_all_languages.append(skill_id)
    return skills_with_all_languages


def get_skills_gt(skill):
    content = []
    label = []
    with open('gt/' + skill + '.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            content.append(nlp(row[3].lower()))
            if ',' in row[1]:
                label.append(int(row[1].split(',')[0]))
            elif row[1] == '':
                label.append(0)
            else:
                label.append(int(row[1]))
    return content, label


def extract_from_skill_policy(country, skill):
    # Here we use Google translation. Later will use ChatGPT
    translation_type = '_txt_google_sentences_results/'
    try:
        data = open(country + translation_type + '/' + skill + '.txt').read()
    except:
        return 0, 0
    country_content = []
    country_label = []
    for line in data.split('\n')[:-1]:
        content, label = line.split('\t')
        country_content.append(nlp(content.lower()))
        country_label.append(int(label))    
    return country_content, country_label


def align_country_evaluate(country, labeled_skills):
    value = 0
    number = 0
    for skill in tqdm(labeled_skills):
        # remove .ipynb_checkpoints
        if skill.startswith('B') == False:
            continue
        skill = skill[:-4]
        US_content, US_label = get_skills_gt(skill)
        country_content, country_label = extract_from_skill_policy(country, skill)
        if country_content == 0 or country_label == 0:
            continue
        if [i.text for i in US_content] == [i.text for i in country_content]:
            print('different link but same content')
        else:
            predict = align_sentence(US_content, country_content)
        if predict == {}:
            continue
        US_label_paired = []
        country_label_paired = []
        for i in predict:
            US_label_paired.append(US_label[i])
            country_label_paired.append(country_label[predict[i]])
        result = metrics.f1_score(US_label_paired,country_label_paired,average = 'weighted')
        value = value + result
        number = number + 1
    # Print the performance of each country
    print(country, value, number) 


def main():

    countries = ['US', 'GE', 'SP', 'IT', 'FR', 'UK', 'US']

    labeled_skills = os.listdir('gt')
    labeled_skills.sort()

    for country in countries:
        align_country_evaluate(country, labeled_skills)


if __name__ == "__main__":
    main()



