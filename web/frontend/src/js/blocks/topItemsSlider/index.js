import { Vue } from '../../vue.js';


var topItemsSlider = new Vue({
    name: 'top-items-slider',
    el: '#top-items-slider',
    data: {
        currentItem: 1
    },
    computed: {
        isNextAvailable() {
            return (this.currentItem < 3)
        },
        isPreviousAvailable() {
            return (this.currentItem > 1)
        }
    },
    methods: {
        setCurrentItem(itemId) {
            this.currentItem = itemId;
        },
        next() {
            if (this.isNextAvailable) {
                this.currentItem += 1;
            }
        },
        previous() {
            if (this.isPreviousAvailable) {
                this.currentItem -= 1;
            }
        }
    }
});
