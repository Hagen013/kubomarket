import {Vue, Vuex, VueResurse} from './vue.js'
import VueMaterial from 'vue-material'
import VueRouter from 'vue-router'
import 'vue-material/dist/vue-material.min.css'
import 'vue-material/dist/theme/default.css'
import 'vue-animate/dist/vue-animate.min.css'
import { directive as onClickOutsideDirective } from 'vue-on-click-outside' 

Vue.use(VueMaterial)
Vue.use(VueRouter)
Vue.directive('on-click-outside', onClickOutsideDirective)

import store from './store';

import app from './md-admin/app.vue'

const routes = [

  ]
  
const router = new VueRouter({
    routes
})

var appContainer = new Vue({
    name: 'app-container',
    el: '#app-container',
    store,
    router,
    data: {
    },
    components: {
        'app': app,
    },
    created: function () {
    },
    mounted: function () {
    },
    methods: {
    }
})

// router.replace({ path: '/upload', redirect: '*' })
