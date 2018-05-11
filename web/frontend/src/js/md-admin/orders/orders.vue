<template>
    <md-content class="orders">
        <div class="md-layout">
            <md-card>
                <md-card-content>
                    <table class="table">
                        <tbody>
                            <tr class="table-row">
                                <th class="table-head">
                                    <div class="table-head-container">
                                        <div class="table-head-label">
                                            №
                                        </div>
                                    </div>
                                </th>
                                <th class="table-head">
                                    <div class="table-head-container">
                                        <div class="table-head-label">
                                        СОЗДАН
                                        </div>
                                    </div>
                                </th>
                                <th class="table-head">
                                    <div class="table-head-container">
                                        <div class="table-head-label">
                                        СУММА
                                        </div>
                                    </div>
                                </th>
                                <th class="table-head">
                                    <div class="table-head-container">
                                        <div class="table-head-label">
                                        ПОКУПАТЕЛЬ
                                        </div>
                                    </div>
                                </th>
                                <th class="table-head">
                                    <div class="table-head-container">
                                        <div class="table-head-label">
                                        СТАТУС
                                        </div>
                                    </div>
                                </th>
                                <th class="table-head">
                                    <div class="table-head-container">
                                        <div class="table-head-label">
                                        ОПЛАТА
                                        </div>
                                    </div>
                                </th>
                                <th class="table-head">
                                    <div class="table-head-container">
                                        <div class="table-head-label">
                                        ДОСТАВКА
                                        </div>
                                    </div>
                                </th>
                            </tr>

                            <tr class="table-row" v-for="order in orders"
                                :class="computeRowStatusClass(order.state)"
                            >
                                <td class="table-cell table-cell--colored">
                                    <a class="table-cell-container table-cell-container--clickable"
                                        @click="orderFormRedirect(order)"
                                    >
                                        <span class="md-body-2">{{order.id}}</span>
                                    </a>
                                </td>
                                <td class="table-cell">
                                    <div class="table-cell-container table-cell-container--time">
                                        {{order.created_at | dataFilter}}
                                    </div>
                                </td>
                                <td class="table-cell">
                                    <div class="table-cell-container table-cell-container--right">
                                        <span class="md-body-2">{{order.data.cart.total_price}} ₽</span>
                                    </div>
                                </td>
                                <td class="table-cell">
                                    <div class="table-cell-container">
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
                                <td class="table-cell table-cell--colored">
                                    <div class="table-cell-container">
                                        <span class="md-body-2">{{order.state | capitalize}}</span>
                                    </div>
                                </td>
                                <td class="table-cell">
                                    <div class="table-cell-container">
                                    </div>
                                </td>
                                <td class="table-cell">
                                    <div class="table-cell-container">
                                    </div>
                                </td>
                            </tr>

                        </tbody>
                    </table>
                </md-card-content>
            </md-card>
        </div>
    </md-content>
</template>

<script>
    import getParameterByName from '../../core/getParameterByName'
    import updateQueryString from '../../core/updateQueryString'
    import normalizeNumber from '../../core/normalizeNumber'

    import store from './../../store';

    export default {
        name: 'orders',
        store,
        data: () => ({
            componentTitle: 'Заказы',
            orderListAPIUrl: '/api/order/list/',
            orderListAPIConnectionFailed: false,
            currentPage: null,
            ordersCount: 0,
            originalOrders: [],
            orders: [],
            orderStatusMap: {
                'новый': 'table-row--new',
                'недозвон': 'table-row--err',
                'доставка': 'table-row--done',
                'выполнен': 'table-row--done',
                'согласован': 'table-row--done',
                'отменён': 'table-row--err',
                'отменён: недозвон': 'table-row--err'
            },
            currentOrder: null,
            editModalIsDisplayed: false,
            refreshTimer: null
        }),
        computed: {
            nonRouterLocation() {
                return window.location.href.replace('#/', '')
            }
        },
        created() {
            this.currentPage = getParameterByName('page', this.nonRouterLocation);
            if ( this.currentPage === null ) {
                this.currentPage = 1;
            }
            this.getOrders();
            this.$store.commit('admin/changeAppTitle', this.componentTitle);
        },
        mounted() {
            this.refreshTimer = setInterval(this.refresh, 5000);
            Notification.requestPermission();
        },
        methods: {
            computeRowStatusClass(value) {
                return this.orderStatusMap[value]
            },
            getOrders() {
                this.$http.get(`${this.orderListAPIUrl}?page=${this.currentPage}`).then(
                    response => {
                        this.processOrdersResponse(response);
                    },
                    response => {
                        this.orderListAPIConnectionFailed = true;
                    }
                )
            },
            processOrdersResponse(response) {
                this.orders = response.body.results;
                let hasChanged = false;

                if (this.originalOrders.length === 0) {
                    this.originalOrders = this.orders.slice();
                } else {
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
            },
            orderFormRedirect(order) {
                let orderPath = `order/${order.id}`;
                this.$router.replace({path: orderPath});
            },
            refresh() {
                this.getOrders();
            },
            checkChanges() {

            },
            notify(order) {
                console.log('notify');
                if (Notification.permission === 'granted') {
                    let options = {
                        body: order.data['cart']['total_price'] + ' рублей'
                    }
                    let notification = new Notification('Новый заказ', options);
                }
            }
        },
        watch: {
            currentPage() {
                console.log('current page changed');
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
        }
    }
</script>

<style lang="scss" scoped>
    $primary: #448aff;
    $accent: #F44336;
    $success: #00BFA5;

    .orders {
        position: relative;
    }
    .table-head {
        color: rgba(0,0,0,.54);
    }
    .table-row {
        &:nth-child(odd) {
            background: rgba(27,54,100,0.03);
        }
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
    .table-head-container {
        height: 56px;
        padding: 14px 0;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    .table-head-label {
        height: 28px;
        padding-right: 32px;
        padding-left: 24px;
        display: inline-block;
        position: relative;
        line-height: 28px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    .table-cell {
        position: relative;
        height: 48px;
        font-size: 13px;
        line-height: 18px;
    }
    .table-cell-container {
        padding: 6px 32px 6px 24px;
    }
    .md-layout {
        width: 100% !important;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .table-cell-container--right {
        text-align: right;
    }
    .table-cell-container--time {
        max-width: 150px;
        padding: 6px 32px 6px 24px;
        line-height: 14px;
    }
    .callback {
        color: $success;
    }
    .table-cell-container--clickable {
        cursor: pointer;
    }
</style>