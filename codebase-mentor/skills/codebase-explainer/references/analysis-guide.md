# Hướng dẫn phân tích từng phần

Mỗi phần: **Mục tiêu** (người đọc phải hiểu được gì) → **Tìm ở đâu** → **Viết thế nào** → **Bẫy thường gặp**.

## Mục lục
0. Đặc tả & tài liệu thiết kế (dùng xuyên suốt)
1. Tổng quan dự án
2. Công nghệ & vai trò
3. Đặc thù ngôn ngữ & framework
4. File cấu hình
5. Kiến trúc & tổ chức thư mục
6. Mô hình dữ liệu
7. Luồng khởi động
8. Luồng request
9. Từng chức năng
10. Từ điển thuật ngữ
11. Nợ kỹ thuật & rủi ro
12. Trạng thái dự án & hướng phát triển
13. Lộ trình đọc tiếp

---

## 0. Đặc tả & tài liệu thiết kế

Đặc tả không phải một phần riêng, mà là nguồn dùng xuyên suốt. Nó trả lời câu "dự án *định* làm gì và *vì sao*", còn code trả lời câu "dự án *thực sự* làm gì". Người mới cần cả hai.

**Tìm ở đâu** (script quét liệt kê ở mục "Đặc tả & tài liệu thiết kế"):
- Thư mục: `openspec/` (`specs/` = đặc tả hiện hành, `changes/` = thay đổi đang đề xuất/đang làm, `changes/archive/` = đã xong), `specs/`, `spec/`, `docs/`, `requirements/`, `rfcs/`, `adr/`/`docs/adr/`/`decisions/`, `design/`.
- File: PRD, SRS, BRD, `requirements*`, `*spec*.md`, `user-stories*`, `use-case*`, `design.md`, `proposal.md`, `tasks.md`, `ARCHITECTURE.md`, `blueprint*`, kế hoạch/timeline (`PLAN.md`, `ROADMAP.md`, `timeline.csv`).
- Đặc tả API/hợp đồng: `openapi.*`, `swagger.*`, `*.graphql`, `*.proto`, `asyncapi.*`, JSON Schema.
- Đặc tả kiểm thử: `*.feature` (Gherkin/BDD), test có mô tả nghiệp vụ.
- File Word/PDF/PowerPoint trong `docs/` — đọc nếu có công cụ đọc được; không đọc được thì liệt kê tên và nói rõ là chưa đọc.
- Đặc tả người dùng đưa kèm ngoài repo.
- Lưu ý: `*.spec.ts`, `*.spec.js`, `*Spec.java`... thường là **file test**, không phải đặc tả.

**Đọc thế nào: lập "bản đồ thiết kế" trước khi đọc code.** Đây là ghi chú làm việc của bạn, không phải một file đầu ra. Nội dung của nó được rải vào các phần bên dưới. Mỗi mục kèm nguồn `file:dòng`:

| Mục | Tìm trong đặc tả | Dùng ở phần |
|---|---|---|
| Mục tiêu, phạm vi, ngoài phạm vi | phần giới thiệu, `proposal.md` "Why" | 1 |
| Tác nhân / vai trò người dùng | actor, persona, role | 1, 9 |
| Chức năng / use case / user story | danh sách tính năng, "As a … I want …" | 9 |
| **Luồng thiết kế**: các bước, ai làm gì, hệ thống phản hồi gì | use case flow, sequence diagram, "Scenario: WHEN … THEN …" | 8, 9 |
| **Quy tắc nghiệp vụ**: điều kiện, giới hạn, công thức, trạng thái | "Requirement: … SHALL/MUST …", business rule, bảng trạng thái | 9 |
| Tiêu chí chấp nhận, edge case | acceptance criteria, scenario lỗi | 9 |
| Mô hình dữ liệu dự kiến | ERD, data model, bảng field | 6 |
| Quyết định thiết kế + lý do + phương án bị loại | `design.md` "Decisions", ADR | 5, 6 |
| Yêu cầu phi chức năng | hiệu năng, bảo mật, giới hạn | 11 |
| Kế hoạch, mốc, việc còn mở | `tasks.md`, roadmap, timeline | 12 |
| Thuật ngữ | glossary, định nghĩa | 10 |

