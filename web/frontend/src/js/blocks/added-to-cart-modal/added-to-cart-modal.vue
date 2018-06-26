<template>
    <modal @close="$emit('close')" 
            title="Товар добавлен в корзину" 
            :sizesStyleName="'added-to-cart-modal__content'">
        <div>
            <div class="float-item added-to-cart-modal__left-ancor">
                <img :src="img" alt="вы добавили корзину" class="added-to-cart-modal__img">
            </div>
    
            <div class="float-item added-to-cart-modal__right-ancor">
                <div class="added-to-cart-modal__name">{{name}}</div>
                <div class="price added-to-cart-modal__price">{{price}} ₽</div>
                <div class="added-to-cart-modal__button-wrap">
                    <a class="button button_blue added-to-cart-modal__button float-item" href="/cart/">Оформить заказ</a>
                    <a class="button button_blue added-to-cart-modal__button added-to-cart-modal__button_last float-item " @click="$emit('close')">Продолжить покупки</a>
                    <div class="clearfix"></div>
                </div>
            </div>
            <div class="clearfix"></div>
        </div>
    </modal>
</template>

<script>
import modal from '../../core/modal.vue'

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
        'modal': modal,
    }
}

</script>
