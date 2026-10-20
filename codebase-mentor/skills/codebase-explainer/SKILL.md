---
name: codebase-explainer
description: Phân tích và giải thích toàn bộ một codebase cho người mới - dự án làm gì, viết bằng công nghệ gì và vai trò từng công nghệ, đặc thù ngôn ngữ/framework, file cấu hình, kiến trúc và tổ chức thư mục, mô hình dữ liệu, luồng khởi động, luồng request đi qua từng file, logic từng chức năng, nợ kỹ thuật, dự án đang ở giai đoạn nào và hướng phát triển đã đề ra - rồi ghi thành bộ tài liệu tiếng Việt trong docs/codebase-guide/. Dùng skill này mỗi khi người dùng muốn hiểu, học, onboard hoặc nắm tổng thể một repo/dự án, kể cả khi họ chỉ nói ngắn kiểu "giải thích dự án này", "học codebase", "dự án này làm gì", "onboard tôi vào repo này", "phân tích cấu trúc dự án", "code này chạy thế nào", "explain this codebase", "walk me through this repo", "how is this project structured". Không dùng cho việc chỉ giải thích một hàm/một file lẻ, sửa bug, hay review một diff.
---

# Codebase Explainer

Mục tiêu: người đọc bộ tài liệu này (thường là chính người dùng, vừa nhận một dự án lạ) phải trả lời được: *dự án làm gì, viết bằng gì và vì sao, code được tổ chức ra sao, một thao tác đi qua những file nào và từng dòng quan trọng làm gì, dự án đang ở đâu và định đi tiếp hướng nào.* Hãy viết như một senior đã làm lâu trong dự án ngồi dẫn người mới đi một vòng — cụ thể, có dẫn chứng, không lý thuyết suông.

## Nguyên tắc (và lý do)

- **Tiếng Việt, giữ thuật ngữ kỹ thuật tiếng Anh** (middleware, dependency injection, hook...). Lần đầu gặp một thuật ngữ thì giải thích ngắn trong ngoặc — người đọc có thể chưa biết.
- **Mọi nhận định có dẫn chứng** dạng `` `đường/dẫn/file.ext:dòng` `` hoặc `` `file.ext:dòng-dòng` `` (đường dẫn tương đối từ gốc repo). Tài liệu onboarding sai còn tệ hơn không có, vì người mới sẽ tin nó. Không chắc thì ghi rõ **(suy đoán)** và nói căn cứ. Không bịa tên file, hàm, phiên bản.
- **Đọc code thật trước khi kết luận.** Tên thư mục và README có thể lỗi thời; code mới là sự thật. Khi README và code mâu thuẫn, nói ra.
- **Từ ngoài vào trong:** tổng quan → công nghệ → cấu trúc → luồng → từng dòng. Người mới cần bản đồ trước khi cần chi tiết.
- **Module mẫu + khác biệt:** nếu dự án chia module/feature/service theo cùng khuôn, giải thích thật kỹ MỘT module tiêu biểu, rồi với các module còn lại chỉ nêu điểm KHÁC (bảng). Lặp lại cùng một giải thích 10 lần làm tài liệu loãng và che mất cái thực sự khác.
- **Chia mức độ sâu:** 2–3 luồng/chức năng cốt lõi giải thích tới từng dòng quan trọng; còn lại giải thích logic ở mức vừa (mục đích, các bước, quy tắc nghiệp vụ). Tài liệu quá dài thì không ai đọc.
- **Vai trò cụ thể, không định nghĩa chung chung.** Đừng viết "Redis là in-memory database"; hãy viết "Redis ở đây dùng để cache kết quả tìm kiếm sản phẩm 5 phút (`src/cache/product.ts:12`)".
- **Sơ đồ Mermaid** cho kiến trúc, luồng request (sequenceDiagram), quan hệ dữ liệu (erDiagram). Một sơ đồ đúng đáng giá hơn một trang chữ.
- **Đặc tả là nguồn "ý định", code là nguồn "sự thật".** Nếu dự án có đặc tả (spec, PRD, SRS, openspec, OpenAPI, user story, use case, ADR, design doc, file `.feature`...), hãy dùng nó để giải thích *vì sao* một quy tắc nghiệp vụ tồn tại, và đối chiếu với code để biết phần nào đã làm, làm dở, chưa làm, hay làm khác đặc tả. Chính sự chênh lệch đó cho người mới biết dự án đang ở bước nào.
- **Chỉ đọc, không sửa code của dự án, không chạy lệnh có thể ghi vào repo** (cài dependency, migrate, build vào thư mục dự án, test ghi file). Thứ duy nhất được ghi là thư mục tài liệu đầu ra.

## Quy trình

### Bước 0 — Trinh sát nhanh

Chạy script quét (chỉ dùng thư viện chuẩn Python, không sửa gì):

