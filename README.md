# Lab 1 - FastAPI + Hugging Face Text Generation

## 1. Thông tin sinh viên
- Họ tên: **[Trần Minh Tiến]**
- MSSV: **[24120465]**
- Lớp: **[Tư duy tính toán - 24CTT 3]**
- GitHub: **[Điền link GitHub cá nhân]**

---

## 2. Mô hình sử dụng
- **Tên mô hình:** `Qwen/Qwen3-0.6B`
- **Link Hugging Face:** https://huggingface.co/Qwen/Qwen3-0.6B
- **Task:** Text Generation (Causal Language Modeling)

---

## 3. Mô tả ngắn hệ thống

Hệ thống triển khai dưới dạng **FastAPI application** với các endpoint:

- `GET /`: mô tả ngắn API
- `GET /health`: kiểm tra trạng thái model
- `POST /generate`: nhận dữ liệu đầu vào và sinh văn bản bằng mô hình Hugging Face

API trả kết quả ở định dạng JSON, có kiểm tra dữ liệu đầu vào và xử lý lỗi cơ bản.
Hệ thống là một ứng dụng FastAPI tích hợp mô hình Qwen/Qwen3-0.6B trên Hugging Face để sinh văn bản tiếng Việt từ câu lệnh người dùng.

## 4. Cấu trúc thư mục
```text
.
├── main.py
├── text_generation.py
├── test_api.py
├── requirements.txt
└── README.md
```

---

## 5. Hướng dẫn cài đặt thư viện

### 5.1 Tạo môi trường (khuyến nghị)
```bash
conda create -n lab1 python=3.10 -y
conda activate lab1
```

### 5.2 Cài dependencies
```bash
pip install -r requirements.txt
```

---

## 6. Hướng dẫn chạy chương trình

```bash
uvicorn main:app --reload
```

Sau khi chạy thành công:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

---

## 7. Hướng dẫn gọi API

### 7.1 Endpoint
- **Method:** `POST`
- **URL:** `http://127.0.0.1:8000/generate`
- **Content-Type:** `application/json`

### 7.2 Request mẫu
```json
{
  "prompt": "Giải thích AI là gì trong 2 câu ngắn.",
  "max_new_tokens": 100,
  "temperature": 0.7,
  "top_p": 0.9
}
```

### 7.3 Response mẫu (thành công)
```json
{
  "model": "Qwen/Qwen3-0.6B",
  "device": "cpu",
  "prompt": "Giải thích AI là gì trong 2 câu ngắn.",
  "generated_text": "AI là lĩnh vực nghiên cứu cách máy tính mô phỏng trí thông minh của con người..."
}
```

### 7.4 Response mẫu (lỗi input)
```json
{
  "detail": "Prompt cannot be empty."
}
```

---

## 8. File test API bằng requests
Chạy:
```bash
python test_api.py
```

---

## 9. Link video demo
- **[Dán link video demo tại đây]**

---
