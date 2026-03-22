"""
Module Blockchain - Quản lý chuỗi khối và cơ chế đồng thuận
"""
import hashlib
import json
import time
from typing import List, Dict, Optional


class Block:
    """
    Lớp Block đại diện cho một khối trong chuỗi Blockchain
    """
    def __init__(self, index: int, timestamp: float, student_name: str, 
                 certificate_name: str, issuer: str, nft_id: str, 
                 previous_hash: str, nonce: int = 0, issued_at: float = None,
                 issuer_id: str = "", issuer_name: str = "", signature: str = "",
                 status: str = "valid", revoked_at: float = 0, revoke_reason: str = ""):
        self.index = index
        self.timestamp = timestamp
        self.student_name = student_name
        self.certificate_name = certificate_name
        self.issuer = issuer  # Giữ để backward compatibility
        self.nft_id = nft_id
        self.previous_hash = previous_hash
        self.nonce = nonce
        
        # Các field mới
        self.issued_at = issued_at if issued_at is not None else timestamp
        self.issuer_id = issuer_id
        self.issuer_name = issuer_name
        self.signature = signature
        self.status = status
        self.revoked_at = revoked_at
        self.revoke_reason = revoke_reason
        
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """
        Tính toán mã băm SHA-256 cho khối dựa trên các thuộc tính cốt lõi
        Không bao gồm signature để tránh circular dependency
        """
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "student_name": self.student_name,
            "certificate_name": self.certificate_name,
            "issuer": self.issuer,
            "nft_id": self.nft_id,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "issued_at": self.issued_at,
            "issuer_id": self.issuer_id,
            "issuer_name": self.issuer_name,
            "status": self.status
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int):
        """
        Đào khối với độ khó được chỉ định (Proof of Work)
        Hash phải bắt đầu với số lượng số 0 tương ứng với difficulty
        """
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
    
    def to_dict(self) -> Dict:
        """
        Chuyển đổi Block thành dictionary để lưu trữ
        """
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "student_name": self.student_name,
            "certificate_name": self.certificate_name,
            "issuer": self.issuer,
            "nft_id": self.nft_id,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash,
            "issued_at": self.issued_at,
            "issuer_id": self.issuer_id,
            "issuer_name": self.issuer_name,
            "signature": self.signature,
            "status": self.status,
            "revoked_at": self.revoked_at,
            "revoke_reason": self.revoke_reason
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Block':
        """
        Tạo Block từ dictionary với backward compatibility
        """
        block = Block(
            index=data["index"],
            timestamp=data["timestamp"],
            student_name=data["student_name"],
            certificate_name=data["certificate_name"],
            issuer=data["issuer"],
            nft_id=data["nft_id"],
            previous_hash=data["previous_hash"],
            nonce=data["nonce"],
            issued_at=data.get("issued_at", data["timestamp"]),
            issuer_id=data.get("issuer_id", ""),
            issuer_name=data.get("issuer_name", ""),
            signature=data.get("signature", ""),
            status=data.get("status", "valid"),
            revoked_at=data.get("revoked_at", 0),
            revoke_reason=data.get("revoke_reason", "")
        )
        block.hash = data["hash"]
        return block


