import Vue from 'vue'

import slide from './__slide.vue'

var siteSlider = new Vue({
    name: 'site-slider',
    el: '#js-site-slider',
    data: {
        currentSlide: 0,
        autoPlayTimeout: 3000,
        autoplayInterval: null,
        sliderReady: false
    },
    components: {
        'slide': slide,
    },
    methods: {
        changeSlide(slide_index) {
            if ( this.currentSlide != slide_index ) {
                this.currentSlide = slide_index;
            }
        },
        showPrevSlide() {
            if ( this.currentSlide == 0 ) {
                this.currentSlide = 2;
            } else {
                this.currentSlide --;
            }
        },
        showNextSlide() {
            if ( this.currentSlide == 2 ) {
                this.currentSlide = 0;
            } else {
                this.currentSlide ++;
            }
        },
        startAutoPlay: function () {
            this.autoplayInterval = setInterval(this.showNextSlide, this.autoPlayTimeout);
        },
        pauseAutoplay: function () {
            if (this.autoplayInterval) {
                this.autoplayInterval = clearInterval(this.autoplayInterval);
            }
        }
    },
    mounted: function() {
        this.$el.addEventListener("mouseenter", this.pauseAutoplay)
        this.$el.addEventListener("mouseleave", this.startAutoPlay)
        this.startAutoPlay();
        this.sliderReady = true;
    }
});