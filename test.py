import sys
from PyQt4 import QtCore, QtGui, QtWebKit


class Capturer(object):
    """A class to capture webpages as images"""

    def __init__(self, url, filename):
        self.url = url
        self.filename = filename
        self.saw_initial_layout = False
        self.saw_document_complete = False

    def loadFinishedSlot(self):
        self.saw_document_complete = True
        if self.saw_initial_layout and self.saw_document_complete:
            self.doCapture()

    def initialLayoutSlot(self):
        self.saw_initial_layout = True
        if self.saw_initial_layout and self.saw_document_complete:
            self.doCapture()

    def capture(self):
        """Captures url as an image to the file specified"""
        self.wb = QtWebKit.QWebPage()
        self.wb.mainFrame().setScrollBarPolicy(
            QtCore.Qt.Horizontal, QtCore.Qt.ScrollBarAlwaysOff)
        self.wb.mainFrame().setScrollBarPolicy(
            QtCore.Qt.Vertical, QtCore.Qt.ScrollBarAlwaysOff)

        self.wb.loadFinished.connect(self.loadFinishedSlot)
        self.wb.mainFrame().initialLayoutCompleted.connect(
            self.initialLayoutSlot)

        self.wb.mainFrame().load(QtCore.QUrl(self.url))

    def doCapture(self):
        self.wb.setViewportSize(self.wb.mainFrame().contentsSize())
        img = QtGui.QImage(self.wb.viewportSize(), QtGui.QImage.Format_ARGB32)
        painter = QtGui.QPainter(img)
        self.wb.mainFrame().render(painter)
        painter.end()
        img.save(self.filename)
        QtCore.QCoreApplication.instance().quit()

if __name__ == "__main__":
    """Run a simple capture"""
    app = QtGui.QApplication(sys.argv)
    c = Capturer(sys.argv[1], sys.argv[2])
    c.capture()
    app.exec_()