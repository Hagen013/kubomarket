<template>
    <md-content class="orders">
        <div class="orders__content"
            v-if="showContent"
        >
            <div class="orders__controls">
                <div class="orders__pagination pagination">
                    <div class="pagination__client-count">
                        {{ordersCount}}
                    </div>
                    <div class="pagination__delimeter">
                        из
                    </div>
                    <div class="pagination__total-count">
                        {{count}}
                    </div>
                    <div class="pagination__controls">
                        <md-button class="md-icon-button"
                            :disabled="!hasPreviousPage"
                            @click="previousPage"
                        >
                            <md-icon>
                            chevron_left
                            </md-icon>
                        </md-button>
                        <md-button class="md-icon-button"
                            :disabled="!hasNextPage"
                            @click="nextPage"
                        >
                            <md-icon>
                            chevron_right
                            </md-icon>
                        </md-button>
                    </div>
                </div>
            </div>
            <div class="orders__table-wrap">
                <table class="table">
                    <tr class="table__head">
                        <th class="table__head numeric">
                            <div class="table__head-container">
                                <div class="table__label">
                                    ID
                                </div>
                            </div>
                        </th>
                        <th class="table__head numeric">
                            <div class="table__head-container">
                                <div class="table__label">
                                    СОЗДАН
                                </div>
                            </div>
                        </th>
                        <th class="table__head numeric">
                            <div class="table__head-container">
                                <div class="table__label">
                                    СУММА
                                </div>
                            </div>
                        </th>
                        <th class="table__head numeric">
                            <div class="table__head-container">
                                <div class="table__label">
                                    КЛИЕНТ
                                </div>
                            </div>
                        </th>
                        <th class="table__head numeric">
                            <div class="table__head-container">
                                <div class="table__label">
                                    СТАТУС
                                </div>
                            </div>
                        </th>
                        <th class="table__head numeric">
                            <div class="table__head-container">
                                <div class="table__label">
                                    ДОСТАВКА
                                </div>
                            </div>
                        </th>
                    </tr>
                    <tr class="table__row"
                        v-for="order of orders"
                        :key="order.id"
                        @click="select(order.id)"
                        :class="computeRowStatusClass(order.state)"
                    >
                        <td class="table__cell">
                            <div class="table__cell-container table-cell--colored">
                                {{order.id}}
                            </div>
                        </td>
                        <td class="table__cell">
                            <div class="table__cell-container">
                                {{order.created_at | dataFilter}}
                            </div>
                        </td>
                        <td class="table__cell">
                            <div class="table__cell-container green">
                                <span class="md-body-2">
                                    {{order.data.cart.total_price}} ₽
                                </span>
                            </div>
                        </td>
                        <td class="table__cell">
                            <div class="table__cell-container">
                                <div class="md-caption">{{order.data.geo.city}}</div>
                                <div class="callback" v-if="order.source=='callback'">
                                    <span class="md-body-2">Обратный звонок</span>
                                </div>
                                <div v-else>
                                    {{order.data.customer.name}}
                                </div>
                                <div>{{order.data.customer.phone}}</div>
                            </div>
                        </td>
                        <td class="table__cell table-cell--colored">
                            <div class="table__cell-container"
                            >
                                {{order.state | capitalize}}
                            </div>
                        </td>
                        <td class="table__cell">
                            <div class="table__cell-container">
                                <div
                                    v-if="order.data.delivery.mod.price !== null"
                                >
                                    <span class="md-body-2">{{order.data.delivery.mod.price}} ₽</span>
                                    <div class="md-caption">
                                        {{order.data.delivery.mod | deliveryFilter}}
                                    </div>
                                </div>
                                <div
                                    class="md-caption"
                                    v-else
                                >
                                    не выбрано
                                </div>
                            </div>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="orders__placeholder"
            v-else
        >
            <md-progress-spinner :md-diameter="100" :md-stroke="10" md-mode="indeterminate">
            </md-progress-spinner>
        </div>
    </md-content>
</template>

