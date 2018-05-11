<template>
  <div>
    <div class="catalog__price-inputs">
        <input 
            id="js-left-price-input" 
            class="input catalog__price-input catalog__price-input_left"
            type="text"
            onkeypress='return event.charCode >= 48 && event.charCode <= 57'
            v-model="proxyValues[0]"
            v-on:change="processProxyValues"
            v-on:keyup.enter="processProxyValues"
        >
        <input 
            id="js-right-price-input" 
            class="input catalog__price-input catalog__price-input_right"
            type="text"
            onkeypress='return event.charCode >= 48 && event.charCode <= 57'
            v-model="proxyValues[1]"
            v-on:change="processProxyValues"
            v-on:keyup.enter="processProxyValues"
        >
    </div>
    <vue-slider
        ref="slider"
        v-model="priceValues"
        v-on:callback="sliderChanged"
        v-on:drag-start="sliderDragStart"
        v-on:drag-end="sliderDragEnd"
        class="catalog__price-slider ranged-slider"
        :min="min"
        :max="max"
        :speed="0"
        :tooltip="false"
    >
    </vue-slider>
  </div>
</template>
<script>

import vueSlider from 'vue-slider-component'
import getParameterByName from '../../core/getParameterByName'
import debounce from 'debounce'

export default {
    name: 'price-filter',
    data: function() {
        return {
            priceValues: this.price_values,
            proxyValues: [0, 400000],
            requestLock: false
        }
    },
    created: function () {
        this.price_values = this.price_values;
    },
    components: {
        'vueSlider': vueSlider
    },
    props: ['min', 'max', 'price_values'],
    methods: {
        processProxyValues: function () {
            let leftValue = parseInt(this.proxyValues[0]);
            let rightValue = parseInt(this.proxyValues[1]);
            if ( isNaN(leftValue) || (this.min>leftValue) || (this.max<leftValue) ) {
                leftValue = this.min;
            }
            if ( isNaN(rightValue) || (this.min>rightValue) || (this.max<rightValue) ) {
                rightValue = this.max;
            }
            this.priceValues = [leftValue, rightValue];
            this.$emit('price-request-triggered', this.priceValues[0], this.priceValues[1]);
        },
        sliderChanged: function () {
            if ( this.requestLock != true ) {
                this.clickRequest();
            }
        },
        sliderDragStart: function () {
            this.requestLock = true;
        },
        sliderDragEnd: function () {
            this.requestLock = false;
            this.$emit('price-request-triggered', this.priceValues[0], this.priceValues[1]);
        },
        refreshSlider: function () {
            this.$refs.slider.refresh();
        },
        clickRequest: debounce(function () {
            this.$emit('price-request-triggered', this.priceValues[0], this.priceValues[1]);
        }, 150)
    },
    watch: {
        price_values: function () {
            this.priceValues = this.price_values;
            this.proxyValues = this.price_values;
        },
        priceValues: function () {
            this.proxyValues = this.priceValues.slice();
        },
    },
}
</script>
