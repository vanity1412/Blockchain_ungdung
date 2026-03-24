# Hệ Thống Quản Lý Chứng Chỉ Điện Tử - Blockchain & NFT

> Dự án ứng dụng Blockchain vào việc cấp và xác thực chứng chỉ học thuật tại các trường thành viên ĐHQG-HCM

---

## 📋 Tổng Quan

Hệ thống cho phép các trường đại học thuộc ĐHQG-HCM cấp phát, lưu trữ và xác thực chứng chỉ điện tử trên nền tảng Blockchain. Mỗi chứng chỉ được đại diện bởi một **NFT ID** duy nhất và được **ký số RSA** bởi đơn vị cấp phát, sau đó ghi vào chuỗi khối bất biến.

---

## 🏗️ Kiến Trúc Hệ Thống

```
main.py
  └── gui.py  (Giao diện chính - Tkinter)
        ├── blockchain.py     (Lớp Block + Blockchain)
        ├── key_manager.py    (Quản lý khóa RSA)
        ├── signature_utils.py (Ký & xác thực chữ ký số)
        ├── nft_manager.py    (Tạo NFT ID)
        ├── qr_manager.py     (Tạo QR code)
        └── storage.py        (Lưu/tải dữ liệu JSON)
```

---

## 📁 Cấu Trúc Thư Mục

```
Blockchain_ungdung/
├── main.py              # Điểm khởi chạy ứng dụng
├── gui.py               # Giao diện đồ họa chính (Tkinter)
├── gui_basic.py         # Giao diện cơ bản (phiên bản đơn giản)
├── blockchain.py        # Logic chuỗi khối
├── key_manager.py       # Quản lý cặp khóa RSA
├── signature_utils.py   # Tiện ích chữ ký số
├── nft_manager.py       # Tạo và xác thực NFT ID
├── qr_manager.py        # Tạo QR code
├── storage.py           # Đọc/ghi dữ liệu blockchain
├── blockchain.json      # Dữ liệu chuỗi khối (tự sinh)
├── requirements.txt     # Thư viện cần thiết
├── keys/                # Thư mục chứa khóa RSA (.pem)
└── exports/             # Thư mục xuất QR code (.png)
```

---

## 🔧 Các Module Chính

### `blockchain.py` — Lớp Block & Blockchain
| Lớp | Mô tả |
|-----|-------|
| `Block` | Đại diện một khối, bao gồm: tên sinh viên, chứng chỉ, NFT ID, chữ ký, trạng thái (`valid`/`revoked`), hash SHA-256, nonce |
| `Blockchain` | Quản lý chuỗi khối: thêm block, kiểm tra tính toàn vẹn, tìm kiếm, lọc, thống kê |

- **Proof of Work**: độ khó mặc định = 3 (hash phải bắt đầu bằng `000`)
- **Genesis Block**: khối đầu tiên được tạo tự động khi khởi tạo blockchain mới
- **Thu hồi chứng chỉ**: thay đổi `status = "revoked"`, ghi lý do và thời điểm thu hồi

---

### `key_manager.py` — Quản Lý Khóa RSA
- Tự động tạo cặp khóa RSA-2048 cho **6 đơn vị cấp** khi khởi động:

| Mã | Tên đầy đủ |
|----|-----------|
| `HCMUS` | Trường ĐH Khoa học Tự nhiên - ĐHQG-HCM |
| `HCMUT` | Trường ĐH Bách khoa - ĐHQG-HCM |
| `HCMIU` | Trường ĐH Quốc tế - ĐHQG-HCM |
| `UIT` | Trường ĐH Công nghệ Thông tin - ĐHQG-HCM |
| `USSH` | Trường ĐH Khoa học Xã hội và Nhân văn - ĐHQG-HCM |
| `UEL` | Trường ĐH Kinh tế - Luật - ĐHQG-HCM |

- Khóa được lưu dưới dạng file `.pem` trong thư mục `keys/`
- Format: `{ISSUER_ID}_private.pem` và `{ISSUER_ID}_public.pem`

