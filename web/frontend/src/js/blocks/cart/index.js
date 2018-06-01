import { Vue } from '../../vue.js'

import store from '../../store'

import cartItem from './components/cartItem.vue'


var Cart = new Vue({
    name: 'cart',
    el: '#cart',
    store,
    data: {

    },
    components: {
        "cart-item": cartItem
    },
    computed: {
        // Содержимое корзины
        isCartItemsDataReady() {
            return this.$store.state.cart.isDataInited;
        },
        isCartItemsDataNotEmpty() {
            return !this.$store.getters['cart/isCartEmpty'];
        },
        sortedCartItemsArray() {
            return this.$store.getters['cart/sortedItemsArray'];
        },
        totalCartItemsQuantity() {
            return this.$store.state.cart.items_quantiy;
        },
        totalCartItemsDeepQuantity() {
            let quantity = 0;
            if (this.isCartItemsDataReady !== true) {
                return quantity
            }
            for (let i=0; i<this.sortedCartItemsArray.length; i++) {
                quantity += this.sortedCartItemsArray[i].quantity;
            }
            return  quantity
        },
        totalCartItemsPrice() {
            return this.$store.state.cart.total_price;
        },
        // Доставка
        isDeliveryDataReady(){
            return this.$store.state.delivery.isDataInited;
        },
        deliveryData(){
            return this.$store.state.delivery.data;
        },
        isDeliveryModSelected(){
            return this.$store.state.delivery.isModSelected;
        },
        cityName(){
            return this.$store.state.geo.city;
        },
        isDeliveryAvailable(){
            return this.$store.getters['delivery/isAvailable'];
        },
        isCurierAvailable(){
            return this.$store.getters['delivery/isCurierAvailable'];
        },
        isPostalServiceAvailable(){
            return this.$store.getters['delivery/isPostalServiceAvailable'];
        },
        isPointsAvailable(){
            return this.$store.getters['delivery/isPointsAvailable'];
        },
        isCustomerDataValid() {
            return (
                (
                    // проверка на непустость корзины
                    !this.$store.getters['cart/isCartEmpty']
                ) && (
                    // проверка на валидность и существование телефона
                    this.$store.getters['customer/isPhoneValid']
                ) && (
                    // проверка на валидность мэйла или его отсутствие
                    (this.$store.state.customer.email.length == 0) ||
                    (
                        (this.$store.state.customer.email.length != 0) &&
                         this.$store.getters['customer/isEmailValid']
                    )
                )
            );
        },
        customerAddress(){
            return this.$store.state.customer.address;
        },
        selectedDeliveryMod(){
            return this.$store.state.delivery.mod;
        },
        selectedDeliveryPoint(){
            return this.$store.getters["delivery/curentSelectedPoint"];
        },
        // Вкладка оплаты
        selectedPaymentMod(){
            return this.$store.state.payment.mod;
        },
        // Заказ
        orderData(){
            return this.$store.getters['orderData']('cart');
        },
        ECProducts(){
            return this.sortedCartItemsArray.map(
                currentValue=>{
                    return{
                        id: currentValue.offer_identifier,
                        name: currentValue.name,
                        price: currentValue.price,
                        quantity: currentValue.quantity
                    }
                }
            );
        }
    },
    methods: {
        cartitempost(offer_identifier, quantity) {
            console.log("posting", offer_identifier);
            this.$store.dispatch('setQuantityInCart', { offer_identifier, quantity });
        },
        cartitemdelete(offer_identifier) {
            console.log("deleting"+offer_identifier);
            this.$store.dispatch('deleteFromCart', { offer_identifier });
        },
        clear() {
            this.$store.dispatch('clearCart');
        }
    }
});
