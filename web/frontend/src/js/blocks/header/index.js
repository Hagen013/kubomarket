import { Vue } from '../../vue.js'

import store from '../../store'


var header = new Vue({
    name: 'header',
    el: '#header',
    store,
    data: {
    },
    computed: {
        mobileMenuIsVisible() {
            return this.$store.state.mobileMenu.active
        }
    },
    methods: {
        showMobileMenu() {
            this.$store.commit("mobileMenu/show");
        }
    }
});
