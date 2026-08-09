/**
 * HelpTour - Lightweight, production-ready interactive help tour.
 * Vanilla JS, no external libraries.
 */
class HelpTour {
  constructor(steps, options = {}) {
    this.steps = steps || [];
    this.options = {
      storageKey: 'helptour_completed',
      role: 'default',
      onComplete: null,
      onSkip: null,
      onStart: null,
      ...options,
    };

    this.currentStep = 0;
    this.isActive = false;
    this.isCompleted = false;
    this._menuOpen = false;

    this.el = {
      overlay: null,
      spotlight: null,
      tooltip: null,
      arrow: null,
      helpBtn: null,
      menu: null,
      finishBtn: null,
    };

    this._boundHandleKeydown = this._handleKeydown.bind(this);
    this._boundHandleResize = this._handleResize.bind(this);

    this._init();
  }

  _init() {
    this._createHelpButton();
    this._checkCompletion();
  }

  _createHelpButton() {
    if (this.el.helpBtn) return;

    const btn = document.createElement('button');
    btn.className = 'help-float-btn';
    btn.setAttribute('aria-label', 'Open help tutorial');
    btn.setAttribute('title', 'Help Tutorial');
    btn.innerHTML = '?';
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      this._toggleMenu();
    });

    const menu = document.createElement('div');
    menu.className = 'help-menu';
    menu.setAttribute('role', 'menu');
    menu.setAttribute('aria-label', 'Help menu');
    Object.assign(menu.style, {
      position: 'fixed',
      bottom: '90px',
      right: '24px',
      zIndex: '9997',
      display: 'none',
      flexDirection: 'column',
      gap: '6px',
      background: 'var(--help-surface, #fff)',
      borderRadius: 'var(--help-radius, 14px)',
      boxShadow: 'var(--help-shadow, 0 10px 25px rgba(0,0,0,0.15))',
      padding: '8px',
      minWidth: '180px',
      border: '1px solid var(--help-border, #e2e8f0)',
      fontFamily: 'inherit',
    });

    if (window.innerWidth <= 768) {
      menu.style.bottom = '80px';
      menu.style.right = '16px';
    }

    const startLabel = this.isCompleted ? 'Restart Tutorial' : 'Start Tutorial';
    const startItem = document.createElement('button');
    startItem.className = 'help-menu__item';
    Object.assign(startItem.style, {
      display: 'block',
      width: '100%',
      textAlign: 'left',
      padding: '8px 12px',
      border: 'none',
      background: 'none',
      borderRadius: '6px',
      fontSize: '13px',
      fontWeight: '500',
      color: 'var(--help-text, #0f172a)',
      cursor: 'pointer',
      transition: 'all 150ms ease',
      fontFamily: 'inherit',
    });
    startItem.textContent = startLabel;
    startItem.addEventListener('click', () => {
      menu.style.display = 'none';
      this._menuOpen = false;
      if (this.isCompleted) {
        this.restart();
      } else {
        this.start();
      }
    });

    const exitItem = document.createElement('button');
    exitItem.className = 'help-menu__item';
    Object.assign(exitItem.style, {
      display: 'block',
      width: '100%',
      textAlign: 'left',
      padding: '8px 12px',
      border: 'none',
      background: 'none',
      borderRadius: '6px',
      fontSize: '13px',
      fontWeight: '500',
      color: 'var(--help-text-secondary, #64748b)',
      cursor: 'pointer',
      transition: 'all 150ms ease',
      fontFamily: 'inherit',
    });
    exitItem.textContent = 'Exit';
    exitItem.addEventListener('click', () => {
      menu.style.display = 'none';
      this._menuOpen = false;
    });

    menu.appendChild(startItem);
    menu.appendChild(exitItem);

    document.body.appendChild(btn);
    document.body.appendChild(menu);

    this.el.helpBtn = btn;
    this.el.menu = menu;

    document.addEventListener('click', (e) => {
      if (this._menuOpen && !btn.contains(e.target) && !menu.contains(e.target)) {
        this._closeMenu();
      }
    });
  }

  _toggleMenu() {
    this._menuOpen = !this._menuOpen;
    if (this.el.menu) {
      this.el.menu.style.display = this._menuOpen ? 'flex' : 'none';
    }
    if (this._menuOpen && this.isCompleted) {
      this._setPulse(false);
    }
  }

  _closeMenu() {
    this._menuOpen = false;
    if (this.el.menu) {
      this.el.menu.style.display = 'none';
    }
    if (!this.isCompleted) {
      this._setPulse(true);
    }
  }

  _setPulse(enabled) {
    if (!this.el.helpBtn) return;
    this.el.helpBtn.classList.toggle('help-float-btn--pulse', enabled);
  }

  _checkCompletion() {
    const key = this._getStorageKey();
    try {
      this.isCompleted = localStorage.getItem(key) === 'true';
    } catch (e) {
      this.isCompleted = false;
    }
    if (this.isCompleted) {
      this._setPulse(false);
    }
  }

  _getStorageKey() {
    return `${this.options.storageKey}_${this.options.role}`;
  }

  _saveCompletion() {
    try {
      localStorage.setItem(this._getStorageKey(), 'true');
    } catch (e) {}
  }

  _clearCompletion() {
    try {
      localStorage.removeItem(this._getStorageKey());
    } catch (e) {}
  }

  _saveCurrentStep() {
    try {
      localStorage.setItem(
        'helptour_current_step',
        JSON.stringify({ role: this.options.role, step: this.currentStep })
      );
    } catch (e) {}
  }

  /* ---------- Public API ---------- */

  start() {
    if (!this.steps.length) {
      this._showNoSteps();
      return;
    }
    this.currentStep = 0;
    this.isActive = true;
    this._saveCurrentStep();

    if (this.options.onStart) this.options.onStart();
    this._buildTourUI();
    this._showStep(0);
  }

  restart() {
    this._clearCompletion();
    this.isCompleted = false;
    this._setPulse(true);
    this.start();
  }

  skip() {
    this._finish(false);
  }

  finish() {
    this._finish(true);
  }

  exit() {
    this.isActive = false;
    this._cleanup();
    document.body.classList.remove('help-tour--active');
    this._closeMenu();
    if (this.options.onSkip) this.options.onSkip();
  }

  isTourCompleted() {
    const key = this._getStorageKey();
    try {
      return localStorage.getItem(key) === 'true';
    } catch (e) {
      return false;
    }
  }

  /* ---------- Tour UI ---------- */

  _buildTourUI() {
    this._createOverlay();
    this._createSpotlight();
    this._createTooltip();
    this._createArrow();

    document.body.classList.add('help-tour--active');
    document.addEventListener('keydown', this._boundHandleKeydown);
    window.addEventListener('resize', this._boundHandleResize);
  }

  _createOverlay() {
    if (this.el.overlay) return;
    const overlay = document.createElement('div');
    overlay.className = 'help-tour__overlay';
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay && this.isActive) this.exit();
    });
    document.body.appendChild(overlay);
    this.el.overlay = overlay;
  }

  _createSpotlight() {
    if (this.el.spotlight) return;
    const spotlight = document.createElement('div');
    spotlight.className = 'help-tour__spotlight';
    document.body.appendChild(spotlight);
    this.el.spotlight = spotlight;
  }

  _createArrow() {
    if (this.el.arrow) return;
    const arrow = document.createElement('div');
    arrow.className = 'help-tour__arrow';
    document.body.appendChild(arrow);
    this.el.arrow = arrow;
  }

  _createTooltip() {
    if (this.el.tooltip) return;
    const tooltip = document.createElement('div');
    tooltip.className = 'help-tour__tooltip';
    tooltip.setAttribute('role', 'dialog');
    tooltip.setAttribute('aria-live', 'polite');
    tooltip.setAttribute('aria-label', 'Tour tooltip');
    tooltip.innerHTML = `
      <button class="help-tour__btn--close" aria-label="Close tour">&times;</button>
      <div class="help-tour__header">
        <div class="help-tour__step-indicator" id="help-tour-step-indicator">1</div>
        <h3 class="help-tour__title" id="help-tour-title"></h3>
      </div>
      <p class="help-tour__description" id="help-tour-description"></p>
      <div class="help-tour__progress">
        <div class="help-tour__progress-bar">
          <div class="help-tour__progress-fill"></div>
        </div>
        <span class="help-tour__step-text" id="help-tour-step-text"></span>
      </div>
      <div class="help-tour__actions">
        <button class="help-tour__btn--skip" id="help-tour-skip">Skip</button>
        <div class="help-tour__btn-group">
          <button class="help-tour__btn help-tour__btn--secondary" id="help-tour-prev" type="button">
            <span>&#8592;</span> Previous
          </button>
          <button class="help-tour__btn help-tour__btn--primary" id="help-tour-next" type="button">
            Next <span>&#8594;</span>
          </button>
        </div>
      </div>
    `;

    tooltip.querySelector('.help-tour__btn--close').addEventListener('click', () => this.exit());
    tooltip.querySelector('#help-tour-prev').addEventListener('click', () => this.prev());
    tooltip.querySelector('#help-tour-next').addEventListener('click', () => this.next());
    tooltip.querySelector('#help-tour-skip').addEventListener('click', () => this.skip());

    document.body.appendChild(tooltip);
    this.el.tooltip = tooltip;
  }

  _updateProgress() {
    if (!this.el.tooltip) return;
    const fill = this.el.tooltip.querySelector('.help-tour__progress-fill');
    const text = this.el.tooltip.querySelector('.help-tour__step-text');
    const total = this.steps.length;
    const current = this.currentStep + 1;

    if (fill) fill.style.width = `${(this.currentStep / Math.max(total - 1, 1)) * 100}%`;
    if (text) text.textContent = `Step ${current} of ${total}`;

    const indicator = this.el.tooltip.querySelector('#help-tour-step-indicator');
    if (indicator) indicator.textContent = current;
  }

  _updateNavButtons() {
    if (!this.el.tooltip) return;

    const prevBtn = this.el.tooltip.querySelector('#help-tour-prev');
    const nextBtn = this.el.tooltip.querySelector('#help-tour-next');
    const btnGroup = this.el.tooltip.querySelector('.help-tour__btn-group');

    if (prevBtn) prevBtn.style.display = this.currentStep === 0 ? 'none' : 'inline-flex';
    if (nextBtn) nextBtn.style.display = this.currentStep === this.steps.length - 1 ? 'none' : 'inline-flex';

    if (this.currentStep === this.steps.length - 1) {
      if (!this.el.finishBtn) {
        const finishBtn = document.createElement('button');
        finishBtn.className = 'help-tour__btn help-tour__btn--finish';
        finishBtn.id = 'help-tour-finish';
        finishBtn.textContent = 'Finish';
        finishBtn.type = 'button';
        finishBtn.addEventListener('click', () => this.finish());
        btnGroup.appendChild(finishBtn);
        this.el.finishBtn = finishBtn;
      }
      this.el.finishBtn.style.display = 'inline-flex';
    } else if (this.el.finishBtn) {
      this.el.finishBtn.style.display = 'none';
    }
  }

  _showStepContent(step) {
    if (!this.el.tooltip) return;

    const indicator = this.el.tooltip.querySelector('#help-tour-step-indicator');
    const titleEl = this.el.tooltip.querySelector('#help-tour-title');
    const descEl = this.el.tooltip.querySelector('#help-tour-description');

    if (indicator) indicator.textContent = this.currentStep + 1;
    if (titleEl) titleEl.textContent = step.title || '';

    let desc = step.description || '';
    if (step.instruction) desc += `\n\n${step.instruction}`;
    if (descEl) descEl.textContent = desc;

    this._updateProgress();
    this._updateNavButtons();

    requestAnimationFrame(() => {
      if (this.el.tooltip) this.el.tooltip.classList.add('help-tour__tooltip--visible');
      if (this.el.arrow) this.el.arrow.classList.add('help-tour__arrow--visible');
    });
  }

  _showStep(index) {
    if (index < 0 || index >= this.steps.length) return;
    this.currentStep = index;
    this._saveCurrentStep();

    const step = this.steps[index];
    const target = this._findTarget(step.selector);

    if (!target) {
      const nextIdx = this._findNextAvailableIndex(index);
      if (nextIdx !== null) {
        this._showStep(nextIdx);
        return;
      }
    }

    this._showOverlay();

    if (target) {
      this._expandParentMenus(target);
      this._scrollToElement(target);
      this._positionSpotlight(target);
      this._showStepContent(step);
      this._positionTooltip(target);
      this._positionArrow(target);
    } else {
      if (this.el.spotlight) this.el.spotlight.style.display = 'none';
      this._showStepContent(step);
      if (this.el.arrow) this.el.arrow.classList.remove('help-tour__arrow--visible');
    }
  }

  _findTarget(selector) {
    try {
      return document.querySelector(selector);
    } catch (e) {
      return null;
    }
  }

  _findNextAvailableIndex(startIndex) {
    for (let i = startIndex + 1; i < this.steps.length; i++) {
      if (this._findTarget(this.steps[i].selector)) return i;
    }
    return null;
  }

  _expandParentMenus(element) {
    let parent = element.parentElement;
    let attempts = 0;
    while (parent && attempts < 10) {
      if (parent.hasAttribute('data-collapse') || parent.classList.contains('collapse')) {
        const toggle = parent.querySelector('[data-toggle="collapse"], .collapse-toggle');
        if (toggle) toggle.click();
        if (parent.classList.contains('collapse')) parent.classList.add('show');
        const targetMenu = parent.getAttribute('data-collapse');
        if (targetMenu) {
          const menuEl = document.querySelector(targetMenu);
          if (menuEl) menuEl.style.display = 'block';
        }
      }
      parent = parent.parentElement;
      attempts++;
    }
  }

  _scrollToElement(element) {
    const rect = element.getBoundingClientRect();
    const offset = 80;
    if (rect.top < offset || rect.bottom > window.innerHeight - offset) {
      window.scrollTo({
        top: rect.top + window.scrollY - offset,
        behavior: 'smooth',
      });
    }
  }

  _showOverlay() {
    if (this.el.overlay) this.el.overlay.classList.add('help-tour__overlay--visible');
  }

  _positionSpotlight(target) {
    if (!this.el.spotlight || !target) return;
    const rect = target.getBoundingClientRect();
    this.el.spotlight.style.cssText = `
      position: fixed;
      top: ${rect.top}px;
      left: ${rect.left}px;
      width: ${rect.width}px;
      height: ${rect.height}px;
      border-radius: 4px;
      box-shadow: 0 0 0 9999px rgba(0,0,0,0.6);
      transition: all 350ms cubic-bezier(0.25, 0.1, 0.25, 1);
      z-index: 9999;
      pointer-events: none;
    `;
    this.el.spotlight.style.display = 'block';
  }

  _getPlacement(target) {
    if (!target) return 'bottom';
    const rect = target.getBoundingClientRect();
    const tooltipWidth = 360;
    const tooltipHeight = 200;
    const margin = 20;

    const canPlaceRight = rect.right + tooltipWidth + margin < window.innerWidth;
    const canPlaceLeft = rect.left - tooltipWidth - margin > 0;
    const canPlaceBottom = rect.bottom + tooltipHeight + margin < window.innerHeight;
    const canPlaceTop = rect.top - tooltipHeight - margin > 0;

    if (canPlaceBottom) return 'bottom';
    if (canPlaceTop) return 'top';
    if (canPlaceRight) return 'right';
    if (canPlaceLeft) return 'left';
    return 'top';
  }

  _positionTooltip(target) {
    if (!this.el.tooltip || !target) return;

    const rect = target.getBoundingClientRect();
    const tooltip = this.el.tooltip;

    tooltip.style.visibility = 'hidden';
    tooltip.style.display = 'block';
    const realWidth = tooltip.offsetWidth;
    const realHeight = tooltip.offsetHeight;

    const placement = this._getPlacement(target);
    const margin = 20;
    const scrollTop = window.scrollY;
    const scrollLeft = window.scrollX;

    let top, left;
    if (placement === 'top') {
      top = Math.max(margin, rect.top + scrollTop - realHeight - margin);
      left = Math.max(margin, Math.min(
        rect.left + rect.width / 2 - realWidth / 2 + scrollLeft,
        window.innerWidth - realWidth - margin
      ));
    } else if (placement === 'bottom') {
      top = Math.max(margin, rect.bottom + scrollTop + margin);
      left = Math.max(margin, Math.min(
        rect.left + rect.width / 2 - realWidth / 2 + scrollLeft,
        window.innerWidth - realWidth - margin
      ));
    } else if (placement === 'right') {
      top = Math.max(margin, Math.min(
        rect.top + rect.height / 2 - realHeight / 2 + scrollTop,
        window.innerHeight - realHeight - margin
      ));
      left = Math.min(window.innerWidth - realWidth - margin, rect.right + scrollLeft + margin);
    } else {
      top = Math.max(margin, Math.min(
        rect.top + rect.height / 2 - realHeight / 2 + scrollTop,
        window.innerHeight - realHeight - margin
      ));
      left = Math.max(margin, rect.left + scrollLeft - realWidth - margin);
    }

    tooltip.style.top = `${top}px`;
    tooltip.style.left = `${left}px`;
    tooltip.style.visibility = 'visible';
    tooltip.style.display = 'block';

    this._positionArrow(target, placement);
  }

  _positionArrow(target, placement) {
    if (!this.el.arrow || !target) return;
    const rect = target.getBoundingClientRect();
    const scrollTop = window.scrollY;
    const scrollLeft = window.scrollX;
    const arrowSize = 22;

    let top, left;
    if (placement === 'top') {
      top = rect.bottom + scrollTop;
      left = rect.left + rect.width / 2 - arrowSize / 2 + scrollLeft;
      this.el.arrow.style.transform = 'rotate(45deg)';
    } else if (placement === 'bottom') {
      top = rect.top + scrollTop - arrowSize / 2;
      left = rect.left + rect.width / 2 - arrowSize / 2 + scrollLeft;
      this.el.arrow.style.transform = 'rotate(-45deg) scaleX(-1)';
    } else if (placement === 'right') {
      top = rect.top + rect.height / 2 - arrowSize / 2 + scrollTop;
      left = rect.left + scrollLeft - arrowSize / 2;
      this.el.arrow.style.transform = 'rotate(-45deg) scaleY(-1)';
    } else {
      top = rect.top + rect.height / 2 - arrowSize / 2 + scrollTop;
      left = rect.right + scrollLeft - arrowSize / 2;
      this.el.arrow.style.transform = 'rotate(45deg) scaleY(-1)';
    }

    this.el.arrow.style.top = `${top}px`;
    this.el.arrow.style.left = `${left}px`;
    this.el.arrow.className = 'help-tour__arrow help-tour__arrow--visible';
  }

  /* ---------- Navigation ---------- */

  next() {
    if (this.currentStep < this.steps.length - 1) {
      this._fadeOut(() => this._showStep(this.currentStep + 1));
    } else {
      this.finish();
    }
  }

  prev() {
    if (this.currentStep > 0) {
      this._fadeOut(() => this._showStep(this.currentStep - 1));
    }
  }

  _fadeOut(callback) {
    if (this.el.tooltip) this.el.tooltip.classList.remove('help-tour__tooltip--visible');
    if (this.el.arrow) this.el.arrow.classList.remove('help-tour__arrow--visible');
    setTimeout(callback, 280);
  }

  _showNoSteps() {
    this._buildTourUI();
    if (this.el.tooltip) {
      const indicator = this.el.tooltip.querySelector('#help-tour-step-indicator');
      const titleEl = this.el.tooltip.querySelector('#help-tour-title');
      const descEl = this.el.tooltip.querySelector('#help-tour-description');
      const prevBtn = this.el.tooltip.querySelector('#help-tour-prev');
      const nextBtn = this.el.tooltip.querySelector('#help-tour-next');

      if (indicator) indicator.style.display = 'none';
      if (titleEl) titleEl.textContent = 'No Tutorial Available';
      if (descEl) descEl.textContent = 'No tutorial steps are configured for this page.';
      if (prevBtn) prevBtn.style.display = 'none';
      if (nextBtn) nextBtn.style.display = 'none';
      if (this.el.spotlight) this.el.spotlight.style.display = 'none';

      this.el.tooltip.classList.add('help-tour__tooltip--visible');
    }
  }

  _finish(completed) {
    if (completed) {
      this._saveCompletion();
      this.isCompleted = true;
      this._setPulse(false);
    }
    this.isActive = false;
    this._cleanup();
    document.body.classList.remove('help-tour--active');
    this._closeMenu();

    if (completed && this.options.onComplete) this.options.onComplete();
    else if (!completed && this.options.onSkip) this.options.onSkip();
  }

  _cleanup() {
    if (this.el.overlay) this.el.overlay.classList.remove('help-tour__overlay--visible');
    if (this.el.tooltip) this.el.tooltip.classList.remove('help-tour__tooltip--visible');
    if (this.el.arrow) this.el.arrow.classList.remove('help-tour__arrow--visible');
    if (this.el.spotlight) this.el.spotlight.style.display = 'none';
  }

  /* ---------- Events ---------- */

  _handleKeydown(e) {
    if (!this.isActive) return;
    switch (e.key) {
      case 'Escape':
        e.preventDefault();
        this.exit();
        break;
      case 'Enter':
        e.preventDefault();
        this.next();
        break;
      case 'ArrowRight':
        e.preventDefault();
        this.next();
        break;
      case 'ArrowLeft':
        e.preventDefault();
        this.prev();
        break;
      case 'Tab':
        e.preventDefault();
        this._trapFocus(e);
        break;
    }
  }

  _handleResize() {
    if (!this.isActive) return;
    const step = this.steps[this.currentStep];
    if (!step) return;
    const target = this._findTarget(step.selector);
    if (target) {
      this._positionSpotlight(target);
      this._positionTooltip(target);
      this._positionArrow(target);
    }
  }

  _trapFocus(e) {
    if (!this.el.tooltip || !this.isActive) return;
    const focusable = this.el.tooltip.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    if (focusable.length === 0) return;
    const first = focusable[0];
    const last = focusable[focusable.length - 1];

    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    } else {
      if (!this._focusHandled) {
        this._focusHandled = true;
        setTimeout(() => {
          const nextBtn = this.el.tooltip.querySelector('#help-tour-next');
          if (nextBtn) nextBtn.focus();
        }, 100);
      }
    }
  }

  _releaseFocus() {
    this._focusHandled = false;
  }

  /* ---------- Destroy ---------- */

  destroy() {
    this.exit();
    if (this.el.helpBtn && this.el.helpBtn.parentNode) this.el.helpBtn.parentNode.removeChild(this.el.helpBtn);
    if (this.el.menu && this.el.menu.parentNode) this.el.menu.parentNode.removeChild(this.el.menu);
    if (this.el.overlay && this.el.overlay.parentNode) this.el.overlay.parentNode.removeChild(this.el.overlay);
    if (this.el.spotlight && this.el.spotlight.parentNode) this.el.spotlight.parentNode.removeChild(this.el.spotlight);
    if (this.el.tooltip && this.el.tooltip.parentNode) this.el.tooltip.parentNode.removeChild(this.el.tooltip);
    if (this.el.arrow && this.el.arrow.parentNode) this.el.arrow.parentNode.removeChild(this.el.arrow);
    this.el = {};
    document.removeEventListener('keydown', this._boundHandleKeydown);
    window.removeEventListener('resize', this._boundHandleResize);
  }
}

/* ===== Auto-init ===== */
(function() {
  function init() {
    if (window.HelpTourInstance) return;

    let steps = null;
    if (window.HELP_TOUR_STEPS && Array.isArray(window.HELP_TOUR_STEPS)) {
      steps = window.HELP_TOUR_STEPS;
    } else {
      const scriptEl = document.getElementById('help-tour-steps');
      if (scriptEl) {
        try {
          steps = JSON.parse(scriptEl.textContent || scriptEl.innerText);
        } catch (e) {
          console.error('[HelpTour] Invalid JSON in #help-tour-steps:', e);
        }
      }
    }

    if (steps && steps.length > 0) {
      window.HelpTourInstance = new HelpTour(steps, {
        storageKey: window.HELP_TOUR_STORAGE_KEY || 'helptour_completed',
        role: window.HELP_TOUR_ROLE || 'default',
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
