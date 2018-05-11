<template>
    <md-content>
        <div class="md-layout">
            <div class="md-layout-item">
                <upload-card
                    upload_url="/controls/images-sync/"
                >
                </upload-card>
            </div>
            <div class="md-layout-item">
            </div>
        </div>
    </md-content>
</template>

<script>
    import uploadCard from './upload-card.vue'

    import store from './../../store';

    export default {
        name: 'sync-images',
        store,
        components: {
            'upload-card': uploadCard
        },
        data: () => ({
            componentTitle: 'Изображения'
        }),
        computed: {
        },
        created() {
            this.$store.commit('admin/changeAppTitle', this.componentTitle);
        },
        methods: {
        },
        watch: {
        }
    }
</script>

<style lang="scss" scoped>
</style>