import { Vue } from "../../vue.js"

import store from "../../store"
import priceFilter from "./components/priceFilter.vue"

import getParameterByName from "../../core/getParameterByName"
import updateQueryString from "../../core/updateQueryString"
import removeQueryParameter from "../../core/removeQueryParameter"
import debounce from "debounce"

var catalog = new Vue({
    name: "catalog",
    el: "#catalog",
    store,
    data: {
        displayBrands: false,
        currentState: null,
        possibleStates: {
             '-scoring': 0,
             'price': 1,
             '-price': 2
        },
        submitStates:{
            0: '-scoring',
            1: 'price',
            2: '-price'
        },
        categoryId: null,
        min_price: 0,
        max_price: 1000,
        pricesResponseRecieved: false,
        price_values: [0, 10000],
        showFilters: false
    },
    components: {
        "price-filter": priceFilter
    },
    created() {
        this.checkUserStatus();
        this.initializeFilters();
        this.initializeSorting();
        this.initializePriceFilter();
        this.currentQuery = location.search;
    },
    computed: {
        sortByScoring: function () {
            if (this.currentState == 0) { return true }
            return false;
        },
        sortByPrice: function () {
            if ((this.currentState == 1) || (this.currentState == 2)) { return true }
            return false;
        },
        showArrowUp: function () {
            if (this.currentState == 1) { return true }
            return false;
        },
        showArrowDown: function () {
            if (this.currentState == 2) { return true } 
        },
        sortingOption: function () {
            return this.submitStates[this.currentState];
        }
    },
    methods: {
        toggleBrands() {
            this.displayBrands = !this.displayBrands;
        },
        initializeFilters() {
            if (hasBeenFiltered) {
                this.showFilters = true;
            }
        },
        checkUserStatus() {
            if (userAdminStatus === true) {
                this.$store.commit("showPageControls/show");
            }
        },
        initializeSorting() {
            let parsedOption = getParameterByName('sort_by');
            if ( Object.keys(this.possibleStates).indexOf(parsedOption) != -1 ) {
                this.currentState = this.possibleStates[parsedOption];
            } else {
                this.currentState = 0;
            }
        },
        initializePriceFilter() {
            this.categoryId = categoryId;
            let apiPricesURL = `/api/cubes/categories/${this.categoryId}/prices/`;
            this.$http.get(apiPricesURL).then(
                response => {
                    this.handleSuccessfulPricesGetResponse(response);
                },
                response => {
                    this.handleFailedPricesGetResponse(response);
                }
            )
        },
        changeState(state) {
            if (state == 0) {
                if ( this.currentState != 0 ) {
                    this.currentState = 0;
                    this.submit();
                }
            }
            else {
                this.currentState = this.currentState == 1 ? 2 : 1;
                this.submit();
            }
        },
        submit() {
            let sortingOption = this.submitStates[this.currentState];
            let currentQuery = location.search;
            currentQuery = updateQueryString(currentQuery, 'sort_by', sortingOption);
            currentQuery = removeQueryParameter(currentQuery, 'page');
            document.location.search = currentQuery;
        },
        handleSuccessfulPricesGetResponse(response) {
            this.min_price = response.body.price__min;
            this.max_price = response.body.price__max;

            let leftValue = parseInt(getParameterByName('price__gte'));
            let rightValue = parseInt(getParameterByName('price__lte'));

            if ( isNaN(leftValue) || (typeof leftValue == undefined) ) {
                leftValue = this.min_price;
            }
            if ( isNaN(rightValue) || (typeof rightValue == undefined)) {
                rightValue = this.max_price;
            }
            if ( leftValue < this.min_price ) {
                leftValue = this.min_price;
            }
            if ( rightValue > this.max_price ) {
                rightValue = this.max_price
            }
            this.price_values = [leftValue, rightValue];
            this.pricesResponseRecieved = true;
        },
        handleFailedPricesGetResponse(response) {

        },
        priceFilterRedirect(leftValue, rightValue) {
            this.currentQuery = updateQueryString(this.currentQuery, 'price__gte', leftValue);
            this.currentQuery = updateQueryString(this.currentQuery, 'price__lte', rightValue);
            this.currentQuery = removeQueryParameter(this.currentQuery, 'page');
            document.location.search = this.currentQuery;
        },
        toggleFilters() {
            this.showFilters = !this.showFilters;
            this.refreshSlider();
        },
        refreshSlider: debounce(function() {
            this.$refs.priceFilter.refreshSlider();
        }, 10)
    }
});
