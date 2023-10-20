import os
import csv
import json
from sklearn import metrics


def get_skills_gt(skill):
    label = []
    predict = []
    with open('gt/' + skill) as f:
        reader = csv.reader(f)
        for row in reader:
            predict.append(int(row[2]))
            if ',' in row[1]:
                label.append(int(row[1].split(',')[0]))
            elif row[1] == '':
                label.append(0)
            else:
                label.append(int(row[1]))
    return label, predict


def read_results(countries):
    skill_results = {}
    for country in countries:
        results = open('results/' + country + '.txt').read().split('\n')[:-1]
        skill_result = {}
        for result in results:
            skill_result[result.split('\t')[0]] = json.loads(result.split('\t')[1])
        skill_results[country] = skill_result
    return skill_results


# Evaluate US sentences with ground-truth. 
# These results were labeled by sentence instead of comparing similarity of sentences, so it is higher than next file.
def get_US_sentences_performance(labeled_skills):
    overall_label = []
    overall_predict = []
    for skill in labeled_skills:
        if skill.endswith('.csv') == False:
            continue
        label, predict = get_skills_gt(skill)
        overall_label = overall_label + label
        overall_predict = overall_predict + predict
    #    print(skill, metrics.f1_score(label, predict, average = 'weighted'))
    #    print('weighted F1', skill, metrics.f1_score(label, predict, average = 'weighted'))
    #    print('micro F1', skill, metrics.f1_score(label, predict, average = 'micro'))
    #    print('macro F1', skill, metrics.f1_score(label, predict, average = 'macro'))
    #    print()
    print('Overall sentence performance: ')
    print('weighted F1', metrics.f1_score(overall_label, overall_predict, average = 'weighted'))    #0.8657818804037475
    print('micro F1', metrics.f1_score(overall_label, overall_predict, average = 'micro'))
    print('macro F1', metrics.f1_score(overall_label, overall_predict, average = 'macro'))


# Get which gdpr types are missed
def get_type_violation(labels):
    violations = []
    if labels[0] != 0:
        for i in range(1,10):
            if labels[i] == 0:
                violations.append(i)
    return violations


# For gdpr types, we need a higher recall (higher precision for violation).
def evaluate(gt, predict):
    tp = 0
    fp = 0
    for i in predict:
        if i in gt:
            tp = tp + 1
        else:
            fp = fp + 1
    return tp, fp


# Evaluate from gdpr types perspective instead of sentences
# [0,0,1,1,2,3,4] => [0,1,2,3,4] 
def get_country_gdpr_types_performance(countries, labeled_skills):
    skill_results = read_results(countries)
    print('Overall gdpr types performance of: ')
    for country in countries:
        overall_tp = 0
        overall_fp = 0
        for skill in labeled_skills:
            # remove .ipynb_checkpoints
            if skill.startswith('B') == False:
                continue
            data, _ = get_skills_gt(skill)
            gt_labels = []
            for i in range(0,10):
                gt_labels.append(data.count(i + 1))
            violations_gt = get_type_violation(gt_labels)
            predict_labels = skill_results[country][skill[:-4]]
            violations_predict = get_type_violation(predict_labels)
            tp, fp = evaluate(violations_gt, violations_predict)
            overall_tp = overall_tp + tp
            overall_fp = overall_fp + fp
        print(country + ': ' + str(overall_tp/(overall_tp + overall_fp)))


def main():

    labeled_skills = os.listdir('gt')
    labeled_skills.sort()

    get_US_sentences_performance(labeled_skills)

    countries = ['US', 'GE', 'SP', 'IT', 'FR', 'ME', 'BR']

    get_country_gdpr_types_performance(countries, labeled_skills)


if __name__ == "__main__":
    main()


