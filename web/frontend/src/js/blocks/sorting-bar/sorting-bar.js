import { Vue } from '../../vue.js';

import getParameterByName from '../../core/getParameterByName'
import updateQueryString from '../../core/updateQueryString'
import removeQueryParameter from '../../core/removeQueryParameter'

var sortingFormController = new Vue({
    el: '#js-catalog-sorting',
    data: {
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
        showIncomplete: true
    },
    created: function () {
        let parsedOption = getParameterByName('sort_by');
        let parsedCompleteOption = getParameterByName('incomplete');
        if ( Object.keys(this.possibleStates).indexOf(parsedOption) != -1 ) {
            this.currentState = this.possibleStates[parsedOption];
        } else {
            this.currentState = 0;
        }
        if (parsedCompleteOption === 'false') {
            this.showIncomplete = false;
        } else {
            this.showIncomplete = true;
        }
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
        changeState(state) {
            if (state == 0) {
                if ( this.currentState != 0 ) {
                    this.currentState = 0;
                    this.formSumbit();
                }
            }
            else {
                this.currentState = this.currentState == 1 ? 2 : 1;
                this.formSumbit();
            }
        },
        formSumbit() {
            let sortingOption = this.submitStates[this.currentState];
            let currentQuery = location.search;
            currentQuery = updateQueryString(currentQuery, 'sort_by', sortingOption);
            currentQuery = removeQueryParameter(currentQuery, 'page');
            document.location.search = currentQuery;
        },
        toggleCompleted() {
            let currentQuery = location.search;
            if ( !this.showIncomplete ) {
                currentQuery = updateQueryString(currentQuery, 'incomplete', false);
            } else {
                currentQuery = removeQueryParameter(currentQuery, 'incomplete');
            }
            document.location.search = currentQuery;
        }
    }
})