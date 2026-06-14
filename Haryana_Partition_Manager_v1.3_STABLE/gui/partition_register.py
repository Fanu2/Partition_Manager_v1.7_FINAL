
from PySide6.QtWidgets import QWidget,QVBoxLayout,QPushButton,QTableWidget,QTableWidgetItem
from database.db import SessionLocal
from database.models import PartitionEvent

class PartitionRegister(QWidget):
    def __init__(self):
        super().__init__()
        self.session=SessionLocal()
        self.setWindowTitle("Partition Register")
        self.resize(1000,600)

        layout=QVBoxLayout()
        self.btn_refresh=QPushButton("Refresh")
        self.table=QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["ID","Source Khewat","New Khewat","Owners Removed","Area Removed","Date"]
        )

        layout.addWidget(self.btn_refresh)
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.btn_refresh.clicked.connect(self.load_data)
        self.load_data()

    def load_data(self):
        events=self.session.query(PartitionEvent).order_by(PartitionEvent.id.desc()).all()
        self.table.setRowCount(len(events))
        for row,event in enumerate(events):
            vals=[event.id,event.source_khewat_id,event.new_khewat_id,event.owners_removed,event.removed_area,event.partition_date]
            for col,val in enumerate(vals):
                self.table.setItem(row,col,QTableWidgetItem(str(val)))
