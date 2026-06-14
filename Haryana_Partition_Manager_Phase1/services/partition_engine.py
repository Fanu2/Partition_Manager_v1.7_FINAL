# gui/partition_wizard.py

from fractions import Fraction

from PySide6.QtWidgets import (
QWidget,
QVBoxLayout,
QHBoxLayout,
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
Khasra
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
            QLabel(
                "Partition Wizard"
            )
        )

        self.setLayout(
            layout
        )

def load_khewats(self):

        pass


# =====================================
# UI
# =====================================

def build_ui(self):

    layout = QVBoxLayout()

    layout.addWidget(
        QLabel("Select Source Khewat")
    )

    self.cmb_khewat = QComboBox()

    layout.addWidget(
        self.cmb_khewat
    )

    self.btn_load = QPushButton(
        "Load Khewat"
    )

    layout.addWidget(
        self.btn_load
    )

    lists = QHBoxLayout()

    self.owner_list = QListWidget()

    self.khasra_list = QListWidget()

    lists.addWidget(
        self.owner_list
    )

    lists.addWidget(
        self.khasra_list
    )

    layout.addLayout(
        lists
    )

    self.preview = QTextEdit()

    self.preview.setReadOnly(
        True
    )

    layout.addWidget(
        self.preview
    )

    self.btn_preview = QPushButton(
        "Preview Partition"
    )

    layout.addWidget(
        self.btn_preview
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

# =====================================
# LOAD KHEWATS
# =====================================

def load_khewats(self):

    self.cmb_khewat.clear()

    khewats = (
        self.session.query(
            Khewat
        )
        .order_by(
            Khewat.khewat_no
        )
        .all()
    )

    for khewat in khewats:

        self.cmb_khewat.addItem(
            str(khewat.khewat_no),
            khewat.id
        )

# =====================================
# LOAD DATA
# =====================================

def load_partition_data(self):

    self.load_owners()

    self.load_khasras()

# =====================================
# LOAD OWNERS
# =====================================

def load_owners(self):

    self.owner_list.clear()

    khewat_id = (
        self.cmb_khewat.currentData()
    )

    ownerships = (
        self.session.query(
            Ownership
        )
        .filter(
            Ownership.khewat_id
            == khewat_id
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

            f"{owner.id} - "
            f"{owner.owner_name}"
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

# =====================================
# LOAD KHASRAS
# =====================================

def load_khasras(self):

    self.khasra_list.clear()

    khewat_id = (
        self.cmb_khewat.currentData()
    )

    khasras = (
        self.session.query(
            Khasra
        )
        .filter(
            Khasra.khewat_id
            == khewat_id
        )
        .all()
    )

    for khasra in khasras:

        item = QListWidgetItem(

            f"{khasra.khasra_no}"
            f" ({khasra.area})"
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

# =====================================
# PREVIEW
# =====================================

def preview_partition(self):

    selected_owners = []

    for row in range(
        self.owner_list.count()
    ):

        item = self.owner_list.item(
            row
        )

        if (
            item.checkState()
            == Qt.Checked
        ):

            selected_owners.append(
                item.text()
            )

    selected_khasras = []

    for row in range(
        self.khasra_list.count()
    ):

        item = self.khasra_list.item(
            row
        )

        if (
            item.checkState()
            == Qt.Checked
        ):

            selected_khasras.append(
                item.text()
            )

    report = []

    report.append(
        "PARTITION PREVIEW"
    )

    report.append("")

    report.append(
        "Selected Owners"
    )

    report.extend(
        selected_owners
    )

    report.append("")

    report.append(
        "Selected Khasras"
    )

    report.extend(
        selected_khasras
    )

    self.preview.setText(
        "\n".join(report)
    )

def closeEvent(self, event):

    try:
        self.session.close()
    except:
        pass

    event.accept()

