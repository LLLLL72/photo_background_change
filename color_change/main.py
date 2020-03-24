import sys
import cv2
import threading
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow ,QGraphicsScene, QGraphicsPixmapItem, QFileDialog
from PyQt5.QtCore import Qt,pyqtSignal,QCoreApplication
from PyQt5.QtGui import QPixmap,QImage
from mainwindow import Ui_MainWindow  # 加载我们的布局

from change import change_bg

class Mainwindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(Mainwindow, self).__init__(*args, **kwargs)
        self.setupUi(self)  # 初始化ui
        # 在这里，可以做一些UI的操作了，或者是点击事件或者是别的
        # 也可以另外写方法，可以改变lable的内容
        self.setMaximumSize(600,400)
        self.setMinimumSize(600, 400)
        self.pushButton.clicked.connect(self.getImage)
        self.pushButton_2.clicked.connect(self.save)

        import numpy as np
        self.result = np.ones((3, 3), dtype=np.uint8)
        self.image = QPixmap()
        self.signal.connect(self.show_result)

    def getImage(self):

        path = QFileDialog.getOpenFileName(self, "选取文件", "h:/test", "(*.png);(*.jpg)")[0]
        if path == '':
            pass
        else:
            self.image.load(path)
            self.image_ = cv2.imread(path)
            self.LoadImage()

    def LoadImage(self):
        self.graphicsView.scene = QGraphicsScene()  # 创建一个图片元素的对象
        item = QGraphicsPixmapItem(self.image)  # 创建一个变量用于承载加载后的图片
        self.graphicsView.scene.addItem(item)  # 将加载后的图片传递给scene对象
        item.setScale(self.graphicsView.width()/self.image.width())
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setScene(self.graphicsView.scene)
        threading.Thread(target=self.convert,args=()).start()


    def convert(self):
        _translate = QCoreApplication.translate
        self.pushButton_2.setText(_translate("MainWindow", "正在转换"))
        self.pushButton_2.setDisabled(True)
        self.result = change_bg(self.image_)
        self.signal.emit()
        self.pushButton_2.setDisabled(False)
        self.pushButton_2.setText(_translate("MainWindow", "保存图片"))


    def show_result(self):
        self.result_show = cv2.cvtColor(self.result, cv2.COLOR_BGR2RGB)        #转换图像通道

        frame = QImage(self.result_show, self.result.shape[1]  , self.result.shape[0], self.result.shape[1]*3,QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        item=QGraphicsPixmapItem(pix)                      #创建像素图元
        item.setScale(self.graphicsView.width() / (self.image.width()+1))
        self.graphicsView_2.scene=QGraphicsScene()                             #创建场景
        self.graphicsView_2.scene.addItem(item)
        self.graphicsView_2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView_2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView_2.setScene(self.graphicsView_2.scene)                      #将场景添加至视图

    def save(self):
        save_path = QFileDialog.getSaveFileName(self, "选取文件", "h:", "(*.png);(*.jpg)")[0]
        if save_path == '':
            pass
        else:
            cv2.imwrite(save_path,self.result)





if __name__ == '__main__':  # 程序的入口
    app = QApplication(sys.argv)
    win = Mainwindow()
    win.show()
    sys.exit(app.exec_())
