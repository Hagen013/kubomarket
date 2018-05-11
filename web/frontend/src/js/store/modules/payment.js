export default {
    namespaced: true,
    state: function () {
        return {
            mod: "cash",
            available_mods: [
                "cash",
                "card_upon_receipt",
                "card",
            ]
        }
    },
    mutations: {
        set_mod(state, payload) {
            if (state.available_mods.includes(payload)) {
                state.mod = payload;
            } else {
                throw new Error("invalid payload value");
            }
        },
    }
};