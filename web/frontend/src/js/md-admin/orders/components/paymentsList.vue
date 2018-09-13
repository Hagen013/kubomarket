<template>
    <div class="list">
        <div class="md-title title">
            Список платежей
        </div>
        <div class="list__item item"
            v-if="showList"
            v-for="item in payments"
            :key="item.id"
        >
            <div class="item__content">
                <div class="item__row">
                    <div class="item__key">
                        Дата:
                    </div>
                    <div class="item__value">
                        {{item.pub_date|dataFilter}}
                    </div>
                </div>
                <div class="item__row">
                    <div class="item__key">
                        Статус:
                    </div>
                    <div class="item__value">
                        {{item.status|statusFilter}}
                    </div>
                </div>
                <div class="item__row">
                    <div class="item__key">
                        Оплачен:
                    </div>
                    <div class="item__value"
                        v-if="item.is_payed"
                        v-once
                    >
                        да
                    </div>
                    <div class="item__value"
                        v-else
                        v-once
                    >
                        нет
                    </div>
                </div>
                <div class="item__row">
                    <div class="item__key">
                        Ссылка:
                    </div>
                    <div class="item__value">
                        <a class="link"
                            :href="item.url"
                            target="_blank"
                        >
                            /cart/payment{{item.uuid}}/
                        </a>
                    </div>
                </div>
            </div>
            <div class="item__close">
                <md-button class="md-icon-button md-accent"
                    v-if="!item.is_payed"
                    @click="deleteItem(item)"
                >
                    <md-icon>delete</md-icon>
                </md-button>
            </div>
        </div>
        <div class="list__placeholder"
            v-else
        >
            Платежей нет
        </div>
    </div>
</template>

<script>
    import normalizeNumber from '../../../core/normalizeNumber'

    export default {
        name: 'payments',
        data: () => ({
        }),
        props: [
            "payments"
        ],
        computed: {
            showList() {
                return this.payments.length > 0
            }
        },
        methods: {
            deleteItem(item) {
                this.$emit("deleteItem", item)
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
            statusFilter(status) {
                const statusMap = {
                    "processed": "новый",
                    "success": "оплачен",
                    "fail": "ошибка" 
                }
                return statusMap[status]
            }
        }
    }
</script>

<style lang="scss" scoped>
    .list {
        padding: 0px 32px;
    }
    .title {
        margin-bottom: 32px;
    }
    .list__item {
        padding: 8px 0px;
        border-top-color: rgba(0,0,0,.12);
        border-top: 1px solid rgba(0,0,0,.12);
    }
    .button {
        margin: 0px !important;
    }
    .item {
        padding: 8px 0px;
        position: relative;
        max-width: 500px;
    }
    .item__close {
        position: absolute;
        top: 8px;
        right: 0px;
    }
    .item__row {
        display: flex;
    }
    .item__key {
        width: 70px;
    }
</style>
