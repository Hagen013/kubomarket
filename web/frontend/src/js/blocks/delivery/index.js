import { Vue } from '../../vue.js'
import store from '../../store'

import yandexMap from '../yandexMap/yandexMap.vue'


var delivery = new Vue({
    name: 'delivery',
    el: '#delivery',
    store,
    data: {
        showSdek: true,
        showPickPoint: true,
        lastPoint: null,
        currentTab: 0,
        ymapsCheckTimer: null,
        ymapsInited: false,
        ymapsReady: false,
        ready: false
    },
    components: {
        "yandex-map": yandexMap
    },
    created() {
        this.ymapsCheckTimer = setInterval(this.checkYmaps, 100);
        this.ready = true;
    },
    mounted() {

    },
    computed: {
        mapIsAvailable() {
            return ( (this.isDeliveryDataReady === true) && (this.ymapsInited === true) && (this.mapReady) ) 
        },
        cityName() {
            return this.$store.state.geo.city;
        },
        deliveryData(){
            return this.$store.state.delivery.data;
        },
        selectedDeliveryMod(){
            return this.$store.state.delivery.mod;
        },
        selectedPointCode() {
            return this.selectedDeliveryMod.code;
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
        // ДАННЫЕ ДОСТАВКИ
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
        priceCurier() {
            return this.deliveryData.curier.price;
        },
        priceDeliveryPoint() {
            return this.deliveryData.delivery_point.price;
        },
        pricePostalService() {
            return this.deliveryData.postal_service.price;
        },
        timeCurier() {
            return [
                this.deliveryData.curier.time_min,
                this.deliveryData.curier.time_max
            ];
        },
        timeDeliveryPoint() {
            return [
                this.deliveryData.delivery_point.time_min,
                this.deliveryData.delivery_point.time_max
            ];
        },
        timePostalService() {
            return [
                this.deliveryData.postal_service.time_min,
                this.deliveryData.postal_service.time_max
            ];
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
        // Содержимое корзины
        isCartItemsDataReady() {
            return this.$store.state.cart.isDataInited;
        },
        isCartItemsDataNotEmpty() {
            return !this.$store.getters['cart/isCartEmpty'];
        },
        sortedCartItemsArray() {
            return this.$store.getters['cart/sortedItemsArray'];
        },
        totalCartItemsQuantity() {
            return this.$store.state.cart.items_quantiy;
        },
        totalCartItemsDeepQuantity() {
            let quantity = 0;
            if (this.isCartItemsDataReady !== true) {
                return quantity
            }
            for (let i=0; i<this.sortedCartItemsArray.length; i++) {
                quantity += this.sortedCartItemsArray[i].quantity;
            }
            return  quantity
        },
        totalCartItemsPrice() {
            return this.$store.state.cart.total_price;
        },
        // GEO
        isGeoDataInited() {
            return this.$store.state.geo.isDataInited;
        },
        isDeliveryRequestDataReady() {
            return (this.isCartItemsDataReady && this.isGeoDataInited)
        },
        // Доставка
        isDeliveryDataReady (){
            return this.$store.state.delivery.isDataInited;
        },
        deliveryData(){
            return this.$store.state.delivery.data;
        },
        isDeliveryModSelected(){
            return this.$store.state.delivery.isModSelected;
        },
        cityName(){
            return this.$store.state.geo.city;
        },
        isDeliveryAvailable(){
            return this.$store.getters['delivery/isAvailable'];
        },
        isCurierAvailable(){
            return this.$store.getters['delivery/isCurierAvailable'];
        },
        isPostalServiceAvailable(){
            return this.$store.getters['delivery/isPostalServiceAvailable'];
        },
        isPointsAvailable(){
            return this.$store.getters['delivery/isPointsAvailable'];
        },
        isCustomerDataValid() {
            return (
                (
                    // проверка на непустость корзины
                    !this.$store.getters['cart/isCartEmpty']
                ) && (
                    // проверка на валидность и существование телефона
                    this.$store.getters['customer/isPhoneValid']
                ) && (
                    // проверка на валидность мэйла или его отсутствие
                    (this.$store.state.customer.email.length == 0) ||
                    (
                        (this.$store.state.customer.email.length != 0) &&
                         this.$store.getters['customer/isEmailValid']
                    )
                )
            );
        },
        customerAddress(){
            return this.$store.state.customer.address;
        },
        selectedDeliveryMod(){
            return this.$store.state.delivery.mod;
        },
        selectedDeliveryPoint(){
            return this.$store.getters["delivery/curentSelectedPoint"];
        },
        // Вкладка оплаты
        selectedPaymentMod(){
            return this.$store.state.payment.mod;
        },
        // Заказ
        orderData(){
            return this.$store.getters['orderData']('cart');
        },
        ECProducts(){
            return this.sortedCartItemsArray.map(
                currentValue=>{
                    return{
                        id: currentValue.offer_identifier,
                        name: currentValue.name,
                        price: currentValue.price,
                        quantity: currentValue.quantity
                    }
                }
            );
        }
    },
    mounted() {
    },
    methods: {
        hideCityChoiceModal() {
            this.$store.commit('showModalCityChoice/hide');
        },
        showCityChoiceModal() {
            this.$store.commit('showModalCityChoice/show');
        },
        pointSelected({code, type}) {
            this.$store.commit('delivery/selectDeliveryPointsMod', {code, type});
            this.close();
        },
        checkYmaps() {
            if ( ymaps.geocode !== undefined ) {
                this.ymapsInited = true;
                clearInterval(this.ymapsCheckTimer);
            }
        },
        mapReady() {
            this.ymapsReady = true;
        }
    },
    watch: {
        isDeliveryRequestDataReady() {
            if (this.isDeliveryRequestDataReady) {
                this.$store.dispatch('delivery/initDelivery');
            }
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
});
