import { Vue } from '../../vue.js';
import CartComponent from './cart.vue'

var Cart = new Vue({
    name: 'cart',
    el: '#js-cart',
    render: h => h(CartComponent)
});
