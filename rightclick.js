(function() {
    'use strict';

    // Theme Colors (synced with localStorage)
    const themeColors = {
        green: { primary: '#22c55e', dim: 'rgba(34, 197, 94, 0.1)' },
        blue: { primary: '#3b82f6', dim: 'rgba(59, 130, 246, 0.1)' },
        red: { primary: '#ef4444', dim: 'rgba(239, 68, 68, 0.1)' },
        cyan: { primary: '#06b6d4', dim: 'rgba(6, 182, 212, 0.1)' },
        pink: { primary: '#ec4899', dim: 'rgba(236, 72, 153, 0.1)' },
        purple: { primary: '#8b5cf6', dim: 'rgba(139, 92, 246, 0.1)' },
        yellow: { primary: '#eab308', dim: 'rgba(234, 179, 8, 0.1)' },
        white: { primary: '#ffffff', dim: 'rgba(255, 255, 255, 0.1)' },
        whiteout: { primary: '#ffffff', dim: 'rgba(255, 255, 255, 0.05)' }
    };

    // Apply current theme
    function applyTheme() {
        const theme = localStorage.getItem('theme') || 'green';
        const colors = themeColors[theme] || themeColors.green;
        document.documentElement.style.setProperty('--accent', colors.primary);
        document.documentElement.style.setProperty('--accent-dim', colors.dim);
    }

    // Listen for theme changes
    window.addEventListener('storage', (e) => {
        if (e.key === 'theme') applyTheme();
    });

    // Create menu element
    const menu = document.createElement('div');
    menu.className = 'custom-context-menu';
    menu.innerHTML = `
        <div class="context-menu-item" data-action="copy">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
            </svg>
            <span>Copy</span>
            <span class="shortcut">Ctrl+C</span>
        </div>
        <div class="context-menu-item" data-action="paste">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path>
                <rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect>
            </svg>
            <span>Paste</span>
            <span class="shortcut">Ctrl+V</span>
        </div>
        <div class="context-menu-item" data-action="cut">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="6" cy="6" r="3"></circle>
                <circle cx="6" cy="18" r="3"></circle>
                <line x1="20" y1="4" x2="8.12" y2="15.88"></line>
                <line x1="14.47" y1="14.48" x2="20" y2="20"></line>
                <line x1="8.12" y1="8.12" x2="12" y2="12"></line>
            </svg>
            <span>Cut</span>
            <span class="shortcut">Ctrl+X</span>
        </div>
        <div class="context-menu-divider"></div>
        <div class="context-menu-item danger" data-action="panic">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                <line x1="12" y1="9" x2="12" y2="13"></line>
                <line x1="12" y1="17" x2="12.01" y2="17"></line>
            </svg>
            <span>Panic</span>
        </div>
        <div class="context-menu-divider"></div>
        <div class="context-menu-item" data-action="theme">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="5"></circle>
                <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"></path>
            </svg>
            <span>Theme</span>
        </div>
        <div class="context-menu-item" data-action="exitFullscreen">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M8 3v3a2 2 0 0 1-2 2H3m18 0h-3a2 2 0 0 1-2-2V3m0 18v-3a2 2 0 0 1 2-2h3M3 16h3a2 2 0 0 1 2 2v3"></path>
            </svg>
            <span>Exit Fullscreen</span>
        </div>
    `;
    document.body.appendChild(menu);

    let activeTextbox = null;

    // Check if element is a text input
    function isTextInput(el) {
        if (!el) return false;
        const tagName = el.tagName.toLowerCase();
        if (tagName === 'textarea') return true;
        if (tagName === 'input') {
            const type = el.type.toLowerCase();
            return ['text', 'password', 'email', 'search', 'url', 'tel', 'number'].includes(type);
        }
        return el.isContentEditable;
    }

    // Update menu item states
    function updateMenuStates() {
        const pasteItem = menu.querySelector('[data-action="paste"]');
        const cutItem = menu.querySelector('[data-action="cut"]');
        const exitFsItem = menu.querySelector('[data-action="exitFullscreen"]');

        // Paste and Cut only enabled for text inputs
        if (activeTextbox) {
            pasteItem.classList.remove('disabled');
            cutItem.classList.remove('disabled');
        } else {
            pasteItem.classList.add('disabled');
            cutItem.classList.add('disabled');
        }

        // Exit fullscreen only if in fullscreen
        if (document.fullscreenElement || document.webkitFullscreenElement) {
            exitFsItem.classList.remove('disabled');
        } else {
            exitFsItem.classList.add('disabled');
        }
    }

    // Show menu
    function showMenu(x, y) {
        updateMenuStates();
        
        // Position menu
        const menuWidth = 220;
        const menuHeight = menu.offsetHeight || 280;
        
        if (x + menuWidth > window.innerWidth) {
            x = window.innerWidth - menuWidth - 10;
        }
        if (y + menuHeight > window.innerHeight) {
            y = window.innerHeight - menuHeight - 10;
        }
        
        menu.style.left = x + 'px';
        menu.style.top = y + 'px';
        menu.classList.add('visible');
    }

    // Hide menu
    function hideMenu() {
        menu.classList.remove('visible');
    }

    // Handle context menu
    document.addEventListener('contextmenu', (e) => {
        e.preventDefault();
        activeTextbox = isTextInput(e.target) ? e.target : null;
        showMenu(e.clientX, e.clientY);
    });

    // Hide on click outside
    document.addEventListener('click', (e) => {
        if (!menu.contains(e.target)) {
            hideMenu();
        }
    });

    // Hide on escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') hideMenu();
    });

    // Handle menu actions
    menu.addEventListener('click', async (e) => {
        const item = e.target.closest('.context-menu-item');
        if (!item || item.classList.contains('disabled')) return;

        const action = item.dataset.action;

        switch (action) {
            case 'copy':
                try {
                    const selection = window.getSelection().toString();
                    if (selection) {
                        await navigator.clipboard.writeText(selection);
                    } else if (activeTextbox) {
                        const text = activeTextbox.value.substring(
                            activeTextbox.selectionStart,
                            activeTextbox.selectionEnd
                        );
                        if (text) await navigator.clipboard.writeText(text);
                    }
                } catch (err) {
                    document.execCommand('copy');
                }
                break;

            case 'paste':
                if (activeTextbox) {
                    try {
                        const text = await navigator.clipboard.readText();
                        const start = activeTextbox.selectionStart;
                        const end = activeTextbox.selectionEnd;
                        const value = activeTextbox.value;
                        activeTextbox.value = value.slice(0, start) + text + value.slice(end);
                        activeTextbox.selectionStart = activeTextbox.selectionEnd = start + text.length;
                        activeTextbox.dispatchEvent(new Event('input', { bubbles: true }));
                    } catch (err) {
                        activeTextbox.focus();
                        document.execCommand('paste');
                    }
                }
                break;

            case 'cut':
                if (activeTextbox) {
                    try {
                        const start = activeTextbox.selectionStart;
                        const end = activeTextbox.selectionEnd;
                        const text = activeTextbox.value.substring(start, end);
                        if (text) {
                            await navigator.clipboard.writeText(text);
                            activeTextbox.value = activeTextbox.value.slice(0, start) + activeTextbox.value.slice(end);
                            activeTextbox.selectionStart = activeTextbox.selectionEnd = start;
                            activeTextbox.dispatchEvent(new Event('input', { bubbles: true }));
                        }
                    } catch (err) {
                        document.execCommand('cut');
                    }
                }
                break;

            case 'panic':
                window.location.replace('https://launchpad.classlink.com/wisd');
                break;

            case 'theme':
                window.location.href = 'theme.html';
                break;

            case 'exitFullscreen':
                if (document.fullscreenElement) {
                    document.exitFullscreen();
                } else if (document.webkitFullscreenElement) {
                    document.webkitExitFullscreen();
                }
                break;
        }

        hideMenu();
    });

    // Initialize theme
    applyTheme();

})();