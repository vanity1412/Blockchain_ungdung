# Dev Log - He Thong Chung Chi Dien Tu Blockchain & NFT

Cap nhat lan cuoi: 2026-03-24 09:05

---

## Nhiem Vu & Trang Thai

1.  Thiet ke lop Block va Blockchain (SHA-256 + PoW) - Hoan thanh
2.  Cap chung chi: sinh NFT ID, ky so RSA, dao block - Hoan thanh
3.  Xac thuc chung chi theo NFT ID + kiem tra chu ky - Hoan thanh
4.  Thu hoi chung chi (revoke) - Hoan thanh
5.  Tim kiem nang cao (ten sinh vien, chung chi, don vi, trang thai) - Hoan thanh
6.  Dashboard thong ke - Hoan thanh
7.  Backup va Restore blockchain - Hoan thanh
8.  Kiem tra bao mat toan chuoi - Hoan thanh
9.  Quan ly khoa RSA tu dong cho 6 truong DHQG-HCM - Hoan thanh
10. Tao QR code cho chung chi - Hoan thanh
11. Luu tru blockchain dang JSON - Hoan thanh
12. Giao dien day du 8 tab (gui.py) + giao dien co ban (gui_basic.py) - Hoan thanh
13. Viet tai lieu README.md, overview.md, dev_log.md - Hoan thanh
14. Cai dat thu vien requirements.txt - Hoan thanh (2026-03-24)
15. Bug fix: Quet toan bo code, phat hien va fix 6 loi logic - Hoan thanh (2026-03-24)
16. Migration: Tao script re-mine blockchain.json cu cho tuong thich voi hash moi - Hoan thanh (2026-03-24)

---

## Bug Fix - 2026-03-24

BUG-01 (blockchain.py) - status trong hash lam chain bao loi sau khi revoke
    Fix: Bo status khoi calculate_hash()

BUG-02 (blockchain.py) - Dashboard hien thi so am khi khong co chung chi
    Fix: Dem lai tu chain[1:] bang sum()

BUG-03 (gui.py) - Verify bao loi sai cho chung chi hop le do BUG-01
    Fix: Tu khac phuc sau fix BUG-01

BUG-04 (gui_basic.py) - Verify bao HOP LE cho chung chi da thu hoi
    Fix: Them kiem tra block.status

BUG-05 (blockchain.py) - timestamp khac issued_at do goi time.time() hai lan
    Fix: Dung mot bien now duy nhat

BUG-06 (gui.py) - Bare except bat ca SystemExit
    Fix: Doi thanh except Exception

---

## Con Lai

- Them .gitignore (loai tru keys/, exports/, backups/, .venv/)
- Config hoa URL xac thuc QR (dang hardcode)
- Ma hoa private key khi luu
- Viet unit tests
- Loi con ton dong: "Loi khi xac thuc chu ky" xuat hien khi khoi dong (can dieu tra)
