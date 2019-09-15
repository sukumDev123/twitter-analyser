import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from collections import Counter

cutOnlyHashTag = lambda txt: re.findall(r"#[ก-๙a-zA-Z0-9]+", txt)

joinHashtag = lambda hashArray: ' '.join(word.strip() for word in hashArray
                                         if len(word) > 2)
handleCut = lambda text: re.split(" ", text)


def handleFindIdfTextOfHashtag(name_file):
    read_csv = pd.read_csv('csv_files/{}'.format(name_file))
    cut_only_hashtag = [cutOnlyHashTag(txt) for txt in read_csv['text']]
    cut_only_hashtag_filter_data_isNotE = [
        hashtTag for hashtTag in cut_only_hashtag if len(hashtTag) > 0
    ]
    join_hash = [
        joinHashtag(hashT) for hashT in cut_only_hashtag_filter_data_isNotE
    ]

    pipeLine = Pipeline([
        ('vect', CountVectorizer(analyzer=lambda word: handleCut(word))),
        ('tfidf', TfidfTransformer()),
    ])

    pipeLine.fit_transform(join_hash)
    datas = {
        "features": pipeLine['vect'].get_feature_names(),
        "idf": pipeLine['tfidf'].idf_
    }
    ff = pd.DataFrame(datas).sort_values(by=["idf"])
    tempp = {
        "features": list(ff.head(10)['features']),
        "idf": list(ff.head(10)["idf"])
    }
    tempp_zip = {"tweet": read_csv['text'], "tempp": tempp}
    return tempp_zip


def findUserIsRetweeted(tweet):
    rt_user = lambda txt: re.findall(r'RT @[a-zA-Z0-9ก-๙]+', txt)
    inf = [rt_user(txt) for txt in tweet]
    inf_not_ = [re.split(' ', txt[0])[1] for txt in inf if len(txt) > 0]
    counter_ = Counter(inf_not_).most_common(10)
    userName = [data[0] for data in counter_]
    retweet_count = [data[1] for data in counter_]
    return {"userName": userName, 'retweet_count': retweet_count}
