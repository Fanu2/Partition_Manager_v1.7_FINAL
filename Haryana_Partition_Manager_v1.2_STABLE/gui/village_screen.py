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
    QDialog
)

from database.db import SessionLocal
from database.models import Village


class VillageDialog(QDialog):

    def __init__(
        self,
        village=None,
        parent=None
    ):

        super().__init__(parent)

        self.village = village

        self.setWindowTitle(
            "Village Details"
        )

        self.resize(
            600,
            350
        )

        layout = QFormLayout()

        self.district_edit = QLineEdit()

        self.tehsil_edit = QLineEdit()

        self.sub_tehsil_edit = QLineEdit()

        self.village_name_edit = QLineEdit()

        self.hadbast_edit = QLineEdit()

        self.jamabandi_edit = QLineEdit()

        if village:

            self.district_edit.setText(
                village.district or ""
            )

            self.tehsil_edit.setText(
                village.tehsil or ""
            )

            self.sub_tehsil_edit.setText(
                village.sub_tehsil or ""
            )

            self.village_name_edit.setText(
                village.village_name or ""
            )

            self.hadbast_edit.setText(
                village.hadbast_no or ""
            )

            self.jamabandi_edit.setText(
                village.jamabandi_year or ""
            )

        layout.addRow(
            "District",
            self.district_edit
        )

        layout.addRow(
            "Tehsil",
            self.tehsil_edit
        )

        layout.addRow(
            "Sub Tehsil",
            self.sub_tehsil_edit
        )

        layout.addRow(
            "Village Name",
            self.village_name_edit
        )

        layout.addRow(
            "Hadbast No",
            self.hadbast_edit
        )

        layout.addRow(
            "Jamabandi Year",
            self.jamabandi_edit
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

        self.setLayout(
            layout
        )

    def get_data(self):

        return {

            "district":
                self.district_edit.text().strip(),

            "tehsil":
                self.tehsil_edit.text().strip(),

            "sub_tehsil":
                self.sub_tehsil_edit.text().strip(),

            "village_name":
                self.village_name_edit.text().strip(),

            "hadbast_no":
                self.hadbast_edit.text().strip(),

            "jamabandi_year":
                self.jamabandi_edit.text().strip()
        }


class VillageScreen(QWidget):

    def __init__(self):

        super().__init__()

        self.session = SessionLocal()

        self.setWindowTitle(
            "Village Management"
        )

        self.resize(
            1300,
            700
        )

        self.build_ui()

        self.load_data()

    def build_ui(self):

        main_layout = QVBoxLayout()

        search_layout = QHBoxLayout()

        search_layout.addWidget(
            QLabel("Search")
        )

        self.search_edit = QLineEdit()

        self.search_edit.setPlaceholderText(
            "Village name..."
        )

        btn_search = QPushButton(
            "Search"
        )

        btn_refresh = QPushButton(
            "Refresh"
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

        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "District",
                "Tehsil",
                "Sub Tehsil",
                "Village",
                "Hadbast",
                "Jamabandi"
            ]
        )

        main_layout.addWidget(
            self.table
        )

        button_layout = QHBoxLayout()

        btn_add = QPushButton(
            "Add Village"
        )

        btn_edit = QPushButton(
            "Edit Village"
        )

        btn_delete = QPushButton(
            "Delete Village"
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
            self.add_village
        )

        btn_edit.clicked.connect(
            self.edit_village
        )

        btn_delete.clicked.connect(
            self.delete_village
        )

        btn_search.clicked.connect(
            self.search_village
        )

        btn_refresh.clicked.connect(
            self.load_data
        )

        self.table.doubleClicked.connect(
            self.edit_village
        )

    def load_data(self):

        villages = (
            self.session.query(
                Village
            )
            .order_by(
                Village.village_name
            )
            .all()
        )

        self.populate_table(
            villages
        )

    def populate_table(
        self,
        villages
    ):

        self.table.setRowCount(
            len(villages)
        )

        for row, village in enumerate(villages):

            values = [

                str(village.id),

                village.district or "",

                village.tehsil or "",

                village.sub_tehsil or "",

                village.village_name or "",

                village.hadbast_no or "",

                village.jamabandi_year or ""
            ]

            for col, value in enumerate(values):

                self.table.setItem(
                    row,
                    col,
                    QTableWidgetItem(
                        value
                    )
                )

        self.table.resizeColumnsToContents()

    def add_village(self):

        dlg = VillageDialog()

        if dlg.exec():

            data = dlg.get_data()

            if not data["village_name"]:

                QMessageBox.warning(
                    self,
                    "Validation",
                    "Village name required."
                )

                return

            village = Village(
                **data
            )

            self.session.add(
                village
            )

            self.session.commit()

            self.load_data()

    def edit_village(self):

        row = self.table.currentRow()

        if row < 0:
            return

        village_id = int(
            self.table.item(
                row,
                0
            ).text()
        )

        village = self.session.get(
            Village,
            village_id
        )

        dlg = VillageDialog(
            village
        )

        if dlg.exec():

            data = dlg.get_data()

            for key, value in data.items():

                setattr(
                    village,
                    key,
                    value
                )

            self.session.commit()

            self.load_data()

    def delete_village(self):

        row = self.table.currentRow()

        if row < 0:
            return

        village_id = int(
            self.table.item(
                row,
                0
            ).text()
        )

        village = self.session.get(
            Village,
            village_id
        )

        reply = QMessageBox.question(
            self,
            "Delete",
            f"Delete {village.village_name} ?"
        )

        if reply == QMessageBox.StandardButton.Yes:

            self.session.delete(
                village
            )

            self.session.commit()

            self.load_data()

    def search_village(self):

        text = (
            self.search_edit.text()
            .strip()
        )

        villages = (
            self.session.query(
                Village
            )
            .filter(
                Village.village_name.contains(
                    text
                )
            )
            .all()
        )

        self.populate_table(
            villages
        )

    def closeEvent(
        self,
        event
    ):

        try:
            self.session.close()
        except:
            pass

        event.accept()