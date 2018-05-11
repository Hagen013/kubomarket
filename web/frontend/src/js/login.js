import {Vue, Vuex, VueResurse} from './vue.js'
import VueMaterial from 'vue-material'
import 'vue-material/dist/vue-material.min.css'
import 'vue-material/dist/theme/default.css'

import loginForm from './md-admin/loginForm.vue'

Vue.use(VueMaterial)


var appContainer = new Vue({
    name: 'app-container',
    el: '#app-container',
    components: {
        "login-form": loginForm
    },
    data: {
    },
    methods: {
    }
})


