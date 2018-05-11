import { Vue } from '../../vue.js';

import getParameterByName from '../../core/getParameterByName'
import updateQueryString from '../../core/updateQueryString'
import removeQueryParameter from '../../core/removeQueryParameter'

import filterItem from './filterItem.vue'
import store from '../../store'


var filtersController = new Vue({
    el: '#js-filters',
    data: {
    },
    store,
    components: {
        'filterItem': filterItem
    },
    beforeCreate() {
        let nodeValues = NODE_VALUES.replace(/&#34;/g, '"');
        nodeValues = JSON.parse(nodeValues);
        for (let i=0; i<nodeValues.length; i++) {
            let item = nodeValues[i];
            let payload = {
                "key": item.key,
                "value": item.id
            }
            this.$store.commit("facetes/addActiveOption", payload);
            this.$store.commit("facetes/addBaseOption", payload);
        }
    },
    methods: {
    }
})
