from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QDialog, QTableView


class ShowCities(QDialog):
    def __init__(self, parent=None):
        super(ShowCities, self).__init__(parent)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.table = QTableWidget()
        self.table.setColumnCount(20)
        self.table.setColumnWidth(0, 100)
        for i in range(1, 20):
            self.table.setColumnWidth(i, 50)
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.verticalLayout.addWidget(self.table)
        self.pushButton = QPushButton(self)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.btnClosed)
        self.verticalLayout.addWidget(self.pushButton)
        self.setWindowTitle("Климатические параметры городов")
        self.pushButton.setText("Закрыть")
        self.setLayout(self.verticalLayout)

    def table_show(self, cities: list):
        head = ["Город", "Тх0,98", "Тх0,92", "Тнхп0,98", "Тнхп0,92", "Т0,94", "Табс", "Аср", "Zот_<0", "tот_<0",
                "Zот_<8", "tот_<8", "Zот_<10", "tот_<10", "Wср", "Wср.м", "Осадк.", "Ветер", "Vветр.макс", "Vветр.ср"]
        self.table.setRowCount(len(cities))
        self.table.setHorizontalHeaderLabels(head)
        for i, c in enumerate(cities):
            for j in range(20):
                self.table.setItem(i, j, QTableWidgetItem(str(c[j])))

    def btnClosed(self):
        self.close()
