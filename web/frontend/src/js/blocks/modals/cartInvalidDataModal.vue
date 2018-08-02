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

            <div class="modal_text-only grey">
                Пожалуйста укажите номер телефона, чтобы мы могли связаться с Вами.
                <br>Для оформления заказа достаточно указать номер телефона
            </div>

        </div>
    </div>
</template>

<script>
import store from '../../store'

export default {
    name: 'cart-invalid-data-modal',
    store,
    data: () => ({
    }),
    methods: {
        hide() {
            this.$store.commit("showCartInvalidData/hide");
        }
    },
}

</script>
