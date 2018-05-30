<template>
    <!--<transition>-->
    <div class="cart__content">
        <div class="cart__personal-info">
            <h3 class="cart__block-title">Заполните даннные</h3>
            <div class="input-group cart__info-input">
                <input class="input" id="input-name" 
                v-model="customerName" 
                :class="{input_success: customerName.length != 0}" 
                @focus="isCustomerNameFocused = true"
                @blur="isCustomerNameFocused = false"
                >
                <label for="input-name"
                class="input-group__placeholder input-group__placeholder_reqiered"
                v-if="this.customerName.length==0 && !isCustomerNameFocused"
                >Имя</label>
            </div>
            <div class="input-group cart__info-input">
                <masked-input class="input" type="tel" id="input-phone"
                :class="{'input_success':customerPhone.length != 0 && isCustomerPhoneValid, 
                         'input_failure':customerPhone.length != 0 && !isCustomerPhoneValid}" 
                for="input-phone"
                v-model="customerPhone"
                @focus="isCustomerPhoneFocused = true"
                @blur="isCustomerPhoneFocused = false"
                :showMask="isCustomerPhoneFocused"
                :mask="['+', '7',' ','(', /\d/, /\d/, /\d/, ')', ' ', /\d/, /\d/, /\d/, '-', /\d/, /\d/, /\d/, /\d/]"
                />
                <label class="input-group__placeholder input-group__placeholder_reqiered" for="input-phone"
                v-if="customerPhone.length==0 && !isCustomerPhoneFocused"
                >Телефон</label>
            </div>
            <input class="input cart__info-input" type="email"
            placeholder="Почта" 
            v-model="customerEmail" 
            :class="{'input_success':customerEmail.length != 0 && isCustomerEmailValid, 
                     'input_failure':customerEmail.length != 0 && !isCustomerEmailValid}" 
            >
        </div>
        <h3 class="cart__block-title">Выберете способ доставки</h3>
        <div class="cart__delivery-choice"
             v-if="isDeliveryAvailable && isDeliveryDataReady"
             :key="1"
        >
            <div class="cart__delivery-routing">
                <div class="cart__delivery-routing-item" 
                     v-if="isCurierAvailable"
                     :class="{ cart__deliveryRoutingItem_active : curentTabKey==0 }" 
                     @click="selectDeliveryTab(0)"
                >
                    <i class="icon icon_delivery-courier cart__delivery-routing-icon"></i>
                    <div class="cart__delivery-routing-caption">
                        Доставка курьером
                    </div>
                </div>
                <div class="cart__delivery-routing-item" 
                    v-if="isPointsAvailable"
                    :class="{ cart__deliveryRoutingItem_active : curentTabKey==1 }" 
                    @click="selectDeliveryTab(1)"
                >
                    <i class="icon icon_delivery-distance cart__delivery-routing-icon"></i>
                    <div class="cart__delivery-routing-caption">
                        Пункты выдачи
                    </div>
                </div>
                <div class="cart__delivery-routing-item cart__delivery-routing-item_last" 
                    v-if="isPostalServiceAvailable"
                    :class="{ cart__deliveryRoutingItem_active : curentTabKey==2 }" 
                    @click="selectDeliveryTab(2)"
                >
                    <i class="icon icon_delivery-box-svg cart__delivery-routing-icon"></i>
                    <div class="cart__delivery-routing-caption">
                        Почта России
                    </div>
                </div>
                <div class="clearfix"></div>
            </div>
            <div class="cart__delivery-outlet"
                 v-if="curentTabKey!=-1"
            >
                <div class="cart__delivery-city-wrap">
                    <p class="bold">
                        Ваш город: <span class="cart__delivery-city" @click="$store.commit('showModalCityChoice/show')"> {{ cityName }} </span>
                    </p>                       
                </div>
                <div class="cart__delivery-info-wrap green_scrollbar">
                    <p v-if="curentTabKey==1" class="cart__delivery-info-checkbox-wrap">
                        <label v-if="deliveryData.points.delivery_data.sdek_delivery_data" class="cart__delivery-info-text">
                            <input type="checkbox" class="checkbox" v-model="showSdek"> 
                            <span class="checkbox-custom cart__delivery-checkbox-custom-sdek"></span> 
                            <span class="checkbox__label">СДЕК</span>
                            <span class="cart__text">- {{deliveryData.points.delivery_data.sdek_delivery_data.price | priceFilter}}</span>
                            <span class="cart__text">{{(({time_min, time_max})=>([time_min, time_max]))(deliveryData.points.delivery_data.sdek_delivery_data) | timeFilter}};</span>

                        </label>
                        <label v-if="deliveryData.points.delivery_data.pick_point_delivery_data" class="cart__delivery-info-text">
                            <input type="checkbox" class="checkbox" v-model="showPickPoint"> 
                            <span class="checkbox-custom cart__delivery-checkbox-custom-pick-point"></span> 
                            <span class="checkbox__label">ПикПоинт</span>
                            <span class="cart__text">- {{deliveryData.points.delivery_data.pick_point_delivery_data.price | priceFilter}}</span>
                            <span class="cart__text">{{(({time_min, time_max})=>([time_min, time_max]))(deliveryData.points.delivery_data.pick_point_delivery_data) | timeFilter}};</span>


                        </label>
                        
                        
                        <!-- <input type="checkbox" v-model="checkedNames">
                        <label for="mike">СДЕК - от 120р от 2 до 5 дней</label> -->
                        
                        <!-- <input type="checkbox" v-model="checkedNames">
                        <label for="mike">ПикПоинт - от 220р от 1 до 6 дней</label> -->
                        
                    </p>
                    <div v-if="deliveryInfo.isSelected">
                        <p class="cart__delivery-info-text bold">
                            {{deliveryInfo.mod}}{{deliveryInfo.pointType}}
                        </p>
                        <p class="cart__delivery-info-text">
                            Срок: <span class="cart__text">{{ deliveryInfo.time | timeFilter}};</span>
                        </p>
                        <p class="cart__delivery-info-text">
                            Стоимость: <span class="cart__text">{{ deliveryInfo.price | priceFilter}};</span>
                        </p>
                        <p v-if="deliveryInfo.pointAddress" class="cart__delivery-info-text">
                            Адрес:<span class="cart__text"> {{ deliveryInfo.pointAddress }}</span>
                        </p>
                        <p v-if="deliveryInfo.pointDescription" class="cart__delivery-info-text">
                            Описание:<span class="cart__text"> {{ deliveryInfo.pointDescription }}</span>
                        </p>
                    </div>
                    
                </div>
                    
                <keep-alive>
                <div class="cart__delivery-wrap">
                <component 
                    :is="curentComponent"
                    :delivery-data="deliveryData"
                    :city-name="cityName"
                    :is-curier-available="isCurierAvailable"
                    :is-postal-service-available="isPostalServiceAvailable"
                    :customer-address="customerAddress"
                    :delivery-points-list="deliveryPointsList"
                    :selected-delivery-mod="selectedDeliveryMod"

                    @pointSelected="pointSelected"
                    >
                </component>
                </div>
                </keep-alive>
                <div class="cart__delivery-selected">
                    <div class="button button_blue cart__proceed"
                    @click="next"
                    >
                        Продолжить
                    </div>
                </div>
            </div>
        </div>
        <div v-else-if="isCartItemsDataReady && isDeliveryDataReady"
             :key="2"
        >
            <h3 v-if="isCartItemsDataNotEmpty"
                :key="3"
            >
                Оператор уточнит способ и стоимость доставки, когда свяжется с вами.
            </h3>
            <h3 v-else-if="!isCartItemsDataNotEmpty"
                :key="4"
            >
                <p>
                Корзин пуста.
                </p>
                <p>
                Наполните её, чтобы узнать доступные способы доставки.
                </p>
            </h3>
        </div>
        <div class="clearfix"></div>
    </div>
    <!--</transition>-->
