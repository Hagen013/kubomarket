import { Vue } from '../../vue.js';
import store from '../../store'

import purchaseModal from '../added-to-cart-modal/purchase-modal.vue';
import cityChoiceModal from '../modals/city-choice-modal.vue';
import deliveryMap from '../modals/deliveryMap.vue';
import searchModal from '../modals/searchModal.vue';
import pageControls from './components/pageControls.vue';
import callbackModal from '../modals/callbackModal.vue';
import cartInvalidDataModal from '../modals/cartInvalidDataModal.vue';


const productPageEditForm = () => import('./components/productPageEditForm.vue')
const categoryNodeEditForm = () => import('./components/categoryNodeEditForm.vue')

var modalController = new Vue({
    name: 'modal-controller',
    el: '#modal-controller',
    store,
    data: {
    },
    components: {
        'purchase-modal': purchaseModal,
        'city-choice-modal': cityChoiceModal,
        'delivery-map': deliveryMap,
        'search-modal': searchModal,
        'page-controls': pageControls,
        'product-page-edit-form': productPageEditForm,
        'callback-modal': callbackModal,
        'category-node-edit-form': categoryNodeEditForm,
        'cart-invalid-data-modal': cartInvalidDataModal
    },
    computed: {
        purchaseModalIsActive() {
            return this.$store.state.showPurchaseModal.isShowModal;
        },
        cityChoiceModalIsActive() {
            return this.$store.state.showModalCityChoice.isShowModal;
        },
        deliveryMapIsActive() {
            return this.$store.state.deliveryMap.isShowModal;
        },
        searchModalIsActive() {
            return this.$store.state.showSearchModal.isShowModal;
        },
        pageControlsIsActive() {
            return this.$store.state.showPageControls.isShowModal;
        },
        productPageEditFormIsActive() {
            //return true
            return this.$store.state.showProductPageEditForm.isShowModal;
        },
        callbackModalIsActive() {
            return this.$store.state.showCallbackModal.isShowModal;
        },
        cartInvalidDataModalIsActive() {
            return this.$store.state.showCartInvalidData.isShowModal;
        }
    }
});