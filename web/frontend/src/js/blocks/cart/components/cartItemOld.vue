<template>
    <div class="cart-item">
        <div class="cart-item__img-wrap">
            <a class="cart-item__link-overlay" :href="url">
                <img class="cart-item__img" :src="image">
            </a>
        </div>
        <div class="cart-item__info">
            <div class="cart-item__title-area">
                <div class="cart-item__name-wrap">
                    <a :href="url" class="cart-item__name">
                        {{name}}
                    </a>
                </div>
                <div class="cart-item__code-wrap">
                    <a :href="url" class="cart-item__code">
                        Артикул: {{offer_identifier.substr(34)}}
                    </a>
                </div>
            </div>
            <div class="cart-item__inc-zone">
                <div class="caounter cart-item__counter">
                    <div class="counter__button" @click="quantityMinus">-</div>
                    <div class="counter__input-box">
                        <input
                            type="text"
                            class="counter__input"
                            onkeypress='return event.charCode >= 48 && event.charCode <= 57'
                            v-model="quantity"
                            @change="quantityChange"
                            @keyup.enter="quantityChange"
                            @keyup.up="quantityPlus"
                            @keyup.down="quantityMinus"
                        >
                    </div>
                    <div class="counter__button" @click="quantityPlus">+</div>
                    <div class="clearfix"></div>
                </div>
            </div>
            <div class="cart-item__price-area">
                <transition name="fade">
                    <div class="cart-item__price-single" v-if="quantity > 1">
                        {{price}} <i class="icon icon_rouble"></i> × {{quantity}}
                    </div>
                </transition>
                <div class="price cart-item__price">
                    {{total_price}} <i class="icon icon_rouble"></i>
                </div>
                <div class="clearfix"></div>
            </div>
        </div>
        <div class="cart-item__close" @click="$parent.$emit('cartItemDelete', offer_identifier)"></div>
    </div>
</template>

<script>
import debounce from 'debounce'

export default {
    name: 'item',
    data: function () {
        return {
            quantity: 0,
        }
    },
    props: {
        offer_identifier: String,
        name: String,
        url: String,
        image: String,
        price: Number,
        init_quantity: Number,
        total_price: Number
    },
    mounted: function () {
        this.quantity = this.init_quantity;
    },
    methods: {
        changeQuantity: debounce(function () {
            this.$parent.$emit("cartItemPost",
                this.offer_identifier,
                this.quantity);
        }, 1000),
        quantityChange: function (newQuantity) {              
            if (this.quantity <= 0) this.quantity = 1;
            if (this.quantity > 1000) this.quantity = 1000;
            if (this.init_quantity != newQuantity) this.changeQuantity();
        },
        quantityMinus:function(){
            if(this.quantity>1){
                this.quantity-=1
                this.changeQuantity();
            }else{
                this.quantity=1;
            }
        },
        quantityPlus:function(){
            if(this.quantity<1000){
                this.quantity+=1
                this.changeQuantity();
            }else{
                this.quantity=1;
            }
        }
    },
    watch: {
        init_quantity: function(newQuantity){
            this.quantity = this.init_quantity;
        }
    }
}
</script>