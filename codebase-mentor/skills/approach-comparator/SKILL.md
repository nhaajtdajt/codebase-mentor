---
name: approach-comparator
description: So sánh cách dự án hiện tại tổ chức hoặc làm một việc (kiến trúc, cấu trúc thư mục, chia module, luồng auth, quản lý state, xử lý lỗi, gọi API giữa service, cách test, cách cấu hình, deploy...) với các cách làm phổ biến của người khác, dựa trên nguồn trên mạng (tài liệu chính thức, dự án mẫu nổi tiếng, bài viết kỹ thuật), rồi đánh giá cái nào hợp với dự án này. Trả lời trực tiếp trong khung chat, có dẫn nguồn, không tạo file hay trang. Dùng skill này khi người dùng hỏi kiểu "người ta thường làm thế nào", "cách này có chuẩn không", "so sánh với best practice", "dự án khác tổ chức ra sao", "có cách nào tốt hơn không", "so với Clean Architecture/feature-based thì sao", "cách làm này khác gì cách X". Không dùng để giải thích một khái niệm đơn lẻ (dùng concept-explainer) hay phân tích toàn bộ dự án (dùng codebase-explainer).
---

# Approach Comparator

Mục tiêu: giúp người dùng thấy cách dự án đang làm **nằm ở đâu** so với các cách làm khác, mạnh và yếu ở điểm nào, và **có nên đổi không**, trong đúng bối cảnh của dự án này. Mục tiêu không phải là đọc lại "best practice" chung chung.

**Trả lời trong khung chat.** Không tạo file, tài liệu, artifact hay trang web.

## Nguyên tắc

- **Hiểu cách của dự án trước, rồi mới đi tìm cách của người khác.** Không nắm được dự án đang làm gì và vì sao thì so sánh sẽ lệch.
- **Có nguồn thật.** Cách làm bên ngoài phải lấy từ nguồn tra được trong phiên này, có link. Kiến thức có sẵn chỉ dùng để định hướng tìm kiếm. Không có công cụ tra web thì nói rõ và đánh dấu phần so sánh là "(từ kiến thức chung, chưa kiểm chứng nguồn mới)".
- **Đúng bối cảnh.** Một cách làm "chuẩn" cho hệ thống 50 service có thể là thừa với đồ án 2 người. Luôn cân theo quy mô, giai đoạn dự án, kích thước team và ràng buộc trong đặc tả. Cách dự án đang làm hợp lý thì nói thẳng là hợp lý.
- **Công bằng.** Nêu cả ưu điểm của cách dự án đang làm lẫn nhược điểm của các cách khác. Tránh giọng "dự án làm sai".
- **Không tự sửa code.** Chỉ đề xuất. Nếu người dùng muốn đổi, gợi ý các bước, còn thực hiện là việc riêng.
- **Bản quyền:** diễn đạt lại bằng lời của mình. Trích nguyên văn nếu cần thì ngắn (dưới 15 từ), trong ngoặc kép, có nguồn.

## Quy trình

Mở đầu câu trả lời bằng **"Câu trả lời ngắn"** (2–3 câu): cách dự án đang làm thuộc kiểu nào, có hợp không, và khuyến nghị (giữ / điều chỉnh nhỏ / cân nhắc chuyển đổi). Phần còn lại là căn cứ cho câu trả lời đó.

### 1. Chốt chủ đề so sánh
Xác định chính xác đang so cái gì (vd. "cách chia thư mục backend", "cách xử lý refresh token", "cách các service gọi nhau"). Câu hỏi mơ hồ thì chọn cách hiểu sát nhất với dự án và nói rõ đang hiểu theo cách đó. Chỉ hỏi lại khi các cách hiểu dẫn tới câu trả lời rất khác nhau.

### 2. Nắm cách dự án đang làm
- Đọc code liên quan, ghi `file:dòng` cho các điểm chính.
- Tìm **lý do** họ chọn cách này trong tài liệu của dự án: `docs/codebase-guide/` (do codebase-explainer tạo), `CLAUDE.md`/`AGENTS.md`, README, ADR (`docs/adr/`, `decisions/`), đặc tả và design doc (`openspec/changes/*/design.md`, `openspec/specs/`, `specs/`, `docs/`). Không tìm thấy thì ghi rõ là không có tài liệu giải thích.
- Ghi nhận phiên bản framework/ngôn ngữ, vì cách làm khuyến nghị thường đổi theo phiên bản.
- Tóm lại trong 3–6 gạch đầu dòng: dự án làm thế nào, vì sao (nếu biết), ràng buộc gì.

