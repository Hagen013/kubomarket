<template>
    <md-toolbar class="md-primary">
        <md-button class="md-icon-button" @click="showNavigation">
            <md-icon>menu</md-icon>
        </md-button>
        <span class="md-title">Администирование kubomarket.ru</span>
    </md-toolbar>
</template>

<script>
    import store from '../../store';

    export default {
        name: 'app-header',
        store,
        data: () => ({
        }),
        components: {
        },
        methods: {
            showNavigation() {
                //console.log('Show navigation triggered');
            }
        }
    }
</script>

<style lang="scss" scoped>
</style>