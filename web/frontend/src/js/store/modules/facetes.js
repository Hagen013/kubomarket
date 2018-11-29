export default {
    namespaced: true,
    state: function() {
        return {
            active: {

            },
            base: {

            },
            removed: {

            },
            removedBase: {

            }
        }
    },
    mutations: {
        addActiveOption(state, payload) {
            let key = payload['key'];
            let value = payload['value'];

            if (state.active[key] === undefined) {
                state.active[key] = [value]
            } else {
                let index = state.active[key].indexOf(value);
                if (index === -1) {
                    state.active[key].push(value);
                }
            }
            console.log(state.active['key']);

            if (state.removedBase[key] !== undefined) {
                let index = state.removedBase[key].indexOf(value);
                if (index !== -1) {
                    state.removedBase[key].splice(index, 1);
                    if (state.removedBase[key].length === 0) {
                        delete state.removedBase[key];
                    }
                }
            } else if (state.removed[key] !== undefined) {
                let index = state.removed[key].indexOf(value);
                if (index !== -1) {
                    state.removed[key].splice(index, 1);
                }
                if (state.removed[key].length === 0) {
                    delete state.removed[key];
                }
            }
        },
        removeActiveOption(state, payload) {
            let key = payload['key'];
            let value = payload['value'];
            let activeBaseEqual = false;

            if (state.active[key] !== undefined) {
                let index = state.active[key].indexOf(value);
                if (index !== -1) {
                    state.active[key].splice(index, 1);
                    if (state.base[key] !== undefined) {
                        activeBaseEqual = true;
                        for (let i=0; i<state.active[key].length; i++) {
                            let value = state.active[key][i];
                            let index = state.base[key].indexOf(value);
                            if (index === -1) {
                                activeBaseEqual = false;
                                break
                            }
                        }
                    }
                    if ( (state.active[key].length === 0) || activeBaseEqual ) {
                        delete state.active[key];
                        state.removed[key] = [];
                    }
                }
            }

            if (state.base[key] !== undefined) {
                let index = state.base[key].indexOf(value);
                if (index !== -1) {
                    if (state.removedBase[key] !== undefined) {
                        let removedIndex = state.removedBase[key].indexOf(value);
                        if (removedIndex !== -1) {
                            state.removedBase[key].push(value);
                        }
                    } else {
                        state.removedBase[key] = [value]
                    }
                }
            }
        },
        addBaseOption(state, payload) {
            let key = payload['key'];
            let value = payload['value'];
            if (state.base[key] !== undefined) {
                state.base[key].push(value);
            } else {
                state.base[key] = [value,]
            }
        },
        clearField(state, payload) {
            let key = payload.key;
            if (state.active[key] !== undefined) {
                state.removed[key] = state.active[key];
                delete state.active[key];
            }
            if (state.base[key] !== undefined) {
                state.removedBase[key] = state.base[key];
                delete state.base[key];
            }
        }
    }
}
