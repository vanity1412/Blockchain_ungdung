# Hệ thống Quản lý Chứng chỉ Điện tử - Blockchain & NFT (Nâng cấp)

## Giới thiệu
Ứng dụng mô phỏng hệ thống quản lý chứng chỉ điện tử nâng cao dựa trên công nghệ Blockchain, NFT và chữ ký số RSA, được xây dựng bằng Python với giao diện Tkinter.

## Tính năng chính

### 1. Cấp Chứng chỉ với Chữ ký số (Issue Certificate)
- Chọn đơn vị cấp từ danh sách có sẵn (HCMUS, HCMUT, HCMIU, UIT, USSH, UEL)
- Tự động tạo NFT ID duy nhất cho mỗi chứng chỉ
- Ký chứng chỉ bằng private key RSA của đơn vị cấp
- Thực hiện Proof of Work (Mining) với độ khó tùy chỉnh
- Tự động tạo QR code cho chứng chỉ
- Hiển thị thông tin chi tiết sau khi cấp thành công

### 2. Xem Chuỗi Khối (View Blockchain)
- Hiển thị toàn bộ blockchain với thông tin mở rộng
- Bao gồm cột trạng thái (valid/revoked)
- Cho phép cuộn để xem tất cả các khối
- Cập nhật real-time khi có khối mới

### 3. Xác thực Chứng chỉ Nâng cao (Verify Certificate)
- Tra cứu chứng chỉ theo NFT ID
- Kiểm tra tính toàn vẹn blockchain
- Xác thực chữ ký số RSA
- Hiển thị trạng thái chứng chỉ (hợp lệ/đã thu hồi)
- Thông tin chi tiết về đơn vị cấp và thời gian

### 4. Tìm kiếm Nâng cao (Advanced Search)
- Tìm kiếm theo tên sinh viên
- Tìm kiếm theo tên chứng chỉ
- Tìm kiếm theo đơn vị cấp
- Lọc theo trạng thái (valid/revoked)

### 5. Thu hồi Chứng chỉ (Certificate Revocation)
- Thu hồi chứng chỉ theo NFT ID
- Ghi nhận lý do thu hồi
- Cập nhật trạng thái và thời gian thu hồi
- Không xóa dữ liệu, chỉ đánh dấu revoked

### 6. Dashboard Thống kê (Statistics Dashboard)
- Tổng số khối và chứng chỉ
- Số chứng chỉ hợp lệ và đã thu hồi
- Độ khó mining hiện tại
- Số đơn vị cấp có khóa
- Trạng thái khóa RSA của từng đơn vị

### 7. Backup & Restore
- Tạo backup blockchain với tên tùy chọn
- Khôi phục từ file backup
- Liệt kê tất cả backup có sẵn
- Tự động backup trước khi restore

### 8. Kiểm tra Bảo mật Chi tiết (Advanced Security Check)
- Xác thực tính toàn vẹn của blockchain
- Kiểm tra hash và liên kết giữa các khối
- Xác nhận Proof of Work
- Kiểm tra chữ ký số của từng chứng chỉ
- Báo cáo chi tiết các lỗi nếu có

## Cấu trúc dự án

```
certificate-blockchain/
│
├── main.py              # File chính để chạy ứng dụng
├── blockchain.py        # Module quản lý Blockchain và Block (nâng cấp)
├── gui.py              # Module giao diện người dùng (nâng cấp)
├── storage.py          # Module lưu trữ và backup (nâng cấp)
├── nft_manager.py      # Module quản lý NFT ID
├── key_manager.py      # Module quản lý khóa RSA (mới)
├── signature_utils.py  # Module xử lý chữ ký số (mới)
├── qr_manager.py       # Module tạo QR code (mới)
├── requirements.txt    # Danh sách thư viện cần cài
├── README.md           # Tài liệu hướng dẫn
├── blockchain.json     # File lưu trữ blockchain (tự động tạo)
├── keys/               # Thư mục chứa khóa RSA (tự động tạo)
├── exports/            # Thư mục chứa QR code (tự động tạo)
└── backups/            # Thư mục chứa backup (tự động tạo)
```

## Công nghệ sử dụng

### Blockchain
- **Block Structure**: Mở rộng với các field mới
  - Cũ: index, timestamp, student_name, certificate_name, issuer, nft_id, previous_hash, nonce, hash
  - Mới: + issued_at, issuer_id, issuer_name, signature, status, revoked_at, revoke_reason
