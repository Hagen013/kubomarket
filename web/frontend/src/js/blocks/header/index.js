import { Vue } from '../../vue.js'
import store from '../../store'
import debounce from 'debounce'

import searchList from './components/searchList.vue'


var header = new Vue({
    name: 'header',
    el: '#header',
    store,
    components: {
        "search-list": searchList
    },
    data: {
        searchQuery: "",
        searchApiUrl: '/api/search/?line=',
        resultsStandard: [],
        resultsAdvanced: []
    },
    computed: {
        mobileMenuIsVisible() {
            return this.$store.state.mobileMenu.active
        },
        isShowModalCityChoice(){
            return this.$store.state.showModalCityChoice.isShowModal;
        },
        isCartReady(){
            return this.$store.state.cart.isDataInited;            
        },
        cartTotalQuantity(){
             return this.$store.state.cart.items_quantiy;
        },
        isGeoReady() {
            return this.$store.state.geo.isDataInited;
        },
        cityName() {
            return this.$store.state.geo.city;
        },
        searchListIsActive() {
            if ( this.searchQuery.length > 2 ) {
                return true
            }
            return false    
        }
    },
    mounted() {

    },
    methods: {
        showMobileMenu() {
            this.$store.commit("mobileMenu/show");
        },
        hideCityChoiceModal() {
            this.$store.commit('showModalCityChoice/hide');
        },
        showCityChoiceModal() {
            this.$store.commit('showModalCityChoice/show');
        },
        searchRedirect() {
            let codePattern = /b-247-.*[0-9].*$/;
            if ( codePattern.exec(this.searchQuery) !== null ) {
                document.location = `/search/by-code/${this.searchQuery}`;
            } else if ( this.searchQuery.length > 0 ) {
                document.location = `/search/${this.searchQuery}`;
            }
        },
        enterPressed() {
            if ( this.searchQuery.length > 2 ) {
                this.searchRedirect();
            }
        },
        searchTriggered: debounce(function () {
            let apiURL = this.searchApiUrl;
            let codePattern = /b-247-.*[0-9].*$/;
            if ( codePattern.exec(this.searchQuery) !== null ) {
                apiURL = '/api/search/by-code/?line=';
            }
            this.$http.get(apiURL + this.searchQuery).then(
                response => {
                    this.handleSuccessfulSearchRequest(response);
                },
                response => {
                    this.handleFailedSearchRequest(response);
                }
            );
        }, 500),
        handleSuccessfulSearchRequest(response) {
            this.resultsStandard = response.body['results_standard'];
            this.resultsAdvanced = response.body['results_advanced'];
        },
        handleFailedSearchRequest(response) {

        }
    }
});
