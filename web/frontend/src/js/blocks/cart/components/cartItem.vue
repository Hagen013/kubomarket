<template>
    <div class="cart-item">
        <div class="cart-item__content">
            <a class="cart-item__img-wrap" :href="url">
                <img class="cart-item__img" :src="image">
            </a>
            <div class="cart-item__name-wrap">
                <a :href="url" class="cart-item__name">
                    {{name}}
                </a>
            </div>
            <div class="cart-item__purchase-info">
                <div class="cart-item__interaction-area">
                    <div class="cart-item__counter-button cart-item__counter-button_dec"
                        @click="quantityMinus"
                    >
                        -
                    </div>
                    <div class="cart-item__input-box">
                        <input class="input cart-item__input"
                            type="text"
                            onkeypress='return event.charCode >= 48 && event.charCode <= 57'
                            v-model="quantity"
                            @change="quantityChange"
                            @keyup.enter="quantityChange"
                            @keyup.up="quantityPlus"
                            @keyup.down="quantityMinus"
                        >
                    </div>
                    <div class="cart-item__counter-button cart-item__counter-button_inc"
                        @click="quantityPlus"
                    >
                        +
                    </div>
                </div>
                <div class="cart-item__price">
                    {{total_price}} ₽
                </div>
            </div>
            <div class="cart-item__delete"
                @click="$emit('cartitemdelete', offer_identifier)"
            >
                <i class="icon icon_close"></i>
            </div>
        </div>
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
            this.$emit("cartitempost",
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