<template>
    <div class="profile-data">
        <div class="profile-data__title bold">
            Мои данные
        </div>
        <div class="profile-data__delimeter">
        </div>
        <div class="profile-data__block">
            <div class="profile-data__fullname">
                <div class="input-box">
                    <input class="input"
                        placeholder="Имя"
                        v-model="customerName"
                    >
                </div>
                <div class="input-box">
                    <input class="input"
                        placeholder="Фамилия"
                        v-model="profile.surname"
                    >
                </div>
                <div class="input-box">
                    <input class="input"
                        placeholder="Отчество"
                        v-model="profile.patronymic"
                    >
                </div>
            </div>
            <div class="profile-data__email">
            </div>
            <div class="profile-data__password">
            </div>
        </div>
        <div class="profile-data__delimeter">
        </div>
        <div class="profile-data__block">
            <div class="profile-data__phone-wrap">
                <div class="input-box">
                    <masked-input
                        class="input"
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
                    <label class="input-box__placeholder"
                        for="input-phone"
                        v-if="customerPhone.length == 0 && !isCustomerPhoneFocused"
                    >
                        Телефон
                    </label>
                </div>
            </div>
        </div>
        <div class="profile-data__delimeter">
        </div>
        <div class="profile-data__block">
            <div class="profile-data__button button button_blue"
                @click="saveData"
            >
                СОХРАНИТЬ ДАННЫЕ
            </div>
        </div>
    </div>
</template>

<script>
import store from "../../../store";
import MaskedInput from 'vue-text-mask';

export default {
    name: "personal-data",
    store,
    data: () => ({
        usersApiUrl: "/api/users/",
        usersProfileApiUrl: "",
        isCustomerPhoneFocused: false
    }),
    components: {
        "masked-input": MaskedInput
    },
    props: [
        "profile"
    ],
    computed: {
        isValid() {
            return true
        },
        customerPhone: {
            get() {
                return this.$store.getters['customer/maskedPhone'];
            },
            set(value) {
                this.$store.commit('customer/maskedPhone', value)
            }
        },
        customerName: {
            get() {
                return this.$store.state.customer.name;
            },
            set(value) {
                this.$store.commit('customer/setData', {name:value})
            }
        },
        isCustomerPhoneValid() {
            return this.$store.getters["customer/isPhoneValid"];
        },
    },
    created() {
        this.initializeData();
    },
    methods: {
        initializeData() {
            this.usersProfileApiUrl = `${this.usersApiUrl}${this.profile.user_id}/profile/`; 
            if (this.customerName !== this.profile.name) {
                this.customerName = this.profile.name;
            }
            if (this.customerPhone !== this.profile.phone_number) {
                this.customerPhone = this.profile.phone_number;
            }
        },
        saveData() {
            if (this.isValid) {
                this.$http.put(this.usersProfileApiUrl, this.profile).then(
                    response => {
                        this.handleSuccessfulResponse(response);
                    },
                    response => {
                        this.handleFailedResponse(response);
                    }
                )
            }
        },
        handleSuccessfulResponse(response) {

        },
        handleFailedResponse(response) {

        }
    },
    watch: {
        customerPhone() {
            this.profile.phone_number = this.customerPhone;
        },
        customerName() {
            this.profile.name = this.customerName;
        }
    }
}
</script>