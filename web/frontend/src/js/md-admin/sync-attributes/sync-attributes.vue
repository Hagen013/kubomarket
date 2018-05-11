<template>
    <md-content>
        <div class="md-layout">
            <div class="md-layout-item">
                <upload-card
                    upload_url="/controls/attrbiute-values/upload/"
                >
                </upload-card>
            </div>
            <div class="md-layout-item">
            </div>
        </div>
    </md-content>
</template>

<script>
    import store from './../../store';

    import uploadCard from './upload-card.vue'

    export default {
        name: 'sync-attributes',
        components: {
            'upload-card': uploadCard
        },
        data: () => ({
            componentTitle: 'Атрибуты'
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