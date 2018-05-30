<template>
    <div v-if="canCalcDelivery" class="product-card__delivery-types">
        <!--            Почтой россии старт             -->
        <div v-if="isPostalServiceAvailable" class="product-card__delivery-type">
            <i class="icon product-card__delivery-icon icon_delivery-box"></i>
            <div class="product-card__delivery-caption">
                <div>Почтой России - {{ pricePostalService | priceFilter }} {{timePostalService | timeFilter}}</div>
            </div>
        </div>
        <div v-else class="product-card__delivery-type">
            <i class="icon product-card__delivery-icon .icon_delivery-box_disable"></i>
            <div class="product-card__delivery-caption">
                <div>Почтой России - Недоступно</div>
            </div>
        </div>
        <!--            Почтой россии конец             -->

        <!--            Курьером старт             -->
        <div v-if="isCurierAvailable" class="product-card__delivery-type">
            <i class="icon product-card__delivery-icon icon_delivery-courier-png"></i>
            <div class="product-card__delivery-caption">
                <div>Курьером - {{ priceCurier | priceFilter }} {{timeCurier | timeFilter}}</div>
            </div>
        </div>
        <div v-else class="product-card__delivery-type">
            <i class="icon product-card__delivery-icon icon_delivery-courier-png_disable"></i>
            <div class="product-card__delivery-caption">
                <div>Курьером - Недоступно</div>
            </div>
        </div>
        <!--            Курьером конец             -->

        <!--            Пункт выдачи старт         -->
        <div v-if="isDeliveryPointAvailable" class="product-card__delivery-type">
            <i class="icon product-card__delivery-icon icon_delivery-point"></i>
            <div class="product-card__delivery-caption">
                <div>Пункт выдачи - {{ priceDeliveryPoint | priceFilter }} {{timeDeliveryPoint | timeFilter}}</div>
            </div>
        </div>
        <div v-else class="product-card__delivery-type">
            <i class="icon product-card__delivery-icon icon_delivery-point_disable"></i>
            <div class="product-card__delivery-caption">
                <div>Пункт выдачи - Недоступно</div>
            </div>
        </div>
        <!--            Пункт выдачи конец         -->
    </div>
    <div v-else class="product-card__delivery-types">
      <div class="product-card__delivery-type">
          <i class="icon product-card__delivery-icon icon_delivery-box"></i>
          <div class="product-card__delivery-caption">
              <div>Почтой России</div>
          </div>
      </div>
      <!--            Почтой россии конец             -->

      <!--            Курьером старт             -->
      <div class="product-card__delivery-type">
          <i class="icon product-card__delivery-icon icon_delivery-courier-png"></i>
          <div class="product-card__delivery-caption">
              <div>Курьером</div>
          </div>
      </div>
      <!--            Курьером конец             -->

      <!--            Пункт выдачи старт         -->

      <div class="product-card__delivery-type">
          <i class="icon product-card__delivery-icon icon_delivery-point"></i>
          <div class="product-card__delivery-caption">
              <div>Пункт выдачи</div>
          </div>
      </div>

    </div>
</template>

<script>
import store from "../../store";

export default {
  name: "delivery-inner",
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
          return `${value} ₽`;
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