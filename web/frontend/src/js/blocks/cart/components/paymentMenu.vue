<template>
    <div class="payment-menu__wrap">
        <div class="payment-menu__title bold">
            Способ оплаты:
        </div>
        <div class="payment-menu">
            <div class="payment-menu__option"
                @click="changePaymentMethod('cash')"
                :class="{ paymentMenu__option_active : mode == 'cash' }"
            >
                <div>
                    Наличными
                </div>
                <div class="green bold">
                    при получении
                </div>
            </div>
            <div class="payment-menu__option"
                @click="changePaymentMethod('card_on_receipt')"
                :class="{ paymentMenu__option_active : mode == 'card_on_receipt' }"
            >
                <div>
                    Картой
                </div>
                <div class="green bold">
                    при получении
                </div>
            </div>
            <div class="payment-menu__option"
                :class="{ paymentMenu__option_active : mode == 'card' }"
            >
                <div>
                    Картой онлайн
                </div>
                <div class="bold">
                    недоступно
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "payment-menu",
    data: () => ({
    }),
    props: [
        "mode"
    ],
    methods: {
        changePaymentMethod(method) {
            this.$emit('changePaymentMethod', method)
        }
    },
}
</script>
