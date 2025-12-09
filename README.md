# Phương pháp xác định vùng mua bán của tài sản số với tỷ suất lợi nhuận cao

## Thành viên nhóm

| STT | Họ và tên | Mã sinh viên |
|-----|-----------|--------------|
| 1 | Phạm Nhật Quang | 23020413 |
| 2 | Bùi Minh Quân | 23020415 |
| 3 | Phan Quang Trường | 23020443 |
| 4 | Hồ Lê Dương | 22022641 |

**Giáo viên hướng dẫn:**
* GS. Nguyễn Phương Thái
* ThS. Ngô Minh Hương

## Phương pháp & Công nghệ

### 1. Dữ liệu (2023 - 2025)
* **Dữ liệu giá:** Lịch sử giá Bitcoin khung 1 phút (Nguồn: Binance).
* **Dữ liệu tin tức:** Tiêu đề và chỉ số tương tác từ CryptoPanic.
* **Phân chia:**
    * *Train:* 01/01/2023 - 31/12/2024 (Xây dựng mô hình & Luật).
    * *Test:* 01/01/2025 - 06/12/2025 (Kiểm thử chiến lược).
* **Link dữ liệu:** https://www.kaggle.com/datasets/minhqunbi/data-mining-dataset


### 2. Kỹ thuật xử lý (Feature Engineering)
* **Chỉ báo kỹ thuật:** RSI, EMA, ATR, Shock Volume.
* **Smart Money Concepts (SMC):** Tự động phát hiện Order Blocks và Fair Value Gaps (FVG).
* **Xử lý tin tức:** Sử dụng Rolling Z-Score để chuẩn hóa chỉ số cảm xúc (Sentiment) và độ quan tâm (Buzz) theo thời gian thực, tránh rò rỉ dữ liệu (Look-ahead bias).

### 3. Thuật toán Khai phá
* **Phân cụm (Clustering):**
    * *Dữ liệu giá:* Sử dụng **K-Means** để phân loại thị trường thành 4 pha theo lý thuyết Wyckoff (Tích lũy, Tăng trưởng, Cao trào, Suy thoái).
    * *Dữ liệu tin tức:* Sử dụng **SBERT (Sentence-BERT)** + **PCA** + **K-Means** để gom nhóm chủ đề tin tức (Vĩ mô, Memecoins, Công nghệ, v.v.).
* **Khai phá luật kết hợp:** Sử dụng thuật toán **FP-Growth** để tìm ra các mẫu hình: *Nếu [Điều kiện A + Tin tức B] -> Xác suất giá tăng là X%*.


### Cài đặt thư viện
```bash
pip install pandas numpy scikit-learn mlxtend sentence-transformers matplotlib seaborn tqdm binance-historical-data