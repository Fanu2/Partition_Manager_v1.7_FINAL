from fractions import Fraction

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QInputDialog,
    QLabel
)

from PySide6.QtCore import Qt

from database.db import SessionLocal
from database.models import Owner

from services.area_service import (
    AreaService
)


class OwnershipWidget(QWidget):

    def __init__(self):

        super().__init__()

        self.session = SessionLocal()

        self.total_area_marla = 0

        self.build_ui()

    # =====================================
    # UI
    # =====================================

    def build_ui(self):

        layout = QVBoxLayout()

        self.table = QTableWidget()

        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels(
            [
                "Owner ID",
                "Owner Name",
                "Numerator",
                "Denominator",
                "Share",
                "Area"
            ]
        )

        layout.addWidget(
            self.table
        )

        self.lbl_total_share = QLabel(
            "Total Share : 0"
        )

        layout.addWidget(
            self.lbl_total_share
        )

        buttons = QHBoxLayout()

        self.btn_add = QPushButton(
            "Add Owner"
        )

        self.btn_remove = QPushButton(
            "Remove Owner"
        )

        self.btn_validate = QPushButton(
            "Validate Shares"
        )

        buttons.addWidget(
            self.btn_add
        )

        buttons.addWidget(
            self.btn_remove
        )

        buttons.addWidget(
            self.btn_validate
        )

        layout.addLayout(
            buttons
        )

        self.setLayout(
            layout
        )

        self.btn_add.clicked.connect(
            self.add_owner
        )

        self.btn_remove.clicked.connect(
            self.remove_owner
        )

        self.btn_validate.clicked.connect(
            self.validate_shares
        )

        self.table.itemChanged.connect(
            self.recalculate_areas
        )

    # =====================================
    # TOTAL AREA
    # =====================================

    def set_total_area(
        self,
        total_area_marla
    ):

        self.total_area_marla = float(
            total_area_marla
        )

        self.recalculate_areas()

    # =====================================
    # ADD OWNER
    # =====================================

    def add_owner(self):

        owners = (
            self.session.query(
                Owner
            )
            .order_by(
                Owner.owner_name
            )
            .all()
        )

        if not owners:

            QMessageBox.warning(
                self,
                "Owners",
                "No owners available."
            )

            return

        names = [

            f"{o.id} - {o.owner_name}"

            for o in owners
        ]

        choice, ok = (
            QInputDialog.getItem(
                self,
                "Select Owner",
                "Owner",
                names,
                0,
                False
            )
        )

        if not ok:
            return

        owner_id = int(
            choice.split("-")[0]
            .strip()
        )

        for row in range(
            self.table.rowCount()
        ):

            existing = int(
                self.table.item(
                    row,
                    0
                ).text()
            )

            if existing == owner_id:

                QMessageBox.warning(
                    self,
                    "Duplicate",
                    "Owner already added."
                )

                return

        owner = self.session.get(
            Owner,
            owner_id
        )

        row = self.table.rowCount()

        self.table.insertRow(
            row
        )

        self.table.setItem(
            row,
            0,
            QTableWidgetItem(
                str(owner.id)
            )
        )

        self.table.setItem(
            row,
            1,
            QTableWidgetItem(
                owner.owner_name
            )
        )

        self.table.setItem(
            row,
            2,
            QTableWidgetItem("1")
        )

        self.table.setItem(
            row,
            3,
            QTableWidgetItem("1")
        )

        self.table.setItem(
            row,
            4,
            QTableWidgetItem("")
        )

        self.table.setItem(
            row,
            5,
            QTableWidgetItem("")
        )

        self.recalculate_areas()

    # =====================================
    # REMOVE OWNER
    # =====================================

    def remove_owner(self):

        row = self.table.currentRow()

        if row >= 0:

            self.table.removeRow(
                row
            )

        self.recalculate_areas()

    # =====================================
    # RECALCULATE
    # =====================================

    def recalculate_areas(self):

        total_share = Fraction(
            0,
            1
        )

        self.table.blockSignals(
            True
        )

        for row in range(
            self.table.rowCount()
        ):

            try:

                num = int(
                    self.table.item(
                        row,
                        2
                    ).text()
                )

                den = int(
                    self.table.item(
                        row,
                        3
                    ).text()
                )

                if den == 0:
                    continue

                share = Fraction(
                    num,
                    den
                )

                total_share += share

                self.table.setItem(
                    row,
                    4,
                    QTableWidgetItem(
                        str(share)
                    )
                )

                area = (
                    self.total_area_marla
                    * float(share)
                )

                area_text = (
                    AreaService
                    .format_area(
                        area
                    )
                )

                self.table.setItem(
                    row,
                    5,
                    QTableWidgetItem(
                        area_text
                    )
                )

            except:
                pass

        self.table.blockSignals(
            False
        )

        self.lbl_total_share.setText(
            f"Total Share : {total_share}"
        )

    # =====================================
    # VALIDATE
    # =====================================

    def validate_shares(self):

        total = Fraction(
            0,
            1
        )

        for row in range(
            self.table.rowCount()
        ):

            try:

                num = int(
                    self.table.item(
                        row,
                        2
                    ).text()
                )

                den = int(
                    self.table.item(
                        row,
                        3
                    ).text()
                )

                total += Fraction(
                    num,
                    den
                )

            except:
                pass

        if total == Fraction(
            1,
            1
        ):

            QMessageBox.information(
                self,
                "Valid",
                "Total share equals 1."
            )

        else:

            QMessageBox.warning(
                self,
                "Invalid",
                f"Total share is {total}"
            )

    # =====================================
    # EXPORT
    # =====================================

    def get_ownership_data(self):

        data = []

        for row in range(
            self.table.rowCount()
        ):

            data.append(
                {
                    "owner_id":
                    int(
                        self.table.item(
                            row,
                            0
                        ).text()
                    ),

                    "numerator":
                    int(
                        self.table.item(
                            row,
                            2
                        ).text()
                    ),

                    "denominator":
                    int(
                        self.table.item(
                            row,
                            3
                        ).text()
                    )
                }
            )

        return data

    # =====================================
    # CLEAR
    # =====================================

    def clear(self):

        self.table.setRowCount(0)

        self.lbl_total_share.setText(
            "Total Share : 0"
        )