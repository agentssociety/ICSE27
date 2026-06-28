# Frontend Bug Fixes

Source: `experiments/project_1/run.log` analysis + current file audit.

---

## Fix 1 — `axios` in `devDependencies` instead of `dependencies`

**File:** `frontend/package.json`

**Symptom:** `npm warn idealTree Removing dependencies.axios in favor of devDependencies.axios` — npm removes
axios from the runtime dependency tree during install, causing axios to be absent in production builds.

**Root cause:** `axios` was listed under `devDependencies`. It is used in `src/api/services.ts` which runs in
the browser, so it must be a runtime dependency.

**Fix:** Moved `axios` from `devDependencies` to `dependencies`.

---

## Fix 2 — Wrong API endpoint paths in `src/api/services.ts`

**File:** `frontend/src/api/services.ts`

**Symptom:** All API calls returned 404 because the paths did not match the backend router prefixes registered
in `main.py`.

**Root cause:** The frontend used singular resource names and wrong path segments. The backend registers:
- `/patients` (plural) — patient CRUD
- `/patient_queues` (plural) — queue CRUD
- `/dashboard/queue/{id}/...` — dashboard views

**Specific wrong → correct path corrections:**

| Function | Was | Now |
|---|---|---|
| `getQueueOverview` | `GET /queue/{id}/overview` | `GET /dashboard/queue/{id}/overview` |
| `getQueuePatients` | `GET /queue/{id}/patients` | `GET /dashboard/queue/{id}/patients` |
| `registerPatient` | `POST /patient` | `POST /patients` |
| `getPatient` | `GET /patient/{id}` | `GET /patients/{id}` |
| `updatePatient` | `PUT /patient/{id}` | `PUT /patients/{id}` |
| `deletePatient` | `DELETE /patient/{id}` | `DELETE /patients/{id}` |
| `dequeuePatient` | `DELETE /patient_queue/{id}` | two-step: fetch + `DELETE /patients/{id}` |
| `getPatientQueue` | `GET /patient_queue/{id}` | `GET /patient_queues/{id}` |
| `updatePatientQueue` | `PUT /patient_queue/{id}` | `PUT /patient_queues/{id}` |
| `deletePatientQueue` | `DELETE /patient_queue/{id}` | `DELETE /patient_queues/{id}` |

**`dequeuePatient` logic fix:** The original called `DELETE /patient_queue/{queueId}` which deletes the queue
entity row. There is no dedicated dequeue endpoint. Fixed to:
1. `GET /dashboard/queue/{id}/patients` to fetch patients
2. Sort ascending by `urgency_level` (1 = Critical = highest priority)
3. `DELETE /patients/{top.id}` to remove the highest-priority patient
4. Return `{ patient: top, removed: true }` or `{ patient: null, removed: false }` if queue is empty.

**`getQueuePatients` return type fix:** The backend wraps patients in `{ queue_id, patients: [...] }`. The
function now extracts `data.patients ?? []` and returns `Patient[]`.

---

## Fix 3 — Type mismatch: `Patient`, `PatientQueue`, `RegisterPatientRequest`

**File:** `frontend/src/types/index.ts`

**Symptom:** TypeScript types described a richer API (name, symptoms, status, patient_name, estimated_wait_minutes)
that the backend never implements. Calls to `registerPatient` sent `name`/`symptoms` which the backend DTOs
do not accept; `Patient` objects used `.name` and `.status` fields that don't exist in `PatientResponse`.

**Root cause:** Types were written assuming a different backend schema. Actual backend DTOs:
- `PatientResponse`: `id, patientId (UUID), patientQueue_id?, state, arrival_time?, urgency_level`
- `PatientQueueResponse`: `id, queueId (UUID)`
- `PatientCreate`: `patientId (UUID), urgency_level, state?, arrival_time?, patientQueue_id?`

**Fix:** Rewrote all interfaces to match the actual backend:

```typescript
// Before (wrong)
interface Patient { id, name, symptoms, urgency_level, arrival_time, estimated_wait_minutes? }
interface PatientQueue { id, patient_id, patient_name, urgency_level, arrival_time, estimated_wait_minutes, status }
interface RegisterPatientRequest { name, symptoms, urgency_level }

// After (correct)
interface Patient { id, patientId (UUID string), patientQueue_id?, state, arrival_time?, urgency_level }
interface PatientQueue { id, queueId (UUID string) }
interface QueueOverview { queue_id, message, status }  // actual backend response shape
interface QueuePatientsResponse { queue_id, patients: Patient[] }
interface RegisterPatientRequest { patientId (UUID string), urgency_level, state?, patientQueue_id? }
interface DequeueResponse { patient: Patient | null, removed: boolean }
```

---

## Fix 4 — `RegisterPatientPage` sent backend-incompatible fields

**File:** `frontend/src/pages/RegisterPatientPage.tsx`

**Symptom:** Submitting the register form called `registerPatient({ name, symptoms, urgency_level })`. The
backend's `PatientCreate` requires `patientId: UUID` and has no `name` or `symptoms` fields. The call would
fail with a Pydantic validation error (missing required `patientId`).

**Fix:**
- Changed API call to send `{ patientId: crypto.randomUUID(), urgency_level, state: 'pending_triage' }`.
- Validation now only requires `name` to be non-empty (for UX); `symptoms` textarea removed from required check.
- The name/symptoms form fields are kept for UX (the backend is not designed to store them, but they don't
  cause errors since Pydantic ignores extra fields).

