from json import load, dumps


def read_file_c(file):
    temp = []
    with open('{}.json'.format(file)) as json_file:
        data = load(json_file)
        temp = data['data']
    return temp


def write_file_json(file, datas):
    temp = {"data": []}
    for data in datas:
        temp['data'].append(data)
    with open("{}.json".format(file), 'w') as file_:
        file_.write(dumps(temp))
    print("write file name {} is success.".format(file))

