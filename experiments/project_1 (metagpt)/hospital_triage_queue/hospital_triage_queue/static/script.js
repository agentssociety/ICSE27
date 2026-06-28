/**
 * static/script.js — Hospital Triage Queue System Frontend
 *
 * Real-time dashboard that polls the REST API every 500ms to update the queue,
 * handles patient registration, dequeue, re-triage, and displays statistics.
 * Uses modern ES6+ async/await and event delegation.
 */

'use strict';

// =============================================================================
// Configuration
// =============================================================================

const API_BASE = ''; // empty means same origin (relative paths)
const POLL_INTERVAL_MS = 500;

// =============================================================================
// DOM References
// =============================================================================

const dom = {
  // Registration
  form: document.getElementById('registration-form'),
  nameInput: document.getElementById('patient-name'),
  symptomsInput: document.getElementById('patient-symptoms'),
  manualUrgencyInput: document.getElementById('manual-urgency'),
  feedback: document.getElementById('registration-feedback'),

  // Queue
  queueBody: document.getElementById('queue-body'),
  emptyRow: document.getElementById('empty-row'),
  queueCount: document.getElementById('queue-count'),
  dequeueBtn: document.getElementById('dequeue-btn'),
  refreshBtn: document.getElementById('refresh-btn'),

  // Re-triage modal
  modal: document.getElementById('re-triage-modal'),
  modalPatientInfo: document.getElementById('re-triage-patient-info'),
  modalPatientId: document.getElementById('re-triage-patient-id'),
  modalNewUrgency: document.getElementById('new-urgency'),
  modalForm: document.getElementById('re-triage-form'),
  modalCloseBtn: document.querySelector('#re-triage-modal .close-btn'),

  // Stats
  avgWaitTime: document.getElementById('avg-wait-time'),
  urgencyCounts: {
    1: document.getElementById('urgency-1-count'),
    2: document.getElementById('urgency-2-count'),
    3: document.getElementById('urgency-3-count'),
    4: document.getElementById('urgency-4-count'),
    5: document.getElementById('urgency-5-count'),
  },
};

// =============================================================================
// Utility Functions
// =============================================================================

/**
 * Formats a number of seconds into a human-readable duration.
 * @param {number} seconds
 * @returns {string} e.g., "2m 15s" or "45s"
 */
function formatDuration(seconds) {
  if (seconds < 0) return '0s';
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  if (mins > 0) {
    return `${mins}m ${secs}s`;
  }
  return `${secs}s`;
}

/**
 * Creates an urgency badge element.
 * @param {number} urgency 1-5
 * @returns {HTMLSpanElement}
 */
function createUrgencyBadge(urgency) {
  const badge = document.createElement('span');
  badge.className = `urgency-badge urgency-${urgency}`;
  badge.textContent = urgency;
  return badge;
}

/**
 * Shows a feedback message on the registration form.
 * @param {string} message
 * @param {'success'|'error'} type
 */
function showFeedback(message, type) {
  dom.feedback.textContent = message;
  dom.feedback.className = `feedback ${type}`;
  dom.feedback.style.display = 'block';
  // Auto-hide after 5 seconds
  setTimeout(() => {
    dom.feedback.style.display = 'none';
  }, 5000);
}

/**
 * Clears the registration form inputs.
 */
function clearRegistrationForm() {
  dom.nameInput.value = '';
  dom.symptomsInput.value = '';
  dom.manualUrgencyInput.value = '';
}

// =============================================================================
// API Calls
// =============================================================================

/**
 * Fetches the current queue from the server.
 * @returns {Promise<Object>} { patients: [], total_patients: number, average_wait_time: number }
 */
async function fetchQueue() {
  const response = await fetch(`${API_BASE}/queue`);
  if (!response.ok) {
    throw new Error(`Failed to fetch queue: ${response.status} ${response.statusText}`);
  }
  return await response.json();
}

/**
 * Registers a new patient.
 * @param {string} name
 * @param {string} symptoms
 * @param {number|null} manualUrgency
 * @returns {Promise<Object>} patient object
 */
async function registerPatient(name, symptoms, manualUrgency) {
  const body = { name, symptoms };
  if (manualUrgency !== null) {
    body.manual_urgency = manualUrgency;
  }
  const response = await fetch(`${API_BASE}/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Registration failed: ${response.status}`);
  }
  return await response.json();
}

/**
 * Dequeues the highest priority patient.
 * @returns {Promise<Object>} { success, patient, message }
 */
async function dequeuePatient() {
  const response = await fetch(`${API_BASE}/dequeue`, { method: 'POST' });
  if (!response.ok) {
    throw new Error(`Dequeue failed: ${response.status} ${response.statusText}`);
  }
  return await response.json();
}

/**
 * Re-triages a patient with a new urgency.
 * @param {number} patientId
 * @param {number} newUrgency 1-5
 * @returns {Promise<Object>} updated patient object
 */
