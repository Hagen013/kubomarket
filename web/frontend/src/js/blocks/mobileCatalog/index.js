import { Vue } from '../../vue.js';
import { setTimeout } from 'timers';
import navMenuSlide from './components/navMenuSlide.vue'

import store from '../../store'


var navMenu = new Vue({
    name: 'nav-menu',
    el: '#nav-menu',
    store,
    components: {
        "nav-menu-slide": navMenuSlide
    },
    data: {
        isActive: false,
        activeSlide: 0,
    },
    computed: {
        isVisible() {
            return this.$store.state.mobileCatalog.active;
        }
    },
    methods: {
        hideNavMenu() {
            document.body.style.overflow='auto';
            this.$store.commit("mobileCatalog/hide");
        },
        showSlide(slideNumber) {
            this.activeSlide = Number(slideNumber);
        },
        setActiveSlideToDefault() {
            this.activeSlide = 0;
        }
    },
    watch: {
        isVisible: function () {
            let navMenuSelector = document.getElementById('nav-menu');
            if ( this.isVisible ) {
                document.body.style.overflow='hidden';
                navMenuSelector.style.transform = 'translate3d(0,-100%,0)';
            } else {
                navMenuSelector.style.transform = 'none';
                setTimeout(function () {
                    document.body.style.overflow='auto';
                }, 300)
            }
        }
    }
})