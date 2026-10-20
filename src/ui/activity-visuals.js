/* A hosting profile owns imagery/hues; the workspace owns presence and focus. */
(function (root) {
  'use strict';
  function rgb(hex) {
    return [1, 3, 5].map(start => parseInt(hex.slice(start, start + 2), 16));
  }
  function tint(hex, amount = .78) {
    return rgb(hex).map(value => Math.round(value + (255 - value) * amount)).join(' ');
  }
  function activityState(state, intent, context = state.activeContext) {
    const panels = state.panels.filter(panel => panel.intent === intent && panel.context === context);
    const open = panels.filter(panel => !panel.minimized);
    return {
      presence: open.some(panel => panel.id === state.focused) ? 'focused'
        : open.length ? 'open' : panels.length ? 'minimized' : 'closed',
      notification: state.events.some(event => event.intent === intent && event.context === context && event.status === 'pending')
    };
  }
  function workspaceEmpty(state) {
    return !state.panels.some(panel => panel.context === state.activeContext && !panel.minimized);
  }
  function install({state}) {
    const profile = root.__UXAI_CONFIG__?.profile;
    const visuals = profile?.activityVisuals || {}, emptyCanvas = profile?.emptyCanvas;
    if (!Object.keys(visuals).length && !emptyCanvas) return null;
    const doc = root.document, applied = new WeakMap(), images = new Map();
    const stage = doc.getElementById('workspaceStage');
    const emptyIcon = emptyCanvas && stage?.querySelector('.empty-icon');
    if (emptyCanvas && stage) stage.dataset.emptyCanvas = 'true';
    if (emptyIcon) emptyIcon.setAttribute('aria-hidden', 'true');
    let scheduled = false;
    function decorate(element, intent, current) {
      const visual = visuals[intent];
      if (!visual || !element) return;
      element.dataset.activityVisual = intent;
      element.dataset.activityPresence = current.presence;
      element.dataset.activityNotification = String(current.notification);
      if (applied.get(element) !== intent) {
        element.style.setProperty('--activity-rgb', rgb(visual.color).join(' '));
        element.style.setProperty('--activity-tint', tint(visual.color));
        element.style.setProperty('--activity-image-position', visual.position || 'center');
        applied.set(element, intent);
      }
      const image = images.get(intent);
      element.style.setProperty('--activity-image', image?.ready ? `url("${image.url}")` : 'none');
    }
    function sync() {
      scheduled = false;
      if (emptyCanvas && stage) stage.dataset.workspaceEmpty = String(workspaceEmpty(state));
      for (const tile of doc.querySelectorAll('.intent-tile[data-intent]')) {
        decorate(tile, tile.dataset.intent, activityState(state, tile.dataset.intent));
      }
      for (const entry of doc.querySelectorAll('.avatar-entry[data-intent]')) {
        const current = activityState(state, entry.dataset.intent);
        decorate(entry, entry.dataset.intent, current);
        const button = entry.querySelector('.avatar-button');
        if (button) {
          if (current.presence === 'focused') button.setAttribute('aria-current', 'true');
          else button.removeAttribute('aria-current');
          // Accessible state supplements, rather than replaces, the original action name.
          const it = root.__UXAI_CONFIG__.profile.locale === 'it';
          const words = it
            ? {closed:'Non aperta', minimized:'Ridotta a icona', open:'Aperta', focused:'In focus', alert:'Notifica da esaminare'}
            : {closed:'Not open', minimized:'Minimized', open:'Open', focused:'In focus', alert:'Notification to review'};
          let status = entry.querySelector('.activity-state-text');
          if (!status) {
            status = doc.createElement('span'); status.className = 'activity-state-text';
            status.id = 'activity-state-' + entry.dataset.intent;
            entry.append(status);
          }
          const value = words[current.presence] + (current.notification ? ' · ' + words.alert : '');
          if (status.textContent !== value) status.textContent = value;
          button.setAttribute('aria-describedby', status.id);
        }
      }
      for (const panel of state.panels) {
        decorate(panel.el, panel.intent, activityState(state, panel.intent, panel.context));
      }
    }
    function schedule() {
      if (scheduled) return;
      scheduled = true; root.requestAnimationFrame(sync);
    }
    // Observe native repaint signals only. Own visual attributes/styles are excluded.
    const observer = new root.MutationObserver(schedule);
    observer.observe(doc.body, {subtree:true, childList:true, attributes:true,
      attributeFilter:['data-focused', 'data-active', 'data-alert', 'data-selected', 'hidden']});
    for (const [intent, visual] of Object.entries(visuals)) {
      if (!visual.image) continue;
      const image = new root.Image();
      images.set(intent, {url:visual.image, ready:false});
      image.onload = () => {images.get(intent).ready = true; schedule();};
      image.onerror = () => {images.get(intent).ready = false; schedule();};
      image.decoding = 'async'; image.src = visual.image;
    }
    if (emptyCanvas?.image && emptyIcon) {
      const image = new root.Image();
      image.onload = () => {
        emptyIcon.style.setProperty('--empty-canvas-image', `url("${emptyCanvas.image}")`);
        emptyIcon.dataset.illustrationReady = 'true';
      };
      image.onerror = () => {delete emptyIcon.dataset.illustrationReady;};
      image.decoding = 'async'; image.src = emptyCanvas.image;
    }
    sync();
    return {sync, destroy:() => observer.disconnect()};
  }
  root.KUXActivityVisuals = Object.freeze({activityState, workspaceEmpty, tint, install});
})(typeof window === 'undefined' ? globalThis : window);
