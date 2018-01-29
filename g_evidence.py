from PyQt4 import QtCore, QtGui, QtWebKit
import sys
import datetime
import piexif

today = str(datetime.datetime.now())

class Browser(QtGui.QMainWindow):
    def __init__(self):

        QtGui.QMainWindow.__init__(self)
        self.resize(800,600)
        self.centralwidget = QtGui.QWidget(self)

        self.mainLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setMargin(1)

        self.frame = QtGui.QFrame(self.centralwidget)

        self.gridLayout = QtGui.QVBoxLayout(self.frame)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)

        self.horizontalLayout = QtGui.QHBoxLayout()
        self.tb_url = QtGui.QLineEdit(self.frame)
        self.bt_back = QtGui.QPushButton(self.frame)
        self.bt_ahead = QtGui.QPushButton(self.frame)
        self.bt_current_capture = QtGui.QPushButton("Current-capture", self.frame)
        self.bt_current_capture.clicked.connect(self.get_current_window)
        self.bt_total_capture = QtGui.QPushButton("All-capture", self.frame)
        self.bt_total_capture.clicked.connect(self.get_total_window)
        self.bt_src_capture = QtGui.QPushButton("Source-capture", self.frame)
        self.bt_src_capture.clicked.connect(self.get_src)

        self.bt_back.setIcon(QtGui.QIcon().fromTheme("go-previous"))
        self.bt_ahead.setIcon(QtGui.QIcon().fromTheme("go-next"))

        self.horizontalLayout.addWidget(self.bt_back)
        self.horizontalLayout.addWidget(self.bt_ahead)
        self.horizontalLayout.addWidget(self.tb_url)
        self.horizontalLayout.addWidget(self.bt_current_capture)
        self.horizontalLayout.addWidget(self.bt_total_capture)
        self.horizontalLayout.addWidget(self.bt_src_capture)
        self.gridLayout.addLayout(self.horizontalLayout)

        self.html = QtWebKit.QWebView()
        self.html.loadFinished.connect(self.get_html)
        #self.html.loadFinished.connect(self.render)
        self.gridLayout.addWidget(self.html)
        self.mainLayout.addWidget(self.frame)
        self.setCentralWidget(self.centralwidget)

        self.connect(self.tb_url, QtCore.SIGNAL("returnPressed()"), self.browse)
        self.connect(self.bt_back, QtCore.SIGNAL("clicked()"), self.html.back)
        self.connect(self.bt_ahead, QtCore.SIGNAL("clicked()"), self.html.forward)

        self.default_url = "http://google.com"
        self.tb_url.setText(self.default_url)
        self.browse()
    
    def get_html(self):
        page = self.html.page()
        frame = page.mainFrame()
        html_code = unicode(frame.toHtml())
        return html_code

    def browse(self):
        url = self.tb_url.text() if self.tb_url.text() else self.default_url
        self.url_name = url.split('//')[1]
        self.html.load(QtCore.QUrl(url))
        self.html.show()

    def get_total_window(self):
        try:
            self.html.page().setViewportSize(self.html.page().mainFrame().contentsSize())
            image = QtGui.QImage(self.html.page().viewportSize(), QtGui.QImage.Format_ARGB32)

            painter = QtGui.QPainter()
            painter.begin(image)
            self.html.page().mainFrame().render(painter)
            painter.end()

            file_name = self.url_name + '_' + today + '_total.jpg'
            print file_name
            image.save(file_name)
            
            QtGui.QMessageBox.about(self, "Success", "Save Full Screen!!")
        except:
            QtGui.QMessageBox.about(self, "Warning", "Can't save full screen!!")
    
    def get_current_window(self):
        try:
            self.html.page().mainFrame().contentsSize()
            image = QtGui.QImage(self.html.page().viewportSize(), QtGui.QImage.Format_ARGB32)

            painter = QtGui.QPainter()
            painter.begin(image)
            self.html.page().mainFrame().render(painter)
            painter.end()

            file_name = self.url_name + '_' + today + '_current.jpg'
            image.save(file_name)
            
            QtGui.QMessageBox.about(self, "Success", "Save Current Screen!!")
        except:
            QtGui.QMessageBox.about(self, "Warning", "Can't save current screen!!")
    
    # get html src
    def get_src(self):
        try:
            page = self.html.page()
            frame = page.mainFrame()
            html_code = unicode(frame.toHtml())
            
            file_name = self.url_name + '_' + today + '_src.txt'
            f = open(file_name, 'w')
            f.write(html_code.encode("utf-8"))
            f.close()
            QtGui.QMessageBox.about(self, "Success", "Save html src!!")
        except:
            QtGui.QMessageBox.about(self, "Warning", "Can't save html src!!")

if __name__ == '__main__':
    qapp = QtGui.QApplication(sys.argv)
    w = Browser()
    w.show()
    sys.exit(qapp.exec_())