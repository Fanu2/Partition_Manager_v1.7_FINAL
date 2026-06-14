from gui.khewat_details import KhewatDetails

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTreeWidget,
    QTreeWidgetItem,
    QPushButton
)

from database.db import SessionLocal
from database.models import (
    PartitionEvent,
    Khewat,
    Owner
)


class KhewatHistory(QWidget):

    def __init__(self):

        super().__init__()

        self.session = SessionLocal()

        self.setWindowTitle(
            "Khewat History / Family Tree"
        )

        self.resize(
            1000,
            650
        )

        layout = QVBoxLayout()

        self.btn = QPushButton(
            "Refresh"
        )

        self.btn_details = QPushButton(
            "View Selected Khewat"
        )

        self.tree = QTreeWidget()

        self.tree.setHeaderLabels(
            ["Khewat / Owner / Area"]
        )

        layout.addWidget(self.btn)
        layout.addWidget(self.btn_details)
        layout.addWidget(self.tree)

        self.setLayout(layout)

        self.btn.clicked.connect(
            self.load_data
        )

        self.btn_details.clicked.connect(
            self.view_details
        )

        self.load_data()

    def owner_names(self, txt):

        if not txt:
            return ""

        names = []

        for oid in str(txt).split(","):

            oid = oid.strip()

            if not oid:
                continue

            try:

                owner = self.session.get(
                    Owner,
                    int(oid)
                )

                if owner:
                    names.append(
                        owner.owner_name
                    )

            except Exception:
                pass

        return ", ".join(names)

    def load_data(self):

        self.tree.clear()

        roots = {}

        events = (
            self.session.query(
                PartitionEvent
            ).all()
        )

        for e in events:

            src = self.session.get(
                Khewat,
                e.source_khewat_id
            )

            new = self.session.get(
                Khewat,
                e.new_khewat_id
            )

            if not src or not new:
                continue

            parent_no = str(
                src.khewat_no
            )

            if parent_no not in roots:

                root = QTreeWidgetItem(
                    [parent_no]
                )

                self.tree.addTopLevelItem(
                    root
                )

                roots[parent_no] = root

            owner_text = self.owner_names(
                e.owners_removed
            )

            child_text = (
                f"{new.khewat_no} | "
                f"{owner_text} | "
                f"Area {e.removed_area}"
            )

            child = QTreeWidgetItem(
                [child_text]
            )

            roots[parent_no].addChild(
                child
            )

        self.tree.expandAll()

    def view_details(self):

        item = self.tree.currentItem()

        if not item:
            print("No item selected")
            return

        if not item.parent():
            print("Please select a child Khewat")
            return

        khewat_no = (
            item.text(0)
            .split("|")[0]
            .strip()
        )

        print(
            "Selected Khewat:",
            khewat_no
        )

        k = (
            self.session.query(Khewat)
            .filter_by(
                khewat_no=khewat_no
            )
            .first()
        )

        if not k:
            print(
                "Khewat not found"
            )
            return

        self.details = KhewatDetails(
            k.id
        )

        self.details.show()