Mẹo theo định dạng:
- **openspec:** `specs/<capability>/spec.md` có `### Requirement:` (quy tắc, thường dùng SHALL/MUST) và `#### Scenario:` (luồng mẫu dạng WHEN/THEN). Đây chính là quy tắc nghiệp vụ và luồng thiết kế, đã viết sẵn. `changes/<tên>/proposal.md` cho biết *vì sao* có thay đổi, `design.md` cho biết *chọn cách nào và vì sao*, `tasks.md` cho biết *đã làm tới đâu*. `specs/` bên trong một change là phần đặc tả sẽ thêm hoặc sửa (ADDED/MODIFIED/REMOVED).
- **User story / use case:** luồng chính, luồng thay thế, luồng ngoại lệ tương ứng với happy path, nhánh rẽ và nhánh lỗi khi trace code.
- **Gherkin `.feature`:** `Given/When/Then` là kịch bản người dùng đã được kiểm thử. Đây là bằng chứng mạnh rằng luồng đó hoạt động.
- **Tài liệu dài:** đọc mục lục trước, rồi đọc kỹ phần yêu cầu chức năng, quy tắc nghiệp vụ và các thay đổi đang mở. Không cần đọc hết từng chữ.
- **File Word/PDF** (ít gặp): PDF đọc bằng công cụ đọc file (theo trang); `.docx` là file zip, phần chữ nằm trong `word/document.xml`. Không đọc được thì liệt kê tên file và nói rõ là chưa đọc.

**Giải thích theo "Thiết kế → Thực tế → Chênh lệch"** (phần 8, 9):
1. **Thiết kế:** đặc tả muốn gì. Tóm tắt luồng hoặc quy tắc bằng lời của bạn, có nguồn. Nếu đặc tả có sơ đồ hoặc scenario thì dựa vào đó để vẽ sơ đồ.
2. **Thực tế:** code hiện thực điều đó ở đâu, như thế nào (trace có dẫn chứng như bình thường).
3. **Chênh lệch:** chỗ code khác đặc tả, phần đặc tả chưa có code, phần code làm thêm mà đặc tả không nói tới. Nếu khớp hoàn toàn thì ghi "khớp" trong một dòng.

Cách này giúp người mới hiểu *ý định* trước rồi mới tới *cách làm*. Nhờ vậy họ đọc code nhanh hơn và biết chỗ nào là lỗi, chỗ nào là chủ ý.

**Dùng vào đâu:**
- **Phần 1:** mục đích, người dùng, phạm vi, lấy từ đặc tả (ghi nguồn).
- **Phần 5/6:** quyết định kiến trúc trong ADR/design doc giải thích *vì sao* code tổ chức như vậy.
- **Phần 9:** mỗi chức năng có dòng "Theo đặc tả" (yêu cầu gốc, trích nguồn) và "Khớp với code?". Quy tắc nghiệp vụ trong đặc tả giúp giải thích code; khi code làm khác đặc tả, nói rõ khác ở đâu.
- **Phần 10:** thuật ngữ thường được định nghĩa trong đặc tả.
- **Phần 12:** bảng **độ phủ đặc tả**: mỗi yêu cầu chính có trạng thái *Đã làm / Làm dở / Chưa làm / Làm khác đặc tả / Không rõ*, kèm dẫn chứng ở cả đặc tả và code. Với openspec: các change chưa archive là việc đang làm hoặc sắp làm; `tasks.md` có checkbox cho biết tiến độ.

