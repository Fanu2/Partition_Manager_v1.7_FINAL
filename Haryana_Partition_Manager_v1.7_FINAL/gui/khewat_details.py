
from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QTextEdit
from database.db import SessionLocal
from database.models import Khewat,Ownership,Khasra

class KhewatDetails(QWidget):
    def __init__(self,khewat_id):
        super().__init__()
        self.session=SessionLocal()
        self.setWindowTitle("Khewat Details")
        self.resize(700,500)

        layout=QVBoxLayout()
        self.info=QTextEdit()
        self.info.setReadOnly(True)
        layout.addWidget(self.info)
        self.setLayout(layout)

        k=self.session.get(Khewat,khewat_id)
        if not k:
            self.info.setText("Khewat not found")
            return

        txt=[]
        txt.append(f"Khewat No: {k.khewat_no}")
        txt.append(f"Khatauni No: {k.khatauni_no}")
        txt.append(f"Area: {k.total_area}")
        txt.append("")
        txt.append("OWNERS")
        for o in self.session.query(Ownership).filter_by(khewat_id=k.id):
            txt.append(f"{o.owner.owner_name} ({o.numerator}/{o.denominator})")
        txt.append("")
        txt.append("KHASRAS")
        for kh in self.session.query(Khasra).filter_by(khewat_id=k.id):
            txt.append(f"{kh.khasra_no} ({kh.area})")

        self.info.setText("\n".join(txt))
