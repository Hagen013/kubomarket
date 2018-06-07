<template>
    <div class="modal delivery-map"
        @click.self="close"
    >
        <div class="modal__content delivery-map__content" v-if="isDeliveryDataReady">
            <div class="content-area">
                <div class="delivery-map__inner">
                    <div class="delivery-map__left">
                        <div class="delivery-map__title">
                        ПУНКТЫ САМОВЫВОЗА
                        </div>
                        <div class="delivery-map__points-list-wrap">
                            <ul class="delivery-map__points-list green_scrollbar">
                                <li class="delivery-map__list-item"
                                    v-for="deliveryPoint in deliveryPointsList"
                                    :key=deliveryPoint.code
                                >
                                    <div class="delivery-map__list-item-adress bold">
                                        {{deliveryPoint.address}}
                                    </div>
                                    <div class="delivery-map__list-item-term green">
                                        {{[deliveryPoint.time_min, deliveryPoint.time_max] | timeFilter}}
                                    </div>
                                    <div class="delivery-map__list-item-price green">
                                        {{deliveryPoint.price}} ₽
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </div>
                    <div class="delivery-map__right">
                        <div class="delivery-map__map">
                            <yandex-map 
                            id="map" 
                            :id-value="'map'"
                            :points="deliveryPointsList"
                            :selected-point-code="selectedPointCode"
                            :cityName="cityName"

                            @pointSelected="pointSelected"
                            >
                            </yandex-map>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import yandexMap from '../yandexMap/yandexMap.vue'

import store from '../../store'

export default {
    name: 'delivery-map',
    store,
    components: {
        "yandex-map": yandexMap
    },
    data: function () {
        return {
            showSdek: true,
            showPickPoint: true,
            lastPoint: null
        }
    },
    store,
    computed: {
        isDeliveryDataReady (){
            return this.$store.state.delivery.isDataInited;
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
        cityName(){
            return this.$store.state.geo.city;
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
        close() {
            this.$store.commit("deliveryMap/hide");
        },
        pointSelected({code, type}) {
            console.log(code, type);
            this.$emit('pointSelected', {code, type});
        },
    },
    watch: {
    },
    filters: {
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
}

</script>
