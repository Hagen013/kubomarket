// Сторонние библиотеки
import Vue from 'vue';
import VueResource from 'vue-resource';
import Vuex from 'vuex';

import VueInputMask from './core/vue-inputmask.js'
Vue.use(VueInputMask);

// Конфигурирование

// Вшивание CSRF-токена в запросы vue-resurs
import csrfToken from './core/csrfToken';

Vue.use(VueResource);
Vue.use(Vuex);

Vue.http.headers.common['X-CSRFToken'] = csrfToken();

Vue.filter('timeFilter', function (value) {
    if(value){
        let [from_time, to_time] = value;
        if (from_time || to_time) {
            if (from_time != to_time) {
                from_time = from_time ? `от ${from_time}` : "";
                to_time = to_time ? ` до ${to_time}` : "";
                return `${from_time}${to_time} дней`;
            } else {
                if (from_time == 1) {
                    return `от 1 дня`;
                } else {
                    return `от ${from_time} дней`;
                }
            }
        } else {
            return "неизвестно";
        }
    }else{
        return "неизвестно";
    }
});

Vue.filter('priceFilter', function (value) {
    if(value === undefined || value === null){
        return "неизвестно";
    }else{
        if (value == 0){
            return "бесплатно";
        }else{
            return `${value} ₽`;
        }
    }
});

export {
    Vue,
    VueResource,
    Vuex,
}