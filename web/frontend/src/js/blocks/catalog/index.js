import { Vue } from '../../vue.js'

import store from '../../store'


var catalog = new Vue({
    name: 'catalog',
    el: '#catalog',
    store,
    data: {
        displayBrands: false
    },
    created() {
        this.checkUserStatus();
    },
    methods: {
        toggleBrands() {
            this.displayBrands = !this.displayBrands;
        },
        checkUserStatus() {
            if (userAdminStatus === true) {
                this.$store.commit('showPageControls/show');
            }
        },
    }
});
