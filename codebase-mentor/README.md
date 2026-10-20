# codebase-mentor

Plugin Claude Code giúp học một codebase bằng tiếng Việt. Gồm 3 skill:

| Skill | Dùng khi | Kết quả |
|---|---|---|
| `codebase-explainer` | "giải thích dự án này", "onboard tôi vào repo này", "học codebase" | Bộ tài liệu 13 phần trong `docs/codebase-guide/` (tổng quan, công nghệ, đặc thù ngôn ngữ/framework, cấu hình, kiến trúc, dữ liệu, luồng khởi động, luồng request, chức năng, thuật ngữ, nợ kỹ thuật, trạng thái & hướng phát triển, lộ trình đọc). Có đặc tả thì học từ đặc tả và đối chiếu Thiết kế → Thực tế → Chênh lệch |
| `concept-explainer` | "X là gì", "giải thích X", "sao lại cần X", "X khác Y thế nào" | Trả lời trong chat; ví dụ ưu tiên lấy từ code thật của dự án |
| `approach-comparator` | "người ta thường làm thế nào", "cách này có chuẩn không", "có cách nào tốt hơn" | Trả lời trong chat; so sánh với 2–4 cách làm có nguồn trên mạng, đánh giá theo bối cảnh dự án |

## Cài đặt

Xem hướng dẫn đầy đủ (Claude Code và các agent khác) ở [README gốc của repo](https://github.com/nhaajtdajt/codebase-mentor#cài-đặt). Với Claude Code:

```bash
claude plugin marketplace add nhaajtdajt/codebase-mentor
```

```bash
claude plugin install codebase-mentor@codebase-mentor
```

## Yêu cầu

- `codebase-explainer` dùng Python 3 (chỉ thư viện chuẩn) cho `scripts/scan_repo.py` và `scripts/check_citations.py`; không có Python vẫn chạy được nhưng chậm hơn.
- `approach-comparator` cần công cụ tra web (WebSearch/WebFetch) để có nguồn; không có thì so sánh từ kiến thức chung và ghi rõ chưa kiểm chứng.

## Nguyên tắc chung

- Chỉ đọc, không sửa code của dự án; không chạy test/build/migrate.
- Mọi nhận định có dẫn chứng `file:dòng`; không chắc thì ghi "(suy đoán)".
- Không chép giá trị bí mật từ file `.env`.
