"""
Module GUI Basic - Giao diện cơ bản không cần thư viện ngoài
"""
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from datetime import datetime
from blockchain import Blockchain
from storage import BlockchainStorage
from nft_manager import NFTManager


class CertificateAppBasic:
    """
    Ứng dụng quản lý chứng chỉ điện tử cơ bản (không cần cryptography)
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Hệ thống Quản lý Chứng chỉ Blockchain & NFT - Phiên bản Cơ bản")
        self.root.geometry("1000x700")
        
        # Khởi tạo các manager cơ bản
        self.storage = BlockchainStorage()
        self.blockchain = self.storage.load()
        self.nft_manager = NFTManager()
        
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
            text="HỆ THỐNG QUẢN LÝ CHỨNG CHỈ BLOCKCHAIN & NFT - CƠ BẢN",
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
        
        # Tab 4: Bảo mật
        self.create_security_tab()
    
    def create_issue_tab(self):
        """
        Tab cấp chứng chỉ mới
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
        
        # Đơn vị cấp
        tk.Label(form_frame, text="Đơn vị cấp:", font=("Arial", 11)).grid(row=2, column=0, sticky=tk.W, pady=10)
        self.issuer_entry = tk.Entry(form_frame, width=40, font=("Arial", 11))
        self.issuer_entry.grid(row=2, column=1, pady=10, padx=10)
        
        # Nút cấp bằng
        issue_button = tk.Button(
            form_frame,
            text="🎓 CẤP CHỨNG CHỈ",
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
        
        # Treeview
        columns = ("Index", "Timestamp", "Student", "Certificate", "Issuer", "NFT ID", "Hash")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        
        # Định nghĩa cột
        self.tree.heading("Index", text="Khối")
        self.tree.heading("Timestamp", text="Thời gian")
        self.tree.heading("Student", text="Sinh viên")
        self.tree.heading("Certificate", text="Chứng chỉ")
        self.tree.heading("Issuer", text="Đơn vị cấp")
        self.tree.heading("NFT ID", text="NFT ID")
        self.tree.heading("Hash", text="Hash")
        
        # Độ rộng cột
        self.tree.column("Index", width=50)
        self.tree.column("Timestamp", width=150)
        self.tree.column("Student", width=150)
        self.tree.column("Certificate", width=150)
        self.tree.column("Issuer", width=120)
        self.tree.column("NFT ID", width=150)
        self.tree.column("Hash", width=200)
        
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
    
    def issue_certificate(self):
        """
        Xử lý việc cấp chứng chỉ mới
        """
        student_name = self.student_name_entry.get().strip()
        certificate_name = self.certificate_name_entry.get().strip()
        issuer = self.issuer_entry.get().strip()
        
        # Kiểm tra dữ liệu đầu vào
        if not student_name or not certificate_name or not issuer:
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin!")
            return
        
        # Hiển thị thông báo đang xử lý
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "⏳ Đang đào khối (Mining)...\n")
        self.result_text.insert(tk.END, "Vui lòng đợi...\n")
        self.root.update()
        
        # Thực hiện đào khối trong thread riêng để không block GUI
        def mine_and_add():
            # Tạo NFT ID
            nft_id = self.nft_manager.generate_nft_id()
            
            # Thêm khối mới
            new_block = self.blockchain.add_block(student_name, certificate_name, issuer, nft_id)
            
            # Lưu blockchain
            self.storage.save(self.blockchain)
            
            # Cập nhật giao diện
            self.root.after(0, lambda: self.display_issue_result(new_block))
        
        threading.Thread(target=mine_and_add, daemon=True).start()
    
    def display_issue_result(self, block):
        """
        Hiển thị kết quả sau khi cấp chứng chỉ
        """
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "✅ CẤP CHỨNG CHỈ THÀNH CÔNG!\n\n")
        self.result_text.insert(tk.END, "=" * 60 + "\n")
        self.result_text.insert(tk.END, f"NFT ID:          {block.nft_id}\n")
        self.result_text.insert(tk.END, f"Sinh viên:       {block.student_name}\n")
        self.result_text.insert(tk.END, f"Chứng chỉ:       {block.certificate_name}\n")
        self.result_text.insert(tk.END, f"Đơn vị cấp:      {block.issuer}\n")
        self.result_text.insert(tk.END, f"Khối số:         {block.index}\n")
        self.result_text.insert(tk.END, f"Nonce:           {block.nonce}\n")
        self.result_text.insert(tk.END, f"Hash:            {block.hash}\n")
        self.result_text.insert(tk.END, "=" * 60 + "\n")
        
        # Xóa form
        self.student_name_entry.delete(0, tk.END)
        self.certificate_name_entry.delete(0, tk.END)
        self.issuer_entry.delete(0, tk.END)
        
        # Làm mới danh sách
        self.refresh_blockchain_view()
        self.update_system_info()
        
        messagebox.showinfo("Thành công", f"Chứng chỉ đã được cấp!\nNFT ID: {block.nft_id}")
    
    def refresh_blockchain_view(self):
        """
        Làm mới danh sách blockchain trong Treeview
        """
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Thêm dữ liệu mới
        for block in self.blockchain.chain:
            timestamp_str = datetime.fromtimestamp(block.timestamp).strftime("%Y-%m-%d %H:%M:%S")
            hash_short = block.hash[:16] + "..."
            
            self.tree.insert("", tk.END, values=(
                block.index,
                timestamp_str,
                block.student_name,
                block.certificate_name,
                block.issuer,
                block.nft_id,
                hash_short
            ))
    
    def verify_certificate(self):
        """
        Xác thực chứng chỉ theo NFT ID
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

            # BUG-04 FIX: Kiểm tra trạng thái revoke trước khi báo hợp lệ
            if block.status == "revoked":
                self.verify_text.insert(tk.END, "❌ CHỨNG CHỈ ĐÃ BỊ THU HỒI!\n\n")
                self.verify_text.insert(tk.END, "=" * 60 + "\n")
                self.verify_text.insert(tk.END, f"NFT ID:          {block.nft_id}\n")
                self.verify_text.insert(tk.END, f"Sinh viên:       {block.student_name}\n")
                self.verify_text.insert(tk.END, f"Chứng chỉ:       {block.certificate_name}\n")
                self.verify_text.insert(tk.END, f"Đơn vị cấp:      {block.issuer}\n")
                self.verify_text.insert(tk.END, f"Trạng thái:      ❌ ĐÃ THU HỒI\n")
                if block.revoked_at:
                    revoked_str = datetime.fromtimestamp(block.revoked_at).strftime("%Y-%m-%d %H:%M:%S")
                    self.verify_text.insert(tk.END, f"Thời gian thu hồi: {revoked_str}\n")
                    self.verify_text.insert(tk.END, f"Lý do thu hồi:   {block.revoke_reason}\n")
                self.verify_text.insert(tk.END, "=" * 60 + "\n")
                messagebox.showwarning("Đã thu hồi", "Chứng chỉ này đã bị thu hồi!")
            else:
                self.verify_text.insert(tk.END, "✅ CHỨNG CHỈ HỢP LỆ!\n\n")
                self.verify_text.insert(tk.END, "=" * 60 + "\n")
                self.verify_text.insert(tk.END, f"NFT ID:          {block.nft_id}\n")
                self.verify_text.insert(tk.END, f"Sinh viên:       {block.student_name}\n")
                self.verify_text.insert(tk.END, f"Chứng chỉ:       {block.certificate_name}\n")
                self.verify_text.insert(tk.END, f"Đơn vị cấp:      {block.issuer}\n")
                self.verify_text.insert(tk.END, f"Trạng thái:      ✅ HỢP LỆ\n")
                self.verify_text.insert(tk.END, f"Thời gian cấp:   {timestamp_str}\n")
                self.verify_text.insert(tk.END, f"Khối số:         {block.index}\n")
                self.verify_text.insert(tk.END, f"Hash:            {block.hash}\n")
                self.verify_text.insert(tk.END, f"Previous Hash:   {block.previous_hash}\n")
                self.verify_text.insert(tk.END, f"Nonce:           {block.nonce}\n")
                self.verify_text.insert(tk.END, "=" * 60 + "\n")
                messagebox.showinfo("Xác thực", "Chứng chỉ hợp lệ!")
        else:
            self.verify_text.insert(tk.END, "❌ KHÔNG TÌM THẤY CHỨNG CHỈ!\n\n")
            self.verify_text.insert(tk.END, f"NFT ID '{nft_id}' không tồn tại trong hệ thống.\n")
            self.verify_text.insert(tk.END, "Vui lòng kiểm tra lại mã NFT ID.\n")
            
            messagebox.showwarning("Không tìm thấy", "NFT ID không tồn tại!")
    
    def check_security(self):
        """
        Kiểm tra tính toàn vẹn của blockchain
        """
        self.security_text.delete(1.0, tk.END)
        self.security_text.insert(tk.END, "🔍 Đang kiểm tra tính toàn vẹn của Blockchain...\n\n")
        self.root.update()
        
        is_valid = self.blockchain.is_chain_valid()
        
        self.security_text.delete(1.0, tk.END)
        
        if is_valid:
            self.security_text.insert(tk.END, "✅ HỆ THỐNG AN TOÀN!\n\n")
            self.security_text.insert(tk.END, "Blockchain đã được xác thực thành công.\n")
            self.security_text.insert(tk.END, "Tất cả các khối đều hợp lệ và liên kết đúng.\n")
            self.security_text.insert(tk.END, "Không phát hiện dấu hiệu can thiệp hoặc giả mạo.\n\n")
            self.security_text.insert(tk.END, "Chi tiết kiểm tra:\n")
            self.security_text.insert(tk.END, f"- Tổng số khối: {len(self.blockchain.chain)}\n")
            self.security_text.insert(tk.END, f"- Độ khó (Difficulty): {self.blockchain.difficulty}\n")
            self.security_text.insert(tk.END, f"- Tất cả hash đều hợp lệ ✓\n")
            self.security_text.insert(tk.END, f"- Tất cả liên kết đều chính xác ✓\n")
            self.security_text.insert(tk.END, f"- Proof of Work đã được xác thực ✓\n")
            
            messagebox.showinfo("Bảo mật", "Hệ thống an toàn và toàn vẹn!")
        else:
            self.security_text.insert(tk.END, "❌ CẢNH BÁO: HỆ THỐNG BỊ XÂM PHẠM!\n\n")
            self.security_text.insert(tk.END, "Blockchain đã bị thay đổi hoặc giả mạo.\n")
            self.security_text.insert(tk.END, "Vui lòng kiểm tra lại dữ liệu.\n")
            
            messagebox.showerror("Cảnh báo Bảo mật", "Blockchain không hợp lệ!")
    
    def update_system_info(self):
        """
        Cập nhật thông tin hệ thống
        """
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, "📊 THÔNG TIN HỆ THỐNG\n")
        self.info_text.insert(tk.END, "=" * 60 + "\n")
        self.info_text.insert(tk.END, f"Tổng số khối:        {len(self.blockchain.chain)}\n")
        self.info_text.insert(tk.END, f"Tổng chứng chỉ:      {len(self.blockchain.chain) - 1}\n")
        self.info_text.insert(tk.END, f"Độ khó (Difficulty): {self.blockchain.difficulty}\n")
        
        if self.blockchain.chain:
            latest_block = self.blockchain.get_latest_block()
            timestamp_str = datetime.fromtimestamp(latest_block.timestamp).strftime("%Y-%m-%d %H:%M:%S")
            self.info_text.insert(tk.END, f"Khối mới nhất:       #{latest_block.index}\n")
            self.info_text.insert(tk.END, f"Thời gian cập nhật:  {timestamp_str}\n")
        
        self.info_text.insert(tk.END, "=" * 60 + "\n")


def main():
    """
    Hàm chính để khởi chạy ứng dụng cơ bản
    """
    root = tk.Tk()
    app = CertificateAppBasic(root)
    root.mainloop()


if __name__ == "__main__":
    main()