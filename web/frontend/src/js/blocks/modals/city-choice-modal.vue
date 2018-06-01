<template>
    <div class="city-choice-modal modal"
        @click.self="$emit('close')"
    >
        <div class="modal__content city-choice-modal__content">
            <div class="modal__title city-choice-modal__title">
                {{city}}
            </div>
            <div class="input-box modal__input-box city-choice-modal__input-box">
                <input class="input modal__input city-choice-modal__input" 
                    placeholder="Поиск по городам" 
                    v-model="searchLine"
                >
                <i class="icon icon_search city-choice-modal__search-icon"></i>
            </div>

            <div class="city-choice-modal__city-list city-choice-modal__city-list_default city-choice-modal__city-list_wide green_scrollbar"
                v-if="(searchLine.length>2)&&(searchResult.length)"
            >
                <div class="city-choice-modal__city-item_wide"
                    v-for="city in searchResult"
                    :key="city.code"
                    @click="choiceCity(city.name, city.code)"
                >
                    <a class="city-choice-modal__city-link">
                        {{city.full_name}}
                    </a>
                </div>
            </div>

            <!--Если результата нет-->
            <div v-else-if="(searchLine.length>2)&&(searchResult.length==0)&&(isInited)">
                <div class="city-choice-modal__error-message">
                По данному запросу ничего не удалось найти
                </div>
            </div>

            <!--Дефолтные города-->
            <div class="city-choice-modal__city-list city-choice-modal__city-list_default green_scrollbar"
                v-else
            >
                <div class="city-choice-modal__city-item"
                    v-for="city in defaultCityList"
                    :key="city.kladr"
                    @click="choiceCity(city.name, city.code)"
                >
                    <a class="city-choice-modal__city-link">
                        {{city.name}}
                    </a>
                </div>
            </div>


            <div class="button_round city-choice-modal__close"
                @click="$emit('close')"
            >
                <i class="icon icon_close"></i>
            </div>
        </div>
    </div>
</template>

<script>
import debounce from 'debounce'
import store from '../../store'

import defaultCityList from './defaultCityList.js'


export default {
    name: 'city-choice-modal',
    data: function () {
        return {
            defaultCityList: defaultCityList,
            searchLine: "",
            searchResult: [],
            isInited: false
        }
    },
    store,
    computed: {
        city() {
            return this.$store.state.geo.city;
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
}

</script>