---

### `signature_utils.py` — Chữ Ký Số
- **Thuật toán ký**: RSA-PSS với SHA-256 (`padding.PSS + MGF1`)
- **Payload ký**: JSON chuẩn (sort_keys) gồm `student_name`, `certificate_name`, `issuer_id`, `issuer_name`, `nft_id`, `issued_at`
- **Lưu trữ chữ ký**: Base64-encoded trong trường `signature` của Block
- Hàm chính:
  - `create_certificate_signature()` — ký khi cấp chứng chỉ
  - `verify_certificate_by_data()` — xác thực chữ ký theo dữ liệu

---

### `nft_manager.py` — NFT ID
- Tạo NFT ID duy nhất bằng UUID4: `NFT-{16 ký tự hex viết hoa}`
- Ví dụ: `NFT-A1B2C3D4E5F60708`
- Độ dài chuẩn: 20 ký tự (bao gồm tiền tố `NFT-`)

---

### `qr_manager.py` — QR Code
- **QR dữ liệu**: mã hóa `NFT_ID:{nft_id}|STUDENT:{student_name}`
- **QR URL**: mã hóa URL xác thực `https://verify.certificate.edu.vn/verify?nft_id={nft_id}`
- File ảnh PNG được lưu trong thư mục `exports/`

---

### `storage.py` — Lưu Trữ
- Lưu blockchain dưới dạng `blockchain.json` (JSON có định dạng đẹp)
- Hỗ trợ **backup** tự động với timestamp: `blockchain_backup_{timestamp}.json`
- Hỗ trợ **restore** từ bản backup (tự backup file hiện tại trước khi restore)
- Backward compatibility khi tải dữ liệu cũ thiếu field mới

---

## 🔄 Luồng Xử Lý Chính

### Cấp Chứng Chỉ
```
1. Người dùng nhập thông tin → GUI thu thập dữ liệu
2. NFTManager.generate_nft_id() → tạo NFT ID duy nhất
3. SignatureUtils.create_certificate_signature() → ký bằng private key của đơn vị cấp
4. Blockchain.add_block() → đào block (Proof of Work)
5. BlockchainStorage.save() → ghi vào blockchain.json
6. QRManager.generate_qr_code() → tạo QR code (tùy chọn)
```

### Xác Thực Chứng Chỉ
```
1. Nhập NFT ID → Blockchain.find_certificate_by_nft()
2. Kiểm tra status (valid/revoked)
3. SignatureUtils.verify_certificate_by_data() → xác thực chữ ký bằng public key
4. Blockchain.is_chain_valid() → kiểm tra tính toàn vẹn chuỗi
```

---

## 📦 Thư Viện Sử Dụng

| Thư viện | Phiên bản | Mục đích |
|----------|-----------|----------|
| `cryptography` | ≥ 41.0.0 | Tạo và quản lý khóa RSA, ký & xác thực chữ ký số |
| `qrcode` | ≥ 7.4.2 | Tạo QR code cho chứng chỉ |
| `pillow` | ≥ 10.0.0 | Xử lý hình ảnh PNG cho QR code |

> Cài đặt: `pip install -r requirements.txt`

---

## ▶️ Cách Chạy

```powershell
# Kích hoạt virtual environment (nếu có)
.venv\Scripts\activate

# Cài thư viện
pip install -r requirements.txt

# Khởi chạy ứng dụng
python main.py
```

---

## 📝 Ghi Chú Kỹ Thuật

- **Backward Compatibility**: `Block.from_dict()` dùng `.get()` với giá trị mặc định để tương thích dữ liệu cũ
- **Hash tính toán**: Không bao gồm field `signature` để tránh circular dependency (ký sau khi tính hash)
- **Trạng thái chứng chỉ**: `status` được include trong hash để việc thay đổi trạng thái cần ghi nhận riêng (revoke không tính lại hash)
- **Thư mục dữ liệu**: `keys/` và `exports/` được tự động tạo khi khởi động lần đầu