### 3. Tìm các cách làm khác
- Nếu công cụ tra web (WebSearch/WebFetch) đang ở dạng hoãn nạp (deferred), nạp chúng một lần qua ToolSearch trước khi tìm.
- Chạy nhiều truy vấn tìm kiếm song song, nhắm vào: tài liệu chính thức của framework (đúng phiên bản), reference architecture / sample app chính thức, repo mã nguồn mở nổi tiếng cùng stack, bài viết kỹ thuật uy tín (blog kỹ sư của công ty lớn, tác giả có tên tuổi), sách/khái niệm kinh điển. Diễn đàn hỏi đáp chỉ dùng làm nguồn phụ.
- Mở và đọc các nguồn chính để kiểm chứng (đừng chỉ dựa vào đoạn trích trong kết quả tìm kiếm). Để ý ngày đăng và phiên bản. Nguồn kinh điển nhưng cũ (vd. bài viết 2019) vẫn dùng được cho **nguyên tắc** nếu tài liệu hiện hành không nói ngược lại. Khi đó ghi năm của nguồn, và đừng dùng nó cho chi tiết API, vì API dễ đã đổi.
- Chọn ra **2–4 cách làm khác biệt rõ ràng** (không lấy 4 biến thể của cùng một ý).

### 4. So sánh
Bảng theo các tiêu chí phù hợp với chủ đề. Chọn trong số: độ phức tạp, dễ hiểu với người mới, khả năng mở rộng, mức độ phụ thuộc giữa các phần (coupling), dễ test, hiệu năng, bảo mật, trải nghiệm phát triển, công sức chuyển đổi, độ phổ biến trong cộng đồng.

| Tiêu chí | Dự án này | Cách A | Cách B |
|---|---|---|---|

Dưới bảng, mỗi cách làm khác có 2–3 câu giải thích nó là gì và ai dùng, kèm link.

### 5. Đánh giá theo bối cảnh dự án
- Cách dự án đang làm **phù hợp ở đâu**, **sẽ gặp vấn đề khi nào** (vd. khi tăng số module, khi thêm người, khi lên production).
- Có điểm nào trong code đi ngược hướng dẫn chính thức của chính framework đang dùng không. Nếu có, chỉ rõ `file:dòng` và nguồn. Điểm lệch lớn (ảnh hưởng tới kiến trúc hoặc độ đúng) đưa vào phần đánh giá. Điểm nhỏ (vd. một wrapper đã thừa ở phiên bản mới) gom vào một danh sách "Điểm nhỏ" tối đa 3 dòng, hoặc bỏ nếu không liên quan tới chủ đề đang so.

### 6. Khuyến nghị
Chọn một: **Giữ nguyên** / **Điều chỉnh nhỏ** / **Cân nhắc chuyển đổi**, kèm lý do. Nếu đề xuất thay đổi: các bước theo thứ tự, việc nào làm trước để ít rủi ro, cái giá phải trả. Kết thúc bằng 1–2 câu hỏi gợi ý tiếp (vd. "Muốn mình phác thảo cấu trúc thư mục mới cho module `order` không?").

### 7. Nguồn
Danh sách link đã dùng, mỗi link kèm một dòng "nguồn này cho biết gì".

## Độ dài
Đây là câu trả lời trong chat: viết vừa đủ để ra quyết định. Phần chữ (không tính bảng, code trích và danh sách nguồn) nhắm khoảng 500–900 từ, tối đa khoảng 1.000 từ. Câu hỏi hẹp (vd. "đặt file DTO ở đâu") thì ngắn hơn nhiều. Để giữ gọn: mỗi cách làm khác chỉ 2–3 câu; phần "dự án đang làm" tối đa 6 gạch đầu dòng; danh sách nguồn mỗi dòng một câu ngắn. Muốn chi tiết hơn thì để người dùng hỏi tiếp. Không chép lại toàn bộ tài liệu tìm được.
