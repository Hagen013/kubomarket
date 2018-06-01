import { Vue } from '../../vue.js';
import store from '../../store'

import purchaseModal from '../added-to-cart-modal/purchase-modal.vue';
import cityChoiceModal from '../modals/city-choice-modal.vue';


var modalController = new Vue({
    name: 'modal-controller',
    el: '#modal-controller',
    store,
    data: {

    },
    components: {
        'purchase-modal': purchaseModal,
        'city-choice-modal': cityChoiceModal
    },
    computed: {
        purchaseModalIsActive() {
            return this.$store.state.showPurchaseModal.isShowModal;
        },
        cityChoiceModalIsActive() {
            return this.$store.state.showModalCityChoice.isShowModal;
        }
    },
    methods: {
        closePurchaseModal() {
            this.$store.commit("showPurchaseModal/hide");
        },
        showPurchaseModal() {
            this.$store.commit("showPurchaseModal/show");
        },
        closeCityChoiceModal() {
            this.$store.commit("showModalCityChoice/hide");
        },
        showCityChoiceModal() {
            this.$store.commit("showModalCityChoice/show");
        }
    }
});