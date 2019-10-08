import json
from pythainlp.tokenize import word_tokenize as wt
import re
import pandas as pd

stop_words = [
    "นี้", "นํา", "นั้น", "นัก", "นอกจาก", "ทุก", "ที่สุด", "ที่", "ทําให้",
    "ทํา", "ทาง", "ทั้งนี้", "ดัง", "ซึ่ง", "ช่วง", "จาก", "จัด", "จะ", "คือ",
    "ความ", "ครั้ง", "คง", "ขึ้น", "ของ", "ขอ", "รับ", "ระหว่าง", "รวม", "ยัง",
    "มี", "มาก", "มา", "พร้อม", "พบ", "ผ่าน", "ผล", "บาง", "น่า", "เปิดเผย",
    "เปิด", "เนื่องจาก", "เดียวกัน", "เดียว", "เช่น", "เฉพาะ", "เข้า", "ถ้า",
    "ถูก", "ถึง", "ต้อง", "ต่างๆ", "ต่าง", "ต่อ", "ตาม", "ตั้งแต่", "ตั้ง",
    "ด้าน", "ด้วย", "อีก", "อาจ", "ออก", "อย่าง", "อะไร", "อยู่", "อยาก",
    "หาก", "หลาย", "หลังจาก", "แต่", "เอง", "เห็น", "เลย", "เริ่ม", "เรา",
    "เมื่อ", "เพื่อ", "เพราะ", "เป็นการ", "เป็น", "หลัง", "หรือ", "หนึ่ง",
    "ส่วน", "ส่ง", "สุด", "สําหรับ", "ว่า", "ลง", "ร่วม", "ราย", "ขณะ", "ก่อน",
    "ก็", "การ", "กับ", "กัน", "กว่า", "กล่าว", "จึง", "ไว้", "ไป", "ได้",
    "ให้", "ใน", "โดย", "แห่ง", "แล้ว", "และ", "แรก", "แบบ", "ๆ", "ไว้", "ไป",
    "ให้", "ใน", "โดย", "แห่ง", "แล้ว", "และ", "แรก", "แบบ", "แต่", "เอง",
    "เห็น", "เลย", "เริ่ม", "เรา", "เมื่อ", "เพื่อ", "เพราะ", "เป็น", "การ",
    "เป็น", "เปิด", "เผย", "เปิด", "เนื่อง", "จาก", "เดียว", "กัน", "เดียว",
    "เช่น", "เฉพาะ", "เคย", "เข้า", "เขา", "อีก", "อาf", "อะไร", "ออก",
    "อย่าง", "อยู่", "อยาก", "หาก", "หลาย", "หลัง", "จาก", "หลัง", "หรือ",
    "หนึ่ง", "ส่วน", "ส่ง", "สุด", "สําหรับ", "ว่า", "วัน", "ลง", "ร่วม",
    "ราย", "รับ", "ระหว่าง", "รวม", "ยัง", "มี", "มาก", "มา", "พร้อม", "พบ",
    "ผ่าน", "ผล", "บาง", "น่า", "นี้", "นํา", "นั้น", "นัก", "นอกจาก",
    "ทุกที่", "สุดที่", "ทําให้", "ทํา", "ทาง", "ทั้งนี้", "ถ้า", "ถูก", "ถึง",
    "ต้อง", "ต่างๆ", "ต่าง", "ต่อ", "ตาม", "ตั้งแต่", "ตั้ง", "ด้าน", "ด้วย",
    "ดัง", "ซึ่ง", "ช่วง", "จึง", "จาก", "จัด", "จะ", "คือ", "ความ", "ครั้ง",
    "คง", "ขึ้น", "ของ", "ขอ", "ขณะ", "ก่อน", "ก็", "การ", "กับกัน", "กว่า",
    "กล่าว", "นะ", "ค่ะ", "คะ", "ขา", "ครับ", "หน่อย", ' ', '...', '  ', '__',
    '   ', 'RT', ":", "http", "https", "://", ".", "co", '...', '', '/', '\n',
    '@', "#", "t"
]


# Merge text for handle array are text to merge text to string.
def merge_text(text_array):
    temp = ""
    for data in text_array:
        temp += data + ' '
    return temp


#Cut word with re and word_tokenize
def handle_wt(txt):
    regx = r'https://t.co/\w+|RT\s@\w*\d*:|\n|\s|#|_|\u200b|[=]+\s[ก-๙]+\s[=]+|\n'  #regrx for handle url to split it.
    txt_ = merge_text(re.split(regx, txt))
    txt__ = merge_text(re.findall(r'[ก-๙]+', txt_, re.MULTILINE))
    text_raw = wt(txt__, engine='newmm')
    datas = list(filter(lambda x: x not in stop_words, text_raw))
    return datas


#Clean text
def clean_text(text):
    text = handle_wt(text)  # cut text to array
    texts = ' '.join(word.strip() for word in text
                     if len(word) > 2)  # delete stopwors from text
    return texts


def hadle_data_to_csv(datas, q):
    tempp = {
        "id": [],
        "text": [],
        "name": [],
        'created_at': [],
        'likes': [],
        'retweets': [],
        'screen_name': [],
        'location': [],
        'followers_count': [],
        "friends_count": [],
        'retweeted': []
    }
    for jj in range(len(datas)):
        retweet_count = datas[jj]['retweet_count']
        tempp['retweets'].append(retweet_count)
        tempp['likes'].append(datas[jj]['favorite_count'])
        tempp['followers_count'].append(datas[jj]['user']['followers_count'])
        tempp['friends_count'].append(datas[jj]['user']['friends_count'])
        tempp['text'].append((datas[jj]['text']))
        tempp['id'].append(datas[jj]['id'])
        tempp['retweeted'].append(datas[jj]['retweeted'])
        tempp['created_at'].append(datas[jj]['created_at'])
        tempp['screen_name'].append(datas[jj]['user']['screen_name'])
        tempp['name'].append(datas[jj]['user']['name'])
        tempp['location'].append(datas[jj]['user']['location'])
    pdDataFrame = pd.DataFrame(tempp)
    pdDataFrame.to_csv('csv_files/{}.csv'.format(q))
    return pdDataFrame