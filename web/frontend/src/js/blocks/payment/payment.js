import { Vue } from '../../vue.js';
import store from '../../store'

var payment = new Vue({
    name: 'payment',
    el: '#js-payment',
    data: {
        paymentMethod: "AC"
    },
    methods: {
        changePaymentMethod(paymentMethod) {
            this.paymentMethod = paymentMethod;
        }
    }
});