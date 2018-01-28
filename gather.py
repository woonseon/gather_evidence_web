#-*-coding:utf-8-*-

import sys
import requests
#pip3 install imgkit
import imgkit
#pip3 install pyscreenshot
import pyscreenshot as ImageGrab
#pip3 install PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QPixmap

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_UI()

    def setup_UI(self):
        # set up window size
        self.setGeometry(500, 100, 300, 200)
        self.setWindowTitle("Gather Evidence")

        # 도메인 넣기
        self.input_domain = QLabel("Put URL")
        self.put_domain = QLineEdit()

        # 현재 화면 저장
        self.current_window = QLabel("현재 화면 저장")
        self.btn_current_store = QPushButton("click", self)
        self.btn_current_store.clicked.connect(self.save_current_window)
        
        # 스크롤 하여 전체 페이지 저장
        self.total_window = QLabel("전체 화면 저장")
        self.btn_total_store = QPushButton("click", self)
        self.btn_total_store.clicked.connect(self.save_total_window)

        # 창닫기
        self.btn_close = QPushButton("창닫기", self)
        self.btn_close.clicked.connect(QCoreApplication.instance().quit)

        # layout
        url_layout = QHBoxLayout()
        url_layout.addWidget(self.input_domain)
        url_layout.addWidget(self.put_domain)

        current_layout = QHBoxLayout()
        current_layout.addWidget(self.current_window)
        current_layout.addWidget(self.btn_current_store)
        
        total_layout = QHBoxLayout()
        total_layout.addWidget(self.total_window)
        total_layout.addWidget(self.btn_total_store)

        close_layout = QHBoxLayout()
        close_layout.addWidget(self.btn_close)
        
        layout = QVBoxLayout()
        layout.addLayout(url_layout)
        layout.addLayout(current_layout)
        layout.addLayout(total_layout)
        layout.addLayout(close_layout)

        self.setLayout(layout)

    def save_file(self, input_domain):
        # 소스 코드 얻어오기
        req = requests.get("http://" + input_domain)
        html_src = req.text

        src_name = input_domain + ".txt"
        # 소스 파일 저장
        self.f = open(src_name, 'w')
        self.f.write(html_src)
        self.f.close()

    def save_current_window(self):
        try:
            input_domain = self.put_domain.text()

            # 현재 화면 상태 저장
            imgkit.from_url('http://' + input_domain, input_domain + ".jpg")
            self.save_file(input_domain)

            #fullscreen
            im=ImageGrab.grab()
            # im.show()

            # part of the screen
            im=ImageGrab.grab(bbox(10,10,510,510)) # x1, y1, x2, y2
            im.show()

            # 성공 메시지 출력
            QMessageBox.about(self, "success", "Get Evidence :)")
        except:
            # 실패 메시지 출력
            QMessageBox.about(self, "fail", "Fail To Get Evidence:(")

    def save_total_window(self):
        try:
            input_domain = self.put_domain.text()

            # 전체 페이지 저장
            imgkit.from_url('http://' + input_domain, input_domain + ".jpg")
            self.save_file(input_domain)

            # 성공 메시지 출력
            QMessageBox.about(self, "success", "Get Evidence :)")
        except:
            # 실패 메시지 출력
            QMessageBox.about(self, "fail", "Fail To Get Evidence:(")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()