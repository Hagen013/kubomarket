<template>
    <md-content>
        <div class="md-layout">
            <div class="md-layout-item">
                <upload-card
                    upload_url='/controls/upload/'
                >
                </upload-card>
            </div>
            <div class="md-layout-item">
                <download-card
                    download_url='/controls/download/'
                    download_status_url='/controls/download/status/'
                >
                </download-card>
            </div>
        </div>
    </md-content>
</template>

<script>
    import uploadCard from './upload-card.vue'
    import downloadCard from './download-card.vue'

    import store from './../../store';

    export default {
        name: 'sync-offers',
        store,
        components: {
            'upload-card': uploadCard,
            'download-card': downloadCard,
        },
        data: () => ({
            componentTitle: 'Остатки'
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