export default {
    namespaced: true,
    state: function(){
        return {
            active: false
        }
    },
    mutations: {
        show(state) {
            state.active = true;
        },
        hide(state) {
            state.active = false;
        },
        toggle(state) {
            state.active = !state.active;
        }
    }
};