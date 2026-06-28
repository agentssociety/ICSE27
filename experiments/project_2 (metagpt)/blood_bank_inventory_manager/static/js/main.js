/**
 * main.js - Blood Bank Management System Frontend Script
 *
 * Provides interactive functionalities such as confirmation dialogs,
 * auto-refresh, and other UI enhancements for the dashboard, inventory,
 * requests, and alerts pages.
 *
 * This script is designed to work with Bootstrap 5 and Flask templates.
 * It follows a modular pattern and uses an IIFE to avoid global scope pollution.
 *
 * NOTES:
 * - This file assumes that the inline `<script>` blocks in the Jinja templates
 *   (inventory.html, requests.html, alerts.html) performing similar actions
 *   have been removed to avoid duplicate functionality (double confirmation
 *   prompts, redundant auto‑refresh timers). Remove those inline scripts to
 *   rely solely on this file.
 */

(function() {
    'use strict';

    // ==========================================================================
    // Configuration
    // ==========================================================================
    const CONFIG = {
        // Default auto-refresh intervals (in milliseconds)
        dashboardRefreshInterval: 60000,   // 60 seconds
        alertsRefreshInterval: 30000,       // 30 seconds
        // Default confirm message when no custom message is present
        defaultConfirmMessage: 'Are you sure you want to perform this action?'
    };

    // ==========================================================================
    // Utility Functions
    // ==========================================================================

    /**
     * Returns the auto-refresh interval (in milliseconds) for the current page.
     * If the <body> element has a `data-auto-refresh` attribute, its value (in seconds)
     * is used; otherwise, returns the default based on the page path.
     *
     * @returns {number|null} Refresh interval in ms, or null if no auto-refresh.
     */
    function getAutoRefreshInterval() {
        const body = document.body;
        // Check for explicit data attribute (value in seconds)
        const explicit = body.getAttribute('data-auto-refresh');
        if (explicit !== null) {
            const seconds = parseInt(explicit, 10);
            return (isNaN(seconds) || seconds <= 0) ? null : seconds * 1000;
        }

        // No explicit attribute, fall back to page-specific defaults
        const path = window.location.pathname;
        if (path === '/' || path === '/dashboard') {
            return CONFIG.dashboardRefreshInterval;
        }
        if (path === '/alerts') {
            return CONFIG.alertsRefreshInterval;
        }
        return null;
    }

    /**
     * Starts auto-refresh if an interval is configured.
     * The page will reload after the specified delay.
     * Only one timer is active at a time.
     */
    function enableAutoRefresh() {
        // Clear any existing timer to prevent duplicates
        if (window._bloodbankAutoRefreshTimer) {
            clearTimeout(window._bloodbankAutoRefreshTimer);
            window._bloodbankAutoRefreshTimer = null;
        }

        const interval = getAutoRefreshInterval();
        if (interval === null) {
            return;
        }

        window._bloodbankAutoRefreshTimer = setTimeout(function() {
            window.location.reload();
        }, interval);

        // Debug log for development
        if (window.console && console.debug) {
            console.debug(
                '[BloodBank] Auto-refresh scheduled in',
                interval / 1000,
                'seconds.'
            );
        }
    }

    /**
     * Binds a confirmation dialog to a form submission.
     * Uses a data attribute `data-confirm-message` or a default message.
     * Prevents double binding by checking a custom dataset flag.
     *
     * @param {HTMLFormElement} form - The form element to bind.
     */
    function bindConfirmDialog(form) {
        // Avoid double-binding
        if (form.dataset._bbConfirmBound) {
            return;
        }
        form.dataset._bbConfirmBound = 'true';

        form.addEventListener('submit', function(event) {
            const message = form.getAttribute('data-confirm-message') ||
                            CONFIG.defaultConfirmMessage;
            if (!confirm(message)) {
                event.preventDefault();
                event.stopPropagation();
            }
        });
    }

    /**
     * Binds confirmation dialogs to all forms that require user confirmation.
     *
     * Targets forms based on:
     * - Presence of a `data-confirm` attribute (set to "true" or "1").
     * - Action URL containing `/issue`, `/cancel`, or `/resolve`.
     */
    function bindAllConfirmDialogs() {
        const forms = document.querySelectorAll(
            'form[data-confirm="true"], ' +
            'form[data-confirm="1"], ' +
            'form[action*="/issue"], ' +
            'form[action*="/cancel"], ' +
            'form[action*="/resolve"]'
        );

        forms.forEach(function(form) {
            bindConfirmDialog(form);
        });
    }

    /**
     * Restarts the auto-refresh timer if it was stopped.
     * Useful if the page uses Ajax to update content without a full reload.
     */
    function restartAutoRefresh() {
        enableAutoRefresh();
    }

    // ==========================================================================
    // Initialization
    // ==========================================================================

    /**
     * Main initialisation function, called after the DOM is ready.
     */
    function init() {
        // 1. Bind confirmation dialogs to all relevant forms
        bindAllConfirmDialogs();

        // 2. Enable auto-refresh if configured (will clear any existing timer)
        enableAutoRefresh();

        // 3. Expose restart function globally in case of dynamic content updates
        window._restartBloodbankAutoRefresh = restartAutoRefresh;

        if (window.console && console.debug) {
            console.debug('[BloodBank] Frontend scripts initialised.');
        }
    }

    // ==========================================================================
    // DOM Ready (supports modern and older browsers)
    // ==========================================================================
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        // DOMContentLoaded has already fired
        init();
    }

})();