```bash
python <đường-dẫn-skill>/scripts/scan_repo.py <gốc-repo>
```

Script in ra: file manifest và stack đoán được, số file theo ngôn ngữ, cây thư mục rút gọn, tài liệu và **đặc tả** (với openspec có cả tiến độ `tasks.md` của từng change), file cấu hình, tên các file `.env` thật, ứng viên entry point, số TODO/FIXME/HACK, tóm tắt git (commit gần đây, branch nào mới hơn branch hiện tại, file thay đổi nhiều nhất). Không có Python thì tự làm tương đương bằng Glob/Grep/git. Kết quả này là điểm xuất phát, không phải kết luận.

Sau đó đọc theo thứ tự ưu tiên: README/docs/CLAUDE.md/AGENTS.md → **đặc tả & tài liệu thiết kế** (script liệt kê ở mục "Đặc tả") → manifest (package.json, pom.xml, go.mod, pyproject...) → entry point → router/định nghĩa API → model/schema → một module tiêu biểu từ đầu đến cuối.

Nếu người dùng đưa kèm đặc tả nằm ngoài repo (file Markdown, Word/PDF, link, đoạn dán vào chat), coi nó như đặc tả của dự án và đọc trước khi đọc code.

**Có đặc tả thì học từ đặc tả trước.** Nhiều dự án viết đặc tả trước khi code. Đặc tả chứa đúng thứ người mới cần mà code không nói ra: ai dùng, muốn luồng chạy thế nào, quy tắc nghiệp vụ là gì, vì sao chọn thiết kế này. Đọc đặc tả trước và ghi thành một **bản đồ thiết kế** (tác nhân, chức năng, luồng thiết kế, quy tắc nghiệp vụ, tiêu chí chấp nhận, quyết định thiết kế, mỗi mục có nguồn). Sau đó đọc code để đối chiếu với bản đồ đó. Khi giải thích luồng (phần 8) và chức năng (phần 9), đi theo thứ tự **Thiết kế → Thực tế → Chênh lệch**. Người đọc hiểu ý định trước, rồi mới thấy code hiện thực ý định đó ra sao và còn thiếu gì.

**Dự án mới có đặc tả, chưa có hoặc có rất ít code:** vẫn làm đủ các phần. Phần 6, 8 và 9 giải thích theo thiết kế, ghi rõ "(chưa hiện thực)". Phần 12 trở thành bảng việc cần làm theo đặc tả.

Cách tìm, đọc và dùng đặc tả: `references/analysis-guide.md` mục 0.

Cách tự nhận diện stack, entry point và "phép màu" của từng framework: xem `references/stack-detection.md`.

### Bước 1 — Quyết định phạm vi và độ sâu

Ước lượng quy mô (số file nguồn, số module/service). Chọn:
- **Luồng đào sâu** (2–3): ưu tiên luồng thể hiện nghiệp vụ cốt lõi (vd. đặt hàng, thanh toán, tạo bài viết), luồng có auth, và luồng chạm DB. Gợi ý chọn: route/command được nhiều code phụ thuộc, file thay đổi nhiều trong git, tên khớp với mục đích dự án trong README.
- **Module mẫu:** module đầy đủ tầng nhất, điển hình nhất (không phải module lạ nhất).

Nếu dự án lớn (khoảng >500 file nguồn hoặc >8 module/service) và người dùng đang tương tác được: đề xuất lựa chọn của bạn kèm lý do ngắn và hỏi họ có muốn đào chỗ khác không, trước khi viết. Nếu không hỏi được (chạy tự động, hoặc người dùng đã bảo cứ làm), tự chọn và ghi rõ lựa chọn + lý do trong README đầu ra.

**Đọc song song bằng subagent** (nếu có công cụ subagent): khi dự án có từ khoảng 150 file nguồn hoặc từ 3 vùng tách biệt trở lên (frontend/backend/worker, nhiều service, đặc tả dày), nên giao cho subagent đọc song song từng vùng (frontend, từng service/module, hạ tầng + tài liệu + git), mỗi vùng một agent, rồi tổng hợp lại. Các luồng đào sâu (phần 8) thì tự đọc. Kết quả subagent là bản nháp: trước khi đưa dẫn chứng của nó vào tài liệu, tự mở lại một phần (nhất là những gì dùng ở phần 8, 9, 11) để chắc file, dòng và nội dung đúng.

### Bước 2 — Phân tích và viết 13 phần

Viết vào `docs/codebase-guide/` ở gốc repo (trừ khi người dùng chỉ định chỗ khác). Mỗi phần một file. Nếu thư mục đã tồn tại, đọc nó trước và cập nhật thay vì ghi đè mù — người dùng có thể đã sửa tay.

Viết từng file ngay khi phân tích xong phần đó (không dồn hết đến cuối), để công sức không mất nếu phiên bị ngắt.

