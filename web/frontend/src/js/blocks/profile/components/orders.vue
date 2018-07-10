<template>
    <div class="orders">
        <div class="orders__content" v-if="recieved">
            <orders-list
                v-if="ordersListActive"
                :orders="orders"
                v-on:order_clicked="showOrderDetails"
            >
            </orders-list>
            <order-details
                v-if="orderDetailsActive"
                :order="currentOrder"
            >
            </order-details>
        </div>
        <div class="orders__error"
            v-else-if="dataRequestError"
        >
        </div>
    </div>
</template>

<script>
import store from "../../../store"

import orderDetails from "./orderDetails.vue"
import ordersList from "./ordersList.vue"

export default {
    name: "orders",
    store,
    data: () => ({
        currentOrder: null,
        mode: 0,
    }),
    components: {
        "orders-list": ordersList,
        "order-details": orderDetails
    },
    props: [
        "orders",
        "recieved",
        "failed"
    ],
    computed: {
        dataRequestError() {
            return ( (this.recieved) && (this.failed) )
        },
        ordersListActive() {
            return ( (this.recieved) && (this.mode==0) )
        },
        orderDetailsActive() {
            return (this.mode === 1)
        }
    },
    created() {
        if (this.orders === null) {
            this.$emit("dataRequest");
        }
    },
    methods: {
        showOrdersList() {
            this.mode = 0;
        },
        showOrderDetails(order) {
            this.currentOrder = order;
            this.mode = 1;
        },
        showOrderDetails(order) {
            this.currentOrder = order;
            this.mode = 1;
        }
    }
}
</script>