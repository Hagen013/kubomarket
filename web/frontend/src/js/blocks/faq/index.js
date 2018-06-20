import { Vue } from '../../vue.js'


var faqController = new Vue({
    name: 'faq',
    el: '#faq',
    data: {
    },
    computed: {
    },
    methods: {
        showItemContent() {
            let element = event.target.parentElement;
            console.log(element);
            element.classList.toggle('accordion__item_active')
        }
    },
});