| File | Nội dung chính |
|---|---|
| `README.md` | Mục lục, tóm tắt dự án 3–5 câu, phạm vi đã chọn (luồng đào sâu, module mẫu, lý do), thứ tự nên đọc |
| `01-tong-quan.md` | Dự án là gì, giải quyết vấn đề gì, cho ai, loại dự án, các thành phần lớn |
| `02-cong-nghe.md` | Bảng công nghệ: tên, phiên bản, vai trò CỤ THỂ trong dự án, dùng ở file nào |
| `03-dac-thu-ngon-ngu-framework.md` | **Phần quan trọng nhất cho người mới** — xem bên dưới |
| `04-file-cau-hinh.md` | Từng file cấu hình/file lạ: tác dụng, thiết lập quan trọng, sửa thì ảnh hưởng gì |
| `05-kien-truc-thu-muc.md` | Pattern kiến trúc, cây thư mục có chú thích, quy tắc phụ thuộc, module mẫu + bảng khác biệt, sơ đồ |
| `06-mo-hinh-du-lieu.md` | Entity/bảng/schema, quan hệ (erDiagram), ý nghĩa nghiệp vụ, nơi định nghĩa, migration |
| `07-luong-khoi-dong.md` | Từ entry point, khởi tạo những gì theo thứ tự nào, trích code |
| `08-luong-request.md` | Trace 1–3 luồng qua từng file, trích code, giải thích dòng, kiến thức nền mỗi chặng, sequenceDiagram |
| `09-chuc-nang.md` | Từng chức năng: mục đích, file, luồng xử lý, quy tắc nghiệp vụ, validate, edge case, lỗi; nếu có đặc tả: yêu cầu gốc và code có khớp không |
| `10-thuat-ngu.md` | Thuật ngữ domain và của dự án, nghĩa, nơi xuất hiện |
| `11-no-ky-thuat-rui-ro.md` | Trùng lặp, chỗ phức tạp, thiếu test, phụ thuộc cũ, chỗ dễ vỡ |
| `12-trang-thai-huong-phat-trien.md` | Dự án đang ở giai đoạn nào, việc dở dang, bảng độ phủ đặc tả (nếu có đặc tả), hướng xử lý/kế hoạch đã đề ra |
| `13-lo-trinh-doc-tiep.md` | Thứ tự file nên đọc tiếp, câu hỏi gợi ý để hỏi sâu |

Hướng dẫn chi tiết từng phần (cần tìm gì, ở đâu, viết thế nào): `references/analysis-guide.md`. Khung mẫu từng file: `references/output-templates.md`. Đọc cả hai trước khi viết.

**Phần nào không áp dụng** (vd. thư viện không có DB, CLI không có HTTP request): đừng bỏ file. Thích nghi nội dung — "luồng request" của CLI là luồng một lệnh, của frontend là luồng một tương tác người dùng, của worker là luồng một message/job. Nếu thật sự không có gì (không có dữ liệu lưu trữ), viết 2–3 câu nói rõ vì sao và dữ liệu nằm ở đâu thay vào đó.

### Phần 3 — Đặc thù ngôn ngữ & framework (viết kỹ nhất)

Đây là phần người mới vấp nhiều nhất: code "chạy mà không thấy ai gọi". Mỗi mục phải minh họa bằng code THẬT trong dự án (trích + `file:dòng`), không dùng ví dụ sách giáo khoa. Bao gồm:

1. **Ngôn ngữ:** hệ thống type, cách tổ chức module/import, mô hình bất đồng bộ, cách xử lý lỗi, idiom/cú pháp đặc trưng dễ gây bỡ ngỡ — chỉ những gì dự án thực sự dùng.
2. **Framework:** vòng đời ứng dụng và request, dependency injection, decorator/annotation, hook, middleware, convention over configuration, ORM, code sinh tự động.
3. **Khác biệt do phiên bản:** dự án dùng API đời nào (vd. Next.js App Router vs Pages Router, Spring Boot 3 `jakarta.*` vs 2 `javax.*`), để người đọc không tra nhầm tài liệu cũ.
4. **"Những thứ chạy ngầm dễ gây bối rối":** bảng — cái gì chạy, nó được kích hoạt bởi đâu (annotation, tên file, config, reflection), file liên quan.
5. **"Nếu bạn quen X":** so sánh ngắn với 1–2 stack phổ biến tương đương (vd. NestJS ↔ Spring Boot, React hooks ↔ Vue composition API).

Danh sách "phép màu" cần kiểm tra theo từng framework phổ biến: `references/stack-detection.md`.

### Mẹo để dẫn chứng chính xác

