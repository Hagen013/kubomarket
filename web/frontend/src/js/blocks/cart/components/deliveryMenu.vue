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
                    v-if="isCurierAvailable"
                    :class="{ cart__deliveryMenuItem_active : currentTabKey == 0 }"
                    @click="selectDeliveryTab(0)"
                >
                    <div class="cart__delivery-menu-caption">
                        <div class="cart__delivery-menu-title">
                        Курьером:
                        </div>
                        <div class="cart__delivery-menu-value green bold">
                        {{ priceCurier | priceFilter }} <i class="icon icon_rouble"></i> {{timeCurier | timeFilter}}
                        </div>
                    </div>
                </div>

                <div class="cart__delivery-menu-item cart__delivery-menu-item_disabled"
                    v-else
                >
                    <div class="cart__delivery-menu-caption">
                        <div class="cart__delivery-menu-title">
                        Курьером:
                        </div>
                        <div class="cart__delivery-menu-value grey">
                        недоступно
                        </div>
                    </div>
                </div>

                <!--            Курьером конец             -->

                <!--            Пунктом выдачи старт             --> 
                <div class="cart__delivery-menu-item"
                    :class="{ cart__deliveryMenuItem_active : currentTabKey == 1 }"
                    @click="selectDeliveryPointsTab"
                    v-if="isPointsAvailable"
                >
                    <div class="cart__delivery-menu-caption">
                        <div class="cart__delivery-menu-title">
                        Пункты выдачи
                        </div>
                        <div class="cart__delivery-menu-value green bold">
                        от {{ priceDeliveryPoint | priceFilter }} <i class="icon icon_rouble"></i> {{timeCurier | timeFilter}}
                        </div>
                    </div>
                </div>

                <div class="cart__delivery-menu-item cart__delivery-menu-item_disabled"
                    v-else
                >
                    <div class="cart__delivery-menu-caption">
                        <div class="cart__delivery-menu-title">
                        Пункты выдачи
                        </div>
                        <div class="cart__delivery-menu-value grey bold">
                        недоступно
                        </div>
                    </div>
                </div>

                <!--            Пунктом выдачи конец             -->

                <!--            Почтой старт             -->
                <div class="cart__delivery-menu-item"
                    :class="{ cart__deliveryMenuItem_active : currentTabKey == 2 }"
                    @click="selectDeliveryTab(2)"
                    v-if="isPostalServiceAvailable"
                >
                    <div class="cart__delivery-menu-caption">
                        <div class="cart__delivery-menu-title">
                        Почтой России:
                        </div>
                        <div class="cart__delivery-menu-value green bold">
                        {{ pricePostalService | priceFilter }} <i class="icon icon_rouble"></i> {{timeCurier | timeFilter}}
                        </div>
                    </div>
                </div>

                <div class="cart__delivery-menu-item"
                    v-else
                >
                    <div class="cart__delivery-menu-caption">
                        <div class="cart__delivery-menu-title">
                        Почтой России:
                        </div>
                        <div class="cart__delivery-menu-value grey">
                            Недоступно
                        </div>
                    </div>
                </div>
                <!--            Почтой конец             -->
            </div>

            <div class="cart__delivery-menu-list-placeholder" v-else>
            </div>

            <div class="cart__delivery-outlet">

                <div class="cart__delivery-info"
                    v-if="currentTabKey == -1"
                >
                    <div class="cart__delivery-placeholder bold">
                    Способ доставки не выбран
                    </div>
                </div>

                <div class="cart__delivery-info"
                    v-if="currentTabKey == 0"
                >
                    <div class="cart__address-form">
                        <div class="input-box cart__address-input-box">
                            <input class="input cart__input cart__address-input"
                                placeholder="Адрес"
                                v-model="customerAddress"
                            >
                        </div>
                        <textarea class="textarea cart__address-text"
                            placeholder="Пожелания"
                            v-model="customerNotes"
                        >
                        </textarea>
                    </div>
                </div>

                <div class="cart__delivery-info"
                    v-if="currentTabKey == 1"
                >
                    <div class="cart__selected-point" v-if="selectedDeliveryPoint !== undefined">
                        <div class="cart__selected-point-address bold">
                            {{selectedDeliveryPoint.address}}
                        </div>
                        <div class="cart__selected-point-term green">
                            {{[selectedDeliveryPoint.time_min, selectedDeliveryPoint.time_max] | timeFilter}}
                        </div>
                        <div class="cart__selected-point-price green">
                            {{selectedDeliveryPoint.price | priceFilter}} <i class="icon icon_rouble"></i>
                        </div>
                        <div class="cart__change-point-link_single">
                            <a class="link link_city"
                                @click="reSelectDeliveryPoint"
                            >
                                выбрать другой пункт выдачи
                                <i class="icon icon_chevron-down cart__city-choice-icon"></i>
                            </a>
                        </div>
                        <textarea class="textarea cart__address-text"
                            placeholder="Пожелания"
                            v-model="customerNotes"
                        >
                        </textarea>
                    </div>
                    <div v-else class="cart__selected-point-placeholder-wrap">
                        <div class="cart__selected-point-placeholder bold">
                            Пункт выдачи не выбран,
                            <a class="link link_city cart__change-point-link"
                                @click="reSelectDeliveryPoint"
                            >
                                выбрать
                                <i class="icon icon_chevron-down cart__city-choice-icon"></i>
                            </a>
                        </div>
                    </div>
                </div>

                <div class="cart__delivery-info"
                    v-if="currentTabKey == 2"
                >
                    <div class="cart__address-form">
                        <div class="input-box cart__address-input-box">
                            <input class="input cart__input cart__address-input"
                                placeholder="Адрес"
                                v-model="customerAddress"
                            >
                        </div>
                        <textarea class="textarea cart__address-text"
                            placeholder="Пожелания"
                        >
                        </textarea>
                    </div>
                </div>

            </div>

        </div>
        </transition>
    </div>
</template>

<script>
import store from '../../../store'
import yandexMap from '../../yandexMap/yandexMap.vue'

export default {
  name: "delivery",
  store,
  data: (function() {
    return {
        currentTabKey: -1,
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
      "selectedDeliveryMod",
      "selectedDeliveryPoint"
  ],
  computed: {
    priceCurier() {
        return this.deliveryData.curier.price
    },
    timeCurier() {
        if (this.isCurierAvailable) {
            return [
                this.deliveryData.curier.time_min,
                this.deliveryData.curier.time_max
            ];           
        }
        else {
            return []
        }
    },
    priceDeliveryPoint() {
        return this.deliveryData.delivery_point.price;
    },
    timeDeliveryPoint() {
        if (this.isPointsAvailable) {
            return [
                this.deliveryData.delivery_point.time_min,
                this.deliveryData.delivery_point.time_max
            ];
        }
        else {
            return []
        }
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
    selectedPointCode() {
        return this.selectedDeliveryMod.code;
    },
    customerAddress: {
        get() {
            return this.$store.state.customer.address
        },
        set(value) {
            this.$store.commit('customer/setData', {address:value});
        }
    },
    customerNotes: {
        get() {
            return this.$store.state.delivery.notes
        },
        set(value) {
            this.$store.commit('delivery/setNotes', value);
        }
    }
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
        selectDeliveryPointsTab() {
            this.selectDeliveryTab(1);
            this.$store.commit("deliveryMap/show");
        },
        reSelectDeliveryPoint() {
            this.$store.commit("deliveryMap/show");
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