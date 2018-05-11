<template>
    <div class="multichoice-field">
    </div>
</template>

<script>
    export default {
        name: 'multichoice-field',
        data: () => ({
        }),
        created() {
        },
        computed: {
        },
        methods: {
        }
    }
</script>

<style lang="scss" scoped>


    .fade {
        opacity: 1 !important;
        transition: opacity 1s
    }
    .fade-fast, .fadeFast {
        opacity: 1 !important;
        transition: opacity 0.2s
    }
    .fade-fast-enter-active, .fade-fast-leave-active{
        transition: opacity 0.2s
    }
    .fade-enter-active, .fade-leave-active{
        transition: opacity 1s
    }
    .fade-enter, .fade-leave-to, 
    .fade-fast-enter, .fade-fast-leave-to  {
        opacity: 0
    }
</style>