**Khi đặc tả và code mâu thuẫn:** đừng tự chọn bên đúng. Ghi cả hai, nêu căn cứ. Tài liệu cũ hơn code thì thường là đặc tả lỗi thời, nhưng cũng có thể là code chưa làm xong. Dùng ngày commit của hai bên để nhận định, và ghi đó là (suy đoán).

**Không có đặc tả:** nói rõ ở README đầu ra là không tìm thấy đặc tả, và các mô tả nghiệp vụ được suy ra từ code, test, UI.

---

## 1. Tổng quan dự án

**Mục tiêu:** đọc 1 phút là biết dự án làm gì, cho ai, gồm những mảnh lớn nào.

**Tìm ở đâu:** README, `docs/`, CLAUDE.md/AGENTS.md, `description` trong manifest, tên package, landing page/route gốc, seed data (cho biết domain), git log đầu tiên và gần nhất.

**Viết thế nào:**
- Một câu "dự án này là…".
- Vấn đề giải quyết, người dùng mục tiêu (suy ra từ route, role, UI text nếu README không nói — ghi (suy đoán)).
- Loại dự án: web app full-stack / REST API / GraphQL / SPA / mobile / CLI / library / monorepo / microservices / data pipeline / smart contract...
- Bảng các thành phần lớn (app, service, package): tên, thư mục, vai trò một dòng.
- Sơ đồ khối Mermaid (`flowchart`) nếu có ≥3 thành phần tương tác.

**Bẫy:** README là template mặc định (vd. "This project was bootstrapped with Create React App") — đừng coi đó là mô tả dự án.

## 2. Công nghệ & vai trò

**Mục tiêu:** biết từng công nghệ được dùng để làm gì *trong dự án này*.

**Tìm ở đâu:** manifest + lockfile (phiên bản thật), Dockerfile/docker-compose (DB, cache, queue), CI config, import thực tế trong code.

**Viết thế nào:** bảng nhóm theo lớp (Ngôn ngữ & runtime / Framework / Dữ liệu / Hạ tầng / Công cụ dev / Thư viện nghiệp vụ):

| Công nghệ | Phiên bản | Vai trò trong dự án | Dùng ở đâu |
|---|---|---|---|

- Vai trò phải cụ thể: "zod — validate body của request ở tầng controller (`src/user/user.schema.ts:5`)".
- Dependency khai báo nhưng không import ở đâu → ghi "có vẻ không dùng" (đáng ghi vào phần 11).
- Chỉ liệt kê thư viện có ý nghĩa; gom các thư viện vặt (types, plugin lint) thành một dòng.

**Bẫy:** lấy phiên bản từ range trong manifest (`^4.0.0`) — nếu có lockfile thì dùng phiên bản thật, hoặc ghi range kèm chú thích.

## 3. Đặc thù ngôn ngữ & framework

**Mục tiêu:** người từ stack khác sang đọc code không bị "lạc"; hiểu những thứ chạy ngầm.

**Tìm ở đâu:** entry point, file cấu hình framework, annotation/decorator phổ biến (grep `@`), hook, file có tên theo quy ước (`page.tsx`, `+page.svelte`, `*.module.ts`, `urls.py`), code sinh tự động (`generated/`, `*.g.dart`, OpenAPI client, Prisma client).

**Viết thế nào:** theo 5 mục trong SKILL.md. Với mỗi đặc thù:
1. Tên khái niệm + giải thích 1–3 câu bằng ngôn ngữ đời thường.
2. Trích code thật từ dự án (5–15 dòng) + `file:dòng`.
3. Giải thích đoạn code đó làm gì, cái gì xảy ra ngầm.
4. "Hệ quả khi làm việc" — vd. "muốn thêm route mới chỉ cần tạo file trong `app/`, không cần đăng ký".

Ưu tiên theo mức độ gây bối rối, không theo mức độ phổ biến. Bỏ những gì dự án không dùng.

