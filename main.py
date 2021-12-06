import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap
from jiemian import Ui_Dialog
import pandas as pd


class License(QMainWindow, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_search.clicked.connect(self.query)
        self.pushButton_fuzzysearch.clicked.connect(self.fuzzy_query)
        self.pushButton_star.clicked.connect(self.star)
        self.pushButton_star.clicked.connect(self.rank)
        self.pushButton_charactor.clicked.connect(self.charactor)
        self.pushButton_gaibian.clicked.connect(self.mingzugaibian)

    def charactor(self):
        charactor_name = self.Edit_input.text()
        file = pd.read_csv('a.csv')
        df = pd.DataFrame(file)
        df.index = range(len(df))
        self.movie_rank.clear()
        for i in range(len(df)):
            document = df[i:i + 1]
            if charactor_name == str(document['导演'][i]):
                self.movie_rank.append(
                    str(document['电影名'][i]) + ' 点击数 ' + str(
                        document['点击数'][i]) + ' 评论 ' + str(document['评论'][i]))

    def search(self, movie_name):
        file = pd.read_csv('a.csv')
        df = pd.DataFrame(file)
        for i in range(len(df)):
            document = df[i:i + 1]
            if movie_name == str(document['电影名'][i]):
                return str(document['评论'][i]), document['点击数'][i], i
        return "找不到"

    def query(self):
        name = self.Edit_input.text()
        info = self.search(name)
        self.movie_list.setText('评论：' + info[0] + '\n' + '点击数：' + str(info[1]))  # 从输入框获取信息
        if info == "找不到":
            self.movie_list.setText('找不到该电影')
        pix = QPixmap('./picture/' + name + '.jpg')
        lb1 = QLabel(self)
        lb1.setGeometry(445, 150, 270, 400)
        lb1.setPixmap(pix)
        lb1.show()
        return name, info[0], info[1], info[2]

    def fuzzy_search(self, movie_name):
        result = []
        file = pd.read_csv('a.csv')
        df = pd.DataFrame(file)
        self.movie_rank.clear()
        for i in range(len(df)):
            document = df[i:i + 1]
            if movie_name in str(document['电影名'][i]):
                result.append([str(document['电影名'][i]), str(document['评论'][i]), document['点击数'][i], i])
        return result

    def fuzzy_query(self):
        name = self.Edit_input.text()
        info = self.fuzzy_search(name)
        self.movie_rank.clear()
        for i in range(len(info)):
            self.movie_rank.append(' 电影名' + info[i][0] + ' 评论' + info[i][1] + ' 点击数' + str(info[i][2]))

    def star(self):
        in_put, comment, click, rank = self.query()
        file = pd.read_csv('a.csv')
        df = pd.DataFrame(file)
        click += 1
        df.loc[rank, '点击数'] = click
        df.to_csv('a.csv', index=False)
        self.movie_list.setText('评论：' + str(df.loc[rank, '评论']) + '\n' + '点击数：' + str(df.loc[rank, '点击数']))  # 从输入框获取信息

    def rank(self):
        file = pd.read_csv('a.csv')
        file.sort_values(by='点击数', inplace=True, ascending=False)  # 点击数从高到低排序
        df = pd.DataFrame(file)
        df.index = range(len(df))
        self.movie_rank.clear()
        for i in range(len(df)):
            self.movie_rank.append(str(df.loc[i, '电影名']) + ' 点击数' + str(df.loc[i, '点击数']) + ' 排名' + str(i + 1))

    def mingzugaibian(self):
        name = self.Edit_input.text()
        file = pd.read_csv('a.csv')
        df = pd.DataFrame(file)
        df.index = range(len(df))
        for i in range(len(df)):
            document = df[i:i + 1]
            if name == str(document['电影名'][i]):
                self.movie_list.append(
                    df.loc[i, '电影名'] + df.loc[i, '名著改编'] * "是名著改编的" + (1 - df.loc[i, '名著改编']) * "不是名著改编的")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    L = License()
    L.show()
    sys.exit(app.exec_())
