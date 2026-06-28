import axios from 'axios';

// ── Type definitions matching backend Pydantic DTOs ──────────────────────

// Patient DTOs
interface PatientCreate {
  username: string;
  authentication_id: number;
}

interface PatientUpdate {
  username?: string;
  authentication_id?: number;
}

interface PatientResponse {
  id: number;
  username: string;
  authentication_id?: number;
}

// Symptom DTOs
interface SymptomCreate {
  description: string;
  language: string;
  patientId: string;
  patient_id: number;
}

interface SymptomUpdate {
  description?: string;
  language?: string;
  patientId?: string;
  patient_id?: number;
}

interface SymptomResponse {
  id: number;
  description: string;
  language: string;
  patientId: string;
  patient_id?: number;
}

// SymptomRecord DTOs
interface SymptomRecordCreate {
  recordId: string;
  symptomData: string;
  patientId: string;
  symptom_id: number;
}

interface SymptomRecordUpdate {
  recordId?: string;
  symptomData?: string;
  patientId?: string;
  symptom_id?: number;
}

interface SymptomRecordResponse {
  id: number;
  recordId: string;
  symptomData: string;
  patientId: string;
  symptom_id?: number;
}

// Resource DTOs
interface ResourceCreate {
  owner_id: number;
}

interface ResourceUpdate {
  owner_id?: number;
}

interface ResourceResponse {
  id: number;
  owner_id?: number;
}

// UserAuthenticationSystem DTOs
interface UserAuthenticationSystemCreate {
  sessionToken: string;
  userId: string;
  patient_id: number;
}

interface UserAuthenticationSystemUpdate {
  sessionToken?: string;
  userId?: string;
  patient_id?: number;
}

interface UserAuthenticationSystemResponse {
  userId: string;
  sessionToken: string;
  patient_id?: number;
}

// Actor and Interface DTOs (not used in this file but defined for completeness)
interface ActorCreate {}
interface ActorUpdate {}
interface ActorResponse {
  id: number;
}

interface InterfaceCreate {}
interface InterfaceUpdate {}
interface InterfaceResponse {
  id: number;
}

// Queue DTOs (backend has empty request/response)
interface QueueCreateRequest {}
interface QueueUpdateRequest {}
interface QueueResponse {}

// Convenience type aliases (response types used in services)
type Patient = PatientResponse;
type Symptom = SymptomResponse;
type SymptomRecord = SymptomRecordResponse;
type Resource = ResourceResponse;
type UserAuthenticationSystem = UserAuthenticationSystemResponse;

// Additional types for queue simulation
type UrgencyLevel = 1 | 2 | 3 | 4 | 5;

interface QueueItem {
  patient: Patient;
  symptom?: Symptom;
  symptomRecord?: SymptomRecord;
  urgency: UrgencyLevel;
  position: number;
  estimatedWaitTimeMinutes: number;
  registeredAt: string;
}

// ── API instance ──────────────────────────────────────────────────────────
const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
});

// ── Patients ──────────────────────────────────────────────────────────────
export const getPatients = (): Promise<Patient[]> =>
  api.get('/patients').then(r => r.data);

export const getPatient = (id: number): Promise<Patient> =>
  api.get(`/patients/${id}`).then(r => r.data);

export const createPatient = (data: PatientCreate): Promise<Patient> =>
  api.post('/patients', data).then(r => r.data);

export const updatePatient = (id: number, data: PatientUpdate): Promise<Patient> =>
  api.put(`/patients/${id}`, data).then(r => r.data);

export const deletePatient = (id: number): Promise<void> =>
  api.delete(`/patients/${id}`);

// ── Symptoms ─────────────────────────────────────────────────────────────
export const getSymptoms = (): Promise<Symptom[]> =>
  api.get('/symptoms').then(r => r.data);

export const getSymptom = (id: number): Promise<Symptom> =>
  api.get(`/symptoms/${id}`).then(r => r.data);

export const createSymptom = (data: SymptomCreate): Promise<Symptom> =>
  api.post('/symptoms', data).then(r => r.data);

export const updateSymptom = (id: number, data: SymptomUpdate): Promise<Symptom> =>
  api.put(`/symptoms/${id}`, data).then(r => r.data);

export const deleteSymptom = (id: number): Promise<void> =>
  api.delete(`/symptoms/${id}`);

