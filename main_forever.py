import gui
import forever
import sys

from PySide2.QtWidgets import *


class MainWindow(QDialog, gui.Ui_Form):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(lambda: self.upload())
        self.pushButton_2.clicked.connect(lambda: self.push_start())
        self.pushButton_3.clicked.connect(lambda: self.get_detail())

        self.token = self.textEdit.toPlainText()
        self.device_id = self.textEdit_2.toPlainText()
        self.user_index = self.textEdit_3.toPlainText()
        self.expect_money = self.textEdit_4.toPlainText()
        self.buy_index = self.textEdit_5.toPlainText()
        self.password = self.textEdit_5.toPlainText()
        self.model = self.buy_index = self.comboBox_7.currentIndex()
        self.num = self.textEdit_8.toPlainText()

        self.threads = None
        self.init_buy = None
        self.key = False
        self.key_count = 0
        self.msg = None
        self.thread_num = 5

        self.token = 'Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiIxM2YzNmE5N2YwMjUwYmMyZWUxMjhiNTcyYjg1ZmFhNCIsImV4cCI6MTY1MjM0MTgwMSwianRpIjoiMTUyNDYyNzkzNjk4NDgyNTg1NiIsInN1YiI6IjE1MDczNDQxODI5OTMxODI3MjAiLCJzY29wZSI6InVzZXIuYWxsIn0.owNV7DwGBWl5ofndYcW0gYh1n13r2XdAl23C37Z_2AxJZyx050O6-CUeplX79Fxspjt4eHa1U3xImVSKGg4Sdw'
        self.textBrowser.setText("默认token：")
        self.textBrowser.append(self.token)
                    
    def push_start(self):
        if self.key is True:
            for thread in self.threads:
                thread._signal.connect(self.call_backlog)
                thread.start()
        else:
            self.textBrowser.append("请初始化！")

    def get_detail(self):
        self.buy_index = self.comboBox_4.currentIndex()
        if self.key is True:

            self.textBrowser_2.setText(forever.get_detail(self.buy_index, self.token, self.device_id))

        else:
            self.textBrowser_2.setText("获取失败！")

    def upload(self):
        # self.comboBox.currentText()
        self.model = self.comboBox_7.currentIndex()

        if self.comboBox.currentText() == "无":
            self.device_id = self.textEdit_2.toPlainText()
            self.key_count = self.key_count + 1
        else:
            self.device_id = self.comboBox.currentText()
            self.key_count = self.key_count + 1

        if self.comboBox_2.currentText() == "无":
            self.user_index = self.textEdit_4.toPlainText()
            self.key_count = self.key_count + 1
        else:
            self.user_index = self.comboBox_2.currentText()
            self.key_count = self.key_count + 1

        if self.comboBox_3.currentText() == "无":
            self.expect_money = self.textEdit_3.toPlainText()
            self.key_count = self.key_count + 1
        else:
            self.expect_money = self.comboBox_3.currentText()
            self.key_count = self.key_count + 1

        if self.comboBox_4.currentText() == "无":
            self.buy_index = self.textEdit_5.toPlainText()
            self.key_count = self.key_count + 1
        else:
            self.buy_index = self.comboBox_4.currentIndex()
            self.key_count = self.key_count + 1

        if self.comboBox_5.currentText() == "无":
            self.password = self.textEdit_6.toPlainText()
            self.key_count = self.key_count + 1
        else:
            self.password = self.comboBox_5.currentText()
            self.key_count = self.key_count + 1

        if self.textEdit.toPlainText() != '':
            self.token = self.textEdit.toPlainText()
            self.key_count = self.key_count + 1
        else:
            self.token = self.token
            self.key_count = self.key_count + 1

        if self.key_count == 6:
            self.thread_num = int(self.comboBox_6.currentText())
            self.threads = []
            for i in range(1, self.thread_num):
                t = forever.ForeverBuyNft(buy_index=int(self.buy_index), device_id=str(self.device_id),
                                          expect_money=float(self.expect_money),
                                          pay_password=self.password, token=self.token, user_index=int(self.user_index),
                                          msage=self.msg, buy_model=self.model, num=self.num)
                self.threads.append(t)

            self.textBrowser.append(self.token)
            self.textBrowser.append("加载信息成功！")

            print(self.textEdit.toPlainText())
            self.key = True
            self.key_count = 0
        else:
            self.key_count = 0
            self.key = False
            self.textBrowser.append("加载信息失败，请从新上传！")

    def call_backlog(self, msg):
        self.textBrowser.append(msg)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    # ui = gui.Ui_Form()
    # ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


