<template>
    <div class="modal"
        @click.self="hide"
    >
        <div class="modal__content">

            <div class="purchase-modal__close button_round"
                @click="hide"
            >
                <i class="icon icon_close"></i>
            </div>

            <div class="modal_content-inner">
                <div class="modal__title">
                    {{title}}
                </div>

                <div class="input-box modal__input-box"
                    v-if="!responseRecieved"
                >
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
                <div class="input-box modal__input-box"
                    v-if="!responseRecieved"
                >
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

                <div class="modal__product-sm">
                    <p class="modal__product-title-sm bold">
                        {{name}}
                    </p>
                    <div class="modal___product-img-sm-wrap">
                        <img :src="img">
                    </div>
                </div>

                <p class="grey modal__text">В ближайшее время с вами свяжется оператор для уточнения заказа</p>

                <div class="button button_blue"
                    @click="submit"
                    v-if="!responseRecieved"
                >
                    Оставить заявку
                </div>

            </div>
        </div>
    </div>
</template>

<script>
import MaskedInput from 'vue-text-mask';
import getCookie from './../../core/getCookie'

import store from '../../store'

export default {
    name: 'callback-modal',
    components: {
        "masked-input": MaskedInput
    },
    store,
    data: () => ({
        title: "Обратный звонок",
        isCustomerPhoneFocused: false,
        isCustomerNameFocused: false,
        apiUrl: '/api/cart/make_order/',
        responseAwaiting: false,
        responseRecieved: false,
        responseFailed: false,
        recievedOrderData: null
    }),
    props: [
        "name",
        "price",
        "img",
        "productData"
    ],
    methods: {
        submit() {
            if (!this.responseAwaiting) {
                this.responseAwaiting = true;
                let source = this.productData !== undefined ? 'callback' : 'product-page';
                let data = this.$store.getters['orderData'](source);
                let admitadCookie = getCookie("tagtag_aid");
                if ( admitadCookie !== undefined) {
                    data['cpa'] = {'networks': ['admitad',]}
                }
                this.$http.put(`/api/cart/items/${this.productData.id}/`).then(
                    response => {
                        this.$http.post(
                            this.apiUrl,
                            data
                        ).then(
                            response => {
                                this.handleSuccessfulResponse(response);
                            },
                            response => {
                                this.handleFailedResponse(response);
                            }
                        )
                    },
                    response => {

                    }
                )
            }
        },
        addToCart() {
            this.$http.put(`/api/cart/items/${this.productData.id}`).then(
                response => {

                },
                response => {

                }
            )
        },
        handleSuccessfulResponse(response) {
            this.title = "Заявка отправлена";
            this.responseAwaiting = false;
            this.responseRecieved = true;
            this.recievedOrderData = response.body;
            // Google analytics and Yandex.Metrika
            dataLayer.push({"event": "callBack"});
            yaCounter49316458.reachGoal("callBack");
            if (this.productData !== undefined) {
                dataLayer.push({
                    "event": "orderConfirmed",
                    "ecommerce": {
                        "currencyCode": "RUB",
                        "purchase": {
                            "actionField": {
                                "id": this.recievedOrderData.id
                            },
                            "products": [
                                this.productData
                            ]
                        }
                    }
                });
            }
            if (this.recievedOrderData['cpa'] !== undefined) {
                this.handleCPA(this.recievedOrderData['cpa']);
            }
        },
        handleFailedResponse(response) {
            this.title = "Сервер временно недоступен"
            this.responseAwaiting = false;
            this.responseRecieved = true;
            this.responseFailed = true;
        },
        hide() {
            this.$store.commit("showCallbackModal/hide");
        },
        handleCPA(data) {
            ADMITAD = window.ADMITAD || {};
            ADMITAD.Invoice = ADMITAD.Invoice || {};
            ADMITAD.Invoice.broker = "adm";     // параметр дедупликации (по умолчанию для admitad)
            ADMITAD.Invoice.category = "1";
            
            let orderedItem = [];

            for (let key in this.recievedOrderData.data.cart.items) {
                let item = this.recievedOrderData.data.cart.items[key];
                orderedItem.push({
                    Product: {
                        productID: item.vendor_code,
                        category: '1',
                        price: item.price,
                        priceCurrency: 'RUB'
                    },
                    orderQuantity: item.quantity,
                    additionalType: 'sale'
                })
            }

            ADMITAD.Invoice.referencesOrder = ADMITAD.Invoice.referencesOrder || [];

            ADMITAD.Invoice.referencesOrder.push({
                orderNumber: this.recievedOrderData.public_id,
                orderedItem: orderedItem
            });

            ADMITAD.Tracking.processPositions();

        }
    },
    computed: {
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
        isCustomerPhoneValid() {
            return this.$store.getters["customer/isPhoneValid"];
        },
    },
}

</script>
