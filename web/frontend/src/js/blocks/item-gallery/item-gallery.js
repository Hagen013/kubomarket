import Vue from 'vue'
import VueResource from 'vue-resource';
Vue.use(VueResource);

import store from '../../store'
import addedToCartModal from '../added-to-cart-modal/added-to-cart-modal.vue'


var ItemGallery = new Vue({
    name: 'item-gallery',
    el: '#js-item-gallery',
    store,
    data: {
        showAddedToCartModal: false,
        addedToCartName: "",
        addedToCartPrice: "",
        addedToCartImg: ""
    },
    computed: {},
    components: {
        'added-to-cart-modal': addedToCartModal
    },
    methods: {
        addProductToCart(offer_identifier, name, price, img) {
            this.addedToCartName = name;
            this.addedToCartPrice = price;
            this.addedToCartImg = img;
            this.$http.put(
                `/api/cart/items/${offer_identifier}/`)
                .then(response => {
                    this.showAddedToCartModal = true;
                    this.$store.dispatch('cart/items/syncCart');
                }, response=>{
                    //error callback
                    // console.log('error in addProductToCart - put');
                });
        },
        addToFavorite(offer_identifier, name, price, img) {
            // console.log('Added to favorites');
            let payload = {offer_identifier: offer_identifier}
            this.$store.commit('favorites/addItem', payload);
        },
        addToCompare(offer_identifier, name, price, img) {
            // console.log('Added to compare');
        }
    }
});