// ── Symptom Records ──────────────────────────────────────────────────────
export const getSymptomRecords = (): Promise<SymptomRecord[]> =>
  api.get('/symptom_records').then(r => r.data);

export const createSymptomRecord = (data: SymptomRecordCreate): Promise<SymptomRecord> =>
  api.post('/symptom_records', data).then(r => r.data);

export const deleteSymptomRecord = (id: number): Promise<void> =>
  api.delete(`/symptom_records/${id}`);

// ── User Authentication Systems ──────────────────────────────────────────
export const getUserAuthSystems = (): Promise<UserAuthenticationSystem[]> =>
  api.get('/user_authentication_systems').then(r => r.data);

export const createUserAuthSystem = (data: UserAuthenticationSystemCreate): Promise<UserAuthenticationSystem> =>
  api.post('/user_authentication_systems', data).then(r => r.data);

// ── Resources ────────────────────────────────────────────────────────────
export const getResources = (): Promise<Resource[]> =>
  api.get('/resources').then(r => r.data);

export const createResource = (data: ResourceCreate): Promise<Resource> =>
  api.post('/resources', data).then(r => r.data);

// ── Queue Operations (client-side simulation) ────────────────────────────
// Since the backend has no dedicated queue endpoints, we build queue logic
// by fetching patients + symptoms and sorting by urgency + arrival time.
// Urgency is determined by symptom severity (1-5) stored in description.

function extractUrgency(description: string): UrgencyLevel {
  const match = description.match(/urgency:\s*(\d)/i);
  if (match) {
    const level = parseInt(match[1], 10);
    if (level >= 1 && level <= 5) return level as UrgencyLevel;
  }
  return 1; // default lowest urgency
}

export const getQueue = async (): Promise<QueueItem[]> => {
  const [patients, symptoms] = await Promise.all([
    getPatients(),
    getSymptoms()
  ]);

  // Build map of patientId -> symptoms
  const symptomMap = new Map<number, Symptom[]>();
  symptoms.forEach(s => {
    const pid = s.patient_id ?? 0;
    if (!symptomMap.has(pid)) symptomMap.set(pid, []);
    symptomMap.get(pid)!.push(s);
  });

  const items: QueueItem[] = patients.map((patient, index) => {
    const patientSymptoms = symptomMap.get(patient.id) || [];
    // Use first symptom for urgency
    const primarySymptom = patientSymptoms[0];
    const urgency = primarySymptom ? extractUrgency(primarySymptom.description) : 1;

    return {
      patient,
      symptom: primarySymptom,
      symptomRecord: undefined,
      urgency,
      position: index + 1,
      estimatedWaitTimeMinutes: index * 15, // approximate
      registeredAt: new Date().toISOString(), // approximate - backend doesn't return this
    };
  });

  // Sort: by urgency descending (5 highest first), then by registration time ascending
  items.sort((a, b) => {
    if (b.urgency !== a.urgency) return b.urgency - a.urgency;
    // Within same urgency, order by registration time (earliest first)
    return new Date(a.registeredAt).getTime() - new Date(b.registeredAt).getTime();
  });

  // Reassign positions after sorting
  items.forEach((item, idx) => {
    item.position = idx + 1;
    item.estimatedWaitTimeMinutes = idx * 15;
  });

  return items;
};

export const dequeueNext = async (): Promise<QueueItem | null> => {
  const queue = await getQueue();
  if (queue.length === 0) return null;
  const next = queue[0];
  await deletePatient(next.patient.id);
  if (next.symptom) {
    await deleteSymptom(next.symptom.id);
  }
  return next;
};

/**
 * Assign urgency level to a patient by updating their symptom description.
 * If no symptom exists, creates one.
 */
export const assignUrgency = async (patientId: number, level: UrgencyLevel): Promise<void> => {
  const symptoms = await getSymptoms();
  const patientSymptoms = symptoms.filter(s => s.patient_id === patientId);
  
  const urgencyStr = `urgency:${level}`;

  if (patientSymptoms.length > 0) {
    // Update first symptom description to include urgency
    await updateSymptom(patientSymptoms[0].id, { description: urgencyStr });
  } else {
    // Create a new symptom with urgency
    await createSymptom({
      description: urgencyStr,
      language: 'en',
      patientId: String(patientId),
      patient_id: patientId,
    });
  }
};