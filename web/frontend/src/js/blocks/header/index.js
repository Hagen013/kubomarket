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
        },
        isShowModalCityChoice(){
            return this.$store.state.showModalCityChoice.isShowModal;
        },
        isCartReady(){
            return this.$store.state.cart.isDataInited;            
        },
        cartTotalQuantity(){
             return this.$store.state.cart.items_quantiy;
        },
        isGeoReady() {
            return this.$store.state.geo.isDataInited;
        },
        cityName() {
            return this.$store.state.geo.city;
        },
    },
    methods: {
        showMobileMenu() {
            this.$store.commit("mobileMenu/show");
        },
        hideCityChoiceModal() {
            this.$store.commit('showModalCityChoice/hide');
        },
        showCityChoiceModal() {
            this.$store.commit('showModalCityChoice/show');
        },
    }
});
