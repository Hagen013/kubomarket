<template>
  <modal @close="$emit('close')" :title="title">
    <transition name="fade">
      <div v-if="!isOrderSended" style="height: 160px;">
        <masked-input class="input modal__raw" type="tel"
        :class="{'input_success':customerPhone.length != 0 && isCustomerPhoneValid, 
                 'input_failure':customerPhone.length != 0 && !isCustomerPhoneValid}" 
        v-model="customerPhone"
        placeholder="Телефон" 
        @focus="isCustomerPhoneFocused = true"
        @blur="isCustomerPhoneFocused = false"
        :showMask="isCustomerPhoneFocused"
        :mask="['+', '7',' ','(', /\d/, /\d/, /\d/, ')', ' ', /\d/, /\d/, /\d/, '-', /\d/, /\d/, /\d/, /\d/]"
        />
      
        <input class="input modal__raw"
        placeholder="Ваше имя"
        v-model="customerName" 
        :class="{input_success: customerName.length != 0}" 
        @focus="isCustomerNameFocused = true"
        @blur="isCustomerNameFocused = false"
        />
        <button class="button button_blue button_long bold" @click="sendOrder">Отправить заявку</button>
      </div>
      <div v-else style="height: 160px;">
        <p class="bold modal__raw" style="height: 10px">
          Ваша заявка принята.
        </p>
        <p class="modal__raw" style="height: 70px;">
          Мы свяжемся с вами в ближайшее время.
        </p>
        <button class="button button_green button_long bold" @click="$emit('close')">Ок</button>

      </div>
    </transition>
  </modal>
</template>

<script>

import { Vue } from '../../vue.js';

import store from '../../store'

import modal from '../../core/modal.vue'
import MaskedInput from 'vue-text-mask';

export default {
  name: 'modal-callback',
  store,
  props: {
    'productData': Object
  },
  data: function () {
    return {
      isCustomerNameFocused: false,
      isCustomerPhoneFocused: false,
      isOrderSended: false,
      isSendingInProgress: false,
      title: "Обратный звонок"
    }
  },
  methods: {
    sendOrder() {
      if(!this.isSendingInProgress){
        this.isSendingInProgress = true;
        let sourse = this.productData !== undefined ? 'callback' : 'product-page';
        this.$http.post(
          '/api/cart/make_order/', 
          this.$store.getters['orderData'](sourse)
        ).then(
          response => {
            this.title = "Спасибо за заявку";
            this.isSendingInProgress = false;
            this.isOrderSended = true;
            // Google Analytics
            dataLayer.push({'event': 'zvonok'});
            // EC
            if (this.productData !== undefined) {
                dataLayer.push({
                  "event": "make_order",
                  "ecommerce": {
                    "purchase": {
                      "actionField": {
                          "id": Math.random().toString(36).slice(2)
                      },
                      "products": [
                        this.productData
                      ]
                    }
                  }
                });
            }

            // YA
            yaCounter46971201.reachGoal('zvonok');
          },
          response => {
            console.error(`Ошибка при отправке обратного звонка ${response.text}`)
            this.title = "Сервер недоступен =("
            this.isSendingInProgress = false;
            this.isSendingInProgress = false;
          },
        );
      }
    },
  },
  computed: {
    customerName: {
      get(){
          return this.$store.state.customer.name;
      },
      set(value) {
          this.$store.commit('customer/setData', {name:value})
      }
    },
    customerPhone: {
      get(){
          return this.$store.getters['customer/maskedPhone'];
      },
      set(value) {
          this.$store.commit('customer/maskedPhone', value)
      }
    },
    isCustomerPhoneValid() {
        return this.$store.getters["customer/isPhoneValid"];
    }
  },
  components: {
    'modal': modal,
    'MaskedInput': MaskedInput
  }
}

</script>