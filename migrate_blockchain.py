"""
Migration script: Tinh lai hash va re-mine tat ca block trong blockchain.json
theo cong thuc moi (khong co 'status' trong calculate_hash).

Chay 1 lan duy nhat sau khi cap nhat blockchain.py (fix BUG-01).
"""
import json
import hashlib
import sys
import os

BLOCKCHAIN_FILE = "blockchain.json"
BACKUP_FILE = "blockchain_premigration_backup.json"


def calculate_hash_new(block_data: dict) -> str:
    """Cong thuc hash MOI - khong co 'status'."""
    payload = {
        "index": block_data["index"],
        "timestamp": block_data["timestamp"],
        "student_name": block_data["student_name"],
        "certificate_name": block_data["certificate_name"],
        "issuer": block_data["issuer"],
        "nft_id": block_data["nft_id"],
        "previous_hash": block_data["previous_hash"],
        "nonce": block_data["nonce"],
        "issued_at": block_data.get("issued_at", block_data["timestamp"]),
        "issuer_id": block_data.get("issuer_id", ""),
        "issuer_name": block_data.get("issuer_name", ""),
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


def mine_block(block_data: dict, difficulty: int) -> dict:
    """Tim nonce de hash bat dau bang '0' * difficulty."""
    block_data["nonce"] = 0
    target = "0" * difficulty
    h = calculate_hash_new(block_data)
    while not h.startswith(target):
        block_data["nonce"] += 1
        h = calculate_hash_new(block_data)
    block_data["hash"] = h
    return block_data


def migrate():
    if not os.path.exists(BLOCKCHAIN_FILE):
        print(f"Khong tim thay {BLOCKCHAIN_FILE}. Bo qua.")
        return

    # Doc du lieu hien tai
    with open(BLOCKCHAIN_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    difficulty = data.get("difficulty", 3)
    chain = data["chain"]
    total = len(chain)

    print(f"Tim thay {total} block, difficulty={difficulty}")
    print("Tao backup truoc khi migration...")

    # Backup truoc
    with open(BACKUP_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Da luu backup: {BACKUP_FILE}")

    print("Bat dau re-mine...")
    new_chain = []

    for i, block in enumerate(chain):
        # Cap nhat previous_hash tu block truoc da duoc cap nhat
        if i > 0:
            block["previous_hash"] = new_chain[i - 1]["hash"]

        # Giu nguyen status va cac metadata khac
        status = block.get("status", "valid")

        print(f"  Block {i} ({block.get('student_name','?')}) - status={status} - mining...", end=" ", flush=True)
        block = mine_block(block, difficulty)
        print(f"nonce={block['nonce']}, hash={block['hash'][:12]}...")

        new_chain.append(block)

    # Luu lai
    output = {"difficulty": difficulty, "chain": new_chain}
    with open(BLOCKCHAIN_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nMigration thanh cong! Da cap nhat {total} block.")
    print(f"Backup cu luu tai: {BACKUP_FILE}")


if __name__ == "__main__":
    migrate()
