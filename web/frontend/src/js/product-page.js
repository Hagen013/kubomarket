// Собственные импорты
import {Vue, Vuex, VueResurse} from './vue.js'

import store from './store';

// Хедер
import headerTop from './blocks/header-top/header-top';
import headerMiddle from './blocks/header-middle/header-middle';
import headerBottom from './blocks/header-bottom/header-bottom';

// Галлерея product-card
import productCard from './blocks/product-card/product-card.js';

// Footer
import footer from './blocks/footer/footer.js'

// Page-overlay
import pageOverlay from './blocks/page-overlay/page-overlay';


// Jquery plugins
// import './jquery-3.2.1.min.js';
// import './plugins/jquery.fancybox.min.js';

store.dispatch('initAll');
