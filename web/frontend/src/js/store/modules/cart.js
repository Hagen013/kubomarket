
import {Vue, Vuex, VueResurse} from '../../vue.js'

// Модуль корзины
export default {
    namespaced: true,
    state:{        
        isDataInited: false,
        // Сериализация API корзины
        
        created_at: undefined,
        modified_at: undefined,
        total_price: undefined,
        items_quantiy: undefined,
        items: {},
    },
    mutations:{
        ready(state){
            state.isDataInited = true;
        },
        notReady(state){
            state.isDataInited = false;
        },
        getData(state, payload) {
            // Синхронизация даных
            state.created_at = Date.parse(payload.created_at);
            state.modified_at = Date.parse(payload.modified_at);
            state.total_price = payload.total_price;
            state.items_quantiy = payload.items_quantiy;
            state.items = payload.items;
        },
        clearData(state, payload) {
            // Обнуление данных
            state.isDataInited = false;            
            state.created_at = undefined;
            state.modified_at = undefined;
            state.total_price = undefined;
            state.items_quantiy = undefined;
            state.items = {};
        }
    },
    actions: {
        initCart({ state, commit, dispatch }, payload) {
            return new Promise((resolve, reject) => {
                console.log('initCart');
                if(!state.isDataInited){
                    return dispatch('syncCart').then(resolve, reject);
                }else{
                    console.log('Cart already inited');
                    resolve();
                }
            });
        },
        syncCart({commit, state, dispatch}) {
            return new Promise((resolve, reject) => {
                commit('notReady');
                commit('clearData');
                Vue.http.get('/api/cart/').then(
                    response => {
                        //колбэк успеха
                        commit('getData', response.body)
                        commit('ready');
                        console.log('initCart inited');                        
                        resolve();
                    },
                    response => {
                        reject();
                    }
                );

            });
        },
        add({commit, state, dispatch}, payload) {
            return new Promise((resolve, reject) => {
                Vue.http.put(`/api/cart/items/${payload.offer_identifier}/`).then(
                    response => {
                        dispatch('syncCart').then(resolve, reject);
                    },
                    response => {
                        console.error(`Can not add item ${payload.offer_identifier}`);
                        dispatch('syncCart').then(reject, reject);
                    }
                );
            });
        },
        delete({commit, state, dispatch}, payload) {
            return new Promise((resolve, reject) => {
                Vue.http.delete(`/api/cart/items/${payload.offer_identifier}/`).then(
                    response => {
                        dispatch('syncCart').then(resolve, reject);
                    },
                    response => {
                        console.error(`Can not delete item ${payload.offer_identifier}`);
                        dispatch('syncCart').then(reject, reject);
                    }
                );
            });
        },
        clear({commit, state, dispatch}) {
            return new Promise((resolve, reject) => {
                Vue.http.delete(`/api/cart/items/`).then(
                    response => {
                        dispatch('syncCart').then(resolve, reject);
                    },
                    response => {
                        console.error(`Can not delete items`);
                        dispatch('syncCart').then(reject, reject);
                    }
                );
            });
        },
        setQuantity({commit, state, dispatch}, payload) {
            return new Promise((resolve, reject) => {
                Vue.http.post(`/api/cart/items/${payload.offer_identifier}/`, { quantity: payload.quantity }).then(
                    response => {
                        //колбэк успеха
                        dispatch('syncCart').then(resolve, reject);                        
                    },
                    response => {
                        //колбэк провала
                        console.error(`Can not setQuantity item ${payload.offer_identifier}`);                    
                        dispatch('syncCart').then(reject, reject);
                    },
                );
            });
        }
    },
    getters: {
        isCartEmpty: state => {
            if (state.isDataInited) {
                return Object.keys(state.items).length == 0;
            } else {
                return undefined;
            }
        },
        sortedItemsArray: state => {
            if (state.isDataInited) {
                let result = [];
                for (let offer_identifier in state.items) {
                    let item = state.items[offer_identifier];
                    item['offer_identifier'] = offer_identifier;
                    item['added_at'] = Date.parse(item['added_at']);

                    result.push(item);
                }
                result.sort(function (a, b) {
                    return a['added_at'] > b['added_at'] ? 1 : -1
                });
                return result;
            } else {
                return undefined;
            }
        }        
    }
}