"""
Module GUI - Giao diện người dùng với Tkinter
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from datetime import datetime
from blockchain import Blockchain
from storage import BlockchainStorage
from nft_manager import NFTManager
from key_manager import KeyManager
from signature_utils import SignatureUtils
from qr_manager import QRManager


class CertificateApp:
    """
    Ứng dụng quản lý chứng chỉ điện tử với giao diện Tkinter
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Hệ thống Quản lý Chứng chỉ Blockchain & NFT - Nâng cấp")
        self.root.geometry("1200x800")
        
        # Khởi tạo các manager
        self.storage = BlockchainStorage()
        self.blockchain = self.storage.load()
        self.nft_manager = NFTManager()
        self.key_manager = KeyManager()
        self.qr_manager = QRManager()
        
        # Tạo giao diện
        self.create_widgets()
        
        # Cập nhật danh sách khối ban đầu
        self.refresh_blockchain_view()
        self.update_system_info()
    
    def create_widgets(self):
        """
        Tạo các widget cho giao diện
        """
        # Tiêu đề
        title_label = tk.Label(
            self.root, 
            text="HỆ THỐNG QUẢN LÝ CHỨNG CHỈ BLOCKCHAIN & NFT - NÂNG CẤP",
            font=("Arial", 16, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=10
        )
        title_label.pack(fill=tk.X)
        
        # Notebook (Tab)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Cấp bằng
        self.create_issue_tab()
        
        # Tab 2: Xem chuỗi
        self.create_view_tab()
        
        # Tab 3: Xác thực
        self.create_verify_tab()
        
        # Tab 4: Tìm kiếm nâng cao
        self.create_search_tab()
        
        # Tab 5: Thu hồi chứng chỉ
        self.create_revoke_tab()
        
        # Tab 6: Dashboard
        self.create_dashboard_tab()
        
        # Tab 7: Backup & Restore
        self.create_backup_tab()
        
        # Tab 8: Bảo mật
        self.create_security_tab()
    
    def create_issue_tab(self):
        """
        Tab cấp chứng chỉ mới với chữ ký số
        """
        issue_frame = ttk.Frame(self.notebook)
        self.notebook.add(issue_frame, text="📜 Cấp Chứng Chỉ")
        
        # Form nhập liệu
        form_frame = tk.LabelFrame(issue_frame, text="Thông tin Chứng chỉ", padx=20, pady=20)
        form_frame.pack(padx=20, pady=20, fill=tk.BOTH)
        
        # Tên sinh viên
        tk.Label(form_frame, text="Tên sinh viên:", font=("Arial", 11)).grid(row=0, column=0, sticky=tk.W, pady=10)
        self.student_name_entry = tk.Entry(form_frame, width=40, font=("Arial", 11))
        self.student_name_entry.grid(row=0, column=1, pady=10, padx=10)
        
        # Tên chứng chỉ
        tk.Label(form_frame, text="Tên chứng chỉ:", font=("Arial", 11)).grid(row=1, column=0, sticky=tk.W, pady=10)
        self.certificate_name_entry = tk.Entry(form_frame, width=40, font=("Arial", 11))
        self.certificate_name_entry.grid(row=1, column=1, pady=10, padx=10)
        
        # Đơn vị cấp (Dropdown)
        tk.Label(form_frame, text="Đơn vị cấp:", font=("Arial", 11)).grid(row=2, column=0, sticky=tk.W, pady=10)
        self.issuer_var = tk.StringVar()
        self.issuer_combo = ttk.Combobox(form_frame, textvariable=self.issuer_var, width=37, font=("Arial", 11))
        
        # Populate dropdown với danh sách đơn vị cấp
        issuers = self.key_manager.get_all_issuers()
        issuer_list = [f"{issuer_id} - {name}" for issuer_id, name in issuers.items()]
        self.issuer_combo['values'] = issuer_list
        self.issuer_combo.grid(row=2, column=1, pady=10, padx=10)
        
        # Nút cấp bằng
        issue_button = tk.Button(
            form_frame,
            text="🎓 CẤP CHỨNG CHỈ (Có chữ ký số)",
            command=self.issue_certificate,
            bg="#27ae60",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10
        )
        issue_button.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Khu vực hiển thị kết quả
        result_frame = tk.LabelFrame(issue_frame, text="Kết quả", padx=20, pady=20)
        result_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        self.result_text = tk.Text(result_frame, height=10, font=("Courier", 10))
        scrollbar_result = ttk.Scrollbar(result_frame, orient="vertical", command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar_result.set)
        
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_result.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_view_tab(self):
        """
        Tab xem chuỗi blockchain
        """
        view_frame = ttk.Frame(self.notebook)
        self.notebook.add(view_frame, text="🔗 Xem Chuỗi Khối")
        
        # Nút làm mới
        refresh_button = tk.Button(
            view_frame,
            text="🔄 Làm mới",
            command=self.refresh_blockchain_view,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold")
        )
        refresh_button.pack(pady=10)
        
        # Treeview để hiển thị blockchain
        tree_frame = tk.Frame(view_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview với cột mới
        columns = ("Index", "Timestamp", "Student", "Certificate", "Issuer", "NFT ID", "Status", "Hash")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        
        # Định nghĩa cột
        self.tree.heading("Index", text="Khối")
        self.tree.heading("Timestamp", text="Thời gian")
        self.tree.heading("Student", text="Sinh viên")
        self.tree.heading("Certificate", text="Chứng chỉ")
        self.tree.heading("Issuer", text="Đơn vị cấp")
        self.tree.heading("NFT ID", text="NFT ID")
        self.tree.heading("Status", text="Trạng thái")
        self.tree.heading("Hash", text="Hash")
        
        # Độ rộng cột
        self.tree.column("Index", width=50)
        self.tree.column("Timestamp", width=130)
        self.tree.column("Student", width=120)
        self.tree.column("Certificate", width=120)
        self.tree.column("Issuer", width=100)
        self.tree.column("NFT ID", width=130)
        self.tree.column("Status", width=80)
        self.tree.column("Hash", width=150)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
    
    def create_verify_tab(self):
        """
        Tab xác thực chứng chỉ
        """
        verify_frame = ttk.Frame(self.notebook)
        self.notebook.add(verify_frame, text="✅ Xác Thực")
        
        # Form tìm kiếm
        search_frame = tk.LabelFrame(verify_frame, text="Tra cứu Chứng chỉ", padx=20, pady=20)
        search_frame.pack(padx=20, pady=20, fill=tk.X)
        
        tk.Label(search_frame, text="Nhập NFT ID:", font=("Arial", 11)).grid(row=0, column=0, sticky=tk.W, pady=10)
        self.nft_search_entry = tk.Entry(search_frame, width=40, font=("Arial", 11))
        self.nft_search_entry.grid(row=0, column=1, pady=10, padx=10)
        
        search_button = tk.Button(
            search_frame,
            text="🔍 TÌM KIẾM",
            command=self.verify_certificate,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=5
        )
        search_button.grid(row=0, column=2, padx=10)
        
        # Kết quả tìm kiếm
        result_frame = tk.LabelFrame(verify_frame, text="Thông tin Chứng chỉ", padx=20, pady=20)
        result_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        self.verify_text = tk.Text(result_frame, height=15, font=("Courier", 10))
        self.verify_text.pack(fill=tk.BOTH, expand=True)
    
    def create_security_tab(self):
        """
        Tab kiểm tra bảo mật
        """
        security_frame = ttk.Frame(self.notebook)
        self.notebook.add(security_frame, text="🔒 Bảo Mật")
        
        # Thông tin hệ thống
        info_frame = tk.LabelFrame(security_frame, text="Thông tin Hệ thống", padx=20, pady=20)
        info_frame.pack(padx=20, pady=20, fill=tk.X)
        
        self.info_text = tk.Text(info_frame, height=8, font=("Courier", 10))
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        # Nút kiểm tra
        check_button = tk.Button(
            security_frame,
            text="🛡️ KIỂM TRA HỆ THỐNG",
            command=self.check_security,
            bg="#9b59b6",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10
        )
        check_button.pack(pady=20)
        
        # Kết quả kiểm tra
        result_frame = tk.LabelFrame(security_frame, text="Kết quả Kiểm tra", padx=20, pady=20)
        result_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        self.security_text = tk.Text(result_frame, height=10, font=("Courier", 10))
        self.security_text.pack(fill=tk.BOTH, expand=True)
        
        # Cập nhật thông tin hệ thống ban đầu
        self.update_system_info()
    
    def create_search_tab(self):
        """
        Tab tìm kiếm nâng cao
        """
        search_frame = ttk.Frame(self.notebook)
        self.notebook.add(search_frame, text="🔍 Tìm Kiếm")
        
        # Form tìm kiếm
        form_frame = tk.LabelFrame(search_frame, text="Tìm kiếm nâng cao", padx=20, pady=20)
        form_frame.pack(padx=20, pady=20, fill=tk.X)
        
        # Loại tìm kiếm
        tk.Label(form_frame, text="Tìm theo:", font=("Arial", 11)).grid(row=0, column=0, sticky=tk.W, pady=10)
        self.search_type_var = tk.StringVar(value="student")
        search_types = [
            ("Tên sinh viên", "student"),
            ("Tên chứng chỉ", "certificate"),
            ("Đơn vị cấp", "issuer"),
            ("Trạng thái", "status")
        ]
        
        for i, (text, value) in enumerate(search_types):
            tk.Radiobutton(form_frame, text=text, variable=self.search_type_var, 
                          value=value, font=("Arial", 10)).grid(row=0, column=i+1, padx=10)
        
        # Từ khóa tìm kiếm
        tk.Label(form_frame, text="Từ khóa:", font=("Arial", 11)).grid(row=1, column=0, sticky=tk.W, pady=10)
        self.search_keyword_entry = tk.Entry(form_frame, width=40, font=("Arial", 11))
        self.search_keyword_entry.grid(row=1, column=1, columnspan=2, pady=10, padx=10)
        
        # Nút tìm kiếm
        search_button = tk.Button(
            form_frame,
            text="🔍 TÌM KIẾM",
            command=self.perform_search,
            bg="#3498db",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=5
        )
        search_button.grid(row=1, column=3, padx=10)
        
        # Kết quả tìm kiếm
        result_frame = tk.LabelFrame(search_frame, text="Kết quả tìm kiếm", padx=20, pady=20)
        result_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # Treeview cho kết quả
        search_tree_frame = tk.Frame(result_frame)
        search_tree_frame.pack(fill=tk.BOTH, expand=True)
        
        search_scrollbar = ttk.Scrollbar(search_tree_frame)
        search_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        search_columns = ("Index", "Student", "Certificate", "Issuer", "NFT ID", "Status", "Issued")
        self.search_tree = ttk.Treeview(search_tree_frame, columns=search_columns, 
                                       show="headings", yscrollcommand=search_scrollbar.set)
        search_scrollbar.config(command=self.search_tree.yview)
        
        for col in search_columns:
            self.search_tree.heading(col, text=col)
            self.search_tree.column(col, width=120)
        
        self.search_tree.pack(fill=tk.BOTH, expand=True)
    
    def create_revoke_tab(self):
        """
        Tab thu hồi chứng chỉ
        """
        revoke_frame = ttk.Frame(self.notebook)
        self.notebook.add(revoke_frame, text="❌ Thu Hồi")
        
        # Form thu hồi
        form_frame = tk.LabelFrame(revoke_frame, text="Thu hồi Chứng chỉ", padx=20, pady=20)
        form_frame.pack(padx=20, pady=20, fill=tk.X)
        
        tk.Label(form_frame, text="NFT ID:", font=("Arial", 11)).grid(row=0, column=0, sticky=tk.W, pady=10)
        self.revoke_nft_entry = tk.Entry(form_frame, width=40, font=("Arial", 11))
        self.revoke_nft_entry.grid(row=0, column=1, pady=10, padx=10)
        
        tk.Label(form_frame, text="Lý do thu hồi:", font=("Arial", 11)).grid(row=1, column=0, sticky=tk.W, pady=10)
        self.revoke_reason_entry = tk.Entry(form_frame, width=40, font=("Arial", 11))
        self.revoke_reason_entry.grid(row=1, column=1, pady=10, padx=10)
        
        revoke_button = tk.Button(
            form_frame,
            text="❌ THU HỒI CHỨNG CHỈ",
            command=self.revoke_certificate,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10
        )
        revoke_button.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Kết quả
        result_frame = tk.LabelFrame(revoke_frame, text="Kết quả", padx=20, pady=20)
        result_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        self.revoke_text = tk.Text(result_frame, height=15, font=("Courier", 10))
        self.revoke_text.pack(fill=tk.BOTH, expand=True)
    
    def create_dashboard_tab(self):
        """
        Tab dashboard thống kê
        """
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="📊 Dashboard")
        
        # Thống kê tổng quan
        stats_frame = tk.LabelFrame(dashboard_frame, text="Thống kê Tổng quan", padx=20, pady=20)
        stats_frame.pack(padx=20, pady=20, fill=tk.X)
        
        self.stats_text = tk.Text(stats_frame, height=12, font=("Courier", 11))
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        
        # Nút làm mới
        refresh_stats_button = tk.Button(
            dashboard_frame,
            text="🔄 CẬP NHẬT THỐNG KÊ",
            command=self.update_dashboard_stats,
            bg="#9b59b6",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10
        )
        refresh_stats_button.pack(pady=10)
        
        # Trạng thái khóa
        keys_frame = tk.LabelFrame(dashboard_frame, text="Trạng thái Khóa RSA", padx=20, pady=20)
        keys_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        self.keys_text = tk.Text(keys_frame, height=8, font=("Courier", 10))
        self.keys_text.pack(fill=tk.BOTH, expand=True)
    
    def create_backup_tab(self):
        """
        Tab backup và restore
        """
        backup_frame = ttk.Frame(self.notebook)
        self.notebook.add(backup_frame, text="💾 Backup")
        
        # Backup section
        backup_section = tk.LabelFrame(backup_frame, text="Tạo Backup", padx=20, pady=20)
        backup_section.pack(padx=20, pady=20, fill=tk.X)
        
        tk.Label(backup_section, text="Tên backup (tùy chọn):", font=("Arial", 11)).grid(row=0, column=0, sticky=tk.W, pady=10)
        self.backup_name_entry = tk.Entry(backup_section, width=30, font=("Arial", 11))
        self.backup_name_entry.grid(row=0, column=1, pady=10, padx=10)
        
        backup_button = tk.Button(
            backup_section,
            text="💾 TẠO BACKUP",
            command=self.create_backup,
            bg="#27ae60",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=5
        )
        backup_button.grid(row=0, column=2, padx=10)
        
        # Restore section
        restore_section = tk.LabelFrame(backup_frame, text="Khôi phục từ Backup", padx=20, pady=20)
        restore_section.pack(padx=20, pady=10, fill=tk.X)
        
        restore_button = tk.Button(
            restore_section,
            text="📁 CHỌN FILE BACKUP",
            command=self.restore_backup,
            bg="#e67e22",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10
        )
        restore_button.pack(pady=10)
        
        # Danh sách backup
        list_frame = tk.LabelFrame(backup_frame, text="Danh sách Backup", padx=20, pady=20)
        list_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        list_button = tk.Button(
            list_frame,
            text="🔄 LÀMỚI DANH SÁCH",
            command=self.refresh_backup_list,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold")
        )
        list_button.pack(pady=5)
        
        self.backup_text = tk.Text(list_frame, height=10, font=("Courier", 10))
        self.backup_text.pack(fill=tk.BOTH, expand=True)
    
    def issue_certificate(self):
        """
        Xử lý việc cấp chứng chỉ mới với chữ ký số
        """
        student_name = self.student_name_entry.get().strip()
        certificate_name = self.certificate_name_entry.get().strip()
        issuer_selection = self.issuer_var.get().strip()
        
        # Kiểm tra dữ liệu đầu vào
        if not student_name or not certificate_name or not issuer_selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin!")
            return
        
        # Parse issuer selection
        try:
            issuer_id = issuer_selection.split(" - ")[0]
            issuer_name = self.key_manager.get_issuer_name(issuer_id)
        except:
            messagebox.showerror("Lỗi", "Vui lòng chọn đơn vị cấp hợp lệ!")
            return
        
        # Kiểm tra khóa
        if not self.key_manager.has_keys(issuer_id):
            messagebox.showerror("Lỗi", f"Không tìm thấy khóa cho {issuer_id}!")
            return
        
        # Hiển thị thông báo đang xử lý
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "⏳ Đang tạo chứng chỉ...\n")
        self.result_text.insert(tk.END, "1. Tạo NFT ID...\n")
        self.root.update()
        
        # Thực hiện tạo chứng chỉ trong thread riêng
        def create_certificate():
            try:
                # Tạo NFT ID
                nft_id = self.nft_manager.generate_nft_id()
                
                # Cập nhật UI
                self.root.after(0, lambda: self.result_text.insert(tk.END, f"   NFT ID: {nft_id}\n"))
                self.root.after(0, lambda: self.result_text.insert(tk.END, "2. Tạo chữ ký số...\n"))
                self.root.after(0, lambda: self.root.update())
                
                # Tạo chữ ký số
                import time
                issued_at = time.time()
                signature = SignatureUtils.create_certificate_signature(
                    self.key_manager, student_name, certificate_name, 
                    issuer_id, nft_id, issued_at
                )
                
                if not signature:
                    self.root.after(0, lambda: messagebox.showerror("Lỗi", "Không thể tạo chữ ký số!"))
                    return
                
                # Cập nhật UI
                self.root.after(0, lambda: self.result_text.insert(tk.END, "   Chữ ký đã tạo ✓\n"))
                self.root.after(0, lambda: self.result_text.insert(tk.END, "3. Đào khối (Mining)...\n"))
                self.root.after(0, lambda: self.root.update())
                
                # Thêm khối mới
                new_block = self.blockchain.add_block(
                    student_name, certificate_name, issuer_name, nft_id,
                    issuer_id, issuer_name, signature
                )
                
                # Lưu blockchain
                self.storage.save(self.blockchain)
                
                # Tạo QR code
                self.root.after(0, lambda: self.result_text.insert(tk.END, "4. Tạo QR code...\n"))
                self.root.after(0, lambda: self.root.update())
                
                qr_path = self.qr_manager.generate_qr_code(nft_id, student_name)
                
                # Cập nhật giao diện
                self.root.after(0, lambda: self.display_issue_result(new_block, qr_path))
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Lỗi", f"Lỗi khi tạo chứng chỉ: {str(e)}"))
        
        threading.Thread(target=create_certificate, daemon=True).start()
    
    def display_issue_result(self, block, qr_path=None):
        """
        Hiển thị kết quả sau khi cấp chứng chỉ
        """
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "✅ CẤP CHỨNG CHỈ THÀNH CÔNG!\n\n")
        self.result_text.insert(tk.END, "=" * 60 + "\n")
        self.result_text.insert(tk.END, f"NFT ID:          {block.nft_id}\n")
        self.result_text.insert(tk.END, f"Sinh viên:       {block.student_name}\n")
        self.result_text.insert(tk.END, f"Chứng chỉ:       {block.certificate_name}\n")
        self.result_text.insert(tk.END, f"Đơn vị cấp:      {block.issuer_name}\n")
        self.result_text.insert(tk.END, f"Mã đơn vị:       {block.issuer_id}\n")
        self.result_text.insert(tk.END, f"Khối số:         {block.index}\n")
        self.result_text.insert(tk.END, f"Trạng thái:      {block.status}\n")
        self.result_text.insert(tk.END, f"Chữ ký số:       {'Có' if block.signature else 'Không'}\n")
        self.result_text.insert(tk.END, f"Nonce:           {block.nonce}\n")
        self.result_text.insert(tk.END, f"Hash:            {block.hash}\n")
        
        if qr_path:
            self.result_text.insert(tk.END, f"QR Code:         {qr_path}\n")
        
        self.result_text.insert(tk.END, "=" * 60 + "\n")
        
        # Xóa form
        self.student_name_entry.delete(0, tk.END)
        self.certificate_name_entry.delete(0, tk.END)
        self.issuer_var.set("")
        
        # Làm mới các view
        self.refresh_blockchain_view()
        self.update_system_info()
        self.update_dashboard_stats()
        
        messagebox.showinfo("Thành công", f"Chứng chỉ đã được cấp!\nNFT ID: {block.nft_id}")
    
    def perform_search(self):
        """
        Thực hiện tìm kiếm nâng cao
        """
        search_type = self.search_type_var.get()
        keyword = self.search_keyword_entry.get().strip()
        
        if not keyword:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập từ khóa tìm kiếm!")
            return
        
        # Xóa kết quả cũ
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)
        
        # Tìm kiếm
        results = []
        if search_type == "student":
            results = self.blockchain.find_by_student_name(keyword)
        elif search_type == "certificate":
            results = self.blockchain.find_by_certificate_name(keyword)
        elif search_type == "issuer":
            results = self.blockchain.find_by_issuer(keyword)
        elif search_type == "status":
            results = self.blockchain.filter_by_status(keyword)
        
        # Hiển thị kết quả
        for block in results:
            if block.index == 0:  # Bỏ qua Genesis block
                continue
            
            issued_str = datetime.fromtimestamp(block.issued_at).strftime("%Y-%m-%d")
            issuer_display = block.issuer_name if block.issuer_name else block.issuer
            
            self.search_tree.insert("", tk.END, values=(
                block.index,
                block.student_name,
                block.certificate_name,
                issuer_display,
                block.nft_id,
                block.status,
                issued_str
            ))
        
        messagebox.showinfo("Kết quả", f"Tìm thấy {len(results)} kết quả")
    
    def revoke_certificate(self):
        """
        Thu hồi chứng chỉ
        """
        nft_id = self.revoke_nft_entry.get().strip()
        reason = self.revoke_reason_entry.get().strip()
        
        if not nft_id or not reason:
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin!")
            return
        
        # Tìm và thu hồi chứng chỉ
        success = self.blockchain.revoke_certificate(nft_id, reason)
        
        self.revoke_text.delete(1.0, tk.END)
        
        if success:
            # Lưu blockchain
            self.storage.save(self.blockchain)
            
            # Hiển thị kết quả
            block = self.blockchain.find_certificate_by_nft(nft_id)
            revoked_time = datetime.fromtimestamp(block.revoked_at).strftime("%Y-%m-%d %H:%M:%S")
            
            self.revoke_text.insert(tk.END, "✅ THU HỒI THÀNH CÔNG!\n\n")
            self.revoke_text.insert(tk.END, f"NFT ID:          {block.nft_id}\n")
            self.revoke_text.insert(tk.END, f"Sinh viên:       {block.student_name}\n")
            self.revoke_text.insert(tk.END, f"Chứng chỉ:       {block.certificate_name}\n")
            self.revoke_text.insert(tk.END, f"Trạng thái:      {block.status}\n")
            self.revoke_text.insert(tk.END, f"Thời gian thu hồi: {revoked_time}\n")
            self.revoke_text.insert(tk.END, f"Lý do:           {block.revoke_reason}\n")
            
            # Xóa form
            self.revoke_nft_entry.delete(0, tk.END)
            self.revoke_reason_entry.delete(0, tk.END)
            
            # Làm mới view
            self.refresh_blockchain_view()
            self.update_dashboard_stats()
            
            messagebox.showinfo("Thành công", "Chứng chỉ đã được thu hồi!")
        else:
            self.revoke_text.insert(tk.END, "❌ THU HỒI THẤT BẠI!\n\n")
            self.revoke_text.insert(tk.END, f"NFT ID '{nft_id}' không tồn tại hoặc đã bị thu hồi.\n")
            messagebox.showerror("Lỗi", "Không thể thu hồi chứng chỉ!")
    
    def update_dashboard_stats(self):
        """
        Cập nhật thống kê dashboard
        """
        stats = self.blockchain.get_dashboard_stats()
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, "📊 THỐNG KÊ HỆ THỐNG\n")
        self.stats_text.insert(tk.END, "=" * 50 + "\n")
        self.stats_text.insert(tk.END, f"Tổng số khối:           {stats['total_blocks']}\n")
        self.stats_text.insert(tk.END, f"Tổng chứng chỉ:         {stats['total_certificates']}\n")
        self.stats_text.insert(tk.END, f"Chứng chỉ hợp lệ:       {stats['valid_certificates']}\n")
        self.stats_text.insert(tk.END, f"Chứng chỉ đã thu hồi:   {stats['revoked_certificates']}\n")
        self.stats_text.insert(tk.END, f"Độ khó mining:          {stats['difficulty']}\n")
        self.stats_text.insert(tk.END, f"Số đơn vị cấp:          {stats['total_issuers']}\n")
        self.stats_text.insert(tk.END, "=" * 50 + "\n")
        
        # Cập nhật trạng thái khóa
        keys_status = self.key_manager.get_keys_status()
        
        self.keys_text.delete(1.0, tk.END)
        self.keys_text.insert(tk.END, "🔐 TRẠNG THÁI KHÓA RSA\n")
        self.keys_text.insert(tk.END, "=" * 40 + "\n")
        
        for issuer_id, has_keys in keys_status.items():
            issuer_name = self.key_manager.get_issuer_name(issuer_id)
            status = "✓ Có khóa" if has_keys else "✗ Thiếu khóa"
            self.keys_text.insert(tk.END, f"{issuer_id:8} - {status}\n")
        
        self.keys_text.insert(tk.END, "=" * 40 + "\n")
    
    def create_backup(self):
        """
        Tạo backup blockchain
        """
        backup_name = self.backup_name_entry.get().strip()
        backup_path = self.storage.backup_blockchain(backup_name)
        
        if backup_path:
            messagebox.showinfo("Thành công", f"Đã tạo backup:\n{backup_path}")
            self.backup_name_entry.delete(0, tk.END)
            self.refresh_backup_list()
        else:
            messagebox.showerror("Lỗi", "Không thể tạo backup!")
    
    def restore_backup(self):
        """
        Khôi phục từ backup
        """
        file_path = filedialog.askopenfilename(
            title="Chọn file backup",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            result = messagebox.askyesno(
                "Xác nhận", 
                "Khôi phục sẽ thay thế blockchain hiện tại.\nBạn có chắc chắn?"
            )
            
            if result:
                success = self.storage.restore_blockchain(file_path)
                if success:
                    # Tải lại blockchain
                    self.blockchain = self.storage.load()
                    
                    # Làm mới tất cả view
                    self.refresh_blockchain_view()
                    self.update_system_info()
                    self.update_dashboard_stats()
                    
                    messagebox.showinfo("Thành công", "Đã khôi phục blockchain!")
                else:
                    messagebox.showerror("Lỗi", "Không thể khôi phục từ file backup!")
    
    def refresh_backup_list(self):
        """
        Làm mới danh sách backup
        """
        backups = self.storage.list_backups()
        
        self.backup_text.delete(1.0, tk.END)
        self.backup_text.insert(tk.END, "📁 DANH SÁCH BACKUP\n")
        self.backup_text.insert(tk.END, "=" * 60 + "\n")
        
        if not backups:
            self.backup_text.insert(tk.END, "Chưa có file backup nào.\n")
        else:
            for backup in backups:
                size_kb = backup['size'] // 1024
                modified_str = backup['modified'].strftime("%Y-%m-%d %H:%M:%S")
                self.backup_text.insert(tk.END, f"File: {backup['filename']}\n")
                self.backup_text.insert(tk.END, f"Kích thước: {size_kb} KB\n")
                self.backup_text.insert(tk.END, f"Sửa đổi: {modified_str}\n")
                self.backup_text.insert(tk.END, "-" * 60 + "\n")
    
    def refresh_blockchain_view(self):
        """
        Làm mới danh sách blockchain trong Treeview
        """
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Thêm dữ liệu mới
        for block in self.blockchain.chain:
            timestamp_str = datetime.fromtimestamp(block.timestamp).strftime("%Y-%m-%d %H:%M")
            hash_short = block.hash[:12] + "..."
            
            # Hiển thị issuer name nếu có, nếu không thì issuer cũ
            issuer_display = block.issuer_name if block.issuer_name else block.issuer
            
            # Màu sắc theo trạng thái
            status_display = block.status
            
            self.tree.insert("", tk.END, values=(
                block.index,
                timestamp_str,
                block.student_name,
                block.certificate_name,
                issuer_display,
                block.nft_id,
                status_display,
                hash_short
            ))
    
    def verify_certificate(self):
        """
        Xác thực chứng chỉ theo NFT ID với kiểm tra chữ ký số
        """
        nft_id = self.nft_search_entry.get().strip()
        
        if not nft_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập NFT ID!")
            return
        
        # Tìm kiếm chứng chỉ
        block = self.blockchain.find_certificate_by_nft(nft_id)
        
        self.verify_text.delete(1.0, tk.END)
        
        if block:
            timestamp_str = datetime.fromtimestamp(block.timestamp).strftime("%Y-%m-%d %H:%M:%S")
            issued_str = datetime.fromtimestamp(block.issued_at).strftime("%Y-%m-%d %H:%M:%S")
            
            # Kiểm tra chữ ký số
            signature_result = self.blockchain.verify_certificate_signature_by_nft(nft_id, self.key_manager)
            
            self.verify_text.insert(tk.END, "🔍 KẾT QUẢ XÁC THỰC CHỨNG CHỈ\n\n")
            self.verify_text.insert(tk.END, "=" * 70 + "\n")
            
            # Thông tin chứng chỉ
            self.verify_text.insert(tk.END, "📋 THÔNG TIN CHỨNG CHỈ:\n")
            self.verify_text.insert(tk.END, f"NFT ID:              {block.nft_id}\n")
            self.verify_text.insert(tk.END, f"Sinh viên:           {block.student_name}\n")
            self.verify_text.insert(tk.END, f"Chứng chỉ:           {block.certificate_name}\n")
            self.verify_text.insert(tk.END, f"Đơn vị cấp:          {block.issuer_name or block.issuer}\n")
            self.verify_text.insert(tk.END, f"Mã đơn vị:           {block.issuer_id}\n")
            self.verify_text.insert(tk.END, f"Thời gian cấp:       {issued_str}\n")
            self.verify_text.insert(tk.END, f"Khối số:             {block.index}\n")
            
            # Trạng thái chứng chỉ
            self.verify_text.insert(tk.END, "\n🏷️  TRẠNG THÁI:\n")
            if block.status == "valid":
                self.verify_text.insert(tk.END, f"Trạng thái:          ✅ HỢP LỆ\n")
            else:
                self.verify_text.insert(tk.END, f"Trạng thái:          ❌ ĐÃ THU HỒI\n")
                if block.revoked_at:
                    revoked_str = datetime.fromtimestamp(block.revoked_at).strftime("%Y-%m-%d %H:%M:%S")
                    self.verify_text.insert(tk.END, f"Thời gian thu hồi:   {revoked_str}\n")
                    self.verify_text.insert(tk.END, f"Lý do thu hồi:       {block.revoke_reason}\n")
            
            # Xác thực blockchain
            self.verify_text.insert(tk.END, "\n🔗 XÁC THỰC BLOCKCHAIN:\n")
            is_chain_valid = self.blockchain.is_chain_valid()
            if is_chain_valid:
                self.verify_text.insert(tk.END, f"Blockchain:          ✅ HỢP LỆ\n")
            else:
                self.verify_text.insert(tk.END, f"Blockchain:          ❌ KHÔNG HỢP LỆ\n")
            
            # Xác thực chữ ký số
            self.verify_text.insert(tk.END, "\n🔐 XÁC THỰC CHỮ KÝ SỐ:\n")
            if signature_result["signature_valid"]:
                self.verify_text.insert(tk.END, f"Chữ ký số:           ✅ HỢP LỆ\n")
            elif not block.signature:
                self.verify_text.insert(tk.END, f"Chữ ký số:           ⚠️  CHƯA CÓ (Chứng chỉ cũ)\n")
            else:
                self.verify_text.insert(tk.END, f"Chữ ký số:           ❌ KHÔNG HỢP LỆ\n")
            
            # Thông tin kỹ thuật
            self.verify_text.insert(tk.END, "\n🔧 THÔNG TIN KỸ THUẬT:\n")
            self.verify_text.insert(tk.END, f"Hash:                {block.hash}\n")
            self.verify_text.insert(tk.END, f"Previous Hash:       {block.previous_hash}\n")
            self.verify_text.insert(tk.END, f"Nonce:               {block.nonce}\n")
            self.verify_text.insert(tk.END, f"Timestamp:           {timestamp_str}\n")
            self.verify_text.insert(tk.END, "=" * 70 + "\n")
            
            # Kết luận
            if block.status == "valid" and is_chain_valid and (signature_result["signature_valid"] or not block.signature):
                self.verify_text.insert(tk.END, "\n🎉 KẾT LUẬN: CHỨNG CHỈ HOÀN TOÀN HỢP LỆ!\n")
                messagebox.showinfo("Xác thực", "Chứng chỉ hoàn toàn hợp lệ!")
            else:
                self.verify_text.insert(tk.END, "\n⚠️  KẾT LUẬN: CHỨNG CHỈ CÓ VẤN ĐỀ!\n")
                messagebox.showwarning("Cảnh báo", "Chứng chỉ có vấn đề!")
                
        else:
            self.verify_text.insert(tk.END, "❌ KHÔNG TÌM THẤY CHỨNG CHỈ!\n\n")
            self.verify_text.insert(tk.END, f"NFT ID '{nft_id}' không tồn tại trong hệ thống.\n")
            self.verify_text.insert(tk.END, "Vui lòng kiểm tra lại mã NFT ID.\n")
            
            messagebox.showwarning("Không tìm thấy", "NFT ID không tồn tại!")
    
    def check_security(self):
        """
        Kiểm tra tính toàn vẹn của blockchain với thông tin chi tiết
        """
        self.security_text.delete(1.0, tk.END)
        self.security_text.insert(tk.END, "🔍 Đang kiểm tra tính toàn vẹn của Blockchain...\n\n")
        self.root.update()
        
        # Kiểm tra chi tiết
        result = self.blockchain.validate_chain_detailed()
        
        self.security_text.delete(1.0, tk.END)
        
        if result["is_valid"]:
            self.security_text.insert(tk.END, "✅ HỆ THỐNG AN TOÀN!\n\n")
            self.security_text.insert(tk.END, "Blockchain đã được xác thực thành công.\n")
            self.security_text.insert(tk.END, "Tất cả các khối đều hợp lệ và liên kết đúng.\n")
            self.security_text.insert(tk.END, "Không phát hiện dấu hiệu can thiệp hoặc giả mạo.\n\n")
            
            self.security_text.insert(tk.END, "📊 CHI TIẾT KIỂM TRA:\n")
            self.security_text.insert(tk.END, f"- Tổng số khối: {result['total_blocks']}\n")
            self.security_text.insert(tk.END, f"- Khối đã kiểm tra: {result['checked_blocks']}\n")
            self.security_text.insert(tk.END, f"- Độ khó (Difficulty): {self.blockchain.difficulty}\n")
            self.security_text.insert(tk.END, f"- Tất cả hash đều hợp lệ ✓\n")
            self.security_text.insert(tk.END, f"- Tất cả liên kết đều chính xác ✓\n")
            self.security_text.insert(tk.END, f"- Proof of Work đã được xác thực ✓\n")
            
            # Kiểm tra chữ ký số
            self.security_text.insert(tk.END, "\n🔐 KIỂM TRA CHỮ KÝ SỐ:\n")
            signed_count = 0
            valid_signatures = 0
            
            for block in self.blockchain.chain[1:]:  # Bỏ Genesis block
                if block.signature and block.issuer_id:
                    signed_count += 1
                    sig_result = self.blockchain.verify_certificate_signature_by_nft(
                        block.nft_id, self.key_manager
                    )
                    if sig_result["signature_valid"]:
                        valid_signatures += 1
            
            self.security_text.insert(tk.END, f"- Chứng chỉ có chữ ký: {signed_count}\n")
            self.security_text.insert(tk.END, f"- Chữ ký hợp lệ: {valid_signatures}\n")
            
            messagebox.showinfo("Bảo mật", "Hệ thống an toàn và toàn vẹn!")
        else:
            self.security_text.insert(tk.END, "❌ CẢNH BÁO: HỆ THỐNG BỊ XÂM PHẠM!\n\n")
            self.security_text.insert(tk.END, "Blockchain đã bị thay đổi hoặc giả mạo.\n\n")
            
            self.security_text.insert(tk.END, "🚨 CHI TIẾT LỖI:\n")
            for error in result["errors"]:
                self.security_text.insert(tk.END, f"- {error}\n")
            
            self.security_text.insert(tk.END, f"\nTổng số lỗi: {len(result['errors'])}\n")
            self.security_text.insert(tk.END, "Vui lòng kiểm tra lại dữ liệu hoặc khôi phục từ backup.\n")
            
            messagebox.showerror("Cảnh báo Bảo mật", "Blockchain không hợp lệ!")
    
    def update_system_info(self):
        """
        Cập nhật thông tin hệ thống
        """
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, "📊 THÔNG TIN HỆ THỐNG\n")
        self.info_text.insert(tk.END, "=" * 60 + "\n")
        
        stats = self.blockchain.get_dashboard_stats()
        self.info_text.insert(tk.END, f"Tổng số khối:        {stats['total_blocks']}\n")
        self.info_text.insert(tk.END, f"Tổng chứng chỉ:      {stats['total_certificates']}\n")
        self.info_text.insert(tk.END, f"Chứng chỉ hợp lệ:    {stats['valid_certificates']}\n")
        self.info_text.insert(tk.END, f"Chứng chỉ thu hồi:   {stats['revoked_certificates']}\n")
        self.info_text.insert(tk.END, f"Độ khó (Difficulty): {stats['difficulty']}\n")
        self.info_text.insert(tk.END, f"Số đơn vị cấp:       {stats['total_issuers']}\n")
        
        if self.blockchain.chain:
            latest_block = self.blockchain.get_latest_block()
            timestamp_str = datetime.fromtimestamp(latest_block.timestamp).strftime("%Y-%m-%d %H:%M:%S")
            self.info_text.insert(tk.END, f"Khối mới nhất:       #{latest_block.index}\n")
            self.info_text.insert(tk.END, f"Cập nhật cuối:       {timestamp_str}\n")
        
        self.info_text.insert(tk.END, "=" * 60 + "\n")


def main():
    """
    Hàm chính để khởi chạy ứng dụng
    """
    root = tk.Tk()
    app = CertificateApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
