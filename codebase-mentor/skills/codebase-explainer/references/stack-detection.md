# Nhận diện stack, entry point và "phép màu" theo framework

Dùng file này để tự nhận diện, không giả định trước stack. Một repo có thể chứa nhiều stack (frontend + backend + script Python) — nhận diện từng phần.

## Mục lục
1. Manifest → ngôn ngữ / hệ sinh thái
2. Dấu hiệu framework
3. Ứng viên entry point
4. Dấu hiệu kiến trúc
5. Phép màu theo framework (checklist cho phần 3)

---

## 1. Manifest → hệ sinh thái

| File | Hệ sinh thái | Đọc thêm |
|---|---|---|
| `package.json` (+ `package-lock.json`/`pnpm-lock.yaml`/`yarn.lock`/`bun.lock`) | JavaScript/TypeScript (Node, Bun, Deno) | `scripts`, `workspaces`, `type: module` |
| `tsconfig.json` | TypeScript | `paths`, `strict`, `module` |
| `pom.xml` / `build.gradle(.kts)` | Java/Kotlin (JVM) | `<modules>`, parent Spring Boot, plugins |
| `pyproject.toml` / `requirements*.txt` / `setup.py` / `Pipfile` / `uv.lock` | Python | entry `[project.scripts]` |
| `go.mod` | Go | module path, `cmd/` |
| `Cargo.toml` | Rust | `[workspace]`, `[[bin]]` |
| `composer.json` | PHP | Laravel/Symfony |
| `Gemfile` | Ruby | Rails |
| `*.csproj` / `*.sln` | C#/.NET | ASP.NET |
| `pubspec.yaml` | Dart/Flutter | |
| `foundry.toml` / `hardhat.config.*` | Solidity | |
| `turbo.json` / `nx.json` / `pnpm-workspace.yaml` / `lerna.json` | Monorepo JS | danh sách package |

## 2. Dấu hiệu framework

- **Next.js**: `next` trong deps, `next.config.*`, thư mục `app/` (App Router) hoặc `pages/` (Pages Router).
- **React SPA**: `react` + `vite`/`react-scripts`, `src/main.tsx`/`src/index.tsx`.
- **Vue/Nuxt**: `vue`, `nuxt.config.*`, `*.vue`. **Svelte/SvelteKit**: `svelte.config.*`, `+page.svelte`. **Angular**: `angular.json`.
- **Express/Koa/Fastify/Hono**: import tương ứng, `app.use(...)`, `app.get(...)`.
- **NestJS**: `@nestjs/core`, `*.module.ts`, `@Controller`, `@Injectable`.
- **Spring Boot**: `spring-boot-starter-*`, `@SpringBootApplication`, `application.yml/properties`.
- **Django**: `manage.py`, `settings.py`, `urls.py`. **Flask**: `Flask(__name__)`. **FastAPI**: `FastAPI()`, `@app.get`.
- **Laravel**: `artisan`, `routes/web.php`. **Rails**: `config/routes.rb`.
- **Go**: `net/http`, `gin`, `echo`, `fiber`, `chi`.
- **ORM**: Prisma (`schema.prisma`), TypeORM/Sequelize/Drizzle/Mongoose, JPA/Hibernate (`@Entity`), SQLAlchemy, Django ORM, GORM, Eloquent.

## 3. Ứng viên entry point

- JS/TS: `main`/`bin`/`exports` trong package.json, script `start`/`dev`, `src/index.*`, `src/main.*`, `server.*`, `app.*`.
- Java: class có `@SpringBootApplication` hoặc `public static void main`.
- Python: `manage.py`, `main.py`, `app.py`, `wsgi.py`/`asgi.py`, `__main__.py`, `[project.scripts]`.
- Go: `cmd/*/main.go`, `main.go`.
- Docker: `CMD`/`ENTRYPOINT` trong Dockerfile; `command` trong docker-compose.
- Frontend: `index.html` → script được nạp.

## 4. Dấu hiệu kiến trúc

- **Layered/MVC**: `controllers/` `services/` `repositories/`/`models/` `routes/`.
- **Feature-based/modular**: `modules/<tên>/` hoặc `features/<tên>/` mỗi cái tự chứa controller/service/model.
- **Clean/Hexagonal**: `domain/` `application/`/`usecases/` `infrastructure/` `adapters/` `ports/`.
- **Microservices**: nhiều thư mục mỗi cái có manifest + Dockerfile riêng, docker-compose/K8s nhiều service, gateway/BFF, message broker (Kafka/RabbitMQ).
- **Monorepo**: workspace config, `packages/`/`apps/`/`libs/`.

---

## 5. Phép màu theo framework

Checklist những thứ "chạy mà không thấy gọi". Chỉ đưa vào tài liệu cái dự án thực sự dùng, kèm code thật.

