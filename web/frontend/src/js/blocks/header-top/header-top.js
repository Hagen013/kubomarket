import { Vue } from '../../vue.js';

import { mapState } from 'vuex'

import cityChoiceModal from './__city-choice-modal.vue'
import modalCallback from './__modal-callback.vue'

import store from '../../store'

var headerTop = new Vue({
    name: 'header-top',
    el: '#js-header-top',
    store,
    data:{
        isMounted:false,
        isShowModalCallback: false,
    },
    props: [
        'productData'
    ],
    mounted: function(){
        // if(!this.$store.state.cart.items.isDataInited){
        //     // console.log('Инициализация корзины в хедертопе', this.$store.state.cart.items.isDataInited);
        //     this.$store.dispatch('cart/items/syncCart');
        // }
        // if(!this.$store.state.geo.isGeoInited){
        //     // console.log('Инициализация карты в хедертопе');
        //     this.$store.dispatch('geo/initGeo');
        // }
        this.isMounted=true; 
    },
    computed: {
        // isShowModalCallback () {
        //     return this.$store.state.showModalCallback.isShowModal
        // },
        isShowModalCityChoice(){
            return this.$store.state.showModalCityChoice.isShowModal;
        },
        isCartReady(){
            return this.$store.state.cart.isDataInited;            
        },
        cartTotalQuantity(){
             return this.$store.state.cart.items_quantiy;
        },
        isGeoReady(){
            return this.$store.state.geo.isDataInited;
        },
        cityName() {
            //let result = this.$store.state.kladr.city;
            return this.$store.state.geo.city;
        },
        phoneNumber() {
            let kladrCode;
            if(this.cityCode){
                kladrCode = this.cityCode.slice(0,2);
            }
            // console.log(kladrCode);
            return {
                "77" : "+7(495)668-09-85", // Москвы, 
                "78" : "+7(812)309-84-63", // Питера, 
                "23" : "+7(861)203-45-69", // Краснодара, 
                "66" : "+7(343)318-24-95", // Екатеринбург, 
                "54" : "+7(383)280-43-71", // Новосибирск, 
                "52" : "+7(831)429-17-47"  // Нижний Новгород, 
            }[kladrCode] || "8 (800) 200-7456";
        }
    },
    components: {
        'modal-callback': modalCallback,
        'city-choice-modal': cityChoiceModal
    },
    methods: {
        hideModalCallback() {
            this.isShowModalCallback = false;
            // this.$store.commit('showModalCallback/hide');
        },
        showModalCallback() {
            this.isShowModalCallback = true;
        },
        hideModalCityChoice() {
            this.$store.commit('showModalCityChoice/hide');
        },
        showModalCityChoice() {
            this.$store.commit('showModalCityChoice/show');
        },
    }
});