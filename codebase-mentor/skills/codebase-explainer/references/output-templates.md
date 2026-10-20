# Khung mẫu đầu ra

Khung để giữ các tài liệu nhất quán. Bỏ mục không áp dụng, thêm mục nếu dự án cần — khung phục vụ người đọc, không phải ngược lại. Mọi file bắt đầu bằng một dòng quay về mục lục: `[← Mục lục](README.md)`.

Quy ước dẫn chứng: `` `src/user/user.service.ts:42` `` hoặc `` `src/user/user.service.ts:42-60` ``, đường dẫn tương đối từ gốc repo, dùng `/`. Code trích dẫn dùng block có ngôn ngữ, dòng đầu block ghi chú vị trí:

````markdown
```ts
// src/user/user.service.ts:42-48
async findByEmail(email: string) {
  ...
}
```
````

---

## README.md

```markdown
# Hướng dẫn codebase: <tên dự án>

> Tạo bởi codebase-explainer ngày <YYYY-MM-DD> từ commit `<hash ngắn>` (branch `<branch>`).

## Tóm tắt
<3–5 câu: dự án là gì, cho ai, stack chính, kiến trúc, trạng thái>

## Phạm vi phân tích
- **Đặc tả đã dùng:** <danh sách file đặc tả đã đọc, hoặc "không tìm thấy đặc tả — nghiệp vụ suy ra từ code/test/UI">
- **Luồng đào sâu:** <luồng 1>, <luồng 2> — lý do chọn: ...
- **Module mẫu:** <module> — lý do: ...
- **Chưa đào sâu:** <các phần chỉ tóm tắt>

## Mục lục
| # | Phần | Đọc để biết |
|---|---|---|
| 01 | [Tổng quan](01-tong-quan.md) | ... |
| ... |

## Nên đọc theo thứ tự nào
- Mới hoàn toàn: 01 → 02 → 03 → 05 → 08
- Cần sửa một chức năng: 05 → 09 → 08
```

## 01-tong-quan.md
```markdown
# 1. Tổng quan dự án
## Dự án này là gì
## Giải quyết vấn đề gì, cho ai
## Loại dự án
## Các thành phần lớn
| Thành phần | Thư mục | Vai trò |
## Sơ đồ tổng thể
```mermaid
flowchart LR
```
```

## 02-cong-nghe.md
```markdown
# 2. Công nghệ & vai trò
## Ngôn ngữ & runtime
| Công nghệ | Phiên bản | Vai trò trong dự án | Dùng ở đâu |
## Framework
## Dữ liệu & lưu trữ
## Hạ tầng & triển khai
## Thư viện nghiệp vụ đáng chú ý
## Công cụ phát triển (gom gọn)
```

## 03-dac-thu-ngon-ngu-framework.md
```markdown
# 3. Đặc thù ngôn ngữ & framework
> Đọc phần này trước khi đọc code — nó giải thích những thứ "chạy mà không thấy ai gọi".

## 3.1 Ngôn ngữ <tên>
### <Đặc thù 1, vd. Type chỉ tồn tại lúc biên dịch>
<giải thích đời thường 1–3 câu>
```<lang>
// <file:dòng>
<code thật>
```
<đoạn code này làm gì, điều gì xảy ra ngầm>
**Hệ quả khi làm việc:** ...

## 3.2 Framework <tên> <phiên bản>
### Vòng đời ứng dụng và request
### Dependency injection / Decorator / Hook / Middleware ...
### Convention over configuration
### ORM / Code sinh tự động

## 3.3 Khác biệt do phiên bản

## 3.4 Những thứ chạy ngầm dễ gây bối rối
| Cái gì chạy | Được kích hoạt bởi | File liên quan | Ghi chú |

## 3.5 Nếu bạn quen <stack khác>
| Ở <stack khác> | Ở dự án này |
```

## 04-file-cau-hinh.md
```markdown
# 4. File cấu hình
## Build & biên dịch
### `<file>`
- **Tác dụng:** ...
- **Thiết lập quan trọng:** `<key>`: <ý nghĩa>
- **Sửa thì sao:** ...
## Runtime & môi trường
### Biến môi trường
| Biến | Ý nghĩa | Đọc ở đâu |
## Hạ tầng (Docker, K8s, nginx)
## Chất lượng code (lint, format, hook)
## CI/CD
## File khác / file lạ
```

