<template>
    <md-content>
        <div class="md-layout">
            <div class="md-layout-item">
                <upload-card
                    upload_url="/controls/upload-offers/"
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
        name: 'upload-offers',
        store,
        components: {
            'upload-card': uploadCard
        },
        data: () => ({
            componentTitle: 'Новые товары'
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