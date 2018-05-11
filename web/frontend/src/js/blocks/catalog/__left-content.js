import { Vue } from '../../vue.js';

import priceFilter from './__price-filter.vue';

import updateQueryString from '../../core/updateQueryString'
import getParameterByName from '../../core/getParameterByName'
import removeQueryParameter from '../../core/removeQueryParameter'
import debounce from 'debounce'


var filterController = new Vue({
    name: 'filterController',
    el: '#js-catalog__left-content',
    components: {
        'price-filter': priceFilter,
    },
    data: {
        loading: true,
        currentCategoryUrl: '',
        currentCategoryId: null,
        currentQuery: '',
        currentFilterString: '',
        activeVendorFilters: [],
        recievedFilters: [],
        min_price: null,
        max_price: null,
        price_values: [0, 10000],
        filterResponseRecieved: false,
        pricesResponseRecieved: false,
        showMenu: false,
    },
    computed: {
        filtersReady() {
            return ( this.pricesResponseRecieved && this.filterResponseRecieved );
        },
        sortedFilters() {
            return this.recievedFilters.sort(function( a, b ) {
                let A = a['vendor'].toLowerCase();
                let B = b['vendor'].toLowerCase();
                if (A < B) {
                    return -1;
                }
                if (A > B) {
                    return 1
                }
                return 0;
            })
        }
    },
    created: function () {
        let vendorList = getParameterByName('vendor');
        this.currentCategoryId = document.getElementsByClassName('catalog')[0].id;
        let leftValue = parseInt(getParameterByName('price__gte'));
        let rightValue = parseInt(getParameterByName('price__lte'));
        let apiPricesURL = `/api/cubes/categories/${this.currentCategoryId}/prices/`;
        let apiFiltersURL = `/api/cubes/categories/${this.currentCategoryId}/filters/?price__gte=${leftValue}&price__lte=${rightValue}`;
        this.currentQuery = location.search;

        if ( vendorList != null ) {
            this.activeVendorFilters = vendorList.split(',')
        }

        this.$http.get(
            apiPricesURL)
            .then(response => {
                this.getPrices(response.body);
            });
        
        this.$http.get(
            apiFiltersURL)
            .then(response => {
                this.getFilters(response.body);
            });
    },
    methods: {
        getPrices(response) {
            this.min_price = response.price__min;
            this.max_price = response.price__max;

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
        getFilters(response) {
            let recievedFilters = [];
            for (let key in response) {
                let item = response[key];
                if (this.activeVendorFilters.indexOf(item.vendor) > -1) {
                    item.active = true;
                } else {
                    item.active = false;
                }
                recievedFilters.push(response[key]);
            }
            this.recievedFilters = recievedFilters;
            this.filterResponseRecieved = true;
        },
        brandFilterRedirect(item) {
            item.active = item.active ? false : true;
            this.currentQuery = removeQueryParameter(this.currentQuery, 'page');
            this.currentQuery = removeQueryParameter(this.currentQuery, 'price__gte');
            this.currentQuery = removeQueryParameter(this.currentQuery, 'price__lte');

            let currentActiveFilters = []
            let newFilterQuery = '';

            for (let i=0; i<this.sortedFilters.length; i++ ) {
                let filter = this.sortedFilters[i];
                if ( filter.active ) {
                    currentActiveFilters.push(filter.vendor);
                }
            }

            if ( currentActiveFilters.length > 0 ) {
                newFilterQuery += `${currentActiveFilters.join(',')}`;
                this.currentQuery = updateQueryString(this.currentQuery, 'vendor', newFilterQuery);
            } else {
                this.currentQuery = '';
            }

            document.location = `${this.currentCategoryUrl}${this.currentQuery}`

        },
        priceFilterRedirect(leftValue, rightValue) {
            this.currentQuery = updateQueryString(this.currentQuery, 'price__gte', leftValue);
            this.currentQuery = updateQueryString(this.currentQuery, 'price__lte', rightValue);
            this.currentQuery = removeQueryParameter(this.currentQuery, 'page');
            document.location.search = this.currentQuery;
        },
        toggleMenu() {
            this.showMenu = this.showMenu == false ? true : false;
            this.refreshSlider();            
        },
        refreshSlider: debounce(function() {
            this.$refs.priceFilter.refreshSlider();
        }, 230)
    }
})