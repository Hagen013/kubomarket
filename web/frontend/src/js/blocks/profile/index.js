import { Vue } from '../../vue.js';
import store from '../../store'


var profile = new Vue({
    name: 'profile',
    el: '#profile',
    store,
    data: {
    },
    created() {
        console.log("created");
    },
    components: {
    },
    computed: {
    },
    methods: {
    }
});