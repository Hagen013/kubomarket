import Vue from 'vue'
import { directive as onClickOutsideDirective } from 'vue-on-click-outside' 
import { mixin as onClickOutside } from 'vue-on-click-outside'
import debounce from 'debounce'

import searchList from './__search-list.vue';
import store from '../../store';

Vue.directive('on-click-outside', onClickOutsideDirective)
var pageOverlay = document.getElementById('js-page-overlay');


var headerBottom = new Vue({
    name: 'header-bottom',
    el: '#js-header-bottom',
    store,
    data: {
        searchBoxActive: false,
        overlayActive: false,
        overlayLock: false,
        searchQuery: '',
        searchApiUrl: '/api/search/?line=',
        resultsStandard: [],
        resultsAdvanced: []
    },
    components: {
        'search-list': searchList,
    },
    mixins: [onClickOutside],
    methods: {
        turnOverlayOn: function () {
            this.overlayLock = true;
            this.$store.commit("showOverlay/show");
        },
        turnOverlayOff: function () {
            this.overlayLock = false;
            this.$store.commit("showOverlay/hide");
        },
        mouseOver: function () {
            //this.$store.commit('showOverlay/toggle');
        },
        searchTriggered: debounce(function () {
            let apiURL = this.searchApiUrl;
            let codePattern = /b-247-.*[0-9].*$/;
            if ( codePattern.exec(this.searchQuery) !== null ) {
                apiURL = '/api/search/by-code/?line=';
            }
            this.$http.get(apiURL + this.searchQuery).then(
                response => {
                    this.handleSuccessfulRequest(response);
                },
                response => {
                    this.handleFailedRequest(response);
                }
            );
        }, 500),
        handleSuccessfulRequest(response) {
            this.resultsStandard = response.body['results_standard'];
            this.resultsAdvanced = response.body['results_advanced'];
        },
        handleFailedRequest(response) {

        },
        setSearchBoxActive: function () {
            this.searchBoxActive = true;
            this.$store.commit("showOverlay/show");
        },
        setSearchBoxDisabled: function () {
            if (( !this.overlayLock ) && (this.searchBoxActive)) {
                this.searchBoxActive = false;
                this.$store.commit("showOverlay/hide");
            }
        },
        searchRedirect: function () {
            let codePattern = /b-247-.*[0-9].*$/;
            if ( codePattern.exec(this.searchQuery) !== null ) {
                document.location = `/search/by-code/${this.searchQuery}`;
            } else if ( this.searchQuery.length > 0 ) {
                document.location = `/search/${this.searchQuery}`;
            }
        },
        enterTriggered: function () {
            if ( this.searchQuery.length > 2 ) {
                this.searchRedirect();
            }
        }
    },
    computed: {
        showSearchList: function () {
            if (( this.searchQuery.length > 2 ) && ( this.searchBoxActive )) {
                return true
            }
            return false
        }
    }
});