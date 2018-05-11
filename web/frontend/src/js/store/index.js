import { Vuex } from '../vue.js';
import createLogger from 'vuex/dist/logger';

import createPersistedState from 'vuex-persistedstate';
import Cookies from 'js-cookie';

import showModal from './modules/show-modal.js';

import cart from './modules/cart.js';
import geo from './modules/geo.js';
import delivery from './modules/delivery.js';
import customer from './modules/customer.js';
import admin from './modules/admin.js';
import facetes from './modules/facetes.js';
import payment from './modules/payment.js';

export default new Vuex.Store({
    modules: {
        showModalCallback: showModal,
        showModalCityChoice: showModal,
        showOverlay: showModal,

        geo: geo,
        cart: cart,
        delivery: delivery,
        customer: customer,
        admin: admin,
        facetes: facetes,
        payment: payment
    },
    actions: {
        changeLocation({ commit, state, dispatch, }, payload) {
            // Глобальное изменение 
            let kladr = {
                city: payload.city,
                code: payload.code
            }

            // Изменение кладера в GEO
            commit('geo/changeKladr', payload);
            console.log(`New Location: ${kladr.code} - ${kladr.city}`);

            // Расчёт доставки для корзины
            dispatch('delivery/syncDelivery');
            // Очистка выбранного способа доставки

        },
        addToCart({ commit, state, dispatch }, payload) {
            dispatch('cart/add', payload).then(
                () => { dispatch('delivery/syncDelivery') },
            );
        },
        deleteFromCart({ commit, state, dispatch, getters }, payload) {
            dispatch('cart/delete', payload).then(
                () => {
                    if (!getters['cart/isCartEmpty']) {
                        dispatch('delivery/syncDelivery');
                    } else {
                        commit('delivery/clearData');
                    }
                }
            )
        },
        setQuantityInCart({ commit, state, dispatch }, payload) {
            dispatch('cart/setQuantity', payload).then(
                () => { dispatch('delivery/syncDelivery') }
            )
        },
        initAll({ commit, state, dispatch, getters }, payload) {
            Promise.all([dispatch('cart/initCart'),
            dispatch('geo/initGeo')
            ]).then(
                () => {
                    dispatch('delivery/initDelivery');
                },
                () => {
                    console.error('Невозможно загрузить данные о доставке');
                }
                )
        }
    },
    getters: {
        orderData: (state, getters) => (source) => {
            return {
                'source': source,
                'data': {
                    "geo": {
                        "city": state.geo.city,
                        "code": state.geo.code
                    },
                    "delivery": {
                        "is_mod_selected": state.delivery.isModSelected,
                        "mod": {
                            "type": state.delivery.mod.type,
                            "code": state.delivery.mod.code,
                            "price": state.delivery.mod.price,
                        }
                    },
                    "customer": {
                        "name": state.customer.name,
                        "email": state.customer.email,
                        "phone": state.customer.phone,
                        "address": getters["customer/fullAddress"]
                    },
                    "payment": {
                        "mod": state.payment.mod
                    }
                }
            }
        }
    },
    plugins: [createPersistedState({
        // key: 'storage',
        paths: [
            'geo',
            'customer',
            // 'cart',
            // 'delivery',
        ],
        storage: {
            getItem: key => Cookies.get(key),
            setItem: (key, value) => Cookies.set(key, value, { expires: 365, domain:  '.'+document.domain.split('.').slice(-2).join('.') }),
            removeItem: key => Cookies.remove(key)
        }
    }),
    // createLogger()
    ]
});