class Blockchain:
    """
    Lớp Blockchain quản lý chuỗi các khối
    """
    def __init__(self, difficulty: int = 3):
        self.chain: List[Block] = []
        self.difficulty = difficulty
    
    def create_genesis_block(self) -> Block:
        """
        Tạo khối nguyên thủy (Genesis Block) - khối đầu tiên trong chuỗi
        """
        genesis_block = Block(
            index=0,
            timestamp=time.time(),
            student_name="Genesis",
            certificate_name="Genesis Certificate",
            issuer="System",
            nft_id="GENESIS-0000",
            previous_hash="0"
        )
        genesis_block.mine_block(self.difficulty)
        return genesis_block
    
    def get_latest_block(self) -> Block:
        """
        Lấy khối mới nhất trong chuỗi
        """
        return self.chain[-1] if self.chain else None
    
    def add_block(self, student_name: str, certificate_name: str, 
                  issuer: str, nft_id: str, issuer_id: str = "", 
                  issuer_name: str = "", signature: str = "") -> Block:
        """
        Thêm một khối mới vào chuỗi với thông tin chứng chỉ
        """
        latest_block = self.get_latest_block()
        issued_at = time.time()
        
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            student_name=student_name,
            certificate_name=certificate_name,
            issuer=issuer,
            nft_id=nft_id,
            previous_hash=latest_block.hash if latest_block else "0",
            issued_at=issued_at,
            issuer_id=issuer_id,
            issuer_name=issuer_name,
            signature=signature
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        return new_block
    
    def is_chain_valid(self) -> bool:
        """
        Kiểm tra tính toàn vẹn của chuỗi Blockchain
        Xác thực mã băm và liên kết giữa các khối
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Kiểm tra mã băm của khối hiện tại
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Kiểm tra liên kết với khối trước
            if current_block.previous_hash != previous_block.hash:
                return False
            
            # Kiểm tra Proof of Work
            if not current_block.hash.startswith("0" * self.difficulty):
                return False
        
        return True
    
    def find_certificate_by_nft(self, nft_id: str) -> Optional[Block]:
        """
        Tìm kiếm chứng chỉ theo NFT ID
        """
        for block in self.chain:
            if block.nft_id == nft_id:
                return block
        return None
    
    def revoke_certificate(self, nft_id: str, reason: str) -> bool:
        """
        Thu hồi chứng chỉ theo NFT ID
        """
        block = self.find_certificate_by_nft(nft_id)
        if block and block.status == "valid":
            block.status = "revoked"
            block.revoked_at = time.time()
            block.revoke_reason = reason
            return True
        return False
    
    def find_by_student_name(self, student_name: str) -> List[Block]:
        """
        Tìm kiếm chứng chỉ theo tên sinh viên
        """
        results = []
        for block in self.chain:
            if student_name.lower() in block.student_name.lower():
                results.append(block)
        return results
    
    def find_by_certificate_name(self, certificate_name: str) -> List[Block]:
        """
        Tìm kiếm chứng chỉ theo tên chứng chỉ
        """
        results = []
        for block in self.chain:
            if certificate_name.lower() in block.certificate_name.lower():
                results.append(block)
        return results
    
    def find_by_issuer(self, issuer: str) -> List[Block]:
        """
        Tìm kiếm chứng chỉ theo đơn vị cấp
        """
        results = []
        for block in self.chain:
            if (issuer.lower() in block.issuer.lower() or 
                issuer.lower() in block.issuer_id.lower() or
                issuer.lower() in block.issuer_name.lower()):
                results.append(block)
        return results
    
    def filter_by_status(self, status: str) -> List[Block]:
        """
        Lọc chứng chỉ theo trạng thái
        """
        results = []
        for block in self.chain:
            if block.status == status:
                results.append(block)
        return results
    
    def get_dashboard_stats(self) -> Dict:
        """
        Lấy thống kê tổng quan cho dashboard
        """
        total_certificates = len(self.chain) - 1  # Trừ Genesis block
        valid_certificates = len(self.filter_by_status("valid")) - 1  # Trừ Genesis
        revoked_certificates = len(self.filter_by_status("revoked"))
        
        # Đếm số đơn vị cấp
        issuers = set()
        for block in self.chain[1:]:  # Bỏ Genesis block
            if block.issuer_id:
                issuers.add(block.issuer_id)
            else:
                issuers.add(block.issuer)
        
        return {
            "total_blocks": len(self.chain),
            "total_certificates": total_certificates,
            "valid_certificates": valid_certificates,
            "revoked_certificates": revoked_certificates,
            "difficulty": self.difficulty,
            "total_issuers": len(issuers)
        }
    
    def validate_chain_detailed(self) -> Dict:
        """
        Kiểm tra tính toàn vẹn của chuỗi với thông tin chi tiết
        """
        result = {
            "is_valid": True,
            "errors": [],
            "total_blocks": len(self.chain),
            "checked_blocks": 0
        }
        
        for i in range(len(self.chain)):
            current_block = self.chain[i]
            result["checked_blocks"] += 1
            
            # Kiểm tra hash của khối hiện tại
            if current_block.hash != current_block.calculate_hash():
                result["is_valid"] = False
                result["errors"].append(f"Block {i}: Hash không hợp lệ")
            
            # Kiểm tra liên kết với khối trước (trừ Genesis block)
            if i > 0:
                previous_block = self.chain[i - 1]
                if current_block.previous_hash != previous_block.hash:
                    result["is_valid"] = False
                    result["errors"].append(f"Block {i}: Previous hash không khớp")
            
            # Kiểm tra Proof of Work
            if not current_block.hash.startswith("0" * self.difficulty):
                result["is_valid"] = False
                result["errors"].append(f"Block {i}: Proof of Work không hợp lệ")
        
        return result
    
    def verify_certificate_signature_by_nft(self, nft_id: str, key_manager) -> Dict:
        """
        Xác thực chữ ký số của chứng chỉ theo NFT ID
        """
        from signature_utils import SignatureUtils
        
        block = self.find_certificate_by_nft(nft_id)
        if not block:
            return {"found": False, "signature_valid": False, "error": "NFT ID không tồn tại"}
        
        if not block.signature:
            return {"found": True, "signature_valid": False, "error": "Chứng chỉ chưa có chữ ký số"}
        
        if not block.issuer_id:
            return {"found": True, "signature_valid": False, "error": "Thiếu thông tin issuer_id"}
        
        # Xác thực chữ ký
        is_valid = SignatureUtils.verify_certificate_by_data(
            key_manager, block.student_name, block.certificate_name,
            block.issuer_id, block.nft_id, block.issued_at, block.signature
        )
        
        return {
            "found": True,
            "signature_valid": is_valid,
            "issuer_id": block.issuer_id,
            "issuer_name": block.issuer_name,
            "status": block.status
        }
    
    def to_json(self) -> str:
        """
        Chuyển đổi toàn bộ chuỗi thành JSON
        """
        return json.dumps({
            "difficulty": self.difficulty,
            "chain": [block.to_dict() for block in self.chain]
        }, indent=2)
    
    @staticmethod
    def from_json(json_str: str) -> 'Blockchain':
        """
        Tạo Blockchain từ JSON
        """
        data = json.loads(json_str)
        blockchain = Blockchain(difficulty=data["difficulty"])
        blockchain.chain = [Block.from_dict(block_data) for block_data in data["chain"]]
        return blockchain
