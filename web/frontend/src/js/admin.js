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

import syncOffers from './admin/main/main.vue'
import syncAttributes from './admin/sync-attributes/sync-attributes.vue'
import syncImages from './admin/sync-images/sync-images.vue'
import uploadOffers from './admin/upload-offers/upload-offers.vue'

import store from './store';


const routes = [
    { path: '/offers', component: syncOffers },
    { path: '/attributes', component: syncAttributes },
    { path: '/images', component: syncImages },
    { path: '/upload', component: uploadOffers }
  ]
  
const router = new VueRouter({
    routes
})

var app = new Vue({
    name: 'app',
    el: '#app',
    store,
    router,
    data: {
        menuVisible: false,
        routerState: 1,
    },
    components: {
        'sync-offers': syncOffers,
        'sync-attributes': syncAttributes
    },
    methods: {
        toggleMenu () {
            this.menuVisible = !this.menuVisible
        },
        route(arg) {
            router.push({ path: arg })
        },
        hideNavigation() {
            if ( this.menuVisible ) {
                this.menuVisible = false;
            }
        }
    }
})

router.replace({ path: '/upload', redirect: '*' })
