
import { Vue, Vuex, VueResurse } from '../../vue.js';


function getPointByCode(selected_code, points) {
    let [code, type] = selected_code.split("__");
    return points[{"pick_point_point": "pick_point_points",
                   "sdek_point": "sdek_points"
                  }[type]].find(
                      element => element.code == code
                  );
}

// Модуль доставки
// Ожидается что для работы с ним должны быть 
// Готовы модули корзины и гео
export default {
    namespaced: true,
    state: {
        isDataInited: false,
        data: {},
        isModSelected: false,
        mod: {
            type: null,
            code: null,
            price: null,
        },
        notes: ""
        // необходимо в автоселект
    },
    mutations: {
        ready(state) {
            state.isDataInited = true;
        },
        notReady(state) {
            state.isDataInited = false;
        },
        clearData(state, payload) {
            isDataInited: false,            
            state.data = {};
            state.isModSelected = false;
            state.mod = {type: null,
                         code: null,
                         price: null}
            state.notes = ""
        },
        getData(state, payload) {
            state.data = payload;
        },
        clearMod(state) {
            state.isModSelected = false;
            state.mod = {type: null,
                         code: null,
                         price: null}
                         
        },
        selectCurierMod(state, payload) {
            state.mod = {type: "curier",
                         code: null,
                         price: state.data.curier.price !== null ? state.data.curier.price : null};
            state.isModSelected = true;
        },
        selectPostalServiceMod(state, payload) {
            state.mod = {type: "postal_service",
                         code: null,
                         price: state.data.postal_service.price !== null ? state.data.postal_service.price : ""};
            state.isModSelected = true;
        },
        selectDeliveryPointsMod(state, payload) {
            let price = getPointByCode(`${payload.code}__${payload.type}`, state.data.points).price;
            state.mod = {type : "delivery_points",
                         code: `${payload.code}__${payload.type}`,
                         price: price !== null ? price: null};
            state.isModSelected = true;
        },
        setNotes(state, payload) {
            state.notes = payload;
        }
    },
    actions: {
        initDelivery({ state, commit, dispatch }, payload) {
            return new Promise((resolve, reject) => {
                console.log('initDelivery');
                if (!state.isDataInited) {
                    dispatch('syncDelivery').then(resolve, reject);
                } else {
                    console.log('Delivery already inited');                    
                    resolve();
                }
            });
        },
        syncDelivery({ commit, state, dispatch, getters }) {
            commit('notReady');
            commit('clearData');
            commit('clearMod');
            return new Promise((resolve, reject) => {
                console.log(getters['deliveryRequestData']);
                if (getters['isCartEmpty']) {
                    Vue.http.post(
                        `${GEO_IP_HOST}/api/delivery/meny_products/`,
                        getters['deliveryRequestData']
                    ).then(
                        (response) => {
                            commit('getData', response.body);
                            commit('ready');
                            console.log('Delivery inited');
                            resolve();
                        },
                        (response) => {
                            commit('clearData');
                            commit('notReady');
                            console.log('Невозможно получить данные о доставке');
                            reject();
                        });
                } else {
                    commit('clearData');
                    commit('ready');
                    resolve();
                }
            });
        },
        autoSelectMod({ commit, state, dispatch, getters }) {
            // 1. Если доступен тот, который был, то использовать его,

            // 2. Если доступен только 1 способ, то использовать его
            // TODO сделать карент таб компьютедом, настроитьт геттер и сеттер
            // 
        }
    },
    getters: {
        isCartEmpty: (state, getters, rootState, rootGetters) => {
            return rootGetters['cart/isCartEmpty'];
        },
        deliveryRequestData: (state, getters, rootState, rootGetters) => {
            if (rootState.geo.isDataInited && rootState.cart.isDataInited) {
                if (rootState.cart.items_quantiy !== 0) {
                    return {
                        'kladr': rootState.geo.code,
                        'products': Object.keys(
                            rootState.cart.items
                        ).map(key => rootState.cart.items[key].data_for_delivery)
                    }
                }
                else {
                    return {
                        'kladr': rootState.geo.code,
                        'products': [{
                            price: 2000,
                            product_type: "CUBE",
                            purchase_price: 0,
                            vendor: "kubomarket"
                        }]
                    }
                }
            } else {
                return undefined;
            }
        },
        isAvailable: (state, getters, rootState, rootGetters) => {
            return Object.keys(state.data).length !== 0;
        },
        isCurierAvailable: (state, getters, rootState, rootGetters) => {
            if (state.isDataInited) {
                if (getters['isAvailable']) {
                    return state.data.curier !== null;
                } else {
                    return false;
                }
            } else {
                return undefined;
            }
        },
        isPostalServiceAvailable: (state, getters, rootState, rootGetters) => {
            if (state.isDataInited) {
                if (getters['isAvailable']) {
                    return state.data.postal_service !== null;
                } else {
                    return false;
                }
            } else {
                return undefined;
            }
        },
        isPointsAvailable: (state, getters, rootState, rootGetters) => {
            if (state.isDataInited) {
                if (getters['isAvailable']) {
                    return state.data.delivery_point !== null;
                } else {
                    return false;
                }
            } else {
                return undefined;
            }
        },
        curentSelectedPoint: (state, getters, rootState, rootGetters) => {
            if (state.isDataInited && state.isModSelected && state.mod.code) {
                return getPointByCode(state.mod.code, state.data.points);
            } else {
                return undefined;
            }
        }
    }
}