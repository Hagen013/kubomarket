export default {
    namespaced: true,
    state: function () {
        return {
            mod: "cash",
            available_mods: [
                "cash",
                "card_on_receipt",
                "card",
            ]
        }
    },
    mutations: {
        setMethod(state, payload) {
            if (state.available_mods.includes(payload)) {
                state.mod = payload;
            } else {
                throw new Error("invalid payload value");
            }
        },
    }
};
