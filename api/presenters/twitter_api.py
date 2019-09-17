from pandas import DataFrame
import re
from tweepy import Cursor
from api.presenters.handle_data import hadle_data_to_csv


class TwitterAPI:
    def __init__(self, api):
        self.api = api

    def get_user_timeline_cursor(self, name_srceen):
        temp = []
        for tweets in Cursor(self.api.user_timeline,
                             screen_name=name_srceen,
                             count=200).pages(20):
            for t in tweets:
                temp.append(t._json)
        return temp

    def get_search_cursor(self, q):
        temp = []
        index_ = 0
        for tweets in Cursor(self.api.search, q=q, count=200).pages(70):
            for gg in tweets:
                print('--> ', index_)
                temp.append(gg._json)
                index_ += 1

        return hadle_data_to_csv(temp, q)
