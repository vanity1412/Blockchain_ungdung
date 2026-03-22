"""
Module Signature Utils - Xử lý ký và xác thực chữ ký số
"""
import base64
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from typing import Dict, Optional


class SignatureUtils:
    """
    Lớp xử lý chữ ký số cho chứng chỉ
    """
    
    @staticmethod
    def build_sign_payload(student_name: str, certificate_name: str, 
                          issuer_id: str, issuer_name: str, nft_id: str, 
                          issued_at: float) -> str:
        """
        Tạo payload chuẩn để ký từ thông tin chứng chỉ
        """
        payload = {
            "student_name": student_name,
            "certificate_name": certificate_name,
            "issuer_id": issuer_id,
            "issuer_name": issuer_name,
            "nft_id": nft_id,
            "issued_at": issued_at
        }
        return json.dumps(payload, sort_keys=True, ensure_ascii=False)
    
    @staticmethod
    def sign_certificate_data(private_key, payload: str) -> Optional[str]:
        """
        Ký dữ liệu chứng chỉ bằng private key
        Trả về chữ ký dưới dạng base64
        """
        try:
            if private_key is None:
                return None
            
            # Chuyển payload thành bytes
            payload_bytes = payload.encode('utf-8')
            
            # Ký dữ liệu
            signature = private_key.sign(
                payload_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            
            # Chuyển thành base64 để lưu trữ
            return base64.b64encode(signature).decode('utf-8')
            
        except Exception as e:
            print(f"Lỗi khi ký dữ liệu: {e}")
            return None
    
    @staticmethod
    def verify_certificate_signature(public_key, payload: str, signature: str) -> bool:
        """
        Xác thực chữ ký của chứng chỉ
        """
        try:
            if public_key is None or not signature:
                return False
            
            # Chuyển payload thành bytes
            payload_bytes = payload.encode('utf-8')
            
            # Decode signature từ base64
            signature_bytes = base64.b64decode(signature.encode('utf-8'))
            
            # Xác thực chữ ký
            public_key.verify(
                signature_bytes,
                payload_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            
            return True
            
        except Exception as e:
            print(f"Lỗi khi xác thực chữ ký: {e}")
            return False
    
    @staticmethod
    def create_certificate_signature(key_manager, student_name: str, 
                                   certificate_name: str, issuer_id: str, 
                                   nft_id: str, issued_at: float) -> Optional[str]:
        """
        Tạo chữ ký cho chứng chỉ mới
        """
        try:
            # Lấy tên đầy đủ của đơn vị cấp
            issuer_name = key_manager.get_issuer_name(issuer_id)
            
            # Tạo payload để ký
            payload = SignatureUtils.build_sign_payload(
                student_name, certificate_name, issuer_id, 
                issuer_name, nft_id, issued_at
            )
            
            # Lấy private key
            private_key = key_manager.load_private_key(issuer_id)
            if private_key is None:
                print(f"Không tìm thấy private key cho {issuer_id}")
                return None
            
            # Ký dữ liệu
            signature = SignatureUtils.sign_certificate_data(private_key, payload)
            return signature
            
        except Exception as e:
            print(f"Lỗi khi tạo chữ ký: {e}")
            return None
    
    @staticmethod
    def verify_certificate_by_data(key_manager, student_name: str, 
                                 certificate_name: str, issuer_id: str, 
                                 nft_id: str, issued_at: float, 
                                 signature: str) -> bool:
        """
        Xác thực chữ ký của chứng chỉ theo dữ liệu
        """
        try:
            if not signature:
                return False
            
            # Lấy tên đầy đủ của đơn vị cấp
            issuer_name = key_manager.get_issuer_name(issuer_id)
            
            # Tạo payload để xác thực
            payload = SignatureUtils.build_sign_payload(
                student_name, certificate_name, issuer_id, 
                issuer_name, nft_id, issued_at
            )
            
            # Lấy public key
            public_key = key_manager.load_public_key(issuer_id)
            if public_key is None:
                print(f"Không tìm thấy public key cho {issuer_id}")
                return False
            
            # Xác thực chữ ký
            return SignatureUtils.verify_certificate_signature(
                public_key, payload, signature
            )
            
        except Exception as e:
            print(f"Lỗi khi xác thực chữ ký: {e}")
            return False