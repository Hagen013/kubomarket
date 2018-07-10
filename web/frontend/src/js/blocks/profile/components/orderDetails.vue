<template>
    <div class="order-details">
        <div class="order-details__top">
            <div class="order__status">
                {{order.state}}
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "order-details",
    data: () => ({
    }),
    props: [
        "order"
    ],
    methods: {
        backToList() {
            this.emit("back")
        }
    }
}
</script>