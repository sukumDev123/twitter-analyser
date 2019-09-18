import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from collections import Counter
from pythainlp.tokenize import word_tokenize as wt
import dill
from api.presenters.handle_data import clean_text


def readFileDill(name_files):
    file_dill = ''
    with open('{}.data'.format(name_files), 'rb') as fs:
        file_dill = dill.load(fs)
    return file_dill


def pipeTextDocumentToVec():
    readWordFile = readFileDill('models/words')
    pipeLine = Pipeline([
        ('vect', CountVectorizer(analyzer=lambda word: wt(word))),
        ('tfidf', TfidfTransformer()),
    ])
    pipeLine.fit_transform(readWordFile)
    return pipeLine


# def chechTextToVec(pipe_line, datas):
#     return pipe_line.transform(datas)


# method export
def predictWord(datas):
    if len(datas) > 0:
        readClassifyModel = readFileDill('models/classify')
        pipeTextToVec = pipeTextDocumentToVec()
        pipeTextHandle = pipeTextToVec.transform(
            [clean_text(data) for data in datas])
        predictResult = readClassifyModel.predict(pipeTextHandle)
        return list(predictResult)
    return []