- **Hashing**: SHA-256 (thư viện hashlib)
- **Proof of Work**: Độ khó 3 (hash phải bắt đầu với 3 số 0)
- **Validation**: Kiểm tra hash, liên kết previous_hash và chữ ký số

### Chữ ký số RSA
- **Key Size**: 2048 bit RSA
- **Padding**: PSS với MGF1 và SHA-256
- **Format**: PEM cho lưu trữ khóa
- **Signature**: Base64 encoding cho lưu trữ

### Đơn vị cấp chứng chỉ
- **HCMUS**: Trường Đại học Khoa học Tự nhiên - ĐHQG-HCM
- **HCMUT**: Trường Đại học Bách khoa - ĐHQG-HCM
- **HCMIU**: Trường Đại học Quốc tế - ĐHQG-HCM
- **UIT**: Trường Đại học Công nghệ Thông tin - ĐHQG-HCM
- **USSH**: Trường Đại học Khoa học Xã hội và Nhân văn - ĐHQG-HCM
- **UEL**: Trường Đại học Kinh tế - Luật - ĐHQG-HCM

### NFT & QR Code
- **UUID4**: Tạo mã định danh duy nhất cho mỗi chứng chỉ
- **Format**: NFT-XXXXXXXXXXXXXXXX (16 ký tự hex)
- **QR Code**: Chứa NFT ID và thông tin sinh viên

### Lưu trữ
- **JSON**: Lưu toàn bộ blockchain với backward compatibility
- **Auto-load**: Tự động tải dữ liệu khi khởi động
- **Genesis Block**: Tự động tạo khối nguyên thủy nếu chưa có
- **Backup**: Hỗ trợ backup/restore với timestamp

## Hướng dẫn sử dụng

### Cài đặt
```bash
pip install -r requirements.txt
```

### Chạy ứng dụng
```bash
python main.py
```

### Sử dụng các chức năng

#### 1. Cấp chứng chỉ mới
1. Chuyển đến tab "📜 Cấp Chứng Chỉ"
2. Nhập thông tin:
   - Tên sinh viên
   - Tên chứng chỉ
   - Chọn đơn vị cấp từ dropdown
3. Nhấn nút "🎓 CẤP CHỨNG CHỈ (Có chữ ký số)"
4. Đợi quá trình tạo chữ ký và Mining hoàn tất
5. Lưu lại NFT ID để tra cứu sau
6. QR code sẽ được tạo trong thư mục exports/

#### 2. Xem chuỗi khối
1. Chuyển đến tab "🔗 Xem Chuỗi Khối"
2. Xem danh sách tất cả các khối với trạng thái
3. Nhấn "🔄 Làm mới" để cập nhật

#### 3. Xác thực chứng chỉ
1. Chuyển đến tab "✅ Xác Thực"
2. Nhập NFT ID cần tra cứu
3. Nhấn "🔍 TÌM KIẾM"
4. Xem thông tin chi tiết bao gồm:
   - Thông tin chứng chỉ
   - Trạng thái (hợp lệ/thu hồi)
   - Xác thực blockchain
   - Xác thực chữ ký số

#### 4. Tìm kiếm nâng cao
1. Chuyển đến tab "🔍 Tìm Kiếm"
2. Chọn loại tìm kiếm (sinh viên, chứng chỉ, đơn vị cấp, trạng thái)
3. Nhập từ khóa
4. Nhấn "🔍 TÌM KIẾM"
5. Xem kết quả trong bảng

#### 5. Thu hồi chứng chỉ
1. Chuyển đến tab "❌ Thu Hồi"
2. Nhập NFT ID cần thu hồi
3. Nhập lý do thu hồi
4. Nhấn "❌ THU HỒI CHỨNG CHỈ"
5. Xác nhận thông tin thu hồi

#### 6. Xem dashboard
1. Chuyển đến tab "📊 Dashboard"
2. Xem thống kê tổng quan
3. Kiểm tra trạng thái khóa RSA
4. Nhấn "🔄 CẬP NHẬT THỐNG KÊ" để làm mới

#### 7. Backup và restore
1. Chuyển đến tab "💾 Backup"
2. Tạo backup:
   - Nhập tên backup (tùy chọn)
   - Nhấn "💾 TẠO BACKUP"
3. Khôi phục:
   - Nhấn "📁 CHỌN FILE BACKUP"
   - Chọn file và xác nhận
4. Xem danh sách backup có sẵn

#### 8. Kiểm tra bảo mật
1. Chuyển đến tab "🔒 Bảo Mật"
2. Xem thông tin hệ thống
3. Nhấn "🛡️ KIỂM TRA HỆ THỐNG"
4. Xem kết quả xác thực chi tiết

