export default {
    namespaced: true,
    state: function(){
        return {
            isOverlayActive: false
        }
    },
    mutations: {
        show(state) {
            state.isOverlayActive = true;
        },
        hide(state) {
            state.isOverlayActive = false;
        }
    }
};