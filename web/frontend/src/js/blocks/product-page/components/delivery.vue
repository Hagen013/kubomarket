<template>
    <div v-if="canCalcDelivery" class="product-page__delivery-types">

        <!--            Курьером старт             -->
        <div v-if="isCurierAvailable" class="product-page__delivery-type">
            <i class="icon product-page__delivery-icon icon_delivery-courier-png"></i>
            <div class="product-page__delivery-caption">
                <div class="product-page__delivery-type-title">
                    Доставка курьером:
                </div>
                <div class="product-page__delivery-type-value green bold">
                {{ priceCurier}} <i class="icon icon_rouble"></i> {{timeCurier | timeFilter}}
                </div>
            </div>
        </div>
        <div v-else class="product-page__delivery-type">
            <i class="icon product-page__delivery-icon icon_delivery-courier-png_disabled"></i>
            <div class="product-page__delivery-caption">
                <div>Курьером - Недоступно</div>
            </div>
        </div>
        <!--            Курьером конец             -->

        <!--            Пункт выдачи старт         -->
        <div v-if="isDeliveryPointAvailable" class="product-page__delivery-type">
            <i class="icon product-page__delivery-icon icon_delivery-point"></i>
            <div class="product-page__delivery-caption">
                <div class="product-page__delivery-type-title">
                    Доставка в пункты выдачи:
                </div>
                <div class="product-page__delivery-type-value green bold">
                {{ priceDeliveryPoint }} <i class="icon icon_rouble"></i> {{timeDeliveryPoint | timeFilter}}
                </div>
            </div>
        </div>
        <div v-else class="product-page__delivery-type">
            <i class="icon product-page__delivery-icon icon_delivery-point_disable"></i>
            <div class="product-page__delivery-caption">
                <div>Пункт выдачи - Недоступно</div>
            </div>
        </div>
        <!--            Пункт выдачи конец         -->

        <!--            Почтой россии старт             -->
        <div v-if="isPostalServiceAvailable" class="product-page__delivery-type">
            <i class="icon product-page__delivery-icon icon_delivery-mail"></i>
            <div class="product-page__delivery-caption">
                <div class="product-page__delivery-type-title">
                    Доставка почтой России:
                </div>
                <div class="product-page__delivery-type-value green bold">
                {{ pricePostalService}} <i class="icon icon_rouble"></i> {{timePostalService | timeFilter}}
                </div>
            </div>
        </div>
        <div v-else class="product-page__delivery-type">
            <i class="icon product-page__delivery-icon icon_delivery-mail_disabled"></i>
            <div class="product-page__delivery-caption">
                <div>Почтой России - Недоступно</div>
            </div>
        </div>
        <!--            Почтой россии конец             -->

    </div>

    <div v-else class="product-page__delivery-types">
      <div class="product-page__delivery-type">
          <i class="icon product-page__delivery-icon icon_delivery-mail"></i>
          <div class="product-page__delivery-caption">
              <div>Почтой России</div>
          </div>
      </div>
      <!--            Почтой россии конец             -->

      <!--            Курьером старт             -->
      <div class="product-page__delivery-type">
          <i class="icon product-page__delivery-icon icon_delivery-courier-png"></i>
          <div class="product-page__delivery-caption">
              <div>Курьером</div>
          </div>
      </div>
      <!--            Курьером конец             -->

      <!--            Пункт выдачи старт         -->

      <div class="product-page__delivery-type">
          <i class="icon product-page__delivery-icon icon_delivery-point"></i>
          <div class="product-page__delivery-caption">
              <div>Пункт выдачи</div>
          </div>
      </div>

    </div>
</template>

<script>
import store from "../../../store";
export default {
  name: "delivery",
  store,
  data: function() {
    return {};
  },
  computed: {
    canCalcDelivery() {
      return Object.keys(this.$parent.deliveryData).length !== 0;
    },
    // delivery price
    priceCurier() {
      return this.$parent.deliveryData.curier.price;
    },
    priceDeliveryPoint() {
      return this.$parent.deliveryData.delivery_point.price;
    },
    pricePostalService() {
      return this.$parent.deliveryData.postal_service.price;
    },
    // delivery time
    timeCurier() {
      return [
        this.$parent.deliveryData.curier.time_min,
        this.$parent.deliveryData.curier.time_max
      ];
    },
    timeDeliveryPoint() {
      return [
        this.$parent.deliveryData.delivery_point.time_min,
        this.$parent.deliveryData.delivery_point.time_max
      ];
    },
    timePostalService() {
      return [
        this.$parent.deliveryData.postal_service.time_min,
        this.$parent.deliveryData.postal_service.time_max
      ];
    },
    // delivery bool
    isCurierAvailable() {
      return this.$parent.deliveryData.curier;
    },
    isDeliveryPointAvailable() {
      return this.$parent.deliveryData.delivery_point;
    },
    isPostalServiceAvailable() {
      return this.$parent.deliveryData.postal_service;
    }
  },
  filters: {
    priceFilter(value) {
      if (value !== null) {
        if (value > 0) {
          return `${value}`;
        } else {
          return "бесплатно";
        }
      } else {
        return "";
      }
    },
    timeFilter(value) {
      let [from_time, to_time] = value;
      if (from_time || to_time) {
        if (from_time != to_time) {
          from_time = from_time ? `от ${from_time}` : "";
          to_time = to_time ? ` до ${to_time}` : "";
          return `${from_time}${to_time} дней`;
        } else {
          if (from_time == 1) {
            return `от 1 дня`;
          } else {
            return `от ${from_time} дней`;
          }
        }
      } else {
        return "";
      }
    }
  }
};
</script>