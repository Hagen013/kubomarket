// Собственные импорты
import {Vue, Vuex, VueResurse} from './vue.js'

import store from './store';

// Хедер
import headerTop from './blocks/header-top/header-top';
import headerMiddle from './blocks/header-middle/header-middle';
import headerBottom from './blocks/header-bottom/header-bottom';

// Footer
import footer from './blocks/footer/footer.js';

// Page-overlay
import pageOverlay from './blocks/page-overlay/page-overlay';

store.dispatch('initAll');
