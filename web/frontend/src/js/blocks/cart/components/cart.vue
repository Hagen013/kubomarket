<template>
    <div class="content-area_mb cart__items-content-area"
        v-if="showCart"
    >
        <div class="cart__content" v-if="showOrderForm">
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
                            <div class="input-box cart__form-input-box">
                                <input class="input cart__input"
                                    id="input-name"
                                    v-model="customerName" 
                                    :class="{input_success: customerName.length != 0}"
                                    @focus="isCustomerNameFocused = true"
                                    @blur="isCustomerNameFocused = false"
                                    autocomplete="name"
                                >
                                <label class="input-box__placeholder"
                                    for="input-phone"
                                    v-if="this.customerName.length == 0 && !isCustomerNameFocused"
                                >
                                    Имя
                                </label>
                            </div>
                            <div class="input-box cart__form-input-box">
                                <input class="input cart__input"
                                    placeholder="Почта"
                                    type="email"
                                    v-model="customerEmail" 
                                    :class="{
                                             'input_success':customerEmail.length != 0 && isCustomerEmailValid, 
                                             'input_failure':customerEmail.length != 0 && !isCustomerEmailValid
                                            }"
                                    autocomplete="email"
                                >
                            </div>
                            <div class="input-box cart__form-input-box">
                                <masked-input
                                    class="input cart__input"
                                    type="tel"
                                    id="input-phone"
                                    :class="{
                                             'input_success':customerPhone.length != 0 && isCustomerPhoneValid, 
                                             'input_failure':customerPhone.length != 0 && !isCustomerPhoneValid
                                            }" 
                                    for="input-phone"
                                    v-model="customerPhone"
                                    @focus="isCustomerPhoneFocused = true"
                                    @blur="isCustomerPhoneFocused = false"
                                    :showMask="isCustomerPhoneFocused"
                                    :mask="['+', '7',' ','(', /\d/, /\d/, /\d/, ')', ' ', /\d/, /\d/, /\d/, '-', /\d/, /\d/, /\d/, /\d/]"
                                />
                                <label class="input-box__placeholder input-box__placeholder_required"
                                    for="input-phone"
                                    v-if="customerPhone.length == 0 && !isCustomerPhoneFocused"
                                >
                                    Телефон
                                </label>
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
                        <button class="button button_blue cart__submit-button"
                            :disabled="!isCustomerDataValid"
                            @click="makeOrder"
                            :class="{ button_disabled : !isCustomerDataValid }"
                        >
                            ОФОРМИТЬ ЗАКАЗ
                        </button>
                    </div>
                </div>
            </div>

        </div>


        <div class="cart__successful-order" v-else-if="showAftercheck">
            <h2>Спасибо за заказ!</h2>
            <p>В ближайшее время с Вами свяжется оператор интернет-магазина для подверждения заказа</p>
            <div class="aftercheck-list">

                <div class="aftercheck-item">
                    <div class="aftercheck-name">
                        Номер вашего заказа:
                    </div>
                    <div class="aftercheck-value">
                        {{recievedOrderData.id}}
                    </div>
                </div>

                <div class="aftercheck-item">
                    <div class="aftercheck-name">
                        Количество товаров:
                    </div>
                    <div class="aftercheck-value">
                        {{calulatedOrderItemsQuantity}}
                    </div>
                </div>

                <div class="aftercheck-item">
                    <div class="aftercheck-name">
                        Стоимость товаров:
                    </div>
                    <div class="aftercheck-value">
                        {{recievedOrderData.data.cart.total_price}} ₽
                    </div>
                </div>

                <div class="aftercheck-item">
                    <div class="aftercheck-name">
                        Стоимость доставки:
                    </div>
                    <div class="aftercheck-value"
                        v-if="recievedOrderData.data.delivery.is_mod_selected === false"
                    >
                        способ не выбран
                    </div>
                    <div class="aftercheck-value"
                        v-else-if="recievedOrderData.data.delivery.mod.pirce === null"
                    >
                        будет уточнена при звонке
                    </div>
                    <div class="aftercheck-value"
                        v-else
                    >
                        {{recievedOrderData.data.delivery.mod.price}}
                    </div>
                </div>

                <div class="aftercheck-item aftercheck-item_all">
                    <div class="aftercheck-name">
                        Сумма к оплате:
                    </div>
                    <div class="aftercheck-value">
                        {{calculatedOrderCombinedPrice}} ₽
                    </div>
                </div>

                <div class="aftercheck-text">
                </div>

            </div>
        </div>

        <div class="cart__placeholder" v-else>
            <div class="cart-placeholder-img-wrap">
                <img src="/static/img/icon/monkey.svg">
            </div>
            <p>В вашей корзине пока ничего нет и, от этого нам грустно</p>
        </div>

    </div>
    
</template>

