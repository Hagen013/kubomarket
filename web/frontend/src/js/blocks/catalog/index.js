import { Vue } from '../../vue.js'

import store from '../../store'


var catalog = new Vue({
    name: 'catalog',
    el: '#catalog',
    store,
    data: {
        displayBrands: false
    },
    methods: {
        toggleBrands() {
            this.displayBrands = !this.displayBrands;
        }
    }
});
