from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from api.presenters.twitter_api import TwitterAPI
from api.presenters.twitter_auth import auth_session
from background_task import background


def responseData(data):
    res = HttpResponse(data)
    res['content'] = data
    res['content_type'] = 'application/json; charset=utf-8'
    res['Access-Control-Allow-Origin'] = '*'
    return res


@background(schedule=5)
def handleWriteFileInTwitter(hashTagSearch):
    auth = auth_session()
    api = TwitterAPI(auth)
    data = api.get_search_cursor(hashTagSearch)
    print(data)
    return data


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
    pass