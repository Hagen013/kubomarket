<template>
    <div class="content-area_mb cart__items-content-area"
        v-if="isCartItemsDataReady"
    >
        <div class="cart__content">
            <div class="cart__items-wrap">
                <div class="cart__title-area">
                    <div class="cart__subtitle">
                        Ваши товары
                    </div>
                    <div class="cart__items-clear"
                        @click="clear"
                    >
                        Удалить все 
                        <i class="icon icon_close"></i>
                    </div>
                </div>
                <div class="cart__items">
                    <cart-item v-for="item in sortedCartItemsArray" :key="item.offer_identifier" 
                    :offer_identifier="item.offer_identifier" 
                    :name="item.name" 
                    :url="item.url" 
                    :image="item.image" 
                    :init_quantity="item.quantity" 
                    :price="item.price" 
                    :total_price="item.total_price" 
                    v-on:cartitempost=cartitempost
                    v-on:cartitemdelete=cartitemdelete
                    >
                    </cart-item>
                </div>
                <div class="cart__summary">
                    <div class="cart__summary-quanity">
                        {{totalCartItemsDeepQuantity}} товаров(a)
                    </div>
                    <div class="cart__summary-price price">
                        {{totalCartItemsPrice}} ₽
                    </div>
                </div>
            </div>

            <div class="cart__delivery-wrap">
                <div class="cart__title-area">
                    <div class="cart__subtitle">
                        Оформление заказа
                    </div>
                </div>
                <div class="cart__delivery-content">
                    <div class="cart__personal-info">
                        <div class="cart__subtitle cart__personal-info-title">
                            Контактное лицо
                        </div>
                        <div class="cart__form">
                            <div class="cart__form-input-box">
                                <input class="input cart__input" placeholder="Имя">
                            </div>
                            <div class="cart__form-input-box">
                                <input class="input cart__input" placeholder="Почта">
                            </div>
                            <div class="cart__form-input-box">
                                <input class="input cart__input" placeholder="Телефон">
                            </div>
                        </div>
                    </div>
                    <delivery-menu
                        @selectDeliveryMod="selectDeliveryMod"

                        :isCartItemsDataReady="isCartItemsDataReady"
                        :isDeliveryDataReady="isDeliveryDataReady"
                        :isDeliveryAvailable="isDeliveryAvailable"
                        :isCurierAvailable="isCurierAvailable"
                        :isPostalServiceAvailable="isPostalServiceAvailable"
                        :isPointsAvailable="isPointsAvailable"
                        :isDeliveryModSelected="isDeliveryModSelected"
                        :isCartItemsDataNotEmpty="isCartItemsDataNotEmpty"
                        :deliveryData="deliveryData"
                        :cityName="cityName"
                        :customerAddress="customerAddress"
                        :selectedDeliveryMod="selectedDeliveryMod"
                        :selectedDeliveryPoint="selectedDeliveryPoint"
                    >
                    </delivery-menu>
                    <div class="cart__order-summary">
                        <div class="cart__order-summary-item">
                        </div>
                        <div class="cart__order-summary-item">
                        </div>
                        <div class="cart__order-total-price">
                        </div>
                    </div>
                    <div class="cart__submit-wrap">
                        <button class="button button_blue cart__submit-button">
                            ОФОРМИТЬ ЗАКАЗ
                        </button>
                    </div>
                </div>
            </div>

        </div>
    </div>
</template>

<script>
import store from '../../../store'

import cartItem from './cartItem.vue'
import deliveryMenu from './deliveryMenu.vue'
import deliveryPoints from './deliveryPoints.vue'
import yandexMap from '../../yandexMap/yandexMap.vue'


export default {
    name: 'cart',
    store,
    data: function () {
        return {

        }
    },
    components: {
        "cart-item": cartItem,
        "delivery-menu": deliveryMenu,
        "delivery-points": deliveryPoints
    },
    mounted() {

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
        // GEO
        isGeoDataInited() {
            return this.$store.state.geo.isDataInited;
        },
        isDeliveryRequestDataReady() {
            return (this.isCartItemsDataReady && this.isGeoDataInited)
        },
        // Доставка
        isDeliveryDataReady (){
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
        },
        selectDeliveryMod(mod, code="", type=""){
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
    },
    watch: {
        isDeliveryRequestDataReady() {
            if (this.isDeliveryRequestDataReady) {
                this.$store.dispatch('delivery/initDelivery');
            }
        }
    }
}
</script>