from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QMessageBox,
    QTabWidget,
    QTextEdit
)

from database.db import SessionLocal

from database.models import (
    Village
)

from widgets.ownership_widget import (
    OwnershipWidget
)

from widgets.khasra_widget import (
    KhasraWidget
)

from services.area_service import (
    AreaService
)

from services.khewat_service import (
    KhewatService
)


class KhewatScreen(QWidget):

    def __init__(self):

        super().__init__()

        self.session = SessionLocal()

        self.setWindowTitle(
            "Khewat Management"
        )

        self.resize(
            1400,
            900
        )

        self.build_ui()

        self.load_villages()

    # =====================================
    # BUILD UI
    # =====================================

    def build_ui(self):

        layout = QVBoxLayout()

        # -----------------------------
        # Village
        # -----------------------------

        layout.addWidget(
            QLabel("Village")
        )

        self.cmb_village = QComboBox()

        layout.addWidget(
            self.cmb_village
        )

        # -----------------------------
        # Khewat No
        # -----------------------------

        layout.addWidget(
            QLabel("Khewat Number")
        )

        self.txt_khewat = QLineEdit()

        layout.addWidget(
            self.txt_khewat
        )

        # -----------------------------
        # Khatauni No
        # -----------------------------

        layout.addWidget(
            QLabel("Khatauni Number")
        )

        self.txt_khatauni = QLineEdit()

        layout.addWidget(
            self.txt_khatauni
        )

        # -----------------------------
        # Area
        # -----------------------------

        area_layout = QHBoxLayout()

        area_layout.addWidget(
            QLabel("Kanal")
        )

        self.txt_kanal = QLineEdit()

        self.txt_kanal.setReadOnly(
            True
        )

        area_layout.addWidget(
            self.txt_kanal
        )

        area_layout.addWidget(
            QLabel("Marla")
        )

        self.txt_marla = QLineEdit()

        self.txt_marla.setReadOnly(
            True
        )

        area_layout.addWidget(
            self.txt_marla
        )

        layout.addLayout(
            area_layout
        )

        # -----------------------------
        # Tabs
        # -----------------------------

        self.tabs = QTabWidget()

        self.ownership_widget = (
            OwnershipWidget()
        )

        self.khasra_widget = (
            KhasraWidget()
        )

        self.tabs.addTab(
            self.ownership_widget,
            "Ownership"
        )

        self.tabs.addTab(
            self.khasra_widget,
            "Khasras"
        )

        layout.addWidget(
            self.tabs
        )

        # -----------------------------
        # Summary
        # -----------------------------

        layout.addWidget(
            QLabel(
                "Khewat Summary"
            )
        )

        self.summary = QTextEdit()

        self.summary.setReadOnly(
            True
        )

        layout.addWidget(
            self.summary
        )

        # -----------------------------
        # Buttons
        # -----------------------------

        button_layout = QHBoxLayout()

        self.btn_refresh = QPushButton(
            "Refresh Area"
        )

        self.btn_save = QPushButton(
            "Save Khewat"
        )

        self.btn_clear = QPushButton(
            "Clear"
        )

        button_layout.addWidget(
            self.btn_refresh
        )

        button_layout.addWidget(
            self.btn_save
        )

        button_layout.addWidget(
            self.btn_clear
        )

        layout.addLayout(
            button_layout
        )

        self.setLayout(
            layout
        )

        # -----------------------------
        # Signals
        # -----------------------------

        self.btn_refresh.clicked.connect(
            self.refresh_area
        )

        self.btn_save.clicked.connect(
            self.save_khewat
        )

        self.btn_clear.clicked.connect(
            self.clear_form
        )

    # =====================================
    # LOAD VILLAGES
    # =====================================

    def load_villages(self):

        self.cmb_village.clear()

        villages = (
            self.session.query(
                Village
            ).order_by(
                Village.village_name
            ).all()
        )

        for village in villages:

            self.cmb_village.addItem(
                village.village_name,
                village.id
            )

    # =====================================
    # REFRESH AREA
    # =====================================

    def refresh_area(self):

        try:

            total_area = (
                self.khasra_widget
                .get_total_area()
            )

            kanal, marla = (
                AreaService
                .marla_to_kanal_marla(
                    total_area
                )
            )

            self.txt_kanal.setText(
                str(kanal)
            )

            self.txt_marla.setText(
                str(marla)
            )

            self.ownership_widget.set_total_area(
                total_area
            )

            self.update_summary()

        except Exception as e:

            QMessageBox.warning(
                self,
                "Area Error",
                str(e)
            )

    # =====================================
    # SUMMARY
    # =====================================

    def update_summary(self):

        total_area = (
            self.khasra_widget
            .get_total_area()
        )

        lines = []

        lines.append(
            "KHEWAT SUMMARY"
        )

        lines.append("")

        lines.append(
            f"Khewat No : "
            f"{self.txt_khewat.text()}"
        )

        lines.append(
            f"Khatauni No : "
            f"{self.txt_khatauni.text()}"
        )

        lines.append("")

        lines.append(
            f"Total Area : "
            f"{AreaService.format_area(total_area)}"
        )

        lines.append(
            f"Total Owners : "
            f"{self.ownership_widget.table.rowCount()}"
        )

        lines.append(
            f"Total Khasras : "
            f"{self.khasra_widget.table.rowCount()}"
        )

        self.summary.setText(
            "\n".join(lines)
        )

    # =====================================
    # SAVE KHEWAT
    # =====================================

    def save_khewat(self):

        try:

            village_id = (
                self.cmb_village.currentData()
            )

            if not village_id:

                raise ValueError(
                    "Select a village."
                )

            total_area = (
                self.khasra_widget
                .get_total_area()
            )

            if total_area <= 0:

                raise ValueError(
                    "Add khasras first."
                )

            KhewatService.create_khewat(

                village_id=village_id,

                khewat_no=
                self.txt_khewat.text().strip(),

                khatauni_no=
                self.txt_khatauni.text().strip(),

                total_area=total_area,

                ownerships=
                self.ownership_widget
                .get_ownership_data(),

                khasras=
                self.khasra_widget
                .get_khasra_data(),

                status="JOINT",

                remarks=""
            )

            QMessageBox.information(
                self,
                "Success",
                "Khewat saved successfully."
            )

            self.clear_form()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )

    # =====================================
    # CLEAR
    # =====================================

    def clear_form(self):

        self.txt_khewat.clear()

        self.txt_khatauni.clear()

        self.txt_kanal.clear()

        self.txt_marla.clear()

        self.summary.clear()

        self.ownership_widget.clear()

        self.khasra_widget.clear()

    # =====================================
    # CLOSE
    # =====================================

    def closeEvent(self, event):

        try:
            self.session.close()
        except:
            pass

        event.accept()