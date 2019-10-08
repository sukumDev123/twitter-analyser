import numpy as np
from sklearn.cluster import KMeans


# this method for use in controller
def handle_data_before_custer_and_custer(read_csv):
    get_data_ = np.array([(read_csv['followers_count'][ind],
                           read_csv['retweets'][ind])
                          for ind, data in enumerate(read_csv['text'])])
    model_cluster = KMeans(n_clusters=3)
    model_cluster.fit(get_data_)
    grop = [0, 1, 2]

    grop_detail = get_min_max_each_of_grop(grop, get_data_, model_cluster)
    show_user_grop = handle_top10_user_each_of_grop(
        model_cluster=model_cluster, grop=grop, read_csv=read_csv)
    return {"grop_detail": grop_detail, "show_user_grop": show_user_grop}


def handle_top10_user_each_of_grop(model_cluster, grop, read_csv):
    top10follower = {'grop1': [], 'grop2': [], 'grop3': []}
    for g in grop:
        tettt = []
        for ind, data in enumerate(model_cluster.labels_):
            if data == g:
                tettt.append((read_csv['screen_name'][ind],
                              read_csv['followers_count'][ind]))
                tettt.sort(key=lambda j: j[1], reverse=True)

        top10follower['grop{}'.format(g +
                                      1)] = [data[0] for data in tettt[:10]]
        tettt = []

    return top10follower


def get_min_max_each_of_grop(grop, get_data_, model_cluster):
    grop_detail = {
        'grop1': {
            'retweet': {
                "min": 0,
                "max": 0
            },
            'follower': {
                "min": 0,
                "max": 0
            }
        },
        'grop2': {
            'retweet': {
                "min": 0,
                "max": 0
            },
            'follower': {
                "min": 0,
                "max": 0
            }
        },
        'grop3': {
            'retweet': {
                "min": 0,
                "max": 0
            },
            'follower': {
                "min": 0,
                "max": 0
            }
        }
    }
    intToString = lambda intNumber: '{}'.format(intNumber)

    grop = [0, 1, 2]
    for g in grop:
        followerCuster = [
            get_data_[ind][0] for ind, data in enumerate(model_cluster.labels_)
            if data == g
        ]
        retweetCuster = [
            get_data_[ind][1] for ind, data in enumerate(model_cluster.labels_)
            if data == g
        ]
        if len(followerCuster) > 0 and len(retweetCuster) > 0:

            minNumberOfFollowers = min(followerCuster)
            maxNumberOfFollowers = max(followerCuster)
            minNumberOfRetweets = min(retweetCuster)
            maxNumberOfRetweets = max(retweetCuster)
            gropNumber = 'grop{}'.format(g + 1)

            grop_detail[gropNumber]['follower']['min'] = intToString(
                minNumberOfFollowers)

            grop_detail[gropNumber]['follower']['max'] = intToString(
                maxNumberOfFollowers)

            grop_detail[gropNumber]['retweet']['min'] = intToString(
                minNumberOfRetweets)

            grop_detail[gropNumber]['retweet']['max'] = intToString(
                maxNumberOfRetweets)

    return grop_detail
