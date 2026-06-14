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

from services.area_service import AreaService


class KhasraWidget(QWidget):

    def __init__(self):

        super().__init__()

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout()

        self.table = QTableWidget()

        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels(
            [
                "Khasra No",
                "Kanal",
                "Marla",
                "Total Marla"
            ]
        )

        layout.addWidget(
            self.table
        )

        buttons = QHBoxLayout()

        self.btn_add = QPushButton(
            "Add Khasra"
        )

        self.btn_remove = QPushButton(
            "Remove Khasra"
        )

        self.btn_total = QPushButton(
            "Show Total Area"
        )

        buttons.addWidget(
            self.btn_add
        )

        buttons.addWidget(
            self.btn_remove
        )

        buttons.addWidget(
            self.btn_total
        )

        layout.addLayout(
            buttons
        )

        self.lbl_total = QLabel(
            "Total Area : 0K-0M"
        )

        layout.addWidget(
            self.lbl_total
        )

        self.setLayout(layout)

        self.btn_add.clicked.connect(
            self.add_khasra
        )

        self.btn_remove.clicked.connect(
            self.remove_khasra
        )

        self.btn_total.clicked.connect(
            self.show_total
        )

    # =====================================
    # ADD KHASRA
    # =====================================

    def add_khasra(self):

        khasra_no, ok = (
            QInputDialog.getText(
                self,
                "Khasra Number",
                "Enter Khasra Number"
            )
        )

        if not ok:
            return

        khasra_no = khasra_no.strip()

        if not khasra_no:
            return

        kanal, ok = (
            QInputDialog.getInt(
                self,
                "Kanal",
                "Enter Kanal",
                0,
                0,
                100000
            )
        )

        if not ok:
            return

        marla, ok = (
            QInputDialog.getDouble(
                self,
                "Marla",
                "Enter Marla",
                0,
                0,
                19.99,
                2
            )
        )

        if not ok:
            return

        total_marla = (
            AreaService
            .kanal_marla_to_marla(
                kanal,
                marla
            )
        )

        row = self.table.rowCount()

        self.table.insertRow(
            row
        )

        self.table.setItem(
            row,
            0,
            QTableWidgetItem(
                khasra_no
            )
        )

        self.table.setItem(
            row,
            1,
            QTableWidgetItem(
                str(kanal)
            )
        )

        self.table.setItem(
            row,
            2,
            QTableWidgetItem(
                str(marla)
            )
        )

        self.table.setItem(
            row,
            3,
            QTableWidgetItem(
                str(total_marla)
            )
        )

        self.update_total()

    # =====================================
    # REMOVE KHASRA
    # =====================================

    def remove_khasra(self):

        row = self.table.currentRow()

        if row >= 0:

            self.table.removeRow(
                row
            )

        self.update_total()

    # =====================================
    # TOTAL AREA
    # =====================================

    def get_total_area(self):

        total = 0

        for row in range(
            self.table.rowCount()
        ):

            try:

                total += float(
                    self.table.item(
                        row,
                        3
                    ).text()
                )

            except:
                pass

        return total

    # =====================================
    # UPDATE TOTAL LABEL
    # =====================================

    def update_total(self):

        total = self.get_total_area()

        self.lbl_total.setText(

            "Total Area : "
            + AreaService.format_area(
                total
            )
        )

    # =====================================
    # SHOW TOTAL
    # =====================================

    def show_total(self):

        total = self.get_total_area()

        QMessageBox.information(

            self,

            "Total Area",

            AreaService.format_area(
                total
            )
        )

    # =====================================
    # EXPORT DATA
    # =====================================

    def get_khasra_data(self):

        data = []

        for row in range(
            self.table.rowCount()
        ):

            data.append(

                {
                    "khasra_no":
                    self.table.item(
                        row,
                        0
                    ).text(),

                    "area":
                    float(
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

        self.table.setRowCount(
            0
        )

        self.update_total()