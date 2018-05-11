// Собственные импорты
import {Vue, Vuex, VueResurse} from './vue.js'

import store from './store';

// Хедер
import headerTop from './blocks/header-top/header-top';
import headerMiddle from './blocks/header-middle/header-middle';
import headerBottom from './blocks/header-bottom/header-bottom';

import catalogLeftContent from './blocks/catalog/__left-content.js';
import itemGallery from './blocks/item-gallery/item-gallery.js';
import sortingBar from './blocks/sorting-bar/sorting-bar.js';
import filters from './blocks/filters/filters.js';


// Page-overlay
import pageOverlay from './blocks/page-overlay/page-overlay';

store.dispatch('initAll');
