
from PySide6.QtWidgets import QWidget,QVBoxLayout,QLineEdit,QPushButton,QTableWidget,QTableWidgetItem
from database.db import SessionLocal
from database.models import Owner,Khewat,Khasra

class SearchScreen(QWidget):

    def __init__(self):
        super().__init__()
        self.session = SessionLocal()

        self.setWindowTitle("Universal Search")
        self.resize(900,600)

        layout = QVBoxLayout()

        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Search Owner, Khewat or Khasra")

        self.btn_search = QPushButton("Search")

        self.table = QTableWidget(0,3)
        self.table.setHorizontalHeaderLabels(["Type","Match","Details"])

        layout.addWidget(self.txt_search)
        layout.addWidget(self.btn_search)
        layout.addWidget(self.table)

        self.setLayout(layout)

        self.btn_search.clicked.connect(self.search)

    def search(self):
        text = self.txt_search.text().strip()
        self.table.setRowCount(0)

        if not text:
            return

        for owner in self.session.query(Owner).filter(Owner.owner_name.contains(text)).all():
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row,0,QTableWidgetItem("Owner"))
            self.table.setItem(row,1,QTableWidgetItem(owner.owner_name or ""))
            self.table.setItem(row,2,QTableWidgetItem(str(owner.id)))

        for khewat in self.session.query(Khewat).filter(Khewat.khewat_no.contains(text)).all():
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row,0,QTableWidgetItem("Khewat"))
            self.table.setItem(row,1,QTableWidgetItem(khewat.khewat_no or ""))
            self.table.setItem(row,2,QTableWidgetItem(str(khewat.total_area)))

        for khasra in self.session.query(Khasra).filter(Khasra.khasra_no.contains(text)).all():
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row,0,QTableWidgetItem("Khasra"))
            self.table.setItem(row,1,QTableWidgetItem(khasra.khasra_no or ""))
            self.table.setItem(row,2,QTableWidgetItem(str(khasra.area)))
