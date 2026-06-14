from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QLabel,
    QLineEdit,
    QMessageBox,
    QFormLayout,
    QDialog,
    QHeaderView
)

from database.db import SessionLocal
from database.models import Owner


# =====================================================
# OWNER DIALOG
# =====================================================

class OwnerDialog(QDialog):

    def __init__(self, owner=None, parent=None):

        super().__init__(parent)

        self.owner = owner

        self.setWindowTitle(
            "Owner Details"
        )

        self.resize(600, 300)

        layout = QFormLayout()

        self.name_edit = QLineEdit()
        self.father_edit = QLineEdit()
        self.address_edit = QLineEdit()
        self.mobile_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.remarks_edit = QLineEdit()

        if owner:

            self.name_edit.setText(
                owner.owner_name or ""
            )

            self.father_edit.setText(
                owner.father_name or ""
            )

            self.address_edit.setText(
                owner.address or ""
            )

            self.mobile_edit.setText(
                owner.mobile or ""
            )

            self.email_edit.setText(
                owner.email or ""
            )

            self.remarks_edit.setText(
                owner.remarks or ""
            )

        layout.addRow(
            "Owner Name",
            self.name_edit
        )

        layout.addRow(
            "Father Name",
            self.father_edit
        )

        layout.addRow(
            "Address",
            self.address_edit
        )

        layout.addRow(
            "Mobile",
            self.mobile_edit
        )

        layout.addRow(
            "Email",
            self.email_edit
        )

        layout.addRow(
            "Remarks",
            self.remarks_edit
        )

        btn_save = QPushButton(
            "Save"
        )

        btn_save.clicked.connect(
            self.accept
        )

        layout.addWidget(
            btn_save
        )

        self.setLayout(layout)

    def get_data(self):

        return {
            "owner_name":
                self.name_edit.text().strip(),

            "father_name":
                self.father_edit.text().strip(),

            "address":
                self.address_edit.text().strip(),

            "mobile":
                self.mobile_edit.text().strip(),

            "email":
                self.email_edit.text().strip(),

            "remarks":
                self.remarks_edit.text().strip()
        }


# =====================================================
# OWNER SCREEN
# =====================================================

class OwnerScreen(QWidget):

    def __init__(self):

        super().__init__()

        self.session = SessionLocal()

        self.setWindowTitle(
            "Owner Management"
        )

        self.resize(1200, 700)

        self.build_ui()

        self.load_data()

    # =================================================

    def build_ui(self):

        main_layout = QVBoxLayout()

        search_layout = QHBoxLayout()

        lbl_search = QLabel(
            "Search"
        )

        self.search_edit = QLineEdit()

        self.search_edit.setPlaceholderText(
            "Owner Name..."
        )

        btn_search = QPushButton(
            "Search"
        )

        btn_refresh = QPushButton(
            "Refresh"
        )

        search_layout.addWidget(
            lbl_search
        )

        search_layout.addWidget(
            self.search_edit
        )

        search_layout.addWidget(
            btn_search
        )

        search_layout.addWidget(
            btn_refresh
        )

        main_layout.addLayout(
            search_layout
        )

        self.table = QTableWidget()

        self.table.setColumnCount(7)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Owner Name",
            "Father Name",
            "Address",
            "Mobile",
            "Email",
            "Remarks"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.doubleClicked.connect(
            self.edit_owner
        )

        main_layout.addWidget(
            self.table
        )

        button_layout = QHBoxLayout()

        btn_add = QPushButton(
            "Add Owner"
        )

        btn_edit = QPushButton(
            "Edit Owner"
        )

        btn_delete = QPushButton(
            "Delete Owner"
        )

        button_layout.addWidget(
            btn_add
        )

        button_layout.addWidget(
            btn_edit
        )

        button_layout.addWidget(
            btn_delete
        )

        main_layout.addLayout(
            button_layout
        )

        self.setLayout(
            main_layout
        )

        btn_add.clicked.connect(
            self.add_owner
        )

        btn_edit.clicked.connect(
            self.edit_owner
        )

        btn_delete.clicked.connect(
            self.delete_owner
        )

        btn_search.clicked.connect(
            self.search_owner
        )

        btn_refresh.clicked.connect(
            self.load_data
        )

    # =================================================

    def load_data(self):

        owners = (
            self.session.query(Owner)
            .order_by(
                Owner.owner_name
            )
            .all()
        )

        self.populate_table(
            owners
        )

    # =================================================

    def populate_table(self, owners):

        self.table.setRowCount(
            len(owners)
        )

        for row, owner in enumerate(
            owners
        ):

            values = [
                str(owner.id),
                owner.owner_name or "",
                owner.father_name or "",
                owner.address or "",
                owner.mobile or "",
                owner.email or "",
                owner.remarks or ""
            ]

            for col, value in enumerate(values):

                item = QTableWidgetItem(
                    value
                )

                self.table.setItem(
                    row,
                    col,
                    item
                )

    # =================================================

    def add_owner(self):

        dlg = OwnerDialog()

        if not dlg.exec():
            return

        data = dlg.get_data()

        if not data["owner_name"]:

            QMessageBox.warning(
                self,
                "Validation",
                "Owner Name Required"
            )

            return

        existing = (
            self.session.query(Owner)
            .filter(
                Owner.owner_name
                == data["owner_name"]
            )
            .first()
        )

        if existing:

            QMessageBox.warning(
                self,
                "Duplicate",
                "Owner already exists."
            )

            return

        owner = Owner(**data)

        self.session.add(
            owner
        )

        self.session.commit()

        self.load_data()

    # =================================================

    def edit_owner(self):

        row = self.table.currentRow()

        if row < 0:
            return

        owner_id = int(
            self.table.item(
                row,
                0
            ).text()
        )

        owner = self.session.get(
            Owner,
            owner_id
        )

        if not owner:
            return

        dlg = OwnerDialog(
            owner
        )

        if not dlg.exec():
            return

        data = dlg.get_data()

        owner.owner_name = data["owner_name"]
        owner.father_name = data["father_name"]
        owner.address = data["address"]
        owner.mobile = data["mobile"]
        owner.email = data["email"]
        owner.remarks = data["remarks"]

        self.session.commit()

        self.load_data()

    # =================================================

    def delete_owner(self):

        row = self.table.currentRow()

        if row < 0:
            return

        owner_id = int(
            self.table.item(
                row,
                0
            ).text()
        )

        owner = self.session.get(
            Owner,
            owner_id
        )

        if not owner:
            return

        if owner.ownerships:

            QMessageBox.warning(
                self,
                "Cannot Delete",
                "Owner is linked to one or more Khewats."
            )

            return

        reply = QMessageBox.question(
            self,
            "Delete Owner",
            f"Delete {owner.owner_name} ?"
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        self.session.delete(
            owner
        )

        self.session.commit()

        self.load_data()

    # =================================================

    def search_owner(self):

        text = (
            self.search_edit.text()
            .strip()
        )

        if not text:

            self.load_data()

            return

        owners = (
            self.session.query(Owner)
            .filter(
                Owner.owner_name.contains(
                    text
                )
            )
            .order_by(
                Owner.owner_name
            )
            .all()
        )

        self.populate_table(
            owners
        )

    # =================================================

    def closeEvent(self, event):

        try:
            self.session.close()
        except:
            pass

        event.accept()