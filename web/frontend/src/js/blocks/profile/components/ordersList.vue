<template>
    <ul class="orders__list"
    >
        <li class="order"
            v-for="order in orders"
            :key="order.id"
        >
            <div class="order__main-info">
                <div class="order__status"
                    :class="computedStatus(order.state)"
                >
                    {{order.state}}
                </div>
                <div class="order__title">
                    № <span class="bold green">100{{order.id}}</span>
                </div>
                <div class="order__total-price price">
                    {{order.data.cart.total_price}} <i class="icon icon_rouble"></i>
                </div>
                <div class="order__date">
                    {{order.created_at | dateFilter}}
                </div>
            </div>
            <ul class="order__items">
                <li class="order__item"
                    v-for="item in order.data.cart.items"
                    :key="item.vendor_code"
                >
                    <div class="order__item-img-wrap">
                        <img :src="item.image">
                    </div>
                </li>
            </ul>
        </li>
    </ul>
</template>

<script>
import normalizeNumber from '../../../core/normalizeNumber'

export default {
    name: "orders-list",
    data: () => ({
        statusMap: {
            'новый': 'order__status_green',
            'недозвон': 'order__status_red',
            'доставка': 'order__status_green',
            'выполнен': 'order__status_green',
            'согласован': 'order__status_blue',
            'отменён': 'order__status_red',
            'отменён: недозвон': 'order__status_red',
            'вручен': 'order__status_violet'
        },
    }),
    props: [
        "orders"
    ],
    methods: {
        showOrderDetails(order) {
            this.$emit("order_clicked", order);
        },
        computedStatus(value) {
            return this.statusMap[value]
        },
    },
    filters: {
        dateFilter(dateString) {
            let date = new Date(dateString);
            let year = date.getFullYear();
            let month = normalizeNumber(date.getMonth()+1);
            let day = normalizeNumber(date.getDate());
            let minutes = normalizeNumber(date.getMinutes());
            let hours = normalizeNumber(date.getHours());
            let seconds = normalizeNumber(date.getSeconds());
            return `${day}.${month}.${year} ${hours}:${minutes}`
        },
    }
}
</script>