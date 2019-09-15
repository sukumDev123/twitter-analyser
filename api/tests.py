from django.test import TestCase
from api.presenters.preprocess import cutOnlyHashTag, handleFindIdfTextOfHashtag


# Create your tests here.
class TestApi(TestCase):
    def test_cut_hashtag_file(self):
        fileName = "#SaveUbon2019.csv"
        hash = handleFindIdfTextOfHashtag(fileName)
        self.assertEqual(hash, 1)

    def test_cut_hashtag(self):
        word = '#123 asdasd #acs adasdasd #การรัก adsd'
        self.assertEqual(cutOnlyHashTag(word), ["#123", "#acs", "#การรัก"],
                         "adasd")