<script>
    import normalizeNumber from '../../core/normalizeNumber'

    import store from './../../store';

    export default {
        name: 'orders',
        store,
        data: () => ({
            componentTitle: 'Заказы',
            orders: [],
            originalOrders: [],
            orderStatusMap: {
                'новый': 'table-row--new',
                'недозвон': 'table-row--err',
                'доставка': 'table-row--done',
                'выполнен': 'table-row--done',
                'согласован': 'table-row--done',
                'отменён': 'table-row--err',
                'отменён: недозвон': 'table-row--err'
            },
            refreshTimer: null,
            count: 0,
            limit: 50,
            offset: 0,
            responseRecieved: false,
            responseError: false
        }),
        computed: {
            listApiUrl() {
                return `/api/order/list/?limit=${this.limit}&offset=${this.offset}`
            },
            showContent() {
                return (this.responseRecieved && !this.responseError)
            },
            ordersCount() {
                let sum = this.offset + this.limit;
                if (sum > this.count) {
                    sum = this.count;
                }
                return sum
            },
            hasPreviousPage() {
                return this.offset > 0
            },
            hasNextPage() {
                return this.ordersCount < this.count;
            }
        },
        created() {
            this.initialize();
            this.$store.commit('admin/changeAppTitle', this.componentTitle);
        },
        mounted() {
            this.refreshTimer = setInterval(this.refresh, 5000);
            Notification.requestPermission();
        },
        methods: {
            initialize() {
                this.getOrders();
            },
            getOrders() {
                this.$http.get(this.listApiUrl).then(
                    response => {
                        this.handleSuccessfulGetResponse(response);
                    },
                    response => {
                        this.handleFailedGetResponse(response);
                    }
                )
            },
            handleSuccessfulGetResponse(response) {
                this.orders = response.body.results;
                this.count = response.body.count;
                if (this.originalOrders.length === 0) {
                    this.originalOrders = this.orders.slice();
                }
                else {
                    let oldIds = this.originalOrders.map(function(order) {
                        return order.id
                    })
                    for (let i=0; i<this.orders.length; i++) {
                        if (oldIds.indexOf(this.orders[i].id) === -1) {
                            this.notify(this.orders[i]);
                            hasChanged = true;
                        }
                    }
                    if (hasChanged === true) {
                        this.originalOrders = this.orders.slice();
                    }
                }
                this.responseError = false;
                this.responseRecieved = true;
            },
            handleFailedGetResponse(response) {
                this.responseError = true;
                this.responseRecieved = true;
            },
            select(orderID) {
                let orderPath = `order/${orderID}`;
                this.$router.push({path: orderPath});
            },
            previousPage() {
                this.offset -= this.limit;
                this.getOrders();
            },
            nextPage() {
                this.offset += this.limit;
                this.getOrders();
            },
            computeRowStatusClass(value) {
                return this.orderStatusMap[value]
            },
            refresh() {
                this.getOrders();
            },
            notify(order) {
                if (Notification.permission === 'granted') {
                    let options = {
                        body: order.data['cart']['total_price'] + ' рублей'
                    }
                    let notification = new Notification('Новый заказ', options);
                }
            }
        },
        filters: {
            dataFilter(dataString) {
                let date = new Date(dataString);
                let year = date.getFullYear();
                let month = normalizeNumber(date.getMonth()+1);
                let day = normalizeNumber(date.getDate());
                let minutes = normalizeNumber(date.getMinutes());
                let hours = normalizeNumber(date.getHours());
                let seconds = normalizeNumber(date.getSeconds());

                return `${day}.${month}.${year} ${hours}:${minutes}:${seconds}`
            },
            capitalize(value) {
                if (!value) return ''
                value = value.toString()
                return value.charAt(0).toUpperCase() + value.slice(1)
            },
            deliveryFilter(deliveryMod) {
                if (deliveryMod.type === "delivery_points") {
                    return "пункт выдачи"
                }
                else if (deliveryMod.type === "curier") {
                    return "курьер"
                }
                else {
                    return "почта"
                }
            }
        }
    }
</script>

<style lang="scss" scoped>
    $primary: #448aff;
    $accent: #F44336;
    $success: #00BFA5;
    .orders {
        min-height: 400px;
    }
    .orders__placeholder {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
        min-height: 400px;
        width: 100%;
    }
    .table {
        width: 100%;
        border-spacing: 0;
        border-collapse: collapse;
    }
    .table__row {
        transition: .3s cubic-bezier(.4,0,.2,1);
        transition-property: background-color,font-weight;
        will-change: background-color,font-weight;
        cursor: pointer;
        &:hover {
            background-color: rgba(0,0,0,.08);
        }
    }
    .table__cell {
        height: 48px;
        position: relative;
        transition: .3s cubic-bezier(.4,0,.2,1);
        font-size: 13px;
        line-height: 18px;
        border-top-color: rgba(0,0,0,.12);
        border-top: 1px solid rgba(0,0,0,.12);
    }
    .table__cell-container {
        padding: 6px 32px 6px 24px;
    }
    .table__head-container {
        height: 56px;
        padding: 14px 0px;
        text-align: left;
    }
    .table__label {
        height: 28px;
        padding-right: 32px;
        padding-left: 24px;
        color: rgba(0, 0, 0, 0.54);
        display: inline-block;
        position: relative;
        line-height: 28px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    .orders__controls {
        padding: 0px 32px;
    }
    .pagination {
        display: flex;
        align-items: center;
        justify-content: flex-end;
    }
    .pagination__delimeter {
        padding: 0px 10px;
    }
    .pagination__total-count {

    }
    .pagination__controls {
        user-select: none;
    }
    .table-row--new {
        .table-cell--colored {
            color: $success;
            a {
                color: $success;
            }
        }
    }
    .table-row--err {
        .table-cell--colored {
            color: $accent;
            a {
                color: $accent;
            }
        }
    }
    .table-row--done {
        .table-cell--colored {
            color: $primary;
            a {
                color: $primary;
            }
        }
    }
    .callback {
        color: $success;
    }
</style>