### JavaScript / TypeScript (chung)
- ESM vs CommonJS (`import` vs `require`, `"type": "module"`), path alias (`@/` từ tsconfig `paths`/vite `resolve.alias`).
- Event loop, Promise, `async/await`, lỗi trong promise không `await` bị nuốt.
- Type chỉ tồn tại lúc biên dịch (type erasure) → cần validate runtime (zod/joi/class-validator).
- Truthy/falsy, `?.`, `??`, destructuring, spread.
- Biến môi trường: `process.env`, `dotenv`, `import.meta.env` (Vite chỉ lộ biến có prefix `VITE_`).

### Express / Koa / Fastify
- Middleware chạy theo thứ tự `app.use`; `next()`; middleware lỗi có 4 tham số `(err, req, res, next)`.
- `req.user` thường được gắn bởi middleware auth (passport/jwt) — chỉ ra ở đâu.
- Router lồng (`app.use('/api', router)`) → URL thật là ghép tiền tố.

### NestJS
- Module/Provider/Controller, DI qua constructor, decorator `@Injectable/@Controller/@Get`.
- Thứ tự: Middleware → Guard → Interceptor (trước) → Pipe → Handler → Interceptor (sau) → Exception filter.
- `ValidationPipe` + DTO class-validator.

### React
- Render lại khi state/props đổi; hook rules; `useEffect` dependency array; StrictMode chạy effect 2 lần ở dev.
- Context/Provider bọc ngoài (`main.tsx`/`App.tsx`) cung cấp dữ liệu ngầm cho component con.
- State management: Redux (store, slice, dispatch), Zustand, React Query/SWR (cache, refetch tự động).
- Router: React Router (định nghĩa route ở đâu), lazy loading.
- JSX biên dịch thành gọi hàm; `key` trong list.

### Next.js
- File-based routing: `app/**/page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx`, `route.ts` (API); hoặc `pages/`.
- Server Component (mặc định) vs Client Component (`"use client"`); Server Actions (`"use server"`).
- `middleware.ts` ở gốc chạy trước mọi request; cache/revalidate; `generateStaticParams`.

### Vue / Nuxt
- Reactivity (`ref`, `reactive`, `computed`), SFC `<script setup>`, auto-import ở Nuxt, file-based routing `pages/`.

### Spring Boot (Java/Kotlin)
- Auto-configuration: thêm starter vào pom là có bean tự cấu hình.
- Component scan: `@Component/@Service/@Repository/@Controller/@RestController` được tự tạo bean; DI qua constructor (thường kèm Lombok `@RequiredArgsConstructor`).
- `@Configuration` + `@Bean`; profile (`application-{profile}.yml`, `spring.profiles.active`); `@Value`/`@ConfigurationProperties`.
- Spring Data JPA: interface `extends JpaRepository` không có implementation — query sinh từ tên method (`findByEmailAndStatus`); `@Query`.
- AOP/proxy: `@Transactional`, `@Cacheable`, `@Async` chỉ hoạt động khi gọi qua proxy (gọi nội bộ cùng class sẽ không có hiệu lực).
- Filter chain của Spring Security; `@PreAuthorize`; OAuth2 resource server (JWT từ Keycloak...).
- `@ControllerAdvice/@RestControllerAdvice` xử lý exception toàn cục.
- Lombok: `@Data/@Getter/@Builder` sinh code lúc biên dịch — không thấy getter/setter trong file.
- MapStruct/ModelMapper sinh mapper; Kafka `@KafkaListener`; `@Scheduled`; Liquibase/Flyway chạy migration lúc khởi động.
- Spring Boot 3 dùng `jakarta.*`; Boot 2 dùng `javax.*`.

### Django / Flask / FastAPI (Python)
- Django: `INSTALLED_APPS`, `urls.py` include, middleware trong `settings.MIDDLEWARE`, ORM manager/queryset lazy, signals, migrations tự sinh, admin tự sinh.
- Flask: `app.route`, blueprint, `g`, application/request context.
- FastAPI: dependency injection qua `Depends`, Pydantic validate tự động, `async def` vs `def`, OpenAPI tự sinh tại `/docs`.
- Python chung: decorator, context manager (`with`), generator, type hints không được kiểm tra lúc chạy, virtualenv.

### Go
- Package theo thư mục, chữ Hoa = exported, xử lý lỗi `if err != nil`, interface ngầm định, goroutine/channel, `context.Context` truyền xuống, `init()` chạy tự động.

### Khác
- ORM: lazy loading / N+1, migration tự động, hook (`beforeSave`), soft delete.
- Code sinh tự động: Prisma client, OpenAPI/GraphQL codegen, protobuf, `*.g.dart` — đừng sửa tay, chỉ ra lệnh sinh lại.
- Hạ tầng: biến môi trường do docker-compose/K8s inject; nginx reverse proxy đổi đường dẫn; CDC (Debezium) đẩy thay đổi DB vào Kafka.
