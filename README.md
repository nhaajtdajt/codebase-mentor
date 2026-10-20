# codebase-mentor

Bộ skill cho AI agent để **học một codebase bằng tiếng Việt**: dự án làm gì, viết bằng gì, chạy ra sao, một request đi qua những file nào, đang ở giai đoạn nào và định đi tiếp hướng nào.

| Skill | Dùng khi | Kết quả |
|---|---|---|
| [`codebase-explainer`](codebase-mentor/skills/codebase-explainer/SKILL.md) | "giải thích dự án này", "onboard tôi vào repo này", "học codebase" | Bộ tài liệu 13 phần trong `docs/codebase-guide/` của dự án |
| [`concept-explainer`](codebase-mentor/skills/concept-explainer/SKILL.md) | "X là gì", "giải thích X", "sao lại cần X", "X khác Y thế nào" | Trả lời trong chat, ví dụ lấy từ code thật của dự án |
| [`approach-comparator`](codebase-mentor/skills/approach-comparator/SKILL.md) | "người ta thường làm thế nào", "cách này có chuẩn không", "có cách nào tốt hơn" | Trả lời trong chat, so sánh với 2–4 cách làm có nguồn trên mạng |

## `codebase-explainer` tạo ra gì

`docs/codebase-guide/` gồm `README.md` (mục lục, phạm vi đã chọn) và 13 phần:

1. Tổng quan dự án
2. Công nghệ và vai trò cụ thể của từng công nghệ trong dự án
3. Đặc thù ngôn ngữ & framework: những thứ "chạy ngầm" dễ gây bối rối, minh họa bằng code thật
4. File cấu hình: tác dụng, thiết lập quan trọng, sửa thì sao
5. Kiến trúc & tổ chức thư mục: giải thích một module mẫu, rồi bảng khác biệt của các module còn lại
6. Mô hình dữ liệu (sơ đồ ER)
7. Luồng khởi động
8. Luồng request: trace qua từng file, giải thích từng dòng quan trọng, có sơ đồ tuần tự
9. Từng chức năng: logic nghiệp vụ, validate, edge case
10. Từ điển thuật ngữ
11. Nợ kỹ thuật & rủi ro
12. Trạng thái dự án & hướng phát triển (git, TODO, độ phủ đặc tả)
13. Lộ trình đọc tiếp

Nếu dự án có đặc tả (openspec, PRD, spec, ADR, user story, `.feature`...), skill đọc đặc tả trước. Luồng và chức năng được giải thích theo thứ tự **Thiết kế → Thực tế → Chênh lệch**.

Mọi nhận định đều có dẫn chứng `file:dòng`, và script `check_citations.py` kiểm tra lại cả vị trí lẫn nội dung code được trích. Skill chỉ đọc: không sửa code, không chạy test/build/migrate, không chép giá trị bí mật từ `.env`.

## Cài đặt

### Claude Code (plugin)

```bash
claude plugin marketplace add nhaajtdajt/codebase-mentor
```

```bash
claude plugin install codebase-mentor@codebase-mentor
```

Trong phiên Claude Code tương tác có thể dùng `/plugin marketplace add nhaajtdajt/codebase-mentor` rồi `/plugin install codebase-mentor@codebase-mentor`. Cập nhật bản mới:

```bash
claude plugin marketplace update codebase-mentor
```

### Các agent khác (Codex, Cursor, Gemini CLI, OpenCode, ...)

Các skill viết theo định dạng `SKILL.md` chuẩn (Agent Skills). Có hai cách cài.

Cách 1: dùng Skills CLI (`npx skills`):

```bash
npx skills add nhaajtdajt/codebase-mentor
```

Cách 2: chép tay. Mỗi skill là một thư mục trong `codebase-mentor/skills/`. Chép thư mục đó vào nơi agent của bạn đọc skill, ví dụ `~/.claude/skills/`, `~/.codex/skills/`, `~/.agents/skills/` hoặc `.cursor/skills/` trong dự án (tùy agent). Với `codebase-explainer`, nhớ chép cả `references/` và `scripts/`.

## Yêu cầu

- `codebase-explainer`: nên có Python 3 (chỉ dùng thư viện chuẩn) cho `scripts/scan_repo.py` và `scripts/check_citations.py`. Không có Python thì agent tự quét bằng công cụ có sẵn, chậm hơn.
- `approach-comparator`: cần công cụ tra web để có nguồn. Không có thì skill so sánh từ kiến thức chung và ghi rõ là chưa kiểm chứng.
- Một lần chạy `codebase-explainer` trên dự án cỡ vừa (vài trăm file) mất khoảng 15–25 phút.

## Giấy phép

MIT
