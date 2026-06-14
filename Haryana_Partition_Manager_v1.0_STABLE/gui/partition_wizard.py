from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox,
    QComboBox,
    QLineEdit,
    QListWidget,
    QListWidgetItem
)

from PySide6.QtCore import Qt

from database.db import SessionLocal

from database.models import (
    Khewat,
    Ownership,
    Owner,
    Khasra
)

from services.partition_engine import (
    PartitionEngine
)


class PartitionWizard(QWidget):

    def __init__(self):

        super().__init__()

        self.session = SessionLocal()

        self.setWindowTitle(
            "Partition Wizard"
        )

        self.resize(
            1000,
            800
        )

        self.build_ui()

        self.load_khewats()

    def build_ui(self):

        layout = QVBoxLayout()

        layout.addWidget(
            QLabel("Select Khewat")
        )

        self.cmb_khewat = QComboBox()

        layout.addWidget(
            self.cmb_khewat
        )

        self.btn_load = QPushButton(
            "Load Data"
        )

        layout.addWidget(
            self.btn_load
        )

        layout.addWidget(
            QLabel("New Khewat Number")
        )

        self.txt_new_khewat = QLineEdit()

        layout.addWidget(
            self.txt_new_khewat
        )

        layout.addWidget(
            QLabel("New Khatauni Number")
        )

        self.txt_new_khatauni = QLineEdit()

        layout.addWidget(
            self.txt_new_khatauni
        )

        layout.addWidget(
            QLabel("Owners To Separate")
        )

        self.owner_list = QListWidget()

        layout.addWidget(
            self.owner_list
        )

        layout.addWidget(
            QLabel("Khasras To Transfer")
        )

        self.khasra_list = QListWidget()

        layout.addWidget(
            self.khasra_list
        )

        self.btn_preview = QPushButton(
            "Preview Partition"
        )

        layout.addWidget(
            self.btn_preview
        )

        self.btn_execute = QPushButton(
            "Execute Partition"
        )

        layout.addWidget(
            self.btn_execute
        )

        self.setLayout(
            layout
        )

        self.btn_load.clicked.connect(
            self.load_partition_data
        )

        self.btn_preview.clicked.connect(
            self.preview_partition
        )

        self.btn_execute.clicked.connect(
            self.execute_partition
        )

    def load_khewats(self):

        self.cmb_khewat.clear()

        khewats = (
            self.session.query(Khewat)
            .order_by(Khewat.khewat_no)
            .all()
        )

        for khewat in khewats:

            self.cmb_khewat.addItem(
                str(khewat.khewat_no),
                khewat.id
            )

    def load_partition_data(self):

        self.owner_list.clear()

        self.khasra_list.clear()

        khewat_id = (
            self.cmb_khewat.currentData()
        )

        ownerships = (
            self.session.query(
                Ownership
            )
            .filter(
                Ownership.khewat_id == khewat_id
            )
            .all()
        )

        for ownership in ownerships:

            owner = self.session.get(
                Owner,
                ownership.owner_id
            )

            if not owner:
                continue

            item = QListWidgetItem(
                f"{owner.owner_name} "
                f"({ownership.numerator}/"
                f"{ownership.denominator})"
            )

            item.setData(
                Qt.UserRole,
                owner.id
            )

            item.setFlags(
                item.flags()
                | Qt.ItemIsUserCheckable
            )

            item.setCheckState(
                Qt.Unchecked
            )

            self.owner_list.addItem(
                item
            )

        khasras = (
            self.session.query(
                Khasra
            )
            .filter(
                Khasra.khewat_id == khewat_id
            )
            .all()
        )

        for khasra in khasras:

            item = QListWidgetItem(
                f"{khasra.khasra_no} "
                f"({khasra.area})"
            )

            item.setData(
                Qt.UserRole,
                khasra.id
            )

            item.setFlags(
                item.flags()
                | Qt.ItemIsUserCheckable
            )

            item.setCheckState(
                Qt.Unchecked
            )

            self.khasra_list.addItem(
                item
            )

        QMessageBox.information(
            self,
            "Loaded",
            (
                f"Owners: {len(ownerships)}\n"
                f"Khasras: {len(khasras)}"
            )
        )

    def get_selected_owner_ids(self):

        result = []

        for row in range(
            self.owner_list.count()
        ):

            item = self.owner_list.item(
                row
            )

            if item.checkState() == Qt.Checked:

                result.append(
                    item.data(
                        Qt.UserRole
                    )
                )

        return result

    def get_selected_khasra_ids(self):

        result = []

        for row in range(
            self.khasra_list.count()
        ):

            item = self.khasra_list.item(
                row
            )

            if item.checkState() == Qt.Checked:

                result.append(
                    item.data(
                        Qt.UserRole
                    )
                )

        return result

    def preview_partition(self):

        owners = (
            self.get_selected_owner_ids()
        )

        khasras = (
            self.get_selected_khasra_ids()
        )

        QMessageBox.information(
            self,
            "Preview",
            (
                f"Selected Owners: {len(owners)}\n\n"
                f"Selected Khasras: {len(khasras)}"
            )
        )

    def execute_partition(self):

        try:

            new_khewat_no = (
                self.txt_new_khewat.text()
                .strip()
            )

            if not new_khewat_no:

                QMessageBox.warning(
                    self,
                    "Error",
                    "Enter New Khewat Number."
                )

                return

            new_khatauni_no = (
                self.txt_new_khatauni.text()
                .strip()
            )

            owner_ids = (
                self.get_selected_owner_ids()
            )

            khasra_ids = (
                self.get_selected_khasra_ids()
            )

            if not owner_ids:

                QMessageBox.warning(
                    self,
                    "Error",
                    "Select Owners."
                )

                return

            if not khasra_ids:

                QMessageBox.warning(
                    self,
                    "Error",
                    "Select Khasras."
                )

                return

            result = (
                PartitionEngine.partition(
                    source_khewat_id=
                    self.cmb_khewat.currentData(),

                    selected_owner_ids=
                    owner_ids,

                    selected_khasra_ids=
                    khasra_ids,

                    new_khewat_no=
                    new_khewat_no,

                    new_khatauni_no=
                    new_khatauni_no
                )
            )

            QMessageBox.information(
                self,
                "Success",
                (
                    f"Partition Completed\n\n"
                    f"New Khewat : "
                    f"{result['khewat_no']}"
                )
            )

            self.load_khewats()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Partition Error",
                str(e)
            )

    def closeEvent(self, event):

        try:
            self.session.close()

        except Exception:
            pass

        event.accept()