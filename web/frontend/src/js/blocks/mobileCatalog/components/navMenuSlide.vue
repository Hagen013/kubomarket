<template>
    <div class="nav-menu-slide"
    >
        <div class="nav-menu__header">
            <div class="nav-menu__control nav-menu__control_back">
                <div class="button_round" @click="previous">
                    <span class="icon icon_chevron-left"></span>
                </div>
            </div>
            <div class="nav-menu__title">
                {{title}}
            </div>
            <div class="nav-menu__control nav-menu__control_close" @click="hide">
                <div class="button_round">
                    <span class="icon icon_close"></span>
                </div>
            </div>
        </div>
        <slot>
        </slot>
    </div>
</template>

<script>
export default {
    name: 'nav-menu-slide',
    props: {
        title: String,
    },
    methods: {
        show() {

        },
        hide() {
            this.$emit('hide');
        },
        previous() {
            this.$emit('hide');
        }
    }
}
</script>