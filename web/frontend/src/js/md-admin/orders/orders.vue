<template>
    <md-content class="orders">
        <div class="orders__loading"
            v-if="loading"
        >
            <md-progress-spinner :md-diameter="50" :md-stroke="4" md-mode="indeterminate">
            </md-progress-spinner>
        </div>
        <div class="orders__content"
            v-if="showContent"
        >
            <div class="orders__controls">
                <div class="orders__inputs">
                    <div class="input-box">
                        <input class="input"
                            placeholder="номер заказа"
                            v-model="queryParams.public_id"
                            @input="triggerSearch"
                        >
                    </div>
                    <div class="input-box">
                        <input class="input"
                            placeholder="ФИО"
                            v-model="queryParams.name"
                            @input="triggerSearch"
                        >
                    </div>
                    <div class="input-box">
                        <input class="input"
                            placeholder="телефон"
                            v-model="queryParams.phone"
                            @input="triggerSearch"
                        >
                    </div>
                    <div class="orders__cpa">
                        <md-checkbox v-model="queryParams.admitad" class="md-primary"
                            @change="triggerSearch"
                        >
                            Admitad
                        </md-checkbox>
                    </div>
                </div>
                <div class="orders__pagination pagination">
                    <div class="pagination__client-count">
                        {{offset}} - {{ordersCount}}
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
                        <th class="table__head numeric">
                            <div class="table__head-container">
                                <div class="table__label">
                                    ОПЛАТА
                                </div>
                            </div>
                        </th>
                    </tr>
                    <tr class="table__row"
                        v-for="order of sortedOrders"
                        :key="order.id"
                        @click="select(order.id)"
                        :class="computeRowStatusClass(order.state)"
                    >
                        <td class="table__cell">
                            <div class="table__cell-container table-cell--colored">
                                <div class="public_id">
                                    {{order.public_id}}
                                </div>
                                <div class="admitad_badge" v-if="containsAdmitadCPA(order)" v-once>
                                    admitad
                                </div>
                            </div>
                        </td>
                        <td class="table__cell">
                            <div class="table__cell-container table-cell-container--time">
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
                                {{order.state|stateFilter|capitalize}}
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
                        <td class="table__cell">
                            <div class="table__cell-container md-caption"
                                :class="{ success : order.data['payment']['mod'] === 'card' }"
                            >
                                <div class="order__payment">
                                {{order.data['payment']['mod']|paymentFilter}}
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
    import debounce from 'debounce';

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
                'недозвон 2': 'table-row--err',
                'доставка': 'table-row--done',
                'выполнен': 'table-row--done',
                'согласован': 'table-row--done',
                'отменён': 'table-row--err',
                'отменён: недозвон': 'table-row--err',
                'вручен': 'table-row-success',
                'отказ': 'table-row--err'
            },
            refreshTimer: null,
            count: 0,
            limit: 50,
            offset: 0,
            responseRecieved: false,
            responseError: false,
            refreshing: false,
            queryParams: {
                name: "",
                phone: "",
                public_id: "",
                admitad: false
            },
            loading: false
        }),
        computed: {
            listApiUrl() {
                let url = `/api/order/list/?limit=${this.limit}&offset=${this.offset}`;
                if (this.queryParams.name !== '') {
                    url += `&name=${this.queryParams.name}`;
                }
                if (this.queryParams.phone !== '') {
                    url += `&phone=${this.queryParams.phone}`
                }
                if (this.queryParams.public_id !== '') {
                    url += `&public_id=${this.queryParams.public_id}`
                }
                if (this.queryParams.admitad === true) {
                    url += `&show_cpa=${this.queryParams.admitad}`
                } 
                return url
            },
            searchLock() {
                return (
                    (this.queryParams.name !== "") ||
                    (this.queryParams.phone !== "") ||
                    (this.queryParams.public_id !== "")
                )
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
            },
            sortedOrders() {
                return this.orders
            }
        },
        created() {
            this.initialize();
            this.$store.commit('admin/changeAppTitle', this.componentTitle);
        },
        mounted() {
            this.refreshTimer = setInterval(this.refresh, 10000);
            Notification.requestPermission();
        },
        methods: {
            initialize() {
                this.getOrders();
            },
            getOrders() {
                this.loading = true;
                this.$http.get(this.listApiUrl).then(
                    response => {
                        this.handleSuccessfulGetResponse(response);
                    },
                    response => {
                        this.handleFailedGetResponse(response);
                    }
                )
            },
            refreshOrders() {
                this.$http.get(this.listApiUrl).then(
                    response => {
                        this.handleSuccessfulRefreshResponse(response);
                    },
                    response => {
                        this.handleFailedGetResponse(response);
                    }
                )
            },
            handleSuccessfulGetResponse(response) {
                this.loading = false;
                this.orders = response.body.results;
                this.originalOrders = this.orders.slice();
                this.count = response.body.count;
                let hasChanged = false;

                this.responseError = false;
                this.responseRecieved = true;
            },
            handleSuccessfulRefreshResponse(response) {
                this.orders = response.body.results;
                this.count = response.body.count;
                let hasChanged = false;

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
                if (!this.searchLock) {
                    this.refreshOrders();
                }
            },
            notify(order) {
                if (Notification.permission === 'granted') {
                    let options = {
                        body: order.data['cart']['total_price'] + ' рублей'
                    }
                    let notification = new Notification('Новый заказ', options);
                }
            },
            containsAdmitadCPA(order) {
                return order.cpa.networks.some(function(currentValue, index, array) {
                    return currentValue === 'admitad'
                })
            },
            triggerSearch: debounce(function () {
                this.getOrders();
            }, 500)
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
            },
            paymentFilter(mode) {
                if (mode === "cash") {
                    return "наличными"
                } else if (mode == "card") {
                    return "онлайн"
                }
                else {
                    return "картой при получении"
                }
            },
            stateFilter(state) {
                if (state === 'недозвон') {
                    return 'недозвон 1'
                }
                return state
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
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0px 32px 0px 0px;
        margin-bottom: 32px;
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
    .success {
        color: $success;
    }
    .table-row--err {
        .table-cell--colored {
            color: $accent;
            a {
                color: $accent;
            }
        }
    }
    .table-row-success {
        .table-cell--colored {
            color: #512DA8;
            a {
                color: #512DA8;
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
    .table-cell-container--time {
        max-width: 150px;
        padding: 6px 32px 6px 24px;
        line-height: 1.6;
    }
    .order__payment {
        max-width: 80px;
    }
    .input-box {
        display: inline-block;
        margin-right: 16px;
        height: 30px;
    }
    .input {
        padding: 0px 8px;
        height: 100%;
    }
    .input-box {
        border: 1px solid rgba(0, 0, 0, 0.12);
        border-radius: 2px;
        &:focus {
            border-color: #448aff;
        }
    }
    .orders__pagination {
        width: 260px;
    }
    .orders__loading {
        display: flex;
        position: fixed;
        justify-content: center;
        align-items: center;
        top: 0px;
        left: 0px;
        height: 100vh;
        width: 100%;
        background: rgba(255, 255, 255, 0.4);
        z-index: 10000;
    }
    .orders__content {
        width: 100%;
        height: 100%;
    }
    .public_id {

    }
    .admitad_badge {
        width: 60px;
        background: #6b31bd;
        color: white;
        border-radius: 8px;
        padding: 0px 4px;
        font-size: 12px;
        text-align: center;
    }
    .orders__inputs {
        display: flex;
        align-items: center;
    }
    .orders__cpa {
        display: inline-block;
    }
</style>