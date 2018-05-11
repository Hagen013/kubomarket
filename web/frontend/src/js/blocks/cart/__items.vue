
<template>
    <div v-if="!isCartItemsDataReady" class="cart__content" :key="1">
        <div class="cart__rolling_icon icon icon_rolling ">
        </div>
    </div>
    <div v-else-if="isCartItemsDataNotEmpty" class="cart__content" :key="2">
        <h3 class="cart__block-title">У вас в корзине</h3>
        <div class="cart__items">
            <cartItem v-for="item in sortedCartItemsArray" :key="item.offer_identifier" 
            :offer_identifier="item.offer_identifier" 
            :name="item.name" 
            :url="item.url" 
            :image="item.image" 
            :init_quantity="item.quantity" 
            :price="item.price" 
            :total_price="item.total_price" 
            ></cartItem>
        </div>
        <div class="cart__total">
            <h3 class="cart__block-title">Итого</h3>
            <div class="cart__total-numbers">
                <div class="cart__total-price">
                    <div class="cart__total-price-caption">
                        К оплате:
                    </div>
                    <div class="cart__total-price-value">
                        {{ totalCartItemsPrice }} ₽
                    </div>
                    <div class="clearfix"></div>
                </div>
                <div class="cart__total-quantity">
                    <div class="cart__total-quantity-caption">
                        Всего товаров:
                    </div>
                    <div class="cart__total-quantity-value">
                        {{ totalCartItemsQuantity }} шт.
                    </div>
                    <div class="clearfix"></div>
                </div>
                <div class="clearfix"></div>
            </div>
            <div class="clearfix"></div>
        </div>
        <div @click="$emit('next')" class="button button_blue cart__proceed">
            Продолжить
        </div>
    </div>
    <div v-else class="cart__content" :key="3">
        <h1 class="cart__block-title">
            <center>
                <br>
                <br>
                <br> В вашей корзине пусто
                <br> и нам от этого грустно
                <br> =(
            </center>
        </h1>
    </div>
</template>

<script>
import Vue from 'vue'
import VueResource from 'vue-resource';
Vue.use(VueResource);

import cartItem from '../cart-item/cart-item.vue';
import store from '../../store'

export default {
    name: "cart-items",
    store,
    data: function () {
        return {}
    },
    components: {
        cartItem: cartItem,
    },
    props: [
        "isCartItemsDataReady",
        "isCartItemsDataNotEmpty",
        "sortedCartItemsArray",
        "totalCartItemsQuantity",
        "totalCartItemsPrice",
    ],
    computed: {
    },
    methods: {

    },
    mounted() {
    }
}
</script>














