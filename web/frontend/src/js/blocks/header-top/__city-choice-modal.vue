<template>
    <modal @close="$emit('close')" :title="city" :sizesStyleName="'modal__city-choice-content'">
        <input class="input modal__row" placeholder="Поиск по городам" v-model="searchLine"></input>
    
        <!--Результат поиска-->
        <div v-if="(searchLine.length>2)&&(searchResult.length)" class="modal__city-choice-wrap modal__city-choice-wrap_search">
            <div class="modal__city-choice-search-link" v-for="city in searchResult" :key="city.code">
                <a class="link" @click="choiceCity(city.name, city.code)">
                    {{city.full_name}}
                </a>
            </div>
        </div>
        <!--Если результата нет-->
        <div v-else-if="(searchLine.length>2)&&(searchResult.length==0)&&(isInited)" class="modal__city-choice-error-message">
            По данному запросу найти ничего не удалось
        </div>
        <!--Дефолтные города-->
        <div v-else class="modal__city-choice-wrap modal__city-choice-wrap_default">
            <div class="modal__city-choice-city" v-for="city in defaultCityList" :key="city.kladr">
                <a class="link" @click="choiceCity(city.name, city.code)">
                    {{city.name}}
                </a>
            </div>
            <div class="clearfix"></div>
        </div>
    
    </modal>
</template>

<script>
import {Vue, Vuex, VueResource} from '../../vue.js';


import debounce from 'debounce'
import store from '../../store'

import modal from '../../core/modal.vue'
import defaultCityList from './__default-city-list.js'

export default {
    name: 'city-choice-modal',
    store,
    data: function () {
        return {
            defaultCityList: defaultCityList,
            searchLine: "",
            searchResult: [],
            isInited: false
        }
    },
    methods: {
        choiceCity(city, code) {
            this.$store.dispatch("changeLocation", {
                city,
                code
            });
            this.$emit('close');
        }
    },
    watch: {
        searchLine: debounce(function (searchLine) {
            if (this.searchLine.length > 2) {
                this.$http.get(`${GEO_IP_HOST}/api/kladr/search/${searchLine}`).then(
                    response => {
                        // хук на успех
                        this.isInited = true;
                        this.searchResult = response.body;
                    }
                )
            } else if (searchLine.length < 3) {
                this.searchResult = [];
                this.isInited = false;
            }
        }, 300)
    },
    computed: {
        city() {
            return this.$store.state.geo.city;
        }
    },
    components: {
        'modal': modal,
    }
}

</script>
