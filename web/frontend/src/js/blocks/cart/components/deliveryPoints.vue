<template>
    <div class="delivery-points">
        <yandex-map 
        id="map" 
        :id-value="'map'"
        :points="deliveryPointsList"
        :selected-point-code="selectedPointCode"
        :cityName="cityName"

        @pointSelected="pointSelected"
        ></yandex-map>
    </div>
</template>

<script>
import { Vue } from '../../../vue.js';
import yandexMap from '../../yandexMap/yandexMap.vue'
import store from '../../../store'


export default {
    store,
    data: function () {
        return {
        }
    },
    props: [
        "deliveryData",
        "selectedDeliveryMod",
        "deliveryPointsList",
        "cityName"
    ],
    components:{
        yandexMap
    },
    methods: {
        isListItemActive(delivery_code) {
            return delivery_code == this.selectedItemCode;
        },
        pointSelected({code, type}) {
            //console.log(code, type);
            this.$emit('pointSelected', {code, type});
        },
    },
    computed: {
        selectedPointCode() {
            return this.selectedDeliveryMod.code;
        }
    }
}
</script>