## 05-kien-truc-thu-muc.md
```markdown
# 5. Kiến trúc & tổ chức thư mục
## Pattern kiến trúc
<tên pattern> — căn cứ: ...
## Sơ đồ
```mermaid
flowchart TB
```
## Cây thư mục
```text
repo/
├── src/            # ...
│   ├── modules/    # ...
```
## Quy tắc phụ thuộc
## Module mẫu: <tên>
| File | Vai trò |
<các file nối nhau ra sao>
## Các module khác so với mẫu
| Module | Giống mẫu? | Khác biệt đáng chú ý |
```

## 06-mo-hinh-du-lieu.md
```markdown
# 6. Mô hình dữ liệu
## Sơ đồ quan hệ
```mermaid
erDiagram
```
## Các entity
| Entity | Ý nghĩa nghiệp vụ | Định nghĩa ở | Quan hệ chính |
## Trường có ý nghĩa đặc biệt
## Migration
```

## 07-luong-khoi-dong.md
```markdown
# 7. Luồng khởi động
Lệnh chạy: `<lệnh>` → `<entry file>`
1. **<bước>** — `<file:dòng>`
   ```<lang>
   ```
   <giải thích>
2. ...
```

## 08-luong-request.md
```markdown
# 8. Luồng request
## Luồng 1: <tên thao tác>
**Thao tác:** ... **Kết quả mong đợi:** ...
### Theo thiết kế (nếu có đặc tả)
<luồng đặc tả muốn: các bước, quy tắc, nhánh lỗi — nguồn `<spec:dòng>`>
### Thực tế trong code
```mermaid
sequenceDiagram
```
### Chặng 1 — <tên chặng> (`<file:dòng-dòng>`)
```<lang>
```
**Dòng này làm gì:** ...
**Kiến thức nền:** ...
**Dữ liệu ra:** ...
### Chặng 2 — ...
### Nhánh lỗi
| Tình huống | Xử lý ở đâu | Trả về |
### Chênh lệch so với thiết kế (nếu có đặc tả)
| Điểm trong đặc tả | Code làm gì | Khớp / Khác / Chưa làm |
```

## 09-chuc-nang.md
```markdown
# 9. Từng chức năng
## Nhóm <module/domain>
### <Chức năng> <thêm "(chưa hiện thực)" nếu chỉ có trong đặc tả>
- **Thiết kế:** <yêu cầu / quy tắc / scenario gốc> (`<file đặc tả:dòng>`)
- **Mục đích:** ...
- **File:** route `<..>` → service `<..>` → model `<..>`
- **Luồng xử lý:** 1. ... 2. ...
- **Quy tắc nghiệp vụ:** ...
- **Validate & phân quyền:** ...
- **Edge case & lỗi:** ...
- **Chênh lệch so với thiết kế:** <khớp / khác ở… / chưa làm / code làm thêm…>
### Các chức năng CRUD đơn giản
| Chức năng | Endpoint/màn hình | File | Ghi chú |
```

## 10-thuat-ngu.md
```markdown
# 10. Từ điển thuật ngữ
| Thuật ngữ | Nghĩa | Xuất hiện ở |
```

## 11-no-ky-thuat-rui-ro.md
```markdown
# 11. Nợ kỹ thuật & rủi ro
| Mức | Vấn đề | Vị trí | Vì sao rủi ro | Gợi ý |
## Chỗ dễ vỡ khi sửa
```

## 12-trang-thai-huong-phat-trien.md
```markdown
# 12. Trạng thái dự án & hướng phát triển
## Giai đoạn hiện tại
<giai đoạn> — căn cứ: ...
## Hoạt động gần đây
## Việc dở dang
| Việc | Dấu hiệu | Vị trí |
## Độ phủ đặc tả
<bỏ mục này nếu không có đặc tả, và ghi một câu "không tìm thấy đặc tả">
| Yêu cầu | Nguồn đặc tả | Trạng thái | Dẫn chứng trong code |
|---|---|---|---|
| ... | `<spec:dòng>` | Đã làm / Làm dở / Chưa làm / Làm khác đặc tả / Không rõ | `<file:dòng>` |
**Tổng kết:** ...
## Hướng xử lý & kế hoạch đã đề ra
| Hướng | Nguồn | Trạng thái |
## Nhận định của tôi (suy đoán)
```

## 13-lo-trinh-doc-tiep.md
```markdown
# 13. Lộ trình đọc tiếp
## Thứ tự file nên đọc
1. `<file>` — đọc để hiểu ...
## Bài tập làm quen
## Câu hỏi gợi ý để hỏi tiếp
```
