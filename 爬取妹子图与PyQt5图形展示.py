# -*-coding:utf-8-*-
import requests
from lxml import etree
import sys
from PyQt5.QtWidgets import QCheckBox,QApplication
from PyQt5.QtGui import QPixmap
from PyQt5 import uic


(form_class,qtbase_class) = uic.loadUiType("Beauty.ui")
def get_url():
    headers = {"User_Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.59"}
    res = requests.get("https://m.tupianzj.com/meinv/mm/meinvxiezhen",headers=headers)
    res.encoding = "gb2312"
    html = etree.HTML(res.text)
    url = html.xpath('//ul[@class="d1 ico3"]//li//a//img//@src')
    text = html.xpath('//ul[@class="d1 ico3"]//li//a//img//@alt')
    img_list = url
    text_list = text
    url2 = html.xpath('//div[@id="tag89ac294e4acd2a965c9559f9cecdfe81"]//li//a//em//img//@lazysrc')
    text2 = html.xpath('//div[@id="tag89ac294e4acd2a965c9559f9cecdfe81"]//li//a//em//@alt')
    img_list.extend(url2)
    text_list.extend(text2)
    return img_list,text_list

class MainWindow(form_class,qtbase_class):
    def __init__(self,img_list,text_list):
        super(MainWindow,self).__init__()
        self.setupUi(self)
        self.setWindowTitle(" "*70+"MainWindow")

        self.num = 1
        self.img_list = img_list
        self.text_list = text_list
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(len(img_list))
        self.checkbox = [self._addCheckBox(i,text) for i,text in enumerate(text_list)]
        self.getButton.clicked.connect(self._printCheckBox)
        self.nextButton.clicked.connect(self._nextPage)
        self.upButton.clicked.connect(self._upPage)

    def _addCheckBox(self,i,text):
        checkbox = QCheckBox()
        checkbox.setObjectName(self.img_list[i])
        checkbox.setText(text)
        self.tableWidget.setCellWidget(i,0,checkbox)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setColumnWidth(1,85)
        return checkbox

    def _printCheckBox(self):
        print_cb = []
        # 清空textBrowser
        self.textBrowser.setPlainText("")
        # textBrowser设置成可打开外部链接
        self.textBrowser.setOpenExternalLinks(True)
        self.print_cb = [i for i in self.checkbox if i.isChecked()==True]
        self.l_num = len(self.print_cb)
        print(self.l_num)
        for i in self.print_cb:
            text = i.text()
            url = i.objectName()
            self.textBrowser.append(text)
            # 将字符串设置成链接
            self.textBrowser.append("<a href = \"{}\">{}</a>".format(url,url))
        if self.print_cb:
            img_url = self.print_cb[0].objectName()
            print(img_url)
            self._showImg(img_url)
            print("展示完毕")
        self.num = 1
        self.pageLable.setText(str(self.num))

    def _nextPage(self):
        if self.num<self.l_num:
            self.num = self.num+1
        else:
            self.num = self.l_num
        print(self.num)
        img_url = self.print_cb[self.num-1].objectName()
        self._showImg(img_url)
        self.pageLable.setText(str(self.num))


    def _upPage(self):
        if self.num>1:
            self.num = self.num-1
        else:
            self.num = 1
        img_url = self.print_cb[self.num - 1].objectName()
        self._showImg(img_url)
        self.pageLable.setText(str(self.num))

    def _showImg(self,img_url):
        headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.59"}
        html = requests.get(img_url, headers=headers).content
        pixmap = QPixmap()
        pixmap.loadFromData(html)
        self.imgLable.setPixmap(pixmap)

        print("我出来啦")

if __name__=="__main__":
    img_list,text_list = get_url()
    app = QApplication(sys.argv)
    uic = MainWindow(img_list,text_list)
    uic.show()
    sys.exit(app.exec_())

