<template>
    <div class="modal"
        @click.self="close"
    >
        <div class="modal__content">
            <div class="purchase-modal__close button_round"
                @click="close"
            >
                <i class="icon icon_close"></i>
            </div>
            <div class="modal__title title_single">
                Спасибо за вашу подписку!
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'subscribe-modal',
    data: function () {
        return {}
    },
    methods: {
        close() {
            this.$store.commit("showSubscribeModal/hide");
        }
    },
    components: {
    }
}
</script>


<style lang="scss" scoped>
    .title_single {
        margin: 64px 0px;
    }
</style>