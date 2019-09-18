from django.test import TestCase
from api.presenters.preprocess import cutOnlyHashTag, handleFindIdfTextOfHashtag
from api.presenters.classifier import predictWord
import pandas as pd


# Create your tests here.
class TestApi(TestCase):
    pass
    # self.assertEqual(onlyText, 1)

    # def test_cut_hashtag_file(self):
    #     fileName = "#SaveUbon2019.csv"
    #     hash = handleFindIdfTextOfHashtag(fileName)
    #     self.assertEqual(hash, 1)

    # def test_cut_hashtag(self):
    #     word = '#123 asdasd #acs adasdasd #การรัก adsd'
    #     self.assertEqual(cutOnlyHashTag(word), ["#123", "#acs", "#การรัก"],
    #                      "adasd")
