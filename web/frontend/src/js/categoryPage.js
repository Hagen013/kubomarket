// Common VUE and store
import {Vue} from './vue.js'
import store from './store';

import header from './blocks/header'
import footer from './blocks/footer'
import mobileMenu from './blocks/mobileMenu/'
import mobileCatalog from './blocks/mobileCatalog/'

// Page-specific
import Catalog from './blocks/catalog/'

//store.dispatch('geo/initGeo');
store.dispatch('initAll');
