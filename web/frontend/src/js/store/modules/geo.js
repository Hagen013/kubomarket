import {Vue, Vuex, VueResurse} from '../../vue.js'


export default {
    namespaced: true,
    state: {
        isDataInited: false,
        code: "7700000000000",
        city: "Москва",
    },
    mutations: {
        ready(state, payload){
            state.isDataInited = true;
        },
        notReady(state, payload){
            state.isDataInited = false;
        },
        changeKladr(state, payload) {
            let kladrValidator = /(\d{13})|(\d{17})|(\d{19})/
            if (kladrValidator.test(payload.code)) {
                state.code = payload.code;
                state.city = payload.city;
            } else {
                state.code = "7700000000000";
                state.city = "Москва";
                throw new Error("Неверный кладер | changeKladr");
            }
        },
    },
    actions: {
        initGeo({ state, commit, dispatch }, payload) {
            return new Promise((resolve, reject) => {
                    if(!state.isDataInited) {
                        return dispatch('getKladr');
                    } else {
                        resolve();
                    }
                }
            );
        },
        getKladr({ state, commit, dispatch }, payload) {
            return new Promise((resolve, reject) => {
                commit('notReady');             
                Vue.http.get(`${GEO_IP_HOST}/api/geo_ip/`).then(
                    response => {
                        // Колбэк на успех
                        if (response.ok) {
                            commit('changeKladr',
                                {
                                    code: response.body.kladr_code,
                                    city: response.body.kladr_name,
                                }
                            );
                            commit('ready');
                            //console.log('initCart finish');                                                    
                            resolve();
                        } else {
                            reject();
                        }
                    },
                    response => {
                        // Колбэк на провал
                        reject();
                    }
                );
            });
        }
    }
};
