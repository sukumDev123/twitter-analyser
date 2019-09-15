from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from api.presenters.twitter_api import TwitterAPI
from api.presenters.twitter_auth import auth_session
from background_task import background
from api.firebase.firebase_db import write_filesName
from api.presenters.preprocess import handleFindIdfTextOfHashtag, findUserIsRetweeted


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
    print("done")
    return True


# search data from hashtag is post method
@csrf_exempt
def searchHashtagAndWriteFileCsv(req, *args, **kwargs):
    loadReqVal = json.loads(req.body)
    handleWriteFileInTwitter(loadReqVal['body'])
    return responseData("file is writing...")


def getHashTagFile():
    pass


@csrf_exempt
def handleDataCsv(req, *args, **kwargs):
    datas = req.body

    zip_datas = {"features": [], "idf": [], "userTopRetweet": []}
    if (datas):
        toJson = json.loads(datas)
        methodd = handleFindIdfTextOfHashtag(toJson['name_file'])
        zip_datas['features'] = methodd['tempp']['features']
        zip_datas['idf'] = methodd['tempp']['idf']
        zip_datas["userTopRetweet"] = findUserIsRetweeted(methodd['tweet'])
        # tempOfUserRetweeted =
    return responseData(json.dumps(zip_datas))