## Kiến trúc hệ thống

### Module blockchain.py (Nâng cấp)
- **Class Block**: Mở rộng với các field mới
- **Class Blockchain**: Thêm các phương thức:
  - `revoke_certificate()`: Thu hồi chứng chỉ
  - `find_by_student_name()`: Tìm theo tên sinh viên
  - `find_by_certificate_name()`: Tìm theo tên chứng chỉ
  - `find_by_issuer()`: Tìm theo đơn vị cấp
  - `filter_by_status()`: Lọc theo trạng thái
  - `get_dashboard_stats()`: Lấy thống kê
  - `validate_chain_detailed()`: Kiểm tra chi tiết
  - `verify_certificate_signature_by_nft()`: Xác thực chữ ký

### Module key_manager.py (Mới)
- **Class KeyManager**: Quản lý khóa RSA
  - `generate_key_pair()`: Tạo cặp khóa mới
  - `load_private_key()`: Tải private key
  - `load_public_key()`: Tải public key
  - `ensure_issuer_keys_exist()`: Đảm bảo có khóa
  - `get_keys_status()`: Kiểm tra trạng thái khóa

### Module signature_utils.py (Mới)
- **Class SignatureUtils**: Xử lý chữ ký số
  - `build_sign_payload()`: Tạo payload để ký
  - `sign_certificate_data()`: Ký dữ liệu
  - `verify_certificate_signature()`: Xác thực chữ ký
  - `create_certificate_signature()`: Tạo chữ ký cho chứng chỉ

### Module qr_manager.py (Mới)
- **Class QRManager**: Tạo QR code
  - `generate_qr_code()`: Tạo QR code cơ bản
  - `generate_verification_url_qr()`: Tạo QR code URL

### Module storage.py (Nâng cấp)
- **Class BlockchainStorage**: Thêm backup/restore
  - `backup_blockchain()`: Tạo backup
  - `restore_blockchain()`: Khôi phục từ backup
  - `list_backups()`: Liệt kê backup
  - `get_file_info()`: Thông tin file

### Module gui.py (Nâng cấp lớn)
- **Class CertificateApp**: Giao diện mở rộng
  - 8 tab thay vì 4 tab cũ
  - Tích hợp đầy đủ các tính năng mới
  - Xử lý chữ ký số và QR code
  - Dashboard và backup/restore

## Đặc điểm kỹ thuật

### Bảo mật
- SHA-256 hashing cho blockchain
- RSA-2048 với PSS padding cho chữ ký số
- Proof of Work với độ khó 3
- Immutable blockchain với signature verification
- Xác thực toàn vẹn dữ liệu đa lớp

### Hiệu năng
- Threading cho Mining và tạo chữ ký (không block GUI)
- Tự động lưu sau mỗi thao tác
- Tối ưu hiển thị với Treeview
- Lazy loading cho các thao tác nặng

### Khả năng mở rộng
- Backward compatibility với dữ liệu cũ
- Dễ dàng thêm đơn vị cấp mới
- Có thể thay đổi độ khó và thuật toán
- Hỗ trợ export/import blockchain
- Modular architecture

### Tính năng nâng cao
- QR code tự động cho mỗi chứng chỉ
- Backup/restore với timestamp
- Tìm kiếm đa tiêu chí
- Dashboard thống kê real-time
- Xác thực chữ ký số tự động

## Lưu ý quan trọng

### Bảo mật
- Private key được lưu trong thư mục keys/ (không commit vào git)
- Chữ ký được lưu dưới dạng base64 trong blockchain
- Không hiển thị private key trên giao diện
- Tự động tạo khóa nếu chưa có

### Dữ liệu
- File blockchain.json tương thích ngược với phiên bản cũ
- Thư mục keys/, exports/, backups/ được tạo tự động
- Không xóa file blockchain.json nếu muốn giữ dữ liệu
- Backup trước khi restore để tránh mất dữ liệu

### Hiệu năng
- Quá trình Mining có thể mất vài giây tùy độ khó
- Tạo chữ ký số thêm thời gian xử lý
- NFT ID là duy nhất và không thể thay đổi
- QR code được lưu trong thư mục exports/

## Thư viện cần thiết
```
cryptography>=41.0.0  # Cho chữ ký số RSA
qrcode>=7.4.2         # Tạo QR code
pillow>=10.0.0        # Xử lý hình ảnh cho QR code
```

## Tác giả
Hệ thống được nâng cấp cho mục đích giáo dục và demo công nghệ Blockchain, NFT và chữ ký số.
