"""Login dialog for voter and admin authentication"""
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QComboBox, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class LoginDialog(QDialog):
    """Dialog for user login"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.user_role = None
        self.user_id = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle("Đăng nhập - DApp Voting System")
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Title
        title = QLabel("🗳️ Hệ thống bỏ phiếu phi tập trung")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Role selection
        role_layout = QHBoxLayout()
        role_label = QLabel("Vai trò:")
        role_label.setMinimumWidth(100)
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Cử tri", "Quản trị viên"])
        role_layout.addWidget(role_label)
        role_layout.addWidget(self.role_combo)
        layout.addLayout(role_layout)
        
        # ID input
        id_layout = QHBoxLayout()
        id_label = QLabel("Mã số:")
        id_label.setMinimumWidth(100)
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Nhập mã cử tri (1-100) hoặc 'admin'")
        id_layout.addWidget(id_label)
        id_layout.addWidget(self.id_input)
        layout.addLayout(id_layout)
        
        # Info label
        info = QLabel("💡 Cử tri: nhập số từ 1-100\n💡 Admin: nhập 'admin'")
        info.setObjectName("infoLabel")
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)
        
        # Buttons
        button_layout = QHBoxLayout()
        login_btn = QPushButton("Đăng nhập")
        login_btn.clicked.connect(self.handle_login)
        cancel_btn = QPushButton("Hủy")
        cancel_btn.setObjectName("dangerButton")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(login_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def handle_login(self):
        """Handle login button click"""
        role = self.role_combo.currentText()
        user_input = self.id_input.text().strip()
        
        if not user_input:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập mã số")
            return
        
        if role == "Quản trị viên":
            if user_input.lower() == "admin":
                self.user_role = "Admin"
                self.user_id = 0
                self.accept()
            else:
                QMessageBox.warning(self, "Lỗi", "Mã quản trị viên không đúng")
        else:
            try:
                voter_id = int(user_input)
                if 1 <= voter_id <= 100:
                    self.user_role = "Voter"
                    self.user_id = voter_id
                    self.accept()
                else:
                    QMessageBox.warning(self, "Lỗi", "Mã cử tri phải từ 1-100")
            except ValueError:
                QMessageBox.warning(self, "Lỗi", "Mã cử tri phải là số")
