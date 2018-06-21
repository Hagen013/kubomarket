<template>
    <div class="page-controls">
        <div class="page-controls__button page-controls__edit-bitton"
            @click="showEditForm"
        >
            <i class="icon icon_edit"></i>
        </div>
    </div>
</template>

<script>
import store from "../../../store";

export default {
    name: "pageControls",
    store,
    data: () => ({
    }),
    methods: {
        showEditForm() {
            this.$store.commit("showProductPageEditForm/show");
        }
    }
}
</script>