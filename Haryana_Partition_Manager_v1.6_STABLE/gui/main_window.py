import shutil
from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QGridLayout,
    QMessageBox,
    QToolBar,
    QFileDialog
)

from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

from gui.owner_screen import OwnerScreen
from gui.village_screen import VillageScreen
from gui.khewat_screen import KhewatScreen
from gui.partition_wizard import PartitionWizard
from gui.search_screen import SearchScreen
from gui.export_screen import ExportScreen
from gui.partition_register import PartitionRegister
from gui.khewat_history import KhewatHistory


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Haryana Partition Manager"
        )

        self.resize(
            1400,
            900
        )

        # Child Windows

        self.owner_window = None
        self.village_window = None
        self.khewat_window = None
        self.partition_window = None
        self.report_window = None
        self.search_window = None
        self.export_window = None
        self.partition_register_window = None
        self.khewat_history_window = None

        self.create_menu()
        self.create_toolbar()
        self.create_dashboard()

        self.statusBar().showMessage(
            "Ready"
        )

    # =====================================
    # MENU
    # =====================================

    def create_menu(self):

        menu_bar = self.menuBar()

        master_menu = menu_bar.addMenu(
            "Masters"
        )

        owner_action = QAction(
            "Owners",
            self
        )

        village_action = QAction(
            "Villages",
            self
        )

        khewat_action = QAction(
            "Khewats",
            self
        )

        master_menu.addAction(
            owner_action
        )

        master_menu.addAction(
            village_action
        )

        master_menu.addAction(
            khewat_action
        )

        partition_menu = menu_bar.addMenu(
            "Partition"
        )

        partition_action = QAction(
            "Partition Wizard",
            self
        )

        partition_menu.addAction(
            partition_action
        )

        register_action = QAction(
            "Partition Register",
            self
        )

        partition_menu.addAction(
            register_action
        )

        reports_menu = menu_bar.addMenu(
            "Reports"
        )

        reports_action = QAction(
            "Ownership Reports",
            self
        )

        reports_menu.addAction(
            reports_action
        )

        owner_action.triggered.connect(
            self.open_owners
        )

        village_action.triggered.connect(
            self.open_villages
        )

        khewat_action.triggered.connect(
            self.open_khewats
        )

        partition_action.triggered.connect(
            self.open_partition
        )

        register_action.triggered.connect(
            self.open_partition_register
        )

        history_action = QAction("Khewat History", self)
        partition_menu.addAction(history_action)
        history_action.triggered.connect(self.open_khewat_history)

        reports_action.triggered.connect(
            self.open_reports
        )

        tools_menu = menu_bar.addMenu('Tools')

        backup_action = QAction('Backup Database', self)
        restore_action = QAction('Restore Database', self)

        tools_menu.addAction(backup_action)
        tools_menu.addAction(restore_action)

        search_action = QAction('Universal Search', self)
        tools_menu.addAction(search_action)

        export_action = QAction('Excel Export', self)
        tools_menu.addAction(export_action)

        backup_action.triggered.connect(self.backup_database)
        restore_action.triggered.connect(self.restore_database)
        search_action.triggered.connect(self.open_search)
        export_action.triggered.connect(self.open_export)

    # =====================================
    # TOOLBAR
    # =====================================

    def create_toolbar(self):

        toolbar = QToolBar()

        self.addToolBar(
            toolbar
        )

        owner_action = QAction(
            "Owners",
            self
        )

        village_action = QAction(
            "Villages",
            self
        )

        khewat_action = QAction(
            "Khewats",
            self
        )

        partition_action = QAction(
            "Partition",
            self
        )

        toolbar.addAction(
            owner_action
        )

        toolbar.addAction(
            village_action
        )

        toolbar.addAction(
            khewat_action
        )

        toolbar.addAction(
            partition_action
        )

        owner_action.triggered.connect(
            self.open_owners
        )

        village_action.triggered.connect(
            self.open_villages
        )

        khewat_action.triggered.connect(
            self.open_khewats
        )

        partition_action.triggered.connect(
            self.open_partition
        )

       

    # =====================================
    # DASHBOARD
    # =====================================

    def create_dashboard(self):

        widget = QWidget()

        layout = QVBoxLayout()

        title = QLabel(
            "HARYANA PARTITION MANAGER"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        title.setStyleSheet(
            """
            font-size:30px;
            font-weight:bold;
            padding:20px;
            """
        )

        layout.addWidget(
            title
        )

        grid = QGridLayout()

        btn_owner = QPushButton(
            "Owner Master"
        )

        btn_village = QPushButton(
            "Village Master"
        )

        btn_khewat = QPushButton(
            "Khewat Management"
        )

        btn_partition = QPushButton(
            "Partition Wizard"
        )

        btn_reports = QPushButton(
            "Reports"
        )

        buttons = [

            btn_owner,
            btn_village,
            btn_khewat,
            btn_partition,
            btn_reports
        ]

        for btn in buttons:

            btn.setMinimumHeight(
                90
            )

        grid.addWidget(
            btn_owner,
            0,
            0
        )

        grid.addWidget(
            btn_village,
            0,
            1
        )

        grid.addWidget(
            btn_khewat,
            1,
            0
        )

        grid.addWidget(
            btn_partition,
            1,
            1
        )

        grid.addWidget(
            btn_reports,
            2,
            0
        )

        layout.addLayout(
            grid
        )

        widget.setLayout(
            layout
        )

        self.setCentralWidget(
            widget
        )

        btn_owner.clicked.connect(
            self.open_owners
        )

        btn_village.clicked.connect(
            self.open_villages
        )

        btn_khewat.clicked.connect(
            self.open_khewats
        )

        btn_partition.clicked.connect(
            self.open_partition
        )

        btn_reports.clicked.connect(
            self.open_reports
        )

    # =====================================
    # OPEN OWNER SCREEN
    # =====================================

    def open_owners(self):

        try:

            self.owner_window = (
                OwnerScreen()
            )

            self.owner_window.show()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Owner Screen Error",
                str(e)
            )

    # =====================================
    # OPEN VILLAGE SCREEN
    # =====================================

    def open_villages(self):

        try:

            self.village_window = (
                VillageScreen()
            )

            self.village_window.show()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Village Screen Error",
                str(e)
            )

    # =====================================
    # OPEN KHEWAT SCREEN
    # =====================================

    def open_khewats(self):

        try:

            self.khewat_window = (
                KhewatScreen()
            )

            self.khewat_window.show()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Khewat Screen Error",
                str(e)
            )

    # =====================================
    # OPEN PARTITION WIZARD
    # =====================================

    def open_partition(self):

        try:

            self.partition_window = (
                PartitionWizard()
            )

            self.partition_window.show()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Partition Wizard Error",
                str(e)
            )

    # =====================================
    # REPORTS
    # =====================================

    def open_reports(self):

        QMessageBox.information(
            self,
            "Reports",
            "Reports module under development."
        )

    def backup_database(self):

        try:
            source = Path(__file__).resolve().parent.parent / "data" / "haryana.db"

            file_name, _ = QFileDialog.getSaveFileName(
                self,
                "Backup Database",
                "haryana_backup.db",
                "Database Files (*.db)"
            )

            if not file_name:
                return

            shutil.copy2(source, file_name)

            QMessageBox.information(
                self,
                "Success",
                "Database backup created."
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Backup Error",
                str(e)
            )

    def restore_database(self):

        try:

            file_name, _ = QFileDialog.getOpenFileName(
                self,
                "Select Backup",
                "",
                "Database Files (*.db)"
            )

            if not file_name:
                return

            target = Path(__file__).resolve().parent.parent / "data" / "haryana.db"

            shutil.copy2(file_name, target)

            QMessageBox.information(
                self,
                "Success",
                "Database restored. Restart application."
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Restore Error",
                str(e)
            )


    def open_search(self):

        try:

            self.search_window = SearchScreen()

            self.search_window.show()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Search Error",
                str(e)
            )


    def open_export(self):

        try:

            self.export_window = ExportScreen()

            self.export_window.show()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Export Error",
                str(e)
            )


    def open_partition_register(self):

        try:

            self.partition_register_window = PartitionRegister()

            self.partition_register_window.show()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Partition Register Error",
                str(e)
            )


    def open_khewat_history(self):

        try:

            self.khewat_history_window = KhewatHistory()

            self.khewat_history_window.show()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Khewat History Error",
                str(e)
            )
