# 基于python的二次开发
- 1、首先需要安装qgis，
- 2、qgis安装完成之后，默认自带了python的解析器，使用该python解析器进行二次开发
- 3、界面可以再qtcreator中创建保存ui，然后利用pyqt工具将ui转换为py文件，最后再自己项目中引用这个界面即可。`pyuic5 -o mainwindow.py D:\code\GIS\qt_py\mainwindow.ui`,安装了pyqt依赖后会包含pyuic5命令。
- 4、加载图层等操作都可以再python代码中进行。