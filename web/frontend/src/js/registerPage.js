// Common VUE and store
import {Vue} from './vue.js'
import store from './store';

// Common
import header from './blocks/header'
import footer from './blocks/footer'
import mobileMenu from './blocks/mobileMenu/'
import mobileCatalog from './blocks/mobileCatalog/'
import modalController from './blocks/modalController/index.js';

// Specific
import registerForm from "./blocks/registerForm"

store.dispatch('initAll');