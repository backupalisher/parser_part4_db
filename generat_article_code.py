import re
import pandas


def generate_article_partcode():
    art = 'P400000000'

    try:
        article = pandas.read_csv('article_code.csv', sep=';', header=None)
        article = article.values.tolist()
        article_code_index = int(article[0][0].replace('P4', ''))
        article_code_index = article_code_index + 1
    except:
        article_code_index = 1

    article_code_index = generate_article_code(article_code_index, art)

    df = pandas.DataFrame([article_code_index])
    df.to_csv('article_code.csv', index=False, mode='w', header=False, sep=";")

    return article_code_index


def generate_article_code(n, art):
    s = 0
    if n <= 9:
        s = re.sub(rf'\d$', str(n), art)
    elif (n >= 10) and (n <= 99):
        s = re.sub(rf'\d.$', str(n), art)
    elif (n >= 100) and (n <= 999):
        s = re.sub(rf'\d..$', str(n), art)
    elif (n >= 1000) and (n <= 9999):
        s = re.sub(rf'\d...$', str(n), art)
    elif (n >= 10000) and (n <= 99999):
        s = re.sub(rf'\d....$', str(n), art)
    elif (n >= 100000) and (n < 999999):
        s = re.sub(rf'\d.....$', str(n), art)
    elif n >= 1000000:
        s = re.sub(rf'\d......$', str(n), art)
    return s
