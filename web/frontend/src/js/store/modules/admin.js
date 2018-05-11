export default {
    namespaced: true,
    state: function(){
        return {
            appTitle: 'Администрирование kubomarket.ru',
        }
    },
    mutations: {
        changeAppTitle(state, payload) {
            state.appTitle = payload;
        },
    }
};