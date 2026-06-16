# Handoff 08: Hub Server Và Portal Sau Khi Local Engine Ổn

**Ưu tiên:** P3
**Loại việc:** future platform implementation
**Plan liên quan:** `TECHNICAL_SPEC_UNIFIED_HUB.md`, `master_plan_ces_academy_stabilization_20260527.md`

---

## 1. Mục tiêu

Xây Hub Server/Portal chỉ sau khi local modules, AI sidecar và manifest contract đủ ổn. Không build platform chỉ để che việc module chưa có output thật.

---

## 2. Trạng thái hiện tại đã xác nhận

- `TECHNICAL_SPEC_UNIFIED_HUB.md` hiện ghi Hub/Portal là planned.
- Repo chưa có `hub_server.py`.
- Chưa có source Next.js Portal trong repo hiện tại.
- AI sidecar và manifest đang là hướng làm sớm trước Hub.

---

## 3. Điều kiện trước khi bắt đầu

Không bắt đầu Hub nếu chưa có ít nhất:

- V12 baseline validated.
- V13 Facebook UAT hoặc failure summary rõ.
- V10 UAT sau config migration.
- AI sidecar template ổn.
- Manifest writer tối thiểu hoặc manifest schema đã chốt.

---

## 4. Hub Server scope tối thiểu

Nếu bắt đầu backend local, tạo `hub_server.py` hoặc `hub_server/` với các endpoint:

```text
GET /health
GET /modules
GET /artifacts
POST /run/<module>
GET /runs/<run_id>
```

Yêu cầu:

- Không chạy module nguy hiểm nếu thiếu confirmation.
- V12/V14 desktop automation phải có warning.
- Mọi run phải ghi stdout/stderr, exit code và summary path.
- Không expose server ra network public mặc định.

---

## 5. Portal scope tối thiểu

Nếu tạo Portal:

- Dashboard module status.
- Artifact list từ manifest.
- Link AI sidecar Markdown/JSON.
- Run button chỉ cho module an toàn hoặc có confirmation.
- Không render raw private content nếu chưa có privacy policy.

Không cần landing page marketing.

---

## 6. Validation tối thiểu

Backend:

```powershell
$py = "C:\Users\vu.hoang\.gemini\antigravity\scratch\tools\python\python.exe"
& $py -m py_compile .\hub_server.py
& $py .\hub_server.py
```

Sau đó test:

```powershell
Invoke-RestMethod http://localhost:<port>/health
Invoke-RestMethod http://localhost:<port>/modules
Invoke-RestMethod http://localhost:<port>/artifacts
```

Portal nếu có:

- Chạy dev server.
- Browser UAT dashboard load.
- Không có console errors nghiêm trọng.

---

## 7. Tiêu chí PASS

PASS khi:

- Hub không claim module nào pass nếu manifest/status chưa chứng minh.
- Run API trả run_id và lưu log.
- Artifact API đọc từ manifest/local output.
- Docs cập nhật `TECHNICAL_SPEC_UNIFIED_HUB.md` từ planned sang implemented chỉ cho phần có file thật.

FAIL khi:

- Tạo UI đẹp nhưng không nối được output thật.
- Hardcode path local của một máy vào server.
- Auto-run desktop automation không có warning.

---

## 8. File được phép tạo/sửa

- `hub_server.py` hoặc `hub_server/`
- Portal folder nếu user duyệt rõ
- `TECHNICAL_SPEC_UNIFIED_HUB.md`
- `README.md`
- `PROJECT_STATUS.md`
- `requirements.txt`