</template>

<script>
import { Vue } from "../../vue.js";

import MaskedInput from 'vue-text-mask';

import store from "../../store";



import deliveryCourier from "./__delivery-courier.vue";
import deliveryPoints from "./__delivery-points.vue";
import deliveryPostalServis from "./__delivery-postal-service.vue";

export default {
  name: "delivery",
  store,
  data: function() {
    return {
      isCustomerNameFocused: false,
      isCustomerPhoneFocused: false,
      isCustomerEmailFocused: false,

      curentTabKey: -1,

      showSdek: true,
      showPickPoint: true,
      lastPoint: null
    };
  },
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
  components: {
    'masked-input': MaskedInput,
    deliveryCourier: deliveryCourier,
    deliveryPoints: deliveryPoints,
    deliveryPostalServis: deliveryPostalServis,
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
    customerEmail: {
        get(){
            return this.$store.state.customer.email;
        },
        set(value) {
            this.$store.commit('customer/setData', {email:value})
        }
    },
    isCustomerPhoneValid() {
      return this.$store.getters["customer/isPhoneValid"];
    },
    isCustomerEmailValid() {
      return this.$store.getters["customer/isEmailValid"];
    },
    isValidEmail() {
      return this.$store.getters["orders/customer/isValidEmail"];
    },
    curentComponent() {
      return ["deliveryCourier", 
              "deliveryPoints", 
              "deliveryPostalServis"][this.curentTabKey];
    },
    deliveryInfo() {
      if ((this.isDeliveryDataReady && this.isDeliveryAvailable)) {
        let data = this.deliveryData[['curier','delivery_point', 'postal_service'][this.curentTabKey]]
        return {
            "mod": ["Доставка курьером", "Доставка в пункт выдачи", "Доставка Почтой России"][this.curentTabKey],
            "isSelected": this.isDeliveryModSelected,
            "price": this.selectedDeliveryMod.price,
            "time": (this.isDeliveryModSelected && this.selectedDeliveryMod.type=="delivery_points") ? [this.selectedDeliveryPoint.time_min, this.selectedDeliveryPoint.time_max] : data === null ? null : [data.time_min, data.time_max],
            "pointType": (this.isDeliveryModSelected && this.selectedDeliveryMod.type=="delivery_points") ? {"pick_point_point":" ПикПоинт", "sdek_point":" СДЕК"}[this.selectedDeliveryMod.code.split("__")[1]] : "",
            "pointAddress": (this.curentTabKey==1 && this.selectedDeliveryPoint !== undefined) ? this.selectedDeliveryPoint.address: null,
            "pointDescription": (this.curentTabKey==1 && this.selectedDeliveryPoint !== undefined) ? this.selectedDeliveryPoint.description: null
        }
      }  else {
        return undefined;
      }
    },
    deliveryPointsList() {
        return [].concat(
            this.showPickPoint ? Array.from(this.deliveryData.points['pick_point_points'],
                x => {
                    x['type'] = 'pick_point_point';
                    return x;
                },
            ) : [],
            this.showSdek ? Array.from(this.deliveryData.points['sdek_points'],
                x => {
                    x['type'] = 'sdek_point';
                    return x;
                }
            ) : []
        );
    },
  },
  methods: {
    next(){
        this.$emit('next');
        // Google Analytics
        dataLayer.push({'event': 'zakaz'});
        yaCounter46971201.reachGoal('zakaz');
    },
    selectDeliveryTab(key = 0) {
        this.curentTabKey = key;
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
    autoSelectTab() {
        if (this.isDeliveryDataReady == true) {
            if ((this.curentTabKey==0 && !this.isCurierAvailable) ||
                (this.curentTabKey==1 && !this.isPointsAvailable) ||
                (this.curentTabKey==2 && !this.isPostalServiceAvailable)
                ){
                    this.selectDeliveryTab(-1);
            }
            if(
                [this.isCurierAvailable,
                 this.isPointsAvailable,
                 this.isPostalServiceAvailable].filter(x=>x==true).length == 1
            ){
                // если доступна только одна - сразу выбираем её
                this.selectDeliveryTab([this.isCurierAvailable,
                                        this.isPointsAvailable,
                                        this.isPostalServiceAvailable].indexOf(true));
            } else {
                // каждый инит идёт по этой ветке
                this.selectDeliveryTab(this.curentTabKey);
            }
        }
    },
    pointSelected({code, type}){
        this.lastPoint = {code, type}
        this.$emit("selectDeliveryMod", "delivery_points", code, type);
    }
  },
  watch: {
    isDeliveryDataReady(value) {
        this.autoSelectTab();
    },
    isDeliveryModSelected(value) {
        // console.log('isDeliveryModSelected');
        if(!value){
            this.lastPoint = null;
        }
        this.autoSelectTab();
    }
  },
  mounted() {
      this.autoSelectTab();
  }
};
</script>
