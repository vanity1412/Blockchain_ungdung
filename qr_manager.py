"""
Module QR Manager - Tạo và quản lý QR code cho chứng chỉ
"""
import os
import qrcode
from PIL import Image
from typing import Optional


class QRManager:
    """
    Lớp quản lý tạo QR code cho chứng chỉ
    """
    def __init__(self, export_dir: str = "exports"):
        self.export_dir = export_dir
        self.ensure_export_directory()
    
    def ensure_export_directory(self):
        """Tạo thư mục exports nếu chưa tồn tại"""
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)
            print(f"Đã tạo thư mục {self.export_dir}")
    
    def generate_qr_code(self, nft_id: str, student_name: str = "") -> Optional[str]:
        """
        Tạo QR code cho chứng chỉ
        Trả về đường dẫn file QR code đã tạo
        """
        try:
            # Tạo dữ liệu cho QR code
            qr_data = f"NFT_ID:{nft_id}"
            if student_name:
                qr_data += f"|STUDENT:{student_name}"
            
            # Tạo QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            # Tạo hình ảnh
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Tên file
            safe_name = nft_id.replace("-", "_")
            filename = f"QR_{safe_name}.png"
            filepath = os.path.join(self.export_dir, filename)
            
            # Lưu file
            img.save(filepath)
            print(f"Đã tạo QR code: {filepath}")
            
            return filepath
            
        except Exception as e:
            print(f"Lỗi khi tạo QR code: {e}")
            return None
    
    def generate_verification_url_qr(self, nft_id: str, base_url: str = "https://verify.certificate.edu.vn") -> Optional[str]:
        """
        Tạo QR code chứa URL xác thực chứng chỉ
        """
        try:
            # URL xác thực
            verify_url = f"{base_url}/verify?nft_id={nft_id}"
            
            # Tạo QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(verify_url)
            qr.make(fit=True)
            
            # Tạo hình ảnh
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Tên file
            safe_name = nft_id.replace("-", "_")
            filename = f"QR_URL_{safe_name}.png"
            filepath = os.path.join(self.export_dir, filename)
            
            # Lưu file
            img.save(filepath)
            print(f"Đã tạo QR code URL: {filepath}")
            
            return filepath
            
        except Exception as e:
            print(f"Lỗi khi tạo QR code URL: {e}")
            return None