Danh sách cần kiểm tra theo stack: `stack-detection.md` mục "Phép màu theo framework".

**Bẫy:** viết thành bài giảng chung về ngôn ngữ. Nếu một đoạn không có code dự án minh họa, có lẽ nó không cần thiết.

## 4. File cấu hình

**Mục tiêu:** nhìn một file cấu hình lạ là biết nó làm gì và có dám sửa không.

**Tìm ở đâu:** file ở gốc repo và gốc từng package/service; file dot (`.env.example`, `.editorconfig`, `.nvmrc`, `.prettierrc`, `.husky/`, `.github/`), build config (`vite.config`, `webpack`, `tsconfig`, `babel`, `pom.xml` plugins, `build.gradle`), `application.yml/properties`, Docker/K8s/nginx, CI/CD, lint/format, file khóa (lockfile), file của công cụ AI (`.claude/`, `CLAUDE.md`, `.cursor/`).

**Viết thế nào:** nhóm theo mục đích (Build & biên dịch / Runtime & môi trường / Hạ tầng / Chất lượng code / CI/CD / Công cụ khác). Mỗi file:
- **Tác dụng** một câu.
- **Thiết lập quan trọng**: trích các key thực sự ảnh hưởng (vd. `paths` alias trong tsconfig, `proxy` trong vite, profile Spring, port, biến môi trường bắt buộc).
- **Sửa thì sao**: hậu quả/rủi ro khi đổi.

Với `.env.example`/biến môi trường: bảng tên biến, ý nghĩa, nơi đọc trong code. **Không bao giờ chép giá trị bí mật** từ `.env` thật — chỉ ghi tên biến.

**Bẫy:** liệt kê mọi file mà không giải thích. File tầm thường (`.gitignore` chuẩn) gom một dòng.

## 5. Kiến trúc & tổ chức thư mục

**Mục tiêu:** có bản đồ — code nào nằm ở đâu, tầng nào được gọi tầng nào.

**Tìm ở đâu:** cây thư mục, import giữa các thư mục, cấu hình workspace (monorepo), docker-compose (microservices), quy tắc lint về import.

**Viết thế nào:**
1. **Pattern kiến trúc** đang dùng (layered, MVC, clean/hexagonal, feature-based/modular, microservices, monorepo, BFF...) + dẫn chứng vì sao nhận định vậy. Pattern pha trộn thì nói rõ.
2. **Cây thư mục có chú thích** (2–3 cấp, rút gọn, mỗi dòng một chú thích ngắn).
3. **Quy tắc phụ thuộc**: tầng nào import tầng nào; có vi phạm nào thấy được không.
4. **Module mẫu**: chọn một module điển hình, liệt kê từng file trong nó và vai trò, cách các file nối với nhau.
5. **Bảng khác biệt** cho các module còn lại:

| Module | Giống mẫu? | Khác biệt đáng chú ý |
|---|---|---|

6. Sơ đồ Mermaid (flowchart các tầng/service và hướng gọi).

**Bẫy:** suy pattern từ tên thư mục mà không kiểm tra import thật.

## 6. Mô hình dữ liệu

**Mục tiêu:** hiểu dữ liệu cốt lõi — đó thường là chìa khóa hiểu nghiệp vụ.

**Tìm ở đâu:** ORM model/entity (Prisma schema, TypeORM/JPA entity, Django/SQLAlchemy model, Mongoose schema), migration, file SQL, GraphQL schema, type/interface DTO, state store ở frontend (Redux/Zustand) nếu không có DB.

**Viết thế nào:**
- `erDiagram` Mermaid cho entity chính (không cần mọi cột — chỉ khóa và cột quan trọng).
- Bảng: entity, ý nghĩa nghiệp vụ, file định nghĩa, quan hệ chính.
- Các trường có ý nghĩa đặc biệt (enum trạng thái, soft delete, cột JSON, version cho optimistic lock).
- Migration: công cụ, thư mục, cách chạy.
- Microservices: DB thuộc service nào, dữ liệu đồng bộ giữa service bằng cách nào (event, CDC...).

