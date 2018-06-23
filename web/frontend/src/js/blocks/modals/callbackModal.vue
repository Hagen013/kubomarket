<template>
    <div class="modal"
        @click.self="$emit('close')"
    >
        <div class="modal__content">
    
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
</template>

<script>
import MaskedInput from 'vue-masked-input'

export default {
    name: 'callback-modal',
    data: () => ({
        isCustomerPhoneFocused: false,
    }),
    props: [
    ],
    methods: {

    },
    computed: {
        customerPhone: {
            get() {
                return this.$store.getters['customer/maskedPhone'];
            },
            set(value) {
                this.$store.commit('customer/maskedPhone', value)
            }
        },
    },
    components: {
    }
}

</script>
