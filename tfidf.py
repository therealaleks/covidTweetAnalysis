import sys
import math
import pandas as pd
import json
import re
import string
from urllib import request

def check_chars(word):
    for letter in word:
        val = ord(letter)
        if ((not (65 <= val <= 90)) and (not (97 <= val <= 122)) and (not (48 <= val <= 57))):
            return False
    return True

def cleanTweet(review):
    splitted = review.split(" ")
    li = []
    for i, word in enumerate(splitted):
        if (len(word) != 0):
            if ((not "https://" in word) and (word[0] != '#') and (word[0] != '@')):
                li.append(word.lower())
    new_review = ' '.join(li)
    table = str.maketrans('','',string.punctuation)
    review = new_review.translate(table)
    review = review.split(" ")
    li2 = []
    for w in review:
        if (check_chars(w) and (not w.isdigit())):
            li2.append(w)
    return li2


def getCounts(input, cutoff):
    # get data
    data = pd.read_csv(input)

    stopwords = request.urlopen(
        'https://gist.githubusercontent.com/larsyencken/1440509/raw/53273c6c202b35ef00194d06751d8ef630e53df2/stopwords.txt')
    stopwords = stopwords.read().decode(stopwords.headers.get_content_charset())
    stopwords = set([str for str in stopwords.splitlines() if not str[0].strip() == '#'])

    # prepare output
    out = {
        "t": {},
        "v": {},
        "p": {},
        "m": {},
        "o": {},
        "a": {},
        "r": {},
        "s": {}
    }

    topics = set([key for key, val in out.items()])

    # function to analyze a row of data
    def logRow(row):
        if row['topic'].lower() in topics:
            # clean = re.sub(r"[()[\],-.?!:;#&]+\ *", " ", row['text'])
            clean = cleanTweet(row['text'])

            text = [str.lower() for str in clean if
                      not str == '' and not str in stopwords]

            for word in text:
                if not word in out[row['topic'].lower()]:
                    out[row['topic'].lower()][word] = 0
                out[row['topic'].lower()][word] += 1

    # apply function above to every row of data
    data.apply(lambda row: logRow(row), axis=1)

    for topic, counts in out.copy().items():
        for word, count in counts.copy().items():
            total = 0
            for top, cs in out.copy().items():
                if word in cs:
                    total += cs[word]
            if total < cutoff:
                del out[topic][word]
    return out

def compute_tf_idf(tcounts):
    n_topics = len(tcounts.items())
    tfidf = {}
    for topic, counts in tcounts.items():
        tfidf[topic] = {}
        for word, count in counts.items():
            nt_w = len([topic for topic, counts in tcounts.items() if word in counts])
            tfidf[topic][word] = math.log(n_topics / nt_w) * count

    return tfidf

def compute_top_k(counts, k):

    tfidf = compute_tf_idf(counts)

    out = {}

    for topic, ts in tfidf.items():
        s = sorted(ts.items(), key=lambda x: x[1], reverse=True)
        out[topic] = [k for k, v in s][:min(len(s), int(k))]

    return out

if __name__ == '__main__':

    counts = getCounts('tweets.csv', 5)
    lang = compute_top_k(counts, 10)
    print(json.dumps(lang, indent=2))