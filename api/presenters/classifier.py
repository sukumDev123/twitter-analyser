import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from collections import Counter
from pythainlp.tokenize import word_tokenize as wt
import dill
from api.presenters.handle_data import clean_text
import os


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
def predictWord(datas, name_files):
    if len(datas) > 0:
        checkIfPredicted = name_files in os.listdir('predict_results/')
        if checkIfPredicted != True:
            readClassifyModel = readFileDill('models/classify')
            pipeTextToVec = pipeTextDocumentToVec()
            pipeTextHandle = pipeTextToVec.transform(datas)
            predictResult = readClassifyModel.predict(pipeTextHandle)
            save_file_to_predicted = pd.DataFrame(predictResult)
            save_file_to_predicted.to_csv(
                'predict_results/{}'.format(name_files))
            return list(predictResult)
        else:
            csvFile = pd.read_csv('predict_results/{}'.format(name_files))
            return list(csvFile['0'])
    return []