- **Đánh số dòng từng file riêng.** Dùng công cụ đọc file (có sẵn số dòng), hoặc `cat -n` một file mỗi lần. **Tuyệt đối không** `cat -n a b c`, `head -n` nhiều file, hay `cat -n a b | grep ...` trong một lệnh: số dòng chạy nối tiếp qua các file, dẫn chứng lệch mà dòng sai vẫn "tồn tại" nên script kiểm tra không bắt được.
- **Ghi đường dẫn đầy đủ từ gốc repo, không viết tắt kiểu `order/.../X.java`.** Tên ngắn (`OrderService.java:56`) chỉ được chấp nhận khi nó khớp duy nhất một file trong repo. Repo có nhiều file trùng tên (microservices có `OrderService.java` ở nhiều service; openspec có hàng chục `spec.md`; monorepo có nhiều `index.ts`) thì luôn ghi đầy đủ. Nếu lỡ viết tắt, `check_citations.py --fix` sẽ tự thay những chỗ có đích duy nhất.
- **Kiểm chứng hành vi mà không chạy code:** đọc mã nguồn thư viện trong cache cục bộ (`node_modules/`, `~/.m2/repository/` (giải nén `*-sources.jar` hoặc `javap` trên jar), `site-packages/`, `~/go/pkg/mod/`) là cách kiểm tra chỉ đọc, chấp nhận được. Ghi rõ phiên bản thư viện đã kiểm.
- **File tạm** (script phụ, ghi chú) đặt trong thư mục scratchpad với tên riêng có tiền tố theo dự án, để tránh đè file của phiên khác.
- **Phân tích code đang checkout (HEAD).** Mọi dẫn chứng `file:dòng` trỏ vào HEAD. Nếu script báo có branch mới hơn, ghi ở phần 12 branch đó thay đổi gì (`git log HEAD..<branch> --oneline`, `git diff --stat HEAD...<branch>`), và dẫn chứng nó dạng `` `<branch>:đường/dẫn` `` không kèm số dòng. Không checkout hay pull để đổi trạng thái repo.
- **Trích code nguyên văn.** Được lược bớt bằng `...`. Nếu viết lại hoặc dồn dòng cho gọn, ghi `(rút gọn)` ngay ở dòng vị trí đầu block, ví dụ `// src/a.ts:10-30 (rút gọn)`.
- **Không chạy test, build, migrate hay cài dependency** để "kiểm chứng": các lệnh đó có thể ghi vào repo, xoá dữ liệu (test dùng chung DB thật) hoặc gọi dịch vụ ngoài. Đọc code và test là đủ. Chỉ chạy khi người dùng yêu cầu, sau khi đã đọc kỹ lệnh đó làm gì. Trong tài liệu đầu ra (vd. bài tập làm quen ở phần 13) vẫn được *gợi ý người dùng* tự chạy test/app, nhưng phải kèm cảnh báo nếu lệnh có rủi ro (vd. test xoá dữ liệu DB đang trỏ tới).
- Repo lớn thì cây thư mục của `scan_repo.py` bị cắt; thêm `--max-tree-lines 400` hoặc `--max-tree-depth 2` nếu cần.

### Bước 3 — Kiểm tra dẫn chứng

Sau khi viết xong, chạy:

```bash
python <đường-dẫn-skill>/scripts/check_citations.py <thư-mục-đầu-ra> <gốc-repo>
# có dẫn chứng viết tắt/tên ngắn với đích duy nhất thì thêm --fix để tự thay bằng đường dẫn đầy đủ
```

Script kiểm tra mọi `file:dòng` trong tài liệu: file có tồn tại không, mọi vùng dòng có nằm trong file không, và block code có ghi vị trí có khớp nội dung file thật không. Sửa mọi dẫn chứng hỏng (tìm lại đúng vị trí, hoặc bỏ số dòng nếu chỉ dẫn tới file) và chạy lại tới khi sạch. Script không biết một câu giải thích có *đúng ý* hay không, nên hãy đọc lại 2–3 đoạn quan trọng nhất ở phần 8 và 9.

### Bước 4 — Tóm tắt trong chat

Ngắn gọn (không dán lại tài liệu):
- Dự án là gì trong 2–3 câu, stack chính.
- Đường dẫn tới `docs/codebase-guide/README.md`.
- Phạm vi đã chọn (luồng đào sâu, module mẫu) và những gì chưa đào.
- 2–3 điều đáng chú ý nhất (rủi ro lớn, chỗ "phép màu" quan trọng, trạng thái dự án).
- 3–5 câu hỏi gợi ý để người dùng hỏi sâu tiếp.

## Khi người dùng hỏi sâu sau đó

Tiếp tục theo cùng nguyên tắc (dẫn chứng, code thật, tiếng Việt). Nếu câu trả lời đáng giữ lại (một luồng mới được trace, một chức năng được giải thích kỹ), đề nghị bổ sung vào file tương ứng trong `docs/codebase-guide/`.