## 7. Luồng khởi động

**Mục tiêu:** biết từ lúc chạy lệnh start đến lúc sẵn sàng nhận việc, chuyện gì xảy ra.

**Tìm ở đâu:** script `start`/`dev` trong manifest, `main`, `Dockerfile CMD/ENTRYPOINT`, file bootstrap (`main.ts`, `index.js`, `Application.java`, `manage.py`, `main.go`, `App.tsx` + `main.tsx`).

**Viết thế nào:** danh sách đánh số theo thứ tự thực thi; mỗi bước trích code + `file:dòng` + giải thích: load config/env → kết nối DB/cache/queue → đăng ký DI/plugin → middleware (theo đúng thứ tự, vì thứ tự quan trọng) → router → lắng nghe port / mount UI. Có thể dùng flowchart.

## 8. Luồng request (trace chi tiết)

**Mục tiêu:** đi cùng một thao tác qua từng file, hiểu từng dòng quan trọng — phần "dạy" sâu nhất.

**Chọn luồng:** 1–3 luồng theo tiêu chí ở SKILL.md bước 1. Với frontend: một tương tác người dùng (click → state → gọi API → render). Với full-stack: nên có ít nhất một luồng đi từ UI xuống DB và quay lại.

Nếu có đặc tả, ưu tiên chọn luồng được đặc tả mô tả kỹ (có scenario/use case), vì khi đó so được thiết kế với thực tế.

**Viết thế nào** cho mỗi luồng:
1. Mô tả: thao tác gì, ai làm, kết quả mong đợi. Nếu có đặc tả: thêm mục **Theo thiết kế** tóm tắt luồng mà đặc tả mô tả (các bước, quy tắc, nhánh lỗi), có nguồn.
2. `sequenceDiagram` Mermaid các thành phần tham gia.
3. Từng chặng (đánh số):
   - **File & vị trí**: `file:dòng-dòng`
   - **Trích code** (chỉ đoạn liên quan, 5–25 dòng)
   - **Dòng này làm gì**: giải thích theo dòng/khối, đặc biệt dòng không hiển nhiên
   - **Kiến thức nền**: khái niệm cần biết ở chặng này (vd. "middleware trong Express nhận `(req, res, next)`; gọi `next()` để chuyển tiếp") — ngắn, gắn với code
   - **Dữ liệu ra**: chặng này trả gì cho chặng sau
4. **Nhánh lỗi**: nếu validate fail / không có quyền / DB lỗi thì đi đường nào, trả về gì.
5. **Chênh lệch so với thiết kế** (nếu có đặc tả): bảng gồm điểm trong đặc tả | code làm gì | khớp/khác/chưa làm.

**Bẫy:** bỏ qua middleware/interceptor/guard chạy ngầm trước controller — đó chính là chỗ người mới hay mù.

## 9. Từng chức năng

**Mục tiêu:** hiểu logic nghiệp vụ của mỗi chức năng — phần người dùng muốn nói rõ nhất.

**Tìm ở đâu:** route/command list, service/use-case, màn hình UI, test (test thường mô tả quy tắc nghiệp vụ rõ nhất).

**Viết thế nào:** liệt kê chức năng theo nhóm (theo module/domain). Nếu có đặc tả, lấy danh sách chức năng từ đặc tả làm khung (kể cả chức năng chưa có code, ghi "(chưa hiện thực)"), rồi bổ sung chức năng có trong code mà đặc tả không nhắc tới. Mỗi chức năng:
- **Thiết kế** (nếu có đặc tả): yêu cầu, quy tắc nghiệp vụ, scenario gốc, có nguồn. Đây là phần giải thích "vì sao"
- **Mục đích** (góc nhìn người dùng)
- **File liên quan** (route → service → model)
- **Luồng xử lý**: các bước
- **Quy tắc nghiệp vụ**: điều kiện, công thức, trạng thái chuyển đổi (state machine thì vẽ `stateDiagram`)
- **Validate & phân quyền**
- **Edge case & xử lý lỗi**
- **Chênh lệch so với thiết kế** (nếu có đặc tả): khớp / làm khác ở điểm… / chưa làm / code làm thêm…

