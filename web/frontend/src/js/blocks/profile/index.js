import { Vue } from '../../vue.js';

import profileComponent from "./components/profile.vue"


var profile = new Vue({
    name: 'profile',
    el: '#profile',
    data: {
    },
    components: {
        "profile": profileComponent
    },
    created() {
        console.log("created");
    },
    computed: {
    },
    methods: {
    }
});