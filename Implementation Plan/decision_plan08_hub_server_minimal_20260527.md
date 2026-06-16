# Decision Note: Plan 08 — Hub Server / Portal

**Ngày:** 2026-05-27  
**Handoff gốc:** `Agent Handoff/remaining_08_hub_server_portal_future_20260527.md`  
**Verdict:** **IMPLEMENTED_MINIMAL**

---

## Đánh giá điều kiện trước khi build

| Điều kiện | Trạng thái |
|---|---|
| V12 baseline validated | PASS |
| V13 Facebook UAT hoặc failure summary rõ | PASS (Partial UAT, blocked by CDP — có summary) |
| V10 UAT sau config migration | PASS (Partial UAT, blocked by login — có summary) |
| AI sidecar template ổn | PASS (`analyze_artifact.py` hoạt động) |
| Manifest writer tối thiểu | PASS (`record_artifact.py` vừa tạo) |

Đủ điều kiện để build Hub minimal.

---

## Thay đổi đã thực hiện

| File | Thay đổi |
|---|---|
| `hub_server.py` | Tạo mới — minimal HTTP server, stdlib only, no extra deps |

---

## Endpoints đã implement

| Endpoint | Method | Trạng thái | Nguồn dữ liệu |
|---|---|---|---|
| `/health` | GET | PASS | Hardcoded liveness |
| `/modules` | GET | PASS | Parse `PROJECT_STATUS.md` table |
| `/artifacts` | GET | PASS | Read `outputs_manifest.jsonl` |
| `/run/<module>` | POST | 501/403 | Intentionally not implemented |

---

## Lệnh verify đã chạy

```powershell
# Compile
python -m py_compile hub_server.py → exit 0

# Live test (server start + 3 endpoints + stop)
Invoke-RestMethod http://127.0.0.1:8765/health
→ {"status":"ok","timestamp":"2026-05-27T14:09:03","server":"CES Academy Hub",...}

Invoke-RestMethod http://127.0.0.1:8765/modules
→ modules count: 8 (đọc từ PROJECT_STATUS.md thật)

Invoke-RestMethod http://127.0.0.1:8765/artifacts
→ artifacts count: 1 (đọc từ outputs_manifest.jsonl thật)
```

---

## Thiết kế an toàn

- Bind `127.0.0.1` only — không expose ra network.
- `POST /run/<module>` trả 501 cho tất cả modules.
- Desktop automation modules (V11/V12/V14) trả 403 với warning rõ.
- `/modules` đọc từ `PROJECT_STATUS.md` thật — không hardcode claim completed.
- `/artifacts` đọc từ manifest thật — không hardcode.

---

## Chưa implement (scope tương lai)

- `POST /run/<module>` với run logging và confirmation guard.
- `GET /runs/<run_id>` — run history.
- Portal Next.js — chưa cần, chưa có user approval.
- `TECHNICAL_SPEC_UNIFIED_HUB.md` update: giữ nguyên "planned" cho Portal; Hub backend = implemented_minimal.

---

## Chưa xác minh được

- Server chạy liên tục nhiều giờ (chỉ test ngắn).
- `/modules` với PROJECT_STATUS.md format thay đổi — parser dùng regex đơn giản.
- `/artifacts` với manifest lớn nhiều records.
