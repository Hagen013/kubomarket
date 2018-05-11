<template>
    <transition name="fade-fast">
        <div class="page-overlay-mask"
            v-if="showOverlay"
        >
        </div>
    </transition>
</template>
<script>
import store from '../../store';

export default {
    name: 'page-overlay',
    store,
    data: function() {
        return {

        }
    },
    computed: {
        showOverlay() {
            return this.$store.state.showOverlay.isShowModal;
        }
    }
}
</script>
