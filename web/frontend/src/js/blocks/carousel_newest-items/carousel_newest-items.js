import { Vue } from '../../vue.js';
import Carousel from '../carousel/Carousel.vue';
import Slide from '../carousel/Slide.vue';
import addedToCartModal from '../added-to-cart-modal/added-to-cart-modal.vue'
import store from '../../store'


var carouselNewestItems = new Vue({
    name: 'carousel',
    el: '#js-carousel-newest',
    store,
    data: {
        showAddedToCartModal: false,
        addedToCartName: "",
        addedToCartPrice: "",
        addedToCartImg: ""
    },
    components: {
        Carousel,
        Slide,
        'added-to-cart-modal': addedToCartModal
    },
    methods: {
        addProductToCart(offer_identifier, name, price, img) {
            // console.log('added');
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
        }
    }
});