import { isTgWebApp } from '../checkApp.js';
import { initializeOnContentLoaded } from './contentLoaded.js';
import { attachButtonEvents } from './btnEventHandlers.js';

document.addEventListener('DOMContentLoaded', function() {
    // if (!isTgWebApp()) {
    //     return;
    // }
  
    initializeOnContentLoaded();
    attachButtonEvents();
});