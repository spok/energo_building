# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'f:\Nextcloud\Python\energo_building\gui_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.5
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(963, 796)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tree = QtWidgets.QTreeView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tree.sizePolicy().hasHeightForWidth())
        self.tree.setSizePolicy(sizePolicy)
        self.tree.setMinimumSize(QtCore.QSize(200, 0))
        self.tree.setMaximumSize(QtCore.QSize(250, 16777215))
        self.tree.setWordWrap(True)
        self.tree.setObjectName("tree")
        self.verticalLayout_2.addWidget(self.tree)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.but_load = QtWidgets.QPushButton(self.centralwidget)
        self.but_load.setMaximumSize(QtCore.QSize(75, 16777215))
        self.but_load.setObjectName("but_load")
        self.horizontalLayout.addWidget(self.but_load)
        self.but_save = QtWidgets.QPushButton(self.centralwidget)
        self.but_save.setMaximumSize(QtCore.QSize(75, 16777215))
        self.but_save.setObjectName("but_save")
        self.horizontalLayout.addWidget(self.but_save)
        self.but_save_as = QtWidgets.QPushButton(self.centralwidget)
        self.but_save_as.setMaximumSize(QtCore.QSize(90, 16777215))
        self.but_save_as.setObjectName("but_save_as")
        self.horizontalLayout.addWidget(self.but_save_as)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setMinimumSize(QtCore.QSize(0, 400))
        self.tabWidget.setObjectName("tabWidget")
        self.tab1 = QtWidgets.QWidget()
        self.tab1.setObjectName("tab1")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab1)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.tab1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(0, 20))
        self.label.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.tab_osn = QtWidgets.QTableWidget(self.tab1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_osn.sizePolicy().hasHeightForWidth())
        self.tab_osn.setSizePolicy(sizePolicy)
        self.tab_osn.setMinimumSize(QtCore.QSize(0, 300))
        self.tab_osn.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tab_osn.setObjectName("tab_osn")
        self.tab_osn.setColumnCount(0)
        self.tab_osn.setRowCount(0)
        self.verticalLayout_3.addWidget(self.tab_osn)
        self.label_2 = QtWidgets.QLabel(self.tab1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(0, 20))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.text_gsop = QtWidgets.QPlainTextEdit(self.tab1)
        self.text_gsop.setMinimumSize(QtCore.QSize(0, 150))
        self.text_gsop.setMaximumSize(QtCore.QSize(16777215, 150))
        self.text_gsop.setObjectName("text_gsop")
        self.verticalLayout_3.addWidget(self.text_gsop)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.tabWidget.addTab(self.tab1, "")
        self.tab2 = QtWidgets.QWidget()
        self.tab2.setObjectName("tab2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tab2)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_4 = QtWidgets.QLabel(self.tab2)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_5.addWidget(self.label_4)
        self.tab_norm = QtWidgets.QTableWidget(self.tab2)
        self.tab_norm.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tab_norm.setObjectName("tab_norm")
        self.tab_norm.setColumnCount(0)
        self.tab_norm.setRowCount(0)
        self.verticalLayout_5.addWidget(self.tab_norm)
        self.label_5 = QtWidgets.QLabel(self.tab2)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_5.addWidget(self.label_5)
        self.text_norm = QtWidgets.QPlainTextEdit(self.tab2)
        self.text_norm.setMaximumSize(QtCore.QSize(16777215, 200))
        self.text_norm.setObjectName("text_norm")
        self.verticalLayout_5.addWidget(self.text_norm)
        self.verticalLayout_6.addLayout(self.verticalLayout_5)
        self.tabWidget.addTab(self.tab2, "")
        self.tab3 = QtWidgets.QWidget()
        self.tab3.setObjectName("tab3")
        self.tabWidget.addTab(self.tab3, "")
        self.tab4 = QtWidgets.QWidget()
        self.tab4.setObjectName("tab4")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.tab4)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.vbox2 = QtWidgets.QVBoxLayout()
        self.vbox2.setObjectName("vbox2")
        self.verticalLayout_8.addLayout(self.vbox2)
        self.tabWidget.addTab(self.tab4, "")
        self.tab5 = QtWidgets.QWidget()
        self.tab5.setObjectName("tab5")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.tab5)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.vbox3 = QtWidgets.QVBoxLayout()
        self.vbox3.setObjectName("vbox3")
        self.verticalLayout_9.addLayout(self.vbox3)
        self.tabWidget.addTab(self.tab5, "")
        self.tab6 = QtWidgets.QWidget()
        self.tab6.setObjectName("tab6")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.tab6)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.vbox4 = QtWidgets.QVBoxLayout()
        self.vbox4.setObjectName("vbox4")
        self.verticalLayout_11.addLayout(self.vbox4)
        self.tabWidget.addTab(self.tab6, "")
        self.tab7 = QtWidgets.QWidget()
        self.tab7.setObjectName("tab7")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.tab7)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.vbox5 = QtWidgets.QVBoxLayout()
        self.vbox5.setObjectName("vbox5")
        self.verticalLayout_10.addLayout(self.vbox5)
        self.tabWidget.addTab(self.tab7, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.but_load.setText(_translate("MainWindow", "Открыть"))
        self.but_save.setText(_translate("MainWindow", "Сохранить"))
        self.but_save_as.setText(_translate("MainWindow", "Сохранить как"))
        self.label.setText(_translate("MainWindow", "Общие данные о здании"))
        self.label_2.setText(_translate("MainWindow", "Расчет отопительного периода"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab1), _translate("MainWindow", "Tab 1"))
        self.label_4.setText(_translate("MainWindow", "Нормативные сопротивления теплопередаче"))
        self.label_5.setText(_translate("MainWindow", "Вывод расчета"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab2), _translate("MainWindow", "Page"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab3), _translate("MainWindow", "Tab 2"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab4), _translate("MainWindow", "Page"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab5), _translate("MainWindow", "Page"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab6), _translate("MainWindow", "Page"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab7), _translate("MainWindow", "Page"))
