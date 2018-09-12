<template>
    <div class="list">
        <div class="md-title title">
            Список платежей
        </div>
        <div class="list__item"
            v-if="showList"
            v-for="item in payments"
            :key="item.id"
        >
            <div class="row">
                <div class="row__name">
                    Дата:
                </div>
                <div class="row__value">
                    {{item.pub_date|dataFilter}}
                </div>
            </div>
            <div class="row">
                <div class="row__name">
                    Статус:
                </div>
                <div class="row__value">
                    {{item.status|statusFilter}}
                </div>
            </div>
            <div class="row row_nf">
                <div class="row__name">
                    Ссылка:
                </div>
                <div class="row__value">
                    <a class="link"
                        :href="item.url"
                        target="_blank"
                    >
                        /cart/payment{{item.uuid}}/
                    </a>
                </div>
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
        margin-bottom: 24px;
        padding: 8px 0px;
        border-top-color: rgba(0,0,0,.12);
        border-top: 1px solid rgba(0,0,0,.12);
    }
    .row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 8px;
    }
    .row_nf { 
        display: block !important;
    }
    .button {
        margin: 0px !important;
    }
</style>
