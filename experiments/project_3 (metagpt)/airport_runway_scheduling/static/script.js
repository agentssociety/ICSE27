/**
 * Flight Scheduling System – Dashboard Scripts
 * Provides dynamic interactions for the timetable view:
 * - Manual refresh button
 * - Auto-refresh every 60 seconds (clears after 5 minutes to save resources)
 *
 * Uses vanilla JavaScript (ES6+). Follows Google JavaScript Style Guide.
 */

'use strict';

/**
 * Namespace to avoid polluting global scope.
 */
const FlightDashboard = (() => {
  // Configuration
  const CONFIG = {
    AUTO_REFRESH_INTERVAL_MS: 60_000,      // 60 seconds
    MAX_AUTO_REFRESH_COUNT: 5,              // stop after 5 refreshes
    REFRESH_BUTTON_TEXT: '↻ Refresh',
    REFRESH_ACTIVE_CLASS: 'refresh-active',
  };

  // State
  let autoRefreshCount = 0;
  let autoRefreshTimerId = null;

  /**
   * Initialize the dashboard: create refresh button and start auto-refresh.
   */
  const init = () => {
    const container = document.querySelector('.container');
    if (!container) {
      console.warn('[FlightDashboard] No container found. Aborting.');
      return;
    }

    addRefreshButton(container);
    startAutoRefresh();
  };

  /**
   * Creates and appends a "Refresh" button to the container.
   * @param {HTMLElement} container - The main container element.
   */
  const addRefreshButton = (container) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'refresh-btn';
    button.textContent = CONFIG.REFRESH_BUTTON_TEXT;
    button.setAttribute('aria-label', 'Reload timetable');
    button.addEventListener('click', (e) => {
      e.preventDefault();
      refreshTimetable(container);
    });

    // Insert after the heading
    const heading = container.querySelector('h1');
    if (heading && heading.nextElementSibling) {
      heading.parentNode.insertBefore(button, heading.nextElementSibling);
    } else if (heading) {
      heading.parentNode.appendChild(button);
    } else {
      container.prepend(button);
    }
  };

  /**
   * Refreshes the timetable by re-fetching the current page content.
   * Replaces the container's inner HTML with the fresh response.
   * @param {HTMLElement} container - The main container to update.
   * @param {boolean} [isAuto=false] - Whether this refresh is automatic.
   */
  const refreshTimetable = async (container, isAuto = false) => {
    if (!container) return;

    // Determine the current runway_id from the URL query string
    const currentParams = new URLSearchParams(window.location.search);
    const runwayId = currentParams.get('runway_id') || '1';

    // Build the same URL (without parameters that might cause issues)
    const baseUrl = window.location.pathname;
    const fetchUrl = `${baseUrl}?runway_id=${encodeURIComponent(runwayId)}`;

    // Show visual feedback
    const refreshBtn = container.querySelector('.refresh-btn');
    if (refreshBtn) {
      refreshBtn.classList.add(CONFIG.REFRESH_ACTIVE_CLASS);
      refreshBtn.disabled = true;
    }

    try {
      const response = await fetch(fetchUrl, {
        method: 'GET',
        headers: { 'Accept': 'text/html' },
      });

      if (!response.ok) {
        throw new Error(`Server responded with ${response.status}`);
      }

      const html = await response.text();

      // Parse the HTML to extract the container part (to avoid replacing entire page)
      const tempDiv = document.createElement('div');
      tempDiv.innerHTML = html;
      const newContainer = tempDiv.querySelector('.container');

      if (newContainer) {
        container.innerHTML = newContainer.innerHTML;
        // Re-add refresh button and re-attach event listeners
        addRefreshButton(container);
        // Update the title if needed
        const newTitle = newContainer.querySelector('h1');
        if (newTitle) {
          document.title = newTitle.textContent;
        }
      } else {
        // Fallback: replace full content
        container.innerHTML = tempDiv.innerHTML;
        addRefreshButton(container);
      }

      if (!isAuto) {
        console.log('[FlightDashboard] Timetable refreshed successfully.');
      }
    } catch (error) {
      console.error('[FlightDashboard] Refresh failed:', error);
      // Display a temporary error message
      const errorMsg = document.createElement('p');
      errorMsg.className = 'error-message';
      errorMsg.textContent = '⚠ Failed to refresh timetable. Please try again later.';
      container.prepend(errorMsg);
      setTimeout(() => errorMsg.remove(), 5000);
    } finally {
      if (refreshBtn) {
        refreshBtn.classList.remove(CONFIG.REFRESH_ACTIVE_CLASS);
        refreshBtn.disabled = false;
      }
    }
  };

  /**
   * Starts automatic periodic refresh of the timetable.
   * Stops after MAX_AUTO_REFRESH_COUNT to avoid unnecessary load.
   */
  const startAutoRefresh = () => {
    if (autoRefreshTimerId) {
      clearInterval(autoRefreshTimerId);
    }

    autoRefreshTimerId = setInterval(() => {
      if (autoRefreshCount >= CONFIG.MAX_AUTO_REFRESH_COUNT) {
        clearInterval(autoRefreshTimerId);
        autoRefreshTimerId = null;
        console.log('[FlightDashboard] Auto-refresh stopped after max count.');
        return;
      }

      const container = document.querySelector('.container');
      if (container) {
        refreshTimetable(container, true);
        autoRefreshCount++;
      } else {
        // Container disappeared; stop auto-refresh
        clearInterval(autoRefreshTimerId);
        autoRefreshTimerId = null;
      }
    }, CONFIG.AUTO_REFRESH_INTERVAL_MS);

    console.log('[FlightDashboard] Auto-refresh started.');
  };

  // Public API
  return {
    init,
    refreshTimetable,
  };
})();

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', FlightDashboard.init);
} else {
  FlightDashboard.init();
}
