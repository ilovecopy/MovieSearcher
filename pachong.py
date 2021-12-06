import requests
from lxml import html
import csv
import re  # 正则表达式，用去匹配去除评论中的符合


# def clear(string):
#     string = string.strip()  # 去掉空格等空白符号
#     string = re.sub("[A-Za-z0-9]", "", string)  # 去掉英文字母 数字
#     string = re.sub(r"[！!？｡。，&;＂★＃＄％＆＇（）＊＋－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃「」『』【】"
#                     r"〔〕〖〗〘〙#〚〛〜〝〞/?=~〟,〰–—‘’‛“”„‟…‧﹏.]", " ", string)  # 去掉中文符号
#     string = re.sub(r"[!\'\"#。$%&()*+,-.←→/:~;<=>?@[\\]^_`_{|}~", " ", string)  # 去掉英文符号
#     return string.lower()  # 所有的英文都换成小写


def get_douban_top250():
    print("--------")
    print('正在获取豆瓣TOP250影片信息并保存至本地...')
    index = 1
    page_count = 10
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    for i in range(page_count):
        url = 'https://movie.douban.com/top250?start={}&filter='.format(i * 25)
        url_content = requests.get(url, headers=headers).content
        # 内容节点
        doc = html.fromstring(url_content)
        for y in doc.xpath('//div[@class="info"]'):
            name = y.xpath('div[@class="hd"]/a/span[@class="title"]/text()')[0]  # 影片名称

            # 影片详情
            move_content = y.xpath('div[@class="bd"]/p[1]/text()')

            # 上映日期
            dates = move_content[1].replace(" ", "").replace("\n", "").split("/")[0]
            dates = dates.replace("\xa0", "").replace("\xee", "").replace("\xf6", "").replace("\u0161", "").replace(
                "\xf4", "").replace("\xfb", "").replace("\u2027", "")
            date = str(dates)

            # 制片国家
            country = move_content[1].replace(" ", "").replace("\n", "").split("/")[1]
            country = country.replace("\xa0", "").replace("\xee", "").replace("\xf6", "").replace("\u0161", "").replace(
                "\xf4", "").replace("\xfb", "").replace("\u2027", "")

            # 影片类型
            type = move_content[1].replace(" ", "").replace("\n", "").split("/")[2]
            type = type.replace("\xa0", "").replace("\xee", "").replace("\xf6", "").replace("\u0161", "").replace(
                "\xf4", "").replace("\xfb", "").replace("\u2027", "")

            # 导演及演员信息
            chractor = move_content[0].replace(" ", "").replace("\n", "")
            chractor = chractor.replace("\xa0", "").replace("\xee", "").replace("\xf6", "").replace("\u0161",
                                                                                                    "").replace(
                "\xf4", "").replace("\xfb", "").replace("\u2027", "").replace("\xe5", "").replace("\u22ef", "").replace(
                "导演:", "")
            list = chractor.split("主演:")
            actor = 'None'
            if len(list) == 2:
                chractor, actor = list
            else:
                chractor = list[0]
                actor = 'None'
            chractor = re.sub("[a-zA-Z]", "", chractor)
            actor = re.sub("[a-zA-Z]", "", actor)
            #  chractor=clear(chractor)
            #  actor=clear(actor)
            # print("导演" + chractor)
            # print("演员" + actor)
            # 影片描述
            remark = y.xpath('div[@class="bd"]/p[@class="quote"]/span[@class="inq"]/text()')
            remark = str(remark)
            remark = remark.replace("[", "").replace("]", "").replace("'", "").replace("\u22ef", "")

            # 评分
            score = y.xpath('div[@class="bd"]/div[@class="star"]/span[2]/text()')[0]

            # 评论人数
            count = y.xpath('div[@class="bd"]/div[@class="star"]/span[4]/text()')[0]

            # 排名
            rank = str(index)

            # 保存至本地
            f = open("douban.txt", "a")  # 将上面的信息每一行以按逗号分隔的规律存入本地
            f.write(rank + ",")
            f.write(name + ",")
            f.write(date + ",")
            f.write(country + ",")
            f.write(type + ",")
            f.write(chractor + ",")
            f.write(actor + ",")
            print("导演" + chractor)
            print("演员" + actor)
            f.write(remark + ",")
            f.write(score + ",")
            f.write(count)
            f.write("\n")
            index += 1
        f.close()  # 记得关闭文件
    # 程序的开始


if __name__ == "__main__":

    # 执行get_douban_top250方法
    get_douban_top250()
    i = 0
    f = open("douban.txt", "r")
    input_csv = open("./a.csv", 'w')
    csv_write = csv.writer(input_csv, dialect='excel')
    csv_write.writerow(['排名', '电影名', '年份', '国家', '类型', '导演', '演员', '评论', '评分', '评价人数', '点击数'])
    while True:
        i += 1
        line = f.readline()
        if line:
            line = line.strip("\n")
            line = line.split(",")  # 将你写的txt文件的数据用逗号分开，此时用逗号将他们转化为列表
            line.append(0)  # 点击数置为0
            csv_write = csv.writer(input_csv, dialect='excel')
            csv_write.writerow(line)
        if i == 250:
            break
print("结束")
