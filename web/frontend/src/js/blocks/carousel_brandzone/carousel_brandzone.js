import { Vue } from '../../vue.js';
import Carousel from '../carousel/Carousel.vue';
import Slide from '../carousel/Slide.vue';

var carouselNewestItems = new Vue({
    name: 'carousel',
    el: '#js-carousel-brandzone',
    components: {
        Carousel,
        Slide
    }
});