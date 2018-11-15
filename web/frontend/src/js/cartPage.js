// Common VUE and store
import {Vue} from './vue.js'
import VueInputMask from './core/vue-inputmask.js'
import store from './store';
Vue.use(VueInputMask);

// Common
import header from './blocks/header'
import footer from './blocks/footer'
import mobileMenu from './blocks/mobileMenu/'
import mobileCatalog from './blocks/mobileCatalog/'
import modalController from './blocks/modalController/index.js';

// Page-specific
import Cart from './blocks/cart/'

//store.dispatch('geo/initGeo');
store.dispatch('initAll');