Chức năng cốt lõi viết đủ mục; chức năng CRUD đơn giản có thể gom vào một bảng. Nếu quá nhiều chức năng, có thể tách thành thư mục `09-chuc-nang/` với một file mỗi module và một `README.md` liệt kê.

## 10. Từ điển thuật ngữ

Bảng: thuật ngữ | nghĩa | nơi xuất hiện. Gồm: thuật ngữ nghiệp vụ (vd. "SKU", "promotion apply type"), từ viết tắt trong tên biến/thư mục (vd. `bff`, `dto`, `uc`), tên riêng nội bộ (tên service, tên tool). Sắp xếp theo alphabet.

## 11. Nợ kỹ thuật & rủi ro

**Tìm ở đâu:** TODO/FIXME/HACK, file rất dài/hàm rất dài, code lặp giữa module, thư mục test rỗng hoặc ít, dependency cũ/không dùng, `any`/`@SuppressWarnings`/`# type: ignore` nhiều, catch nuốt lỗi, bí mật hardcode (chỉ nêu vị trí, không chép giá trị), cấu hình bảo mật lỏng (CORS `*`, tắt CSRF).

**Viết thế nào:** bảng mức độ (Cao/Trung bình/Thấp) | vấn đề | vị trí | vì sao rủi ro | gợi ý. Ưu tiên những gì ảnh hưởng tới người sắp sửa code ("chỗ dễ vỡ khi sửa").

## 12. Trạng thái dự án & hướng phát triển

**Mục tiêu:** biết dự án đang ở bước nào và đã định đi tiếp hướng nào.

**Tìm ở đâu:**
- git: `git log --oneline -30`, ngày commit đầu/cuối, tần suất, branch đang có (`git branch -a`), branch hiện tại, thay đổi chưa commit (`git status`).
- TODO/FIXME/HACK trong code (gom theo chủ đề).
- Tài liệu kế hoạch: ROADMAP, CHANGELOG, `docs/`, ADR, spec/openspec, issue template, PLAN/TODO file, CLAUDE.md.
- Tính năng làm dở: route khai báo nhưng handler trống, flag tắt, code comment-out, UI placeholder, `throw new Error("not implemented")`.

**Viết thế nào:**
- **Giai đoạn hiện tại** (prototype / MVP / đang phát triển tích cực / ổn định / bảo trì / bỏ dở) + căn cứ.
- **Đang làm gì gần đây**: tóm tắt các commit/branch gần nhất theo chủ đề.
- **Việc dở dang**: bảng việc | dấu hiệu | vị trí.
- **Độ phủ đặc tả** (nếu có đặc tả): bảng yêu cầu | nguồn đặc tả | trạng thái | dẫn chứng trong code. Kết thúc bằng một dòng tổng kết (vd. "khoảng 12/18 yêu cầu chính đã làm xong").
- **Hướng xử lý/kế hoạch đã đề ra**: tổng hợp từ tài liệu và comment, trích nguồn. Phân biệt rõ "đã được ghi trong dự án" với "suy đoán của tôi".

## 13. Lộ trình đọc tiếp

- Danh sách 8–15 file theo thứ tự nên đọc, mỗi file kèm "đọc để hiểu gì".
- Gợi ý bài tập nhỏ để làm quen (vd. "thử thêm một field vào entity X và theo dấu nó tới API").
- 5–8 câu hỏi gợi ý để hỏi sâu tiếp (cụ thể theo dự án, không chung chung).