<script>
import MaskedInput from 'vue-text-mask';

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
            isCustomerNameFocused: false,
            isCustomerPhoneFocused: false,
            isCustomerEmailFocused: false,
            isOrderSended: false,
            isCartSubmissionInProgress: false,
            recievedOrderData: null,
        }
    },
    components: {
        "cart-item": cartItem,
        "delivery-menu": deliveryMenu,
        "delivery-points": deliveryPoints,
        "masked-input": MaskedInput
    },
    mounted() {
    },
    computed: {
        // Отображаемые формы и данные
        showCart() {
            return ( this.isCartItemsDataReady || this.isOrderSended )
        },
        showOrderForm() {
            return ( (!this.isOrderSended) && (this.isCartItemsDataNotEmpty) )
        },
        showAftercheck() {
            return this.isOrderSended
        },
        // Данные пользователя
        customerName: {
            get() {
                return this.$store.state.customer.name;
            },
            set(value) {
                this.$store.commit('customer/setData', {name:value})
            }
        },
        customerPhone: {
            get() {
                return this.$store.getters['customer/maskedPhone'];
            },
            set(value) {
                this.$store.commit('customer/maskedPhone', value)
            }
        },
        customerEmail: {
            get() {
                return this.$store.state.customer.email;
            },
            set(value) {
                this.$store.commit('customer/setData', {email:value})
            }
        },
        customerAddress: {
            get() {
                return this.$store.state.customer.address
            },
            set(value) {
                this.$store.commit('customer/setData', {address:value})
            }
        },
        // Данные полученные по API
        calulatedOrderItemsQuantity() {
            let totalQuanity = null;
            if (this.isOrderSended) {
                totalQuanity = 0;
                for (let item in this.recievedOrderData.data.cart.items) {
                    totalQuanity += this.recievedOrderData.data.cart.items[item].quantity;
                }
            }
            return totalQuanity
        },
        calculatedOrderCombinedPrice() {
            if (this.isOrderSended) {
                if (this.recievedOrderData.data.delivery.mod.price !== null) {
                    return (this.recievedOrderData.data.cart.total_price + this.recievedOrderData.data.delivery.mod.price)
                } else {
                    return this.recievedOrderData.data.cart.total_price
                }
            }
            return null
        },
        // ДАННЫЕ ДОСТАВКИ
        deliveryInfo() {
            if ((this.isDeliveryDataReady && this.isDeliveryAvailable)) {
                let data = this.deliveryData[['curier','delivery_point', 'postal_service'][this.curentTabKey]]
                return {
                    "mod": ["Доставка курьером", "Доставка в пункт выдачи", "Доставка Почтой России"][this.curentTabKey],
                    "isSelected": this.isDeliveryModSelected,
                    "price": this.selectedDeliveryMod.price,
                    "time": (this.isDeliveryModSelected && this.selectedDeliveryMod.type=="delivery_points") ? [this.selectedDeliveryPoint.time_min, this.selectedDeliveryPoint.time_max] : data === null ? null : [data.time_min, data.time_max],
                    "pointType": (this.isDeliveryModSelected && this.selectedDeliveryMod.type=="delivery_points") ? {"pick_point_point":" ПикПоинт", "sdek_point":" СДЕК"}[this.selectedDeliveryMod.code.split("__")[1]] : "",
                    "pointAddress": (this.curentTabKey==1 && this.selectedDeliveryPoint !== undefined) ? this.selectedDeliveryPoint.address: null,
                    "pointDescription": (this.curentTabKey==1 && this.selectedDeliveryPoint !== undefined) ? this.selectedDeliveryPoint.description: null
                }
            }  else {
                return undefined;
            }
        },
        isCustomerPhoneValid() {
            return this.$store.getters["customer/isPhoneValid"];
        },
        isCustomerEmailValid() {
            return this.$store.getters["customer/isEmailValid"];
        },
        isValidEmail() {
            return this.$store.getters["orders/customer/isValidEmail"];
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
        makeOrder() {
            if (this.isCustomerDataValid) {
                if (!this.isCartSubmissionInProgress) {
                    this.isCartSubmissionInProgress = true;
                    this.postOrder();
                };
            } else {
                this.isShowNotValidModal = true;
            }
        },
        postOrder() {
            this.$http.post('/api/cart/make_order/', this.orderData).then(
                response => {
                    this.handleSuccessfulPostOrderRequest(response);
                },
                response => {
                    this.handleFailedPostOrderRequest(response);
                },
            );
        },
        handleSuccessfulPostOrderRequest(response) {
            this.recievedOrderData = response.body;
            this.isOrderSended = true;
            this.isCartSubmissionInProgress = false;
            this.$store.commit('cart/clearData');
            this.$store.commit('delivery/clearData');
            this.$store.commit('delivery/clearMod');
        },
        handleFailedPostOrderRequest(response) {
            this.isCartSubmissionInProgress = false;
        }
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