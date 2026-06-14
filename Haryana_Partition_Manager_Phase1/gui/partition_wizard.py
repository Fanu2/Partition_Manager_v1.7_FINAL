from fractions import Fraction

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QTextEdit
)

from PySide6.QtCore import Qt

from database.db import SessionLocal

from database.models import (
    Khewat,
    Ownership,
    Owner,
    PartitionEvent
)


class PartitionWizard(QWidget):

    def __init__(self):

        super().__init__()

        self.session = SessionLocal()

        self.setWindowTitle(
            "Partition Wizard"
        )

        self.resize(900, 700)

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
            "Load Owners"
        )

        layout.addWidget(
            self.btn_load
        )

        layout.addWidget(
            QLabel(
                "Select Owners To Separate"
            )
        )

        self.owner_list = QListWidget()

        layout.addWidget(
            self.owner_list
        )

        self.preview = QTextEdit()

        self.preview.setReadOnly(True)

        layout.addWidget(
            self.preview
        )

        self.btn_preview = QPushButton(
            "Preview Partition"
        )

        self.btn_execute = QPushButton(
            "Execute Partition"
        )

        layout.addWidget(
            self.btn_preview
        )

        layout.addWidget(
            self.btn_execute
        )

        self.setLayout(layout)

        self.btn_load.clicked.connect(
            self.load_owners
        )

        self.btn_preview.clicked.connect(
            self.preview_partition
        )

        self.btn_execute.clicked.connect(
            self.execute_partition
        )

    def load_khewats(self):

        self.cmb_khewat.clear()

        khewats = self.session.query(
            Khewat
        ).order_by(
            Khewat.khewat_no
        ).all()

        for khewat in khewats:

            self.cmb_khewat.addItem(
                str(khewat.khewat_no),
                khewat.id
            )

    def load_owners(self):

        self.owner_list.clear()

        khewat_id = (
            self.cmb_khewat.currentData()
        )

        if not khewat_id:
            return

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
                f"{owner.id} - {owner.owner_name}"
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

    def get_selected_owner_ids(self):

        owner_ids = []

        for row in range(
            self.owner_list.count()
        ):

            item = self.owner_list.item(
                row
            )

            if item.checkState() == Qt.Checked:

                owner_id = int(
                    item.text()
                    .split("-")[0]
                    .strip()
                )

                owner_ids.append(
                    owner_id
                )

        return owner_ids

    def preview_partition(self):

        khewat_id = (
            self.cmb_khewat.currentData()
        )

        if not khewat_id:

            QMessageBox.warning(
                self,
                "Error",
                "Select a Khewat."
            )

            return

        khewat = self.session.get(
            Khewat,
            khewat_id
        )

        if not khewat:

            QMessageBox.warning(
                self,
                "Error",
                "Khewat not found."
            )

            return

        selected_ids = (
            self.get_selected_owner_ids()
        )

        if not selected_ids:

            QMessageBox.warning(
                self,
                "Selection Required",
                "Select at least one owner."
            )

            return

        ownerships = (
            self.session.query(
                Ownership
            )
            .filter(
                Ownership.khewat_id == khewat_id
            )
            .all()
        )

        removed_share = Fraction(
            0,
            1
        )

        selected_owners = []

        for ownership in ownerships:

            if ownership.owner_id in selected_ids:

                removed_share += Fraction(
                    ownership.numerator,
                    ownership.denominator
                )

                owner = self.session.get(
                    Owner,
                    ownership.owner_id
                )

                if owner:
                    selected_owners.append(
                        owner.owner_name
                    )

        removed_area = (
            float(removed_share)
            * float(khewat.total_area)
        )

        remaining_area = (
            float(khewat.total_area)
            - removed_area
        )

        report = []

        report.append(
            f"Khewat No : {khewat.khewat_no}"
        )

        report.append(
            f"Total Area : {khewat.total_area}"
        )

        report.append("")

        report.append(
            "Owners Selected:"
        )

        for name in selected_owners:

            report.append(
                f"  • {name}"
            )

        report.append("")

        report.append(
            f"Removed Share : {removed_share}"
        )

        report.append(
            f"Removed Area : {removed_area:.2f}"
        )

        report.append(
            f"Remaining Area : {remaining_area:.2f}"
        )

        self.preview.setText(
            "\n".join(report)
        )

    def execute_partition(self):

        QMessageBox.information(
            self,
            "Phase 1",
            (
                "Partition preview completed.\n\n"
                "Automatic Khewat creation,\n"
                "ownership transfer,\n"
                "share recalculation,\n"
                "and partition history\n"
                "will be implemented next."
            )
        )

    def closeEvent(self, event):

        try:
            self.session.close()
        except:
            pass

        event.accept()