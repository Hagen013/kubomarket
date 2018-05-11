import { Vue } from '../../vue.js';
import pageOverlay from './__page-overlay.vue';


var jsModal = new Vue({
    name: 'js-modal',
    el: '#js-modal',
    data: {

    },
    components: {
        'page-overlay': pageOverlay,
    },
});