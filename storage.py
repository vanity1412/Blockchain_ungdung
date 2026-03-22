"""
Module Storage - Quản lý lưu trữ và tải dữ liệu Blockchain
"""
import os
import json
import shutil
from datetime import datetime
from blockchain import Blockchain


class BlockchainStorage:
    """
    Lớp quản lý việc lưu trữ và tải Blockchain từ file
    """
    def __init__(self, filename: str = "blockchain.json"):
        self.filename = filename
        self.backup_dir = "backups"
        self.ensure_backup_directory()
    
    def ensure_backup_directory(self):
        """Tạo thư mục backup nếu chưa tồn tại"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def save(self, blockchain: Blockchain) -> bool:
        """
        Lưu Blockchain vào file JSON
        """
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                f.write(blockchain.to_json())
            return True
        except Exception as e:
            print(f"Lỗi khi lưu blockchain: {e}")
            return False
    
    def load(self) -> Blockchain:
        """
        Tải Blockchain từ file JSON với backward compatibility
        Nếu file không tồn tại, tạo blockchain mới với Genesis Block
        """
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    json_str = f.read()
                    blockchain = Blockchain.from_json(json_str)
                    print(f"Đã tải {len(blockchain.chain)} khối từ file")
                    return blockchain
            except Exception as e:
                print(f"Lỗi khi tải blockchain: {e}")
                print("Tạo blockchain mới...")
                return self._create_new_blockchain()
        else:
            print("File blockchain không tồn tại. Tạo blockchain mới...")
            return self._create_new_blockchain()
    
    def _create_new_blockchain(self) -> Blockchain:
        """
        Tạo blockchain mới với Genesis Block
        """
        blockchain = Blockchain(difficulty=3)
        genesis_block = blockchain.create_genesis_block()
        blockchain.chain.append(genesis_block)
        self.save(blockchain)
        return blockchain
    
    def backup_blockchain(self, custom_name: str = "") -> str:
        """
        Tạo bản sao lưu của blockchain
        Trả về đường dẫn file backup
        """
        try:
            if not os.path.exists(self.filename):
                raise FileNotFoundError("File blockchain không tồn tại")
            
            # Tạo tên file backup
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if custom_name:
                backup_filename = f"blockchain_backup_{custom_name}_{timestamp}.json"
            else:
                backup_filename = f"blockchain_backup_{timestamp}.json"
            
            backup_path = os.path.join(self.backup_dir, backup_filename)
            
            # Copy file
            shutil.copy2(self.filename, backup_path)
            print(f"Đã tạo backup: {backup_path}")
            
            return backup_path
            
        except Exception as e:
            print(f"Lỗi khi tạo backup: {e}")
            return ""
    
    def restore_blockchain(self, backup_path: str) -> bool:
        """
        Khôi phục blockchain từ file backup
        """
        try:
            if not os.path.exists(backup_path):
                raise FileNotFoundError(f"File backup không tồn tại: {backup_path}")
            
            # Tạo backup của file hiện tại trước khi restore
            if os.path.exists(self.filename):
                current_backup = self.backup_blockchain("before_restore")
                print(f"Đã backup file hiện tại: {current_backup}")
            
            # Copy file backup thành file chính
            shutil.copy2(backup_path, self.filename)
            print(f"Đã khôi phục từ: {backup_path}")
            
            # Kiểm tra tính hợp lệ của file đã restore
            test_blockchain = self.load()
            if len(test_blockchain.chain) > 0:
                print("Khôi phục thành công!")
                return True
            else:
                raise ValueError("File backup không hợp lệ")
                
        except Exception as e:
            print(f"Lỗi khi khôi phục: {e}")
            return False
    
    def list_backups(self) -> list:
        """
        Liệt kê tất cả file backup có sẵn
        """
        try:
            if not os.path.exists(self.backup_dir):
                return []
            
            backups = []
            for filename in os.listdir(self.backup_dir):
                if filename.startswith("blockchain_backup_") and filename.endswith(".json"):
                    filepath = os.path.join(self.backup_dir, filename)
                    stat = os.stat(filepath)
                    backups.append({
                        "filename": filename,
                        "filepath": filepath,
                        "size": stat.st_size,
                        "modified": datetime.fromtimestamp(stat.st_mtime)
                    })
            
            # Sắp xếp theo thời gian sửa đổi (mới nhất trước)
            backups.sort(key=lambda x: x["modified"], reverse=True)
            return backups
            
        except Exception as e:
            print(f"Lỗi khi liệt kê backup: {e}")
            return []
    
    def file_exists(self) -> bool:
        """
        Kiểm tra xem file blockchain có tồn tại không
        """
        return os.path.exists(self.filename)
    
    def get_file_info(self) -> dict:
        """
        Lấy thông tin về file blockchain
        """
        try:
            if not os.path.exists(self.filename):
                return {"exists": False}
            
            stat = os.stat(self.filename)
            return {
                "exists": True,
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime),
                "path": os.path.abspath(self.filename)
            }
        except Exception as e:
            print(f"Lỗi khi lấy thông tin file: {e}")
            return {"exists": False, "error": str(e)}
