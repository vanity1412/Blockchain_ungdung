"""
Module NFT Manager - Quản lý việc tạo NFT ID duy nhất cho chứng chỉ
"""
import uuid


class NFTManager:
    """
    Lớp quản lý việc tạo và xác thực NFT ID
    """
    @staticmethod
    def generate_nft_id() -> str:
        """
        Tạo một NFT ID duy nhất sử dụng UUID4
        """
        return f"NFT-{uuid.uuid4().hex[:16].upper()}"
    
    @staticmethod
    def is_valid_nft_format(nft_id: str) -> bool:
        """
        Kiểm tra định dạng NFT ID có hợp lệ không
        """
        if not nft_id:
            return False
        
        # NFT ID phải bắt đầu với "NFT-" và có độ dài phù hợp
        if nft_id.startswith("NFT-") and len(nft_id) == 20:
            return True
        
        # Cho phép Genesis NFT
        if nft_id == "GENESIS-0000":
            return True
        
        return False
