<template>
  <div class="cart__content">
        <h3 class="cart__block-title">
            Выберите способ оплаты
        </h3>
        <!-- LIST -->
        <div class="cart-payment__wrap">
            <div class="cart-payment__list float-item">
                <div class="cart-payment__list-item"
                :class="{cartPayment__listItem_selected:(selectedPaymentMod=='cash')}"
                @click="$emit('selectPaymentMod','cash')"
                >
                    <div class="cart-payment__list-item-selection"></div> 
                    Наличными при получении
                </div>
                <div class="cart-payment__list-item"
                :class="{cartPayment__listItem_selected:(selectedPaymentMod=='card_upon_receipt')}"
                @click="$emit('selectPaymentMod','card_upon_receipt')"
                >
                    <div class="cart-payment__list-item-selection"></div> 
                    Банковской картой при получении
                </div>
                <div class="cart-payment__list-item"
                :class="{cartPayment__listItem_selected:(selectedPaymentMod=='card')}"
                @click="$emit('selectPaymentMod','card')"
                >
                    <div class="cart-payment__list-item-selection"></div> 
                    Банковским переводом
                </div>
            </div>
            <!-- TEXT -->
            <div class="cart-payment__text float-item">
                Оплата производится при получении товара и включает в себя
                стоимость товаров и стоимость доставки. 
                Включает в себя все расходы по формированию, упаковке и пересылке заказа.
            </div>
            <div class="clearfix"></div>
        </div>


        <!-- BUTTONS -->

        <div class="cart-payment__button-wrap">
            <button class="button button_blue bold cart-payment__button-back"
            @click="$emit('back')"
            >
                Назад
            </button>
            <button class="button button_green bold cart-payment__button-validate"
            @click="$emit('makeOrder')"
            >
                Подтвердить заказ
            </button>
        </div>

  </div>
</template>

<script>
export default {
  data: function(){
      return {
    }
  },
  props: [
      "selected-payment-mod"
  ],
  computed:{
      selectedMod(){
          return this.PAYMENT_MODS[this.selectedKey];
      },
      selectedKey(){
          return [
                "cash",
                "card_upon_receipt",
                "card",
            ].indexOf(this.selectedPaymentMod)
      }
  }
}
</script>
