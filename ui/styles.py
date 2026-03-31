"""Modern stylesheet for the application"""

MAIN_STYLE = """
QMainWindow {
    background-color: #FAFAFA;
}

QWidget {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 10pt;
}

QPushButton {
    background-color: #2196F3;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    font-weight: bold;
    min-width: 100px;
}

QPushButton:hover {
    background-color: #1976D2;
}

QPushButton:pressed {
    background-color: #0D47A1;
}

QPushButton:disabled {
    background-color: #BDBDBD;
    color: #757575;
}

QPushButton#successButton {
    background-color: #4CAF50;
}

QPushButton#successButton:hover {
    background-color: #388E3C;
}

QPushButton#dangerButton {
    background-color: #F44336;
}

QPushButton#dangerButton:hover {
    background-color: #D32F2F;
}

QPushButton#warningButton {
    background-color: #FF9800;
}

QPushButton#warningButton:hover {
    background-color: #F57C00;
}

QLineEdit, QTextEdit, QSpinBox, QComboBox {
    padding: 8px;
    border: 2px solid #E0E0E0;
    border-radius: 4px;
    background-color: white;
}

QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QComboBox:focus {
    border: 2px solid #2196F3;
}

QLabel {
    color: #212121;
}

QLabel#titleLabel {
    font-size: 24pt;
    font-weight: bold;
    color: #2196F3;
}

QLabel#subtitleLabel {
    font-size: 14pt;
    font-weight: bold;
    color: #424242;
}

QLabel#infoLabel {
    color: #757575;
    font-size: 9pt;
}

QTableWidget {
    background-color: white;
    border: 1px solid #E0E0E0;
    border-radius: 4px;
    gridline-color: #E0E0E0;
}

QTableWidget::item {
    padding: 8px;
}

QTableWidget::item:selected {
    background-color: #BBDEFB;
    color: #212121;
}

QHeaderView::section {
    background-color: #2196F3;
    color: white;
    padding: 10px;
    border: none;
    font-weight: bold;
}

QTabWidget::pane {
    border: 1px solid #E0E0E0;
    background-color: white;
    border-radius: 4px;
}

QTabBar::tab {
    background-color: #E0E0E0;
    color: #212121;
    padding: 10px 20px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background-color: #2196F3;
    color: white;
}

QTabBar::tab:hover {
    background-color: #BBDEFB;
}

QGroupBox {
    border: 2px solid #E0E0E0;
    border-radius: 4px;
    margin-top: 10px;
    padding-top: 10px;
    font-weight: bold;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 5px;
    color: #2196F3;
}

QMessageBox {
    background-color: white;
}

QScrollBar:vertical {
    border: none;
    background-color: #F5F5F5;
    width: 10px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background-color: #BDBDBD;
    border-radius: 5px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #9E9E9E;
}

QProgressBar {
    border: 2px solid #E0E0E0;
    border-radius: 4px;
    text-align: center;
    background-color: white;
}

QProgressBar::chunk {
    background-color: #4CAF50;
    border-radius: 2px;
}
"""
