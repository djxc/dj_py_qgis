import sys
import traceback

from qgis.PyQt.QtWidgets import QMainWindow
from qgis.core import QgsProject, QgsLayerTreeModel, QgsCoordinateReferenceSystem, QgsMapSettings
from qgis.gui import QgsLayerTreeView, QgsMapCanvas, QgsLayerTreeMapCanvasBridge
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QFileDialog, QStatusBar, QLabel, QComboBox
# from mainwindow import Ui_MainWindow
from ui.mainwindow import Ui_MainWindow
from qgis_utils import addMapLayer, readRasterFile, readVectorFile, menuProvider

PROJECT = QgsProject.instance()
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        # 1 修改标题
        self.setWindowTitle("QGIS自定义界面")

        # 2 初始化图层树
        vl = QVBoxLayout(self.dockWidgetContents)
        self.layerTreeView = QgsLayerTreeView(self)
        vl.addWidget(self.layerTreeView)

        # 3 初始化地图画布
        self.mapCanvas = QgsMapCanvas(self)
        hl = QHBoxLayout(self.frame)
        hl.setContentsMargins(0,0,0,0) #设置周围间距
        hl.addWidget(self.mapCanvas)

        # 4 设置图层树风格
        self.model = QgsLayerTreeModel(PROJECT.layerTreeRoot(),self)
        self.model.setFlag(QgsLayerTreeModel.AllowNodeRename) #允许图层节点重命名
        self.model.setFlag(QgsLayerTreeModel.AllowNodeReorder) #允许图层拖拽排序
        self.model.setFlag(QgsLayerTreeModel.AllowNodeChangeVisibility) #允许改变图层节点可视性
        self.model.setFlag(QgsLayerTreeModel.ShowLegendAsTree) #展示图例
        self.model.setAutoCollapseLegendNodes(10) #当节点数大于等于10时自动折叠
        self.layerTreeView.setModel(self.model)

        # 4 建立图层树与地图画布的桥接
        self.layerTreeBridge = QgsLayerTreeMapCanvasBridge(PROJECT.layerTreeRoot(),self.mapCanvas,self)

        # 5 初始加载影像
        self.firstAdd = True

        # 7 图层树右键菜单创建
        self.rightMenuProv = menuProvider(self)
        self.layerTreeView.setMenuProvider(self.rightMenuProv)

        # 8.0 提前给予基本CRS
        self.mapCanvas.setDestinationCrs(QgsCoordinateReferenceSystem("EPSG:4326"))

        # 8 状态栏控件
        self.statusBar = QStatusBar()
        self.statusBar.setStyleSheet('color: black; border: none')
        self.statusXY = QLabel('{:<40}'.format('')) #x y 坐标状态
        self.statusBar.addWidget(self.statusXY,1)
        self.statusScaleLabel = QLabel('比例尺')
        self.statusScaleComboBox = QComboBox(self)
        self.statusScaleComboBox.setFixedWidth(120)  
        self.statusScaleComboBox.addItems(["1:500","1:1000","1:2500","1:5000","1:10000","1:25000","1:100000","1:500000","1:1000000"])
        self.statusScaleComboBox.setEditable(True)
        self.statusBar.addWidget(self.statusScaleLabel)
        self.statusBar.addWidget(self.statusScaleComboBox)
        self.statusCrsLabel = QLabel(f"坐标系: {self.mapCanvas.mapSettings().destinationCrs().description()}-{self.mapCanvas.mapSettings().destinationCrs().authid()}")
        self.statusBar.addWidget(self.statusCrsLabel)
        self.setStatusBar(self.statusBar)

        # A 按钮、菜单栏功能
        self.connectFunc()

    def connectFunc(self):
        #每次移动鼠标，坐标和比例尺变化
        self.mapCanvas.xyCoordinates.connect(self.showXY)
        self.mapCanvas.scaleChanged.connect(self.showScale)
        self.mapCanvas.destinationCrsChanged.connect(self.showCrs)
        self.statusScaleComboBox.editTextChanged.connect(self.changeScaleForString)

        self.action_open_raster.triggered.connect(self.actionOpenRasterTriggered)
        self.action_open_vector.triggered.connect(self.actionOpenShpTriggered)
        self.actionexit.triggered.connect(self.close_app)

    def showXY(self,point):
        x = point.x()
        y = point.y()
        self.statusXY.setText(f'{x:.6f}, {y:.6f}')
    
    def showScale(self,scale):
        self.statusScaleComboBox.setEditText(f"1:{int(scale)}")
    
    def showCrs(self):
        mapSetting : QgsMapSettings = self.mapCanvas.mapSettings()
        self.statusCrsLabel.setText(f"坐标系: {mapSetting.destinationCrs().description()}-{mapSetting.destinationCrs().authid()}")

    def changeScaleForString(self,str):
        try:
            left,right = str.split(":")[0],str.split(":")[-1]
            if int(left)==1 and int(right)>0 and int(right)!=int(self.mapCanvas.scale()):
                self.mapCanvas.zoomScale(int(right))
                self.mapCanvas.zoomWithCenter()
        except:
            print(traceback.format_stack())

    def close_app(self):
        """关闭程序"""
        sys.exit()

    def actionOpenRasterTriggered(self):
        data_file, ext = QFileDialog.getOpenFileName(self, '打开', '','GeoTiff(*.tif;*tiff;*TIF;*TIFF);;All Files(*);;JPEG(*.jpg;*.jpeg;*.JPG;*.JPEG);;*.png;;*.pdf')
        if data_file:
            self.addRasterLayer(data_file)

    def actionOpenShpTriggered(self):
        data_file, ext = QFileDialog.getOpenFileName(self, '打开', '',"ShapeFile(*.shp);;All Files(*);;Other(*.gpkg;*.geojson;*.kml)")
        if data_file:
            self.addVectorLayer(data_file)

    def addRasterLayer(self, rasterFilePath):
        rasterLayer = readRasterFile(rasterFilePath)
        if self.firstAdd:
            addMapLayer(rasterLayer,self.mapCanvas,True)
            self.firstAdd = False
        else:
            addMapLayer(rasterLayer,self.mapCanvas)

    def addVectorLayer(self,vectorFilePath):
        vectorLayer = readVectorFile(vectorFilePath)
        if self.firstAdd:
            addMapLayer(vectorLayer,self.mapCanvas,True)
            self.firstAdd = False
        else:
            addMapLayer(vectorLayer,self.mapCanvas)