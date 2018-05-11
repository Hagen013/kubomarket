export default {
    namespaced: true,
    state: function(){
        return {
            isShowModal: false
        }
    },
    mutations: {
        show(state) {
            state.isShowModal = true;
        },
        hide(state) {
            state.isShowModal = false;
        },
        toggle(state) {
            state.isShowModal = !state.isShowModal;
        }
    }
};