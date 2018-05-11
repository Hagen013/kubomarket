<template>
    <div class="content-area cart-wrapper">
        <div v-if="!isOrderSended" class="cart">
            <routing
            @selectTab="selectTab"
            :curent-tab-key="curentTabKey"
            id="js-routing"
            ></routing>
        <transition name="cart">

            <keep-alive>
                <component :is="curentComponent"
                @next="nextComponent" 
                @back="previousComponent" 
                
                @makeOrder="makeOrder"
                @cartItemDelete="cartItemDelete" 
                @cartItemPost="cartItemPost"

                @changeCustomerAddress="changeCustomerAddress"
                @selectDeliveryMod="selectDeliveryMod"

                @selectPaymentMod="selectPaymentMod"

                :isCartItemsDataReady="isCartItemsDataReady"                
                :isCartItemsDataNotEmpty="isCartItemsDataNotEmpty"
                :sortedCartItemsArray="sortedCartItemsArray"
                :totalCartItemsQuantity="totalCartItemsQuantity"
                :totalCartItemsPrice="totalCartItemsPrice"

                :isDeliveryDataReady="isDeliveryDataReady"
                :delivery-data="deliveryData"
                :isDeliveryModSelected="isDeliveryModSelected"
                :isDeliveryAvailable="isDeliveryAvailable"
                :isCurierAvailable="isCurierAvailable"
                :isPostalServiceAvailable="isPostalServiceAvailable"
                :isPointsAvailable="isPointsAvailable"
                :city-name="cityName"
                :customer-address="customerAddress"
                :selected-delivery-mod="selectedDeliveryMod"
                :selected-delivery-point="selectedDeliveryPoint"

                :selected-payment-mod="selectedPaymentMod"
                >
                </component>
            </keep-alive>
        </transition>

        </div>
        <div v-else class="cart">
            <div class="cart__content">
                <h2 class="cart__block-title">
                    Спасибо за заказ
                </h2>
                <p class="cart__text">
                    Мы благодарны вам за совершение заказа в интернет магазине
                    <a class="link link_market ">kubomarket.ru</a>.
                </p>
                <p class="cart__text">
                    В ближайшее время наши операторы свяжутся с вами.
                </p>
            </div>
        </div>
        <modal v-if="isShowNotValidModal" :title="'Недостаточно данных'" @close="isShowNotValidModal=false">
            <div style="color:#717c86">
                Для совершения заказа необходимо:
                <ul style="padding-left:10px;">
                    <li style="padding:5px 0px;">
                        1. Иметь хотя бы 1 товар в корзине;
                    </li>
                    <li>
                        2. Ввести свой номер телефона на вкладке "Доставка";
                    </li>
                </ul>
                <br> Если вы всё же указали номер телефона или почту, то проверьте их на корректность.
                <br>
            </div>
        </modal>
    </div>
</template>


<script>
import { Vue } from '../../vue.js';

import debounce from 'debounce';
import modal from '../../core/modal.vue'

import store from '../../store'

import routing from './__routing.vue'

import cartItems from './__items.vue'
import cartDelivery from './__delivery.vue'
import cartPayment from './__payment.vue'

export default {
    name: 'cart',
    store,
    data: function () {
        return {
            curentTabKey: 0,
            isOrderSended: false,
            isShowNotValidModal: false,
            isCartSubmissionInProgress: false,
        }
    },
    components: {
        routing: routing,
        cartItems: cartItems,
        cartDelivery: cartDelivery,
        cartPayment: cartPayment,
        modal: modal,
    },
    mounted() {
        // if (!this.$store.state.cart.items.isDataInited) {
        //     this.$store.dispatch('cart/items/syncCart');
        // }else{
        //     if (this.isGeoDataReady){
        //         //если гео не инит то должен заинититься в 
        //         // хедере и дёрнуть потом вотчер в этом классе
        //         this.getDeliveryData();
        //     }
        // }
    },
    computed: {
        // Текущий компонент для роутинга
        curentComponent() {
            return [
                "cartItems",
                "cartDelivery",
                "cartPayment"
            ][this.curentTabKey];
        },
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
        // Роутинг
        selectTab(key){
            this.curentTabKey=key;
        },
        nextComponent() {
            let routingElem = $("#js-routing")
            let docViewTop = $(window).scrollTop();
            let docViewBottom = docViewTop + $(window).height();

            let elemTop = routingElem.offset().top;
            let elemBottom = elemTop + routingElem.height();

            let isScrolledIntoView  = ((elemBottom <= docViewBottom) && (elemTop >= docViewTop));
            if (!isScrolledIntoView) {
                $('html, body').animate({
                    scrollTop: $("#js-routing").offset().top
                }, 300);
            }
            // $("#js-routing").offset().top - $(window).scrollTop();

            return this.curentTabKey+=1;
        },
        previousComponent() {
            return this.curentTabKey-=1;
        },
        // Вкладка Корзины
        cartItemDelete(offer_identifier) {
            console.log(offer_identifier);
            this.$store.dispatch('deleteFromCart', { offer_identifier });
        },
        cartItemPost(offer_identifier, quantity) {
            //console.log(offer_identifier);
            this.$store.dispatch('setQuantityInCart', { offer_identifier, quantity });
        },
        // Вкладка Доставки
        changeCustomerAddress(payload){
            this.$store.commit('customer/setAddress', payload);
        },
        selectDeliveryMod(mod, code="", type=""){
            // console.log(mod)
            if (mod == ''){
                this.$store.commit('delivery/clearMod');
            } else if (mod == 'curier') {
                this.$store.commit('delivery/selectCurierMod');
            } else if (mod == 'delivery_points') {
                this.$store.commit('delivery/selectDeliveryPointsMod', {code, type});
                // console.log(code, type);
            } else if (mod == 'postal_service') {
                this.$store.commit('delivery/selectPostalServiceMod');
            }
        },
        selectPaymentMod(mod){
            this.$store.commit("payment/set_mod", mod);
        },
        // Вкладка оплаты
        makeOrder() {
            if (this.isCustomerDataValid) {
                if(!this.isCartSubmissionInProgress){
                    this.isCartSubmissionInProgress = true;
    
                    this.$http.post('/api/cart/make_order/', this.orderData).then(
                        response => {
                            // колбэк на успех
                            this.isOrderSended = true;
                            this.isCartSubmissionInProgress = false;
                            // Google Analytics
                            dataLayer.push({'event': 'zakaz_send'});
                            // GM
                            dataLayer.push({'event': 'make_order',
                                            'ecommerce': {
                                                'purchase': {
                                                    'actionField': {
                                                        'id': Math.random().toString(36).slice(2)
                                                    },
                                                    'products': this.ECProducts
                                                }
                                            }
                            });
                            // YM
                            yaCounter46971201.reachGoal('zakaz_send');
                            this.$store.commit('cart/clearData');
                            this.$store.commit('delivery/clearData');
                            this.$store.commit('delivery/clearMod');
                            //this.$store.dispatch('cart/items/syncCart');
                            debounce(function () {
                                window.location.replace("/");
                                },
                                5000
                            )();
                        },
                        response => {
                            this.isCartSubmissionInProgress = false;
                            // колбэк на ошибку
                            console.error(
                                `Ошибка принятия заказа sendOrder
                                ${response.data}
                            `);

                            // console.log(orderData);
                            // console.log(response.body);
                            // console.log(response.code);
                        },
                    );
                };

            } else {
                this.isShowNotValidModal = true;
            }
        },
    },
}
</script>