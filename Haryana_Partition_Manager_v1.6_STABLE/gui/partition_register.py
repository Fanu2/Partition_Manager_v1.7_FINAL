
from PySide6.QtWidgets import QWidget,QVBoxLayout,QPushButton,QTableWidget,QTableWidgetItem
from database.db import SessionLocal
from database.models import PartitionEvent,Khewat,Owner

class PartitionRegister(QWidget):
    def __init__(self):
        super().__init__()
        self.session=SessionLocal()
        self.setWindowTitle("Partition Register")
        self.resize(1100,600)
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

    def owner_names(self, txt):
        if not txt:
            return ""
        names=[]
        for oid in str(txt).split(","):
            oid=oid.strip()
            if not oid:
                continue
            owner=self.session.get(Owner,int(oid))
            names.append(owner.owner_name if owner else oid)
        return ", ".join(names)

    def khewat_no(self, kid):
        k=self.session.get(Khewat,kid)
        return str(k.khewat_no) if k else str(kid)

    def load_data(self):
        events=self.session.query(PartitionEvent).order_by(PartitionEvent.id.desc()).all()
        self.table.setRowCount(len(events))
        for row,event in enumerate(events):
            vals=[
                event.id,
                self.khewat_no(event.source_khewat_id),
                self.khewat_no(event.new_khewat_id),
                self.owner_names(event.owners_removed),
                event.removed_area,
                event.partition_date
            ]
            for col,val in enumerate(vals):
                self.table.setItem(row,col,QTableWidgetItem(str(val)))
