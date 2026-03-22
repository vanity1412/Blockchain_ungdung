"""
Module Key Manager - Quản lý khóa RSA cho từng đơn vị cấp chứng chỉ
"""
import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from typing import Dict, Optional


class KeyManager:
    """
    Lớp quản lý khóa RSA cho các đơn vị cấp chứng chỉ
    """
    def __init__(self, keys_dir: str = "keys"):
        self.keys_dir = keys_dir
        self.ensure_keys_directory()
        self.issuers = {
            "HCMUS": "Trường Đại học Khoa học Tự nhiên - ĐHQG-HCM",
            "HCMUT": "Trường Đại học Bách khoa - ĐHQG-HCM", 
            "HCMIU": "Trường Đại học Quốc tế - ĐHQG-HCM",
            "UIT": "Trường Đại học Công nghệ Thông tin - ĐHQG-HCM",
            "USSH": "Trường Đại học Khoa học Xã hội và Nhân văn - ĐHQG-HCM",
            "UEL": "Trường Đại học Kinh tế - Luật - ĐHQG-HCM"
        }
        self.ensure_all_issuer_keys()
    
    def ensure_keys_directory(self):
        """Tạo thư mục keys nếu chưa tồn tại"""
        if not os.path.exists(self.keys_dir):
            os.makedirs(self.keys_dir)
            print(f"Đã tạo thư mục {self.keys_dir}")
    
    def get_issuer_name(self, issuer_id: str) -> str:
        """Lấy tên đầy đủ của đơn vị cấp"""
        return self.issuers.get(issuer_id, issuer_id)
    
    def get_all_issuers(self) -> Dict[str, str]:
        """Lấy danh sách tất cả đơn vị cấp"""
        return self.issuers.copy()
    
    def generate_key_pair(self, issuer_id: str) -> bool:
        """
        Tạo cặp khóa RSA mới cho đơn vị cấp
        """
        try:
            # Tạo private key
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
            
            # Lấy public key
            public_key = private_key.public_key()
            
            # Serialize private key
            private_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            
            # Serialize public key
            public_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            
            # Lưu private key
            private_path = os.path.join(self.keys_dir, f"{issuer_id}_private.pem")
            with open(private_path, 'wb') as f:
                f.write(private_pem)
            
            # Lưu public key
            public_path = os.path.join(self.keys_dir, f"{issuer_id}_public.pem")
            with open(public_path, 'wb') as f:
                f.write(public_pem)
            
            print(f"Đã tạo cặp khóa cho {issuer_id}")
            return True
            
        except Exception as e:
            print(f"Lỗi khi tạo khóa cho {issuer_id}: {e}")
            return False
    
    def load_private_key(self, issuer_id: str):
        """
        Tải private key của đơn vị cấp
        """
        try:
            private_path = os.path.join(self.keys_dir, f"{issuer_id}_private.pem")
            if not os.path.exists(private_path):
                return None
            
            with open(private_path, 'rb') as f:
                private_key = serialization.load_pem_private_key(
                    f.read(),
                    password=None
                )
            return private_key
            
        except Exception as e:
            print(f"Lỗi khi tải private key cho {issuer_id}: {e}")
            return None
    
    def load_public_key(self, issuer_id: str):
        """
        Tải public key của đơn vị cấp
        """
        try:
            public_path = os.path.join(self.keys_dir, f"{issuer_id}_public.pem")
            if not os.path.exists(public_path):
                return None
            
            with open(public_path, 'rb') as f:
                public_key = serialization.load_pem_public_key(f.read())
            return public_key
            
        except Exception as e:
            print(f"Lỗi khi tải public key cho {issuer_id}: {e}")
            return None
    
    def has_keys(self, issuer_id: str) -> bool:
        """
        Kiểm tra xem đơn vị cấp đã có cặp khóa chưa
        """
        private_path = os.path.join(self.keys_dir, f"{issuer_id}_private.pem")
        public_path = os.path.join(self.keys_dir, f"{issuer_id}_public.pem")
        return os.path.exists(private_path) and os.path.exists(public_path)
    
    def ensure_issuer_keys_exist(self, issuer_id: str) -> bool:
        """
        Đảm bảo đơn vị cấp có cặp khóa, tạo mới nếu chưa có
        """
        if not self.has_keys(issuer_id):
            return self.generate_key_pair(issuer_id)
        return True
    
    def ensure_all_issuer_keys(self):
        """
        Đảm bảo tất cả đơn vị cấp đều có cặp khóa
        """
        for issuer_id in self.issuers.keys():
            self.ensure_issuer_keys_exist(issuer_id)
    
    def get_keys_status(self) -> Dict[str, bool]:
        """
        Lấy trạng thái khóa của tất cả đơn vị cấp
        """
        status = {}
        for issuer_id in self.issuers.keys():
            status[issuer_id] = self.has_keys(issuer_id)
        return status