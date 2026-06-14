
from PySide6.QtWidgets import QWidget,QVBoxLayout,QPushButton,QFileDialog,QMessageBox
from database.db import SessionLocal
from database.models import Owner,Khewat,Khasra
import pandas as pd

class ExportScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.session=SessionLocal()
        self.setWindowTitle("Excel Export")
        self.resize(300,200)
        layout=QVBoxLayout()
        self.b1=QPushButton("Export Owners")
        self.b2=QPushButton("Export Khewats")
        self.b3=QPushButton("Export Khasras")
        for b in (self.b1,self.b2,self.b3):
            layout.addWidget(b)
        self.setLayout(layout)
        self.b1.clicked.connect(self.export_owners)
        self.b2.clicked.connect(self.export_khewats)
        self.b3.clicked.connect(self.export_khasras)

    def save_df(self,df,name):
        fn,_=QFileDialog.getSaveFileName(self,"Save Excel",name,"Excel Files (*.xlsx)")
        if not fn:
            return
        df.to_excel(fn,index=False)
        QMessageBox.information(self,"Success",f"Saved: {fn}")

    def export_owners(self):
        rows=self.session.query(Owner).all()
        self.save_df(pd.DataFrame([{"ID":r.id,"Owner":getattr(r,"owner_name","")} for r in rows]),"owners.xlsx")

    def export_khewats(self):
        rows=self.session.query(Khewat).all()
        self.save_df(pd.DataFrame([{"ID":r.id,"Khewat":getattr(r,"khewat_no",""),"Area":getattr(r,"total_area","")} for r in rows]),"khewats.xlsx")

    def export_khasras(self):
        rows=self.session.query(Khasra).all()
        self.save_df(pd.DataFrame([{"ID":r.id,"Khasra":getattr(r,"khasra_no",""),"Area":getattr(r,"area","")} for r in rows]),"khasras.xlsx")
