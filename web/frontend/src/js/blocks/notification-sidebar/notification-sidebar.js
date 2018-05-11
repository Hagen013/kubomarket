import { Vue } from '../../vue.js';
import pageOverlay from './__page-overlay.vue';


var notificationSidebar = new Vue({
    name: 'notification-sidebar',
    el: '#notification-sidebar',
    data: {

    },
    components: {
        'page-overlay': pageOverlay,
    },
});