async function reTriagePatient(patientId, newUrgency) {
  const response = await fetch(`${API_BASE}/re_triage`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ patient_id: patientId, new_urgency: newUrgency }),
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Re-triage failed: ${response.status}`);
  }
  return await response.json();
}

// =============================================================================
// UI Rendering
// =============================================================================

/**
 * Renders the queue table rows.
 * @param {Array} patients - list of patient objects
 */
function renderQueue(patients) {
  // Clear existing rows except empty row
  const rows = dom.queueBody.querySelectorAll('tr:not(#empty-row)');
  rows.forEach(row => row.remove());

  if (patients.length === 0) {
    dom.emptyRow.style.display = '';
    dom.queueCount.textContent = '0 patients';
    dom.dequeueBtn.disabled = true;
    return;
  }

  dom.emptyRow.style.display = 'none';
  dom.queueCount.textContent = `${patients.length} patient${patients.length !== 1 ? 's' : ''}`;
  dom.dequeueBtn.disabled = false;

  patients.forEach(patient => {
    const tr = document.createElement('tr');

    // ID
    const tdId = document.createElement('td');
    tdId.textContent = patient.id;
    tr.appendChild(tdId);

    // Name
    const tdName = document.createElement('td');
    tdName.textContent = patient.name;
    tr.appendChild(tdName);

    // Symptoms
    const tdSymptoms = document.createElement('td');
    tdSymptoms.textContent = patient.symptoms;
    tr.appendChild(tdSymptoms);

    // Urgency badge
    const tdUrgency = document.createElement('td');
    tdUrgency.appendChild(createUrgencyBadge(patient.urgency));
    tr.appendChild(tdUrgency);

    // Waiting time
    const tdWait = document.createElement('td');
    const waitSpan = document.createElement('span');
    waitSpan.className = 'waiting-time';
    const seconds = patient.waiting_seconds || 0;
    waitSpan.textContent = formatDuration(seconds);
    // Color the waiting time based on duration
    if (seconds > 600) { // more than 10 minutes
      waitSpan.classList.add('long');
    } else if (seconds > 300) { // more than 5 minutes
      waitSpan.classList.add('medium');
    } else {
      waitSpan.classList.add('short');
    }
    tdWait.appendChild(waitSpan);
    tr.appendChild(tdWait);

    // Actions (re-triage + dequeue per row)
    const tdActions = document.createElement('td');
    tdActions.classList.add('actions');

    const reTriageBtn = document.createElement('button');
    reTriageBtn.className = 'action-btn';
    reTriageBtn.textContent = 'Re-triage';
    reTriageBtn.dataset.id = patient.id;
    reTriageBtn.dataset.name = patient.name;
    reTriageBtn.dataset.urgency = patient.urgency;
    reTriageBtn.addEventListener('click', () => openReTriageModal(patient.id, patient.name, patient.urgency));
    tdActions.appendChild(reTriageBtn);

    const dequeueRowBtn = document.createElement('button');
    dequeueRowBtn.className = 'action-btn dequeue-btn';
    dequeueRowBtn.textContent = 'Take';
    dequeueRowBtn.dataset.id = patient.id;
    dequeueRowBtn.addEventListener('click', () => handleDequeueRow(patient.id));
    tdActions.appendChild(dequeueRowBtn);

    tr.appendChild(tdActions);

    dom.queueBody.appendChild(tr);
  });
}

/**
 * Updates the statistics section (average wait time + urgency counts).
 * @param {Array} patients
 */
function renderStats(patients) {
  if (!patients || patients.length === 0) {
    dom.avgWaitTime.textContent = '0s';
    for (let i = 1; i <= 5; i++) {
      dom.urgencyCounts[i].textContent = '0';
    }
    return;
  }

  const totalSeconds = patients.reduce((sum, p) => sum + (p.waiting_seconds || 0), 0);
  const avgSeconds = totalSeconds / patients.length;
  dom.avgWaitTime.textContent = formatDuration(Math.round(avgSeconds));

  const counts = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 };
  patients.forEach(p => {
    if (counts.hasOwnProperty(p.urgency)) {
      counts[p.urgency]++;
    }
  });
  for (let i = 1; i <= 5; i++) {
    dom.urgencyCounts[i].textContent = counts[i];
  }
}

/**
 * Main update function called on poll and manual refresh.
 */
async function updateDashboard() {
  try {
    const data = await fetchQueue();
    const patients = data.patients || [];
    renderQueue(patients);
    renderStats(patients);
  } catch (error) {
    console.error('Polling error:', error);
    // Optionally show a brief error indicator
  }
}

// =============================================================================
// Polling
// =============================================================================

let pollInterval = null;

function startPolling() {
  if (pollInterval) clearInterval(pollInterval);
  updateDashboard();
  pollInterval = setInterval(updateDashboard, POLL_INTERVAL_MS);
}

function stopPolling() {
  if (pollInterval) {
    clearInterval(pollInterval);
    pollInterval = null;
  }
}

// =============================================================================
// Event Handlers
// =============================================================================

/**
 * Handles the registration form submission.
 * @param {Event} event
 */
async function handleRegistration(event) {
  event.preventDefault();

  const name = dom.nameInput.value.trim();
  const symptoms = dom.symptomsInput.value.trim();
  const manualUrgencyRaw = dom.manualUrgencyInput.value.trim();
  let manualUrgency = null;
  if (manualUrgencyRaw !== '') {
    manualUrgency = parseInt(manualUrgencyRaw, 10);
    if (isNaN(manualUrgency) || manualUrgency < 1 || manualUrgency > 5) {
      showFeedback('Manual urgency must be a number between 1 and 5, or leave empty.', 'error');
      return;
    }
  }

  if (!name || !symptoms) {
    showFeedback('Name and symptoms are required.', 'error');
    return;
  }

  try {
    const patient = await registerPatient(name, symptoms, manualUrgency);
    showFeedback(`Patient "${patient.name}" registered successfully (Urgency ${patient.urgency}).`, 'success');
    clearRegistrationForm();
    // Immediately refresh the dashboard (next poll will also catch)
    await updateDashboard();
  } catch (error) {
    showFeedback(error.message, 'error');
  }
}

/**
 * Handles the global dequeue button click.
 */
async function handleDequeue() {
  dom.dequeueBtn.disabled = true;
  try {
    const result = await dequeuePatient();
    if (!result.success) {
      console.warn('Dequeue returned no patient:', result.message);
      return;
    }
    // Immediately refresh
    await updateDashboard();
  } catch (error) {
    console.error('Dequeue error:', error);
    showFeedback(`Dequeue failed: ${error.message}`, 'error');
  } finally {
    dom.dequeueBtn.disabled = false;
  }
}

/**
 * Handles dequeue from a specific row's "Take" button.
 * @param {number} patientId - not strictly needed but kept for potential logging
 */
async function handleDequeueRow(patientId) {
  // The main dequeue always takes the top patient, so we just call it.
  // However, if we want to enforce taking the specific row, we could check.
  // For simplicity, we use the same global dequeue since the queue is sorted.
  await handleDequeue();
}

/**
 * Opens the re-triage modal and fills with patient info.
 * @param {number} patientId
 * @param {string} patientName
 * @param {number} currentUrgency
 */
function openReTriageModal(patientId, patientName, currentUrgency) {
  dom.modalPatientId.value = patientId;
  dom.modalPatientInfo.textContent = `Patient: ${patientName} (Current urgency: ${currentUrgency})`;
  dom.modalNewUrgency.value = '';
  dom.modal.classList.remove('hidden');
  dom.modalNewUrgency.focus();
}

/**
 * Hides the re-triage modal.
 */
function hideReTriageModal() {
  dom.modal.classList.add('hidden');
}

/**
 * Handles the re-triage form submission.
 * @param {Event} event
 */
async function handleReTriage(event) {
  event.preventDefault();

  const patientId = parseInt(dom.modalPatientId.value, 10);
  const newUrgency = parseInt(dom.modalNewUrgency.value, 10);

  if (isNaN(newUrgency) || newUrgency < 1 || newUrgency > 5) {
    alert('Please enter a valid urgency between 1 and 5.');
    return;
  }

  try {
    const updatedPatient = await reTriagePatient(patientId, newUrgency);
    hideReTriageModal();
    showFeedback(`Patient "${updatedPatient.name}" re-triaged to urgency ${updatedPatient.urgency}.`, 'success');
    await updateDashboard();
  } catch (error) {
    alert(`Re-triage failed: ${error.message}`);
  }
}

/**
 * Handles the manual refresh button click.
 */
async function handleRefresh() {
  dom.refreshBtn.disabled = true;
  try {
    await updateDashboard();
  } finally {
    dom.refreshBtn.disabled = false;
  }
}

// =============================================================================
// Initialization
// =============================================================================

document.addEventListener('DOMContentLoaded', () => {
  // Attach event listeners
  dom.form.addEventListener('submit', handleRegistration);
  dom.dequeueBtn.addEventListener('click', handleDequeue);
  dom.refreshBtn.addEventListener('click', handleRefresh);
  dom.modalForm.addEventListener('submit', handleReTriage);
  dom.modalCloseBtn.addEventListener('click', hideReTriageModal);

  // Close modal by clicking outside
  dom.modal.addEventListener('click', (event) => {
    if (event.target === dom.modal) {
      hideReTriageModal();
    }
  });

  // Start polling
  startPolling();

  // Initial fetch
  updateDashboard();
});

// Expose necessary functions for inline onclick in HTML (if used)
window.hideReTriageModal = hideReTriageModal;
