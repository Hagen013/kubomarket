import { Vue } from '../../vue.js'

import store from '../../store'

import cartComponent from './components/cart.vue'


var Cart = new Vue({
    name: 'cart',
    el: '#cart',
    store,
    data: {

    },
    components: {
        "cart": cartComponent,
    },
});
