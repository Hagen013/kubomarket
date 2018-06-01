import { Vue } from '../../vue.js';
import store from '../../store'

import purchaseModal from '../added-to-cart-modal/purchase-modal.vue';


var modalController = new Vue({
    name: 'modal-controller',
    el: '#modal-controller',
    store,
    data: {

    },
    components: {
        'purchase-modal': purchaseModal,
    },
    computed: {
        purchaseModalIsActive() {
            return this.$store.state.showPurchaseModal.isShowModal;
        }
    },
    methods: {
        closePurchaseModal() {
            this.$store.commit("showPurchaseModal/hide");
        },
        showPurchaseModal() {
            this.$store.commit("showPurchaseModal/show");
        }
    }
});