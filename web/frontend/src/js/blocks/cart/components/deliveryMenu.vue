<template>
    <div class="cart__delivery-menu__wrap">
        <transition name="fade-fast">
        <div class="cart__delivery-menu">
            <div class="cart__city-choice">
                <div class="cart__city-choice-title">
                Доставка в городе
                </div>
                <a class="cart__city-choice-link link_city"
                    @click="showCityChoiceModal"
                >
                    {{cityName}}
                    <i class="icon icon_chevron-down cart__city-choice-icon"></i>
                </a>
                <div class="clearfix"></div>
            </div>
            <div class="cart__delivery-menu-list" v-if="isDeliveryDataReady">

                <!--            Курьером старт             -->
                <div class="cart__delivery-menu-item"
                    :class="{ cart__deliveryMenuItem_active : currentTabKey == 0 }"
                    @click="selectDeliveryTab(0)"
                >
                    <div class="cart__delivery-menu-caption">
                        <div class="cart__delivery-menu-title">
                        Курьером:
                        </div>
                        <div class="cart__delivery-menu-value green bold">
                        {{ priceCurier | priceFilter }} {{timeCurier | timeFilter}}
                        </div>
                    </div>
                </div>
                <!--            Курьером конец             -->

                <!--            Пунктом выдачи старт             --> 
                <div class="cart__delivery-menu-item"
                    :class="{ cart__deliveryMenuItem_active : currentTabKey == 1 }"
                    @click="selectDeliveryTab(1)"
                >
                    <div class="cart__delivery-menu-caption">
                        <div class="cart__delivery-menu-title">
                        Пункты выдачи
                        </div>
                        <div class="cart__delivery-menu-value green bold">
                        {{ priceCurier | priceFilter }} {{timeCurier | timeFilter}}
                        </div>
                    </div>
                </div>
                <!--            Пунктом выдачи конец             -->

                <!--            Почтой старт             -->
                <div class="cart__delivery-menu-item"
                    :class="{ cart__deliveryMenuItem_active : currentTabKey == 2 }"
                    @click="selectDeliveryTab(2)"
                >
                    <div class="cart__delivery-menu-caption">
                        <div class="cart__delivery-menu-title">
                        Почтой России:
                        </div>
                        <div class="cart__delivery-menu-value green bold">
                        {{ priceCurier | priceFilter }} {{timeCurier | timeFilter}}
                        </div>
                    </div>
                </div>
                <!--            Почтой конец             -->
            </div>

            <div class="cart__delivery-outlet">

                <div class="cart__delivery-info"
                    v-if="currentTabKey == -1"
                >
                    <div>
                    Способ доставки не выбран
                    </div>
                </div>

                <div class="cart__delivery-info"
                    v-if="currentTabKey == 0"
                >
                    <div class="input-box">
                        <input class="input cart__input"
                            placeholder="Адрес"
                        >
                    </div>
                    <textarea class="textarea"
                        placeholder="Пожелания"
                    >
                    </textarea>
                </div>

                <div class="cart__delivery-info"
                    v-if="currentTabKey == 1"
                >
                </div>

                <div class="cart__delivery-info"
                    v-if="currentTabKey == 2"
                >
                    <div class="input-box">
                        <input class="input cart__input"
                            placeholder="Адрес"
                        >
                    </div>
                    <textarea class="textarea"
                        placeholder="Пожелания"
                    >
                    </textarea>
                </div>

            </div>

        </div>
        </transition>
    </div>
</template>

<script>
import store from '../../../store'

export default {
  name: "delivery",
  store,
  data: (function() {
    return {
        currentTabKey: -1
    };
  }),
  props: [
      "isCartItemsDataReady",
      "isDeliveryDataReady", 
      "isDeliveryAvailable",
      "isCurierAvailable",
      "isPostalServiceAvailable",
      "isPointsAvailable",
      "isDeliveryModSelected",
      "isCartItemsDataNotEmpty",
      "deliveryData",
      "cityName",
      "customerAddress",
      "selectedDeliveryMod",
      "selectedDeliveryPoint"
  ],
  computed: {
    priceCurier() {
        return this.deliveryData.curier.price
    },
    timeCurier() {
        return [
            this.deliveryData.curier.time_min,
            this.deliveryData.curier.time_max
        ];
    },
    priceDeliveryPoint() {
        return this.deliveryData.delivery_point.price;
    },
    timeDeliveryPoint() {
        return [
            this.deliveryData.delivery_point.time_min,
            this.deliveryData.delivery_point.time_max
        ];
    },
    pricePostalService() {
        return this.deliveryData.postal_service.price;
    },
    timePostalService() {
        return [
            this.deliveryData.postal_service.time_min,
            this.deliveryData.postal_service.time_max
        ];
    },
  },
  methods: {
        hideCityChoiceModal() {
            this.$store.commit('showModalCityChoice/hide');
        },
        showCityChoiceModal() {
            this.$store.commit('showModalCityChoice/show');
        },
        selectDeliveryTab(key = 0) {
            this.currentTabKey = key;
            if (key == -1) {
                this.$emit("selectDeliveryMod", "");
            } else if(key == 0 && this.isCurierAvailable) {
                this.$emit("selectDeliveryMod", "curier");
            } else if( key == 1 && this.isPointsAvailable) {
                if(this.lastPoint){
                    this.$emit("selectDeliveryMod", "delivery_points", this.lastPoint.code, this.lastPoint.type);
                }else{
                    this.$emit("selectDeliveryMod", "");
                }
            } else if( key == 2 && this.isPostalServiceAvailable) {
                this.$emit("selectDeliveryMod", "postal_service");
            }
        },
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