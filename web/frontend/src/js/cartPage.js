// Common VUE and store
import {Vue} from './vue.js'
import store from './store';

// Common
import header from './blocks/header'
import footer from './blocks/footer'
import mobileMenu from './blocks/mobileMenu/'
import mobileCatalog from './blocks/mobileCatalog/'

// Page-specific
import Cart from './blocks/cart/'

//store.dispatch('geo/initGeo');
store.dispatch('initAll');
