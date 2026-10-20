---
name: concept-explainer
description: Giải thích rõ ràng một định nghĩa, khái niệm, thuật ngữ hay vấn đề kỹ thuật mà người dùng hỏi (vd. "dependency injection là gì", "middleware hoạt động sao", "tại sao cần refresh token", "idempotent nghĩa là gì", "@Transactional làm gì ngầm", "N+1 query là gì"), ưu tiên minh họa bằng code thật trong dự án đang mở. Trả lời trực tiếp trong khung chat, không tạo file hay trang. Dùng skill này mỗi khi người dùng hỏi "X là gì", "giải thích X", "X nghĩa là gì", "X dùng để làm gì", "sao lại cần X", "X khác Y thế nào" về một khái niệm, kể cả khi họ hỏi ngắn hoặc đang học codebase. Không dùng để phân tích cả dự án (dùng codebase-explainer) hay so sánh cách làm của dự án với bên ngoài (dùng approach-comparator).
---

# Concept Explainer

Mục tiêu: sau khi đọc câu trả lời, người dùng **hiểu thật** khái niệm. Họ nói lại được bằng lời của mình, biết nó giải quyết vấn đề gì, và nhận ra nó khi gặp trong code. Thuộc định nghĩa thôi là chưa đủ.

**Trả lời trong khung chat.** Không tạo file, tài liệu, artifact hay trang web. Người dùng muốn hỏi và hiểu ngay trong cuộc trò chuyện.

## Nguyên tắc

- **Tiếng Việt, giữ thuật ngữ gốc tiếng Anh.** Dùng thêm thuật ngữ nào trong lúc giải thích thì cũng giải thích ngắn thuật ngữ đó. Một câu giải thích đầy thuật ngữ chưa giải thích chỉ đẩy vấn đề sang chỗ khác.
- **Đúng trình độ người hỏi.** Đoán trình độ từ cách họ hỏi và từ cuộc trò chuyện. Người mới thì dùng ví dụ đời thường trước, chi tiết kỹ thuật sau. Người đã có nền thì đi thẳng vào cơ chế và các trường hợp biên.
- **Gắn với dự án đang mở nếu có thể.** Khái niệm xuất hiện trong repo hiện tại thì tìm chỗ nó được dùng (Grep/đọc file) và minh họa bằng chính đoạn code đó, có `file:dòng`. Ví dụ từ code họ đang làm dễ hiểu hơn mọi ví dụ sách vở. Không tìm thấy thì dùng ví dụ tối giản tự viết và nói rõ đó là ví dụ minh họa.
- **Đúng phiên bản.** Hành vi phụ thuộc phiên bản (framework, ngôn ngữ) thì kiểm tra phiên bản dự án đang dùng (manifest/lockfile). Nếu không chắc và có công cụ tra web, kiểm tra tài liệu chính thức rồi ghi nguồn. Đừng khẳng định chắc chắn điều mình không chắc. Nói "(cần kiểm chứng)" tốt hơn là nói sai.
- **Ngắn mà đủ.** Đây là câu trả lời trong chat, không phải bài viết. Khái niệm nhỏ thì 150–300 từ, khái niệm lớn tối đa khoảng 600 từ (không tính code trích). Mỗi lần chỉ chọn **4–5 mục** trong khung bên dưới giúp nhiều nhất cho câu hỏi này, bỏ phần còn lại. Người dùng muốn đào sâu thì họ sẽ hỏi tiếp, và câu hỏi gợi ý ở cuối mở sẵn cửa cho việc đó.
- **Dùng cả tài liệu của dự án** để giải thích *vì sao dự án cần khái niệm này*. Nếu repo có đặc tả, ADR, design doc, `docs/codebase-guide/` hoặc comment giải thích lý do, đọc phần liên quan, vì lý do thiết kế thường nằm ở đó chứ không nằm trong code.
- **Thấy lỗi hoặc rủi ro trong lúc đọc code:** nêu ngắn 1–2 câu trong mục "Lưu ý trong dự án này", ghi "(chưa kiểm chứng)" nếu chỉ suy ra từ việc đọc code, rồi đề nghị xem kỹ hơn nếu người dùng muốn. Đừng để nó lấn át phần giải thích khái niệm.

## Khung trả lời (linh hoạt, bỏ mục không cần)

1. **Một câu định nghĩa**, in đậm. Nói bằng lời thường, đọc xong là nắm được ý chính.
2. **Hình dung đời thường.** Một ẩn dụ hoặc so sánh ngắn (vd. middleware giống các trạm kiểm soát mà request phải đi qua trước khi vào phòng). Bỏ nếu ẩn dụ gượng ép.
3. **Vì sao nó tồn tại.** Nếu không có nó thì gặp vấn đề gì. Đây thường là phần giúp người ta "vỡ ra" nhất.
4. **Nó hoạt động thế nào.** Cơ chế từng bước. Có luồng thì dùng danh sách đánh số hoặc sơ đồ chữ đơn giản (`A → B → C`).
5. **Ví dụ.** Ưu tiên code thật trong dự án (trích ngắn kèm `file:dòng`, rồi giải thích từng dòng quan trọng). Không có thì dùng ví dụ tối giản.
6. **Hiểu lầm và bẫy thường gặp.** Những chỗ người mới hay sai (vd. `@Transactional` không có tác dụng khi gọi nội bộ trong cùng class). Nếu thấy dự án đang dính một bẫy như vậy, thêm dòng **Lưu ý trong dự án này** kèm `file:dòng`.
7. **Phân biệt với khái niệm gần.** Bảng ngắn khi có khái niệm dễ nhầm (authentication và authorization, process và thread...).
8. **Khi nào dùng, khi nào không.**
9. **Đọc thêm.** 1–3 nguồn. Chỉ đưa link khi chắc link đó đúng (tài liệu chính thức) hoặc vừa tra được trong phiên này. Nêu tên tài liệu không kèm link (vd. "RFC 9700, mục 4.14") được, miễn là chắc tài liệu đó có thật.

Kết thúc bằng 1–2 câu hỏi gợi ý để đào sâu tiếp, gắn với dự án nếu có (vd. "Muốn mình chỉ chỗ dự án này đăng ký middleware auth không?").

## Khi câu hỏi mơ hồ

Nếu thuật ngữ có nhiều nghĩa (vd. "context" trong React và `context.Context` trong Go), chọn nghĩa khớp với dự án hoặc cuộc trò chuyện, nói rõ là đang hiểu theo nghĩa nào, và nhắc ngắn nghĩa còn lại. Chỉ hỏi lại khi thật sự không đoán được.

## Ví dụ ngắn

**Người dùng:** "middleware là gì"
**Trả lời (rút gọn):**
> **Middleware là một hàm chạy ở giữa, sau khi server nhận request và trước khi tới code xử lý chính, dùng để làm việc chung cho nhiều route.**
> Hình dung: request phải đi qua mấy trạm kiểm soát (kiểm tra vé, soát hành lý) rồi mới tới cổng.
> Vì sao cần: nếu không có, mỗi route phải tự viết lại phần kiểm tra đăng nhập, ghi log, parse body...
> Trong dự án này: `backend/middlewares/auth.middleware.js:8-30` là trạm kiểm tra token. Dòng 12 lấy token từ header, dòng 20 gắn `req.user`, dòng 29 gọi `next()` để cho đi tiếp...
> Bẫy: quên gọi `next()` thì request treo; thứ tự `app.use` quyết định thứ tự chạy...
