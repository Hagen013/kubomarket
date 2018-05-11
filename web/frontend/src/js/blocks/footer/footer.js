import Vue from 'vue'
import VueResource from 'vue-resource';

Vue.use(VueResource);

var footer = new Vue({
    name: 'footer',
    el: '#js-footer',
    data:{
        customerEmail: '',
    },
    methods: {
        sendNotificationData() {
            this.customerEmail = '';
        }
    }
});