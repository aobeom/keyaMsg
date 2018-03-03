# -*- coding: utf-8 -*-
import argparse
import json
import os
import sqlite3
import time


class keyaTalk(object):
    def __init__(self):
        pass

    # 格式化unix时间戳 / unix timestamp -> datetime
    def __unix2time(self, unixtime):
        unixtime = unixtime / 1000
        t_format = '%Y-%m-%d %H:%M:%S'
        t_unix = time.localtime(unixtime)
        dt = time.strftime(t_format, t_unix)
        return dt

    # 获取媒体文件路径 / get the media path
    def keyaMedia(self, mediapath):
        if os.path.exists(mediapath):
            media = os.listdir(mediapath)
            keya_media = []
            for m in media:
                info_dict = {}
                dt_name = os.path.splitext(m)[0]
                dt_str = time.mktime(time.strptime(dt_name, "%Y%m%d%H%M%S"))
                info_dict["time"] = self.__unix2time(int(dt_str) * 1000)
                info_dict["media"] = os.path.join(mediapath, m)
                keya_media.append(info_dict)
            return keya_media
        else:
            print("No media folder")
            exit()

    # 从sqlite.db提取内容 / get all messages
    def keyaText(self, dbpath):
        if os.path.exists(dbpath):
            connect = sqlite3.connect(dbpath)
            cursor = connect.cursor()
            talkinfo = cursor.execute("select * from TalkInfo")
            keya_text = []
            for info in talkinfo:
                info_dict = {}
                info_dict["utime"] = info[6]
                info_dict["time"] = self.__unix2time(info[6])
                info_dict["text"] = info[14]
                info_dict["mediaType"] = info[9]
                keya_text.append(info_dict)
            keya_text.sort(key=lambda x: x["utime"])
            return keya_text
        else:
            print("No database")
            exit()

    # 根据时间将正文和媒体内容合并 / add media path to message
    def keyaInfo(self, dbpath, mediapath):
        text = self.keyaText(dbpath)
        media = self.keyaMedia(mediapath)
        keya_info = []
        for t in text:
            ttime = t["time"]
            for m in media:
                mtime = m["time"]
                if mtime == ttime:
                    t["media"] = m["media"]
                else:
                    t = t
            keya_info.append(t)
        return keya_info


# html format
def htmlbody(info):
    index = "<html><body>"
    value = ""
    for i in info:
        if i["mediaType"] == 1:
            element = "<div><p>{time}</p><p>{text}</p><img src='{media}' width='300px'></div>".format(
                time=i["time"], text=i["text"].encode("utf-8"), media=i["media"])
        elif i["mediaType"] > 1:
            element = "<div><p>{time}</p><p>{text}</p><video src='{media}' width='300px' controls='controls'></video></div>".format(
                time=i["time"], text=i["text"].encode("utf-8"), media=i["media"])
        else:
            element = "<div><p>{time}</p><p>{text}</p></div>".format(
                time=i["time"], text=i["text"].encode("utf-8"))
        value = value + element + "<hr/>"
    body = index + value + "</body></html>"
    f = open("index.html", "wb")
    f.write(body)
    f.close()


def opts():
    parser = argparse.ArgumentParser(description="keyaki meassages")
    parser.add_argument('--json', dest="json", action='store_true',
                        default=False, help='save to data.json')
    parser.add_argument('--html', dest="html", action='store_true',
                        default=True, help='save to index.html')
    parser.add_argument('--time', dest="ptime", action='store_true',
                        default=False, help='print media datetime')
    parser.add_argument('-d', dest='database', type=str,
                        help='main.db', required=True)
    parser.add_argument('-f', dest='media', type=str,
                        help='a media folder', required=True)
    args = parser.parse_args()
    return args


def main():
    args = opts()
    file_json = args.json
    file_html = args.html
    ptime = args.ptime
    dbpath = args.database
    mediapath = args.media

    k = keyaTalk()
    info = k.keyaInfo(dbpath, mediapath)

    # 输出媒体文件的时间戳 / get the media filename
    if ptime:
        f = open("media_name_list.txt", "wb")
        for i in info:
            if i["mediaType"] != 0:
                t = i["time"]
                media_name = t.replace(
                    "-", "").replace(":", "").replace(" ", "")
                f.write(t + " " + media_name + "\r\n")
        f.close()

    # json
    elif file_json:
        datas = json.dumps(info, ensure_ascii=False)
        # print datas
        f = open("data.json", "wb")
        f.write(datas.encode("utf-8"))
        f.close()

    # html
    elif file_html:
        htmlbody(info)


if __name__ == "__main__":
    main()
