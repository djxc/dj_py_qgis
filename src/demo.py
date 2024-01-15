from qgis.core import QgsApplication
from PyQt5.QtCore import Qt
from mainWindow1 import MainWindow

def demo():
    # 告知QGIS路径
    QgsApplication.setPrefixPath('D:/ProgramFiles/QGIS 3.22.9/apps/qgis-ltr', True)

    # 第二个参数为是否启用GUI
    qgs = QgsApplication([], False)

    # 初始化QGIS
    qgs.initQgis()

    # 开始写代码
    print(QgsApplication.prefixPath())
    print("Hello Qgis！")

    # 从内存中删除数据提供程序和层注册表来结束
    qgs.exitQgis()

def main():
    QgsApplication.setPrefixPath('D:/ProgramFiles/QGIS 3.22.9/apps/qgis-ltr', True)
    QgsApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QgsApplication([], True)
    app.initQgis()
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()
    app.exitQgis()

if __name__ == "__main__":
    main()