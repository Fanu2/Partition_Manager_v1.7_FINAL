
from PySide6.QtWidgets import QWidget,QVBoxLayout,QTreeWidget,QTreeWidgetItem,QPushButton
from database.db import SessionLocal
from database.models import PartitionEvent,Khewat,Owner

class KhewatHistory(QWidget):
    def __init__(self):
        super().__init__()
        self.session=SessionLocal()
        self.setWindowTitle("Khewat History / Family Tree")
        self.resize(1000,650)
        layout=QVBoxLayout()
        self.btn=QPushButton("Refresh")
        self.tree=QTreeWidget()
        self.tree.setHeaderLabels(["Khewat / Owner / Area"])
        layout.addWidget(self.btn)
        layout.addWidget(self.tree)
        self.setLayout(layout)
        self.btn.clicked.connect(self.load_data)
        self.load_data()

    def owner_names(self, txt):
        if not txt:
            return ""
        names=[]
        for oid in str(txt).split(","):
            oid=oid.strip()
            if not oid:
                continue
            try:
                owner=self.session.get(Owner,int(oid))
                if owner:
                    names.append(owner.owner_name)
            except:
                pass
        return ", ".join(names)

    def load_data(self):
        self.tree.clear()
        roots={}
        events=self.session.query(PartitionEvent).all()

        for e in events:
            src=self.session.get(Khewat,e.source_khewat_id)
            new=self.session.get(Khewat,e.new_khewat_id)

            if not src or not new:
                continue

            parent_no=str(src.khewat_no)

            if parent_no not in roots:
                root=QTreeWidgetItem([parent_no])
                self.tree.addTopLevelItem(root)
                roots[parent_no]=root

            owner_text=self.owner_names(e.owners_removed)
            child_text=f"{new.khewat_no} | {owner_text} | Area {e.removed_area}"

            child=QTreeWidgetItem([child_text])
            roots[parent_no].addChild(child)

        self.tree.expandAll()
