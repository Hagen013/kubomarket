<template>
    <transition name="modal">
        <div class="modal" @click.self="$emit('close')">
            <div class="modal__default-content" :class="sizesStyleName">
                <div class="modal__close bold" @click="$emit('close')"></div>
                <div class="modal__title bold">{{title}}</div>
                <slot>hello</slot>
            </div>
        </div>
    </transition>
</template>

<script>

export default {
    name: 'modal',
    props: [
        'title',
        'sizesStyleName'
    ],
}

</script>
