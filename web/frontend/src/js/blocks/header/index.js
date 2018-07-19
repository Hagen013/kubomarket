import { Vue } from '../../vue.js'
import store from '../../store'
import debounce from 'debounce'
import { directive as onClickOutsideDirective } from 'vue-on-click-outside'
Vue.directive('on-click-outside', onClickOutsideDirective)

import searchList from './components/searchList.vue'


var header = new Vue({
    name: 'header',
    el: '#header',
    store,
    components: {
        "search-list": searchList
    },
    data: {
        searchBoxIsActive: true,
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
        codeMatches() {
            let codePattern = /^[0-9]*$/;
            return ( codePattern.exec(this.searchQuery) !== null ) 
        },
        searchListIsActive() {
            if ( ((this.searchQuery.length > 2) || (this.codeMatches) ) && (this.searchBoxIsActive === true)) {
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
            if ( this.codeMatches ) {
                document.location = `/search/by-code/${this.searchQuery}`;
            } else if ( this.searchQuery.length > 0 ) {
                document.location = `/search/${this.searchQuery}`;
            }
        },
        enterPressed() {
            if ( (this.searchQuery.length > 2) || (this.codeMatches) ) {
                this.searchRedirect();
            }
        },
        searchTriggered: debounce(function () {
            let apiURL = this.searchApiUrl;
            if (this.codeMatches) {
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

        },
        setSearchBoxActive() {
            this.searchBoxIsActive = true;
        },
        setSearchBoxDisabled() {
            this.searchBoxIsActive = false;
        }
    }
});
