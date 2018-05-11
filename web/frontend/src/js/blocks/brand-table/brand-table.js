import { Vue } from '../../vue.js';


var brandTableController = new Vue({
    name: 'brandTableController',
    el: '#js-brand-table',
    data: {
        state: 0
    },
    methods: {
        switchState: function (newState) {
            if ( this.state != newState ) {
                this.state = newState;
            }
        }
    },
    computed: {
        showLeft: function () {
            if ( this.state == 0 ) {
                return true;
            }
            return false;
        },
        showRight: function () {
            if ( this.state == 1 ) {
                return true;
            }
        }
    }
});