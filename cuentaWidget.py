# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cuentaView.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QHeaderView, QLabel,
    QLineEdit, QPushButton, QScrollArea, QSizePolicy,
    QTableView, QWidget)

class Ui_cuenta_view(object):
    def setupUi(self, cuenta_view):
        if not cuenta_view.objectName():
            cuenta_view.setObjectName(u"cuenta_view")
        cuenta_view.resize(334, 537)
        cuenta_view.setMinimumSize(QSize(334, 537))
        cuenta_view.setMaximumSize(QSize(334, 537))
        cuenta_view.setStyleSheet(u"background-color:rgb(222, 221, 218)")
        self.paciente_label_2 = QLabel(cuenta_view)
        self.paciente_label_2.setObjectName(u"paciente_label_2")
        self.paciente_label_2.setGeometry(QRect(10, 10, 311, 31))
        font = QFont()
        font.setPointSize(18)
        self.paciente_label_2.setFont(font)
        self.paciente_label_2.setStyleSheet(u"color:black")
        self.dr_label = QLabel(cuenta_view)
        self.dr_label.setObjectName(u"dr_label")
        self.dr_label.setGeometry(QRect(10, 50, 311, 31))
        self.dr_label.setFont(font)
        self.dr_label.setStyleSheet(u"color:black")
        self.label = QLabel(cuenta_view)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 450, 66, 17))
        self.label.setStyleSheet(u"color:black")
        self.scrollArea = QScrollArea(cuenta_view)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(0, 90, 331, 271))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 329, 269))
        self.tableView = QTableView(self.scrollAreaWidgetContents)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setGeometry(QRect(0, 0, 331, 271))
        self.tableView.setStyleSheet(u"color:black;")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.Total_label = QLabel(cuenta_view)
        self.Total_label.setObjectName(u"Total_label")
        self.Total_label.setGeometry(QRect(170, 440, 161, 21))
        font1 = QFont()
        font1.setPointSize(16)
        self.Total_label.setFont(font1)
        self.Total_label.setStyleSheet(u"color:black")
        self.remove_btn_extra = QPushButton(cuenta_view)
        self.remove_btn_extra.setObjectName(u"remove_btn_extra")
        self.remove_btn_extra.setGeometry(QRect(80, 400, 61, 31))
        font2 = QFont()
        font2.setBold(True)
        self.remove_btn_extra.setFont(font2)
        self.remove_btn_extra.setAutoFillBackground(False)
        self.remove_btn_extra.setStyleSheet(u"background-color:rgb(53, 132, 228); color: rgb(246, 245, 244); border-radius:10px;")
        self.remove_btn_extra.setAutoRepeat(False)
        self.add_btn_extra = QPushButton(cuenta_view)
        self.add_btn_extra.setObjectName(u"add_btn_extra")
        self.add_btn_extra.setGeometry(QRect(10, 400, 61, 31))
        self.add_btn_extra.setFont(font2)
        self.add_btn_extra.setAutoFillBackground(False)
        self.add_btn_extra.setStyleSheet(u"background-color:rgb(53, 132, 228); color: rgb(246, 245, 244); border-radius:10px;")
        self.add_btn_extra.setAutoRepeat(False)
        self.finish_btn = QPushButton(cuenta_view)
        self.finish_btn.setObjectName(u"finish_btn")
        self.finish_btn.setGeometry(QRect(230, 400, 91, 31))
        self.finish_btn.setFont(font2)
        self.finish_btn.setAutoFillBackground(False)
        self.finish_btn.setStyleSheet(u"background-color:rgb(53, 132, 228); color: rgb(246, 245, 244); border-radius:10px;")
        self.finish_btn.setAutoRepeat(False)
        self.efeCheckBox = QCheckBox(cuenta_view)
        self.efeCheckBox.setObjectName(u"efeCheckBox")
        self.efeCheckBox.setGeometry(QRect(20, 370, 92, 23))
        self.efeCheckBox.setStyleSheet(u"color:black;")
        self.tarjCheckBox = QCheckBox(cuenta_view)
        self.tarjCheckBox.setObjectName(u"tarjCheckBox")
        self.tarjCheckBox.setGeometry(QRect(210, 370, 92, 23))
        self.tarjCheckBox.setStyleSheet(u"color:black;")
        self.notaLe = QLineEdit(cuenta_view)
        self.notaLe.setObjectName(u"notaLe")
        self.notaLe.setGeometry(QRect(10, 470, 301, 61))

        self.retranslateUi(cuenta_view)

        self.remove_btn_extra.setDefault(False)
        self.add_btn_extra.setDefault(False)
        self.finish_btn.setDefault(False)


        QMetaObject.connectSlotsByName(cuenta_view)
    # setupUi

    def retranslateUi(self, cuenta_view):
        cuenta_view.setWindowTitle(QCoreApplication.translate("cuenta_view", u"Form", None))
        self.paciente_label_2.setText(QCoreApplication.translate("cuenta_view", u"Paciente:", None))
        self.dr_label.setText(QCoreApplication.translate("cuenta_view", u"Doctor:", None))
        self.label.setText(QCoreApplication.translate("cuenta_view", u"Nota:", None))
        self.Total_label.setText(QCoreApplication.translate("cuenta_view", u"Total:", None))
        self.remove_btn_extra.setText(QCoreApplication.translate("cuenta_view", u"Quitar", None))
#if QT_CONFIG(shortcut)
        self.remove_btn_extra.setShortcut(QCoreApplication.translate("cuenta_view", u"Return", None))
#endif // QT_CONFIG(shortcut)
        self.add_btn_extra.setText(QCoreApplication.translate("cuenta_view", u"A\u00f1adir", None))
#if QT_CONFIG(shortcut)
        self.add_btn_extra.setShortcut(QCoreApplication.translate("cuenta_view", u"Return", None))
#endif // QT_CONFIG(shortcut)
        self.finish_btn.setText(QCoreApplication.translate("cuenta_view", u"Finalizar", None))
#if QT_CONFIG(shortcut)
        self.finish_btn.setShortcut(QCoreApplication.translate("cuenta_view", u"Return", None))
#endif // QT_CONFIG(shortcut)
        self.efeCheckBox.setText(QCoreApplication.translate("cuenta_view", u"Efectivo", None))
        self.tarjCheckBox.setText(QCoreApplication.translate("cuenta_view", u"Tarjeta", None))
    # retranslateUi