---

## Fix 5 — DashboardPage used mismatched types and unavailable API fields

**File:** `frontend/src/pages/DashboardPage.tsx`

**Symptom:** `DashboardPage` rendered `p.patient_name`, `p.status`, `p.estimated_wait_minutes` — fields that
do not exist in `PatientResponse`. The `QueueOverview` from the dashboard endpoint does not return the count
fields (`total_waiting`, `critical_count`, etc.) the page expected.

**Fix:**
- Changed patient state type from `PatientQueue[]` to `Patient[]`.
- Removed `getQueueOverview()` call (backend endpoint returns only `{ queue_id, message, status }` — no useful stats).
- Added local `computeStats(patients)` that derives total/critical/high/medium/low counts from the patients list.
- Updated table columns: `patient_name → patientId`, `status → state`, removed `estimated_wait_minutes` column.
- `arrival_time` display now guards against `undefined` with a `'—'` fallback.

---

## Fix 6 — QueuePage used mismatched types and API fields

**File:** `frontend/src/pages/QueuePage.tsx`

**Symptom:** Same type mismatch as DashboardPage — `p.patient_name`, `p.status`, `p.estimated_wait_minutes`
don't exist; dequeue result message referenced `result.patient.name` which doesn't exist on `Patient`.

**Fix:**
- Changed patient state type from `PatientQueue[]` to `Patient[]`.
- Updated table columns: `patient_name → patientId`, `status → state`, removed `estimated_wait_minutes`.
- Dequeue result message changed from `result.patient.name` to `result.patient.patientId`.

---

## Fix 7 — `ECONNREFUSED` in tests: DashboardPage and QueuePage make real HTTP calls

**Files:** `frontend/src/__tests__/DashboardPage.test.tsx`, `frontend/src/__tests__/QueuePage.test.tsx`

**Symptom:** Both pages call `getQueuePatients()` (and previously `getQueueOverview()`) in `useEffect` on
mount. In jsdom/vitest, axios makes real HTTP requests. With no backend running on port 3000, every test
logged `ECONNREFUSED 127.0.0.1:3000` to stderr, polluting output and making tests flaky.

**Fix:** Added `vi.mock('../api/services', ...)` at the top of both test files, stubbing all called service
functions with resolved empty values:

```typescript
// DashboardPage.test.tsx
vi.mock('../api/services', () => ({
  getQueuePatients: vi.fn().mockResolvedValue([]),
}))

// QueuePage.test.tsx
vi.mock('../api/services', () => ({
  getQueuePatients: vi.fn().mockResolvedValue([]),
  dequeuePatient: vi.fn().mockResolvedValue({ patient: null, removed: false }),
}))
```

---

## Fix 8 — React Router v7 future flag warnings in all tests

**Files:** `frontend/src/App.tsx`, all three test files

**Symptom:** Every test printed:
```
React Router Future Flag Warning: React Router will begin wrapping state updates in `React.startTransition` in v7...
React Router Future Flag Warning: Relative route resolution within Splat routes is changing in v7...
```

**Fix:** Added `future` prop to `BrowserRouter` in `App.tsx` and in all three test files:
```tsx
<BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
```

---

## Fix 9 — `RegisterPatientPage` test matched multiple elements with `getByText`

**File:** `frontend/src/__tests__/RegisterPatientPage.test.tsx`

**Symptom (from run.log line ~11905):**
```
TestingLibraryElementError: Found multiple elements with the text: Register Patient
```
Both the `<h1>Register Patient</h1>` and the submit `<button>Register Patient</button>` matched.

**Fix:** Already corrected by the agent during the run — changed assertion from:
```typescript
screen.getByText('Register Patient')
```
to:
```typescript
screen.getByRole('heading', { name: 'Register Patient' })
```
The test file on disk already contains this fix; it was preserved as-is.

---

## Summary of Files Changed

| File | Change |
|---|---|
| `frontend/package.json` | `axios` moved from `devDependencies` → `dependencies` |
| `frontend/src/types/index.ts` | All interfaces rewritten to match actual backend DTOs |
| `frontend/src/api/services.ts` | All endpoint paths corrected; `dequeuePatient` reimplemented; `getQueuePatients` return type fixed |
| `frontend/src/App.tsx` | Added React Router v7 future flags to `BrowserRouter` |
| `frontend/src/pages/DashboardPage.tsx` | Removed `QueueOverview` API call; compute stats client-side; use `Patient[]` type; correct field names |
| `frontend/src/pages/QueuePage.tsx` | Use `Patient[]` type; correct field names; fix dequeue result message |
| `frontend/src/pages/RegisterPatientPage.tsx` | Send `patientId` (UUID) not `name`/`symptoms` to backend |
| `frontend/src/__tests__/DashboardPage.test.tsx` | Added `vi.mock` for services; added v7 future flags |
| `frontend/src/__tests__/QueuePage.test.tsx` | Added `vi.mock` for services; added v7 future flags |
| `frontend/src/__tests__/RegisterPatientPage.test.tsx` | Added v7 future flags (heading fix already in place) |
| `frontend/src/__tests__/App.test.tsx` | Added `vi.mock` for services; wrapped render in `act(async () => ...)` |
