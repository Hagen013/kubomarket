<template>
    <div class="modal"
        @click.self="$emit('close')"
    >
        <div class="modal__content">
            <div class="purchase-modal__close button_round"
                @click="$emit('close')"
            >
                <i class="icon icon_close"></i>
            </div>
            <div class="purchase-modal__title">
                Товар добавлен в корзину
            </div>
            <div class="purchase-modal__offer-content">
                <div class="purchase-modal__img-wrap">
                    <img class="purchase-modal__img" :src="img">
                </div>
                <div class="purchase-modal__name">
                    {{name}}
                </div>
                <div class="purchase-modal__price price">
                    {{price}} ₽
                </div>
            </div>
            <div class="purchase-modal__controls">
                <div class="purchase-modal__continue button purchase-modal__button"
                    @click="$emit('close')"
                >
                    Продолжить покупки
                </div>
                <a class="purchase-modal__make-order button purchase-modal__button" 
                    href="/cart/"
                >
                    Оформить заказ
                </a>
            </div>
        </div>
    </div>
</template>

<script>
import MaskedInput from 'vue-masked-input'

export default {
    name: 'added-to-cart-modal',
    data: function () {
        return {}
    },
    props: [
        'img',
        'price',
        'name'
    ],
    methods: {

    },
    components: {
    }
}

</script>
