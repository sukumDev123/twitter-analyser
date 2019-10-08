from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from api.presenters.twitter_api import TwitterAPI
from api.presenters.twitter_auth import auth_session
from background_task import background
from api.firebase.firebase_db import write_filesName
from api.presenters.preprocess import handleFindIdfTextOfHashtag, findUserIsRetweeted
from api.presenters.classifier import predictWord
# from celery
from api.presenters.clustering import handle_data_before_custer_and_custer
datas = []


def responseData(data):
    res = HttpResponse(data)
    res['content'] = data
    res['content_type'] = 'application/json; charset=utf-8'
    res['Access-Control-Allow-Origin'] = '*'
    res['Access-Control-Allow-Headers'] = "*"
    return res


@background(schedule=1)
def handleWriteFileInTwitter(hashTagSearch):
    auth = auth_session()
    api = TwitterAPI(auth)
    data = api.get_search_cursor(hashTagSearch)
    write_filesName('{}.csv'.format(hashTagSearch))
    print("done", hashTagSearch)


# search data from hashtag is post method
@csrf_exempt
def searchHashtagAndWriteFileCsv(req, *args, **kwargs):
    loadReqVal = json.loads(req.body)
    message = handleWriteFileInTwitter(loadReqVal['body'])

    return responseData("Waiting for write file.")


def getHashTagFile():
    pass


def handle_textType(predResult, tweet):
    data_1 = [
        tweet[ind] for ind, data in enumerate(predResult)
        if '{}'.format(data) == "1"
    ]
    data_1Neg = [
        tweet[ind] for ind, data in enumerate(predResult)
        if '{}'.format(data) == "-1"
    ]
    data_0 = [
        tweet[ind] for ind, data in enumerate(predResult)
        if '{}'.format(data) == "0"
    ]
    return {"good": data_1[:10], "neg": data_1Neg[:10], "neutral": data_0[:10]}


@csrf_exempt
def handleDataCsv(req, *args, **kwargs):
    datas = req.body

    zip_datas = {
        "features": [],
        "idf": [],
        "userTopRetweet": [],
        "word_predict": [],
        "text_sentiments": {
            "good": [],
            "neg": [],
            "neutral": []
        },
        "clustering_grop": {
            "grop_detail": [],
            "show_user_grop": []
        }
    }
    if (datas):
        toJson = json.loads(datas)
        methodd = handleFindIdfTextOfHashtag(toJson['name_file'])
        zip_datas['features'] = methodd['tempp']['features']
        zip_datas['idf'] = methodd['tempp']['idf']
        zip_datas["userTopRetweet"] = findUserIsRetweeted(methodd['tweet'])
        pred_fun = predictWord(methodd['tweet'], toJson['name_file'])
        zip_datas['word_predict'] = pred_fun
        twt = handle_textType(pred_fun, methodd['tweet'])
        zip_datas['text_sentiments'] = twt
        zip_datas['clustering_grop'] = handle_data_before_custer_and_custer(
            methodd['alldata'])
    return responseData(json.dumps(zip_datas))