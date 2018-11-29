<template>
    <md-content class="reviews">
        <div class="reviews__placeholder"
            v-if="!initialized"
        >
            <md-progress-spinner :md-diameter="100" :md-stroke="10" md-mode="indeterminate">
            </md-progress-spinner>
        </div>
        <div class="reviews__content"
            v-else-if="!responseError"
        >
            <div class="controls reviews__controls">
                <div class="reviews__pagination pagination">
                    <div class="pagination__client-count">
                        {{offset}} - {{totalCount}}
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
            <table class="table">
                <tr class="table__head-row">
                    <th class="table__head-container">
                        ID
                    </th>
                    <th class="table__head-container">
                        User
                    </th>
                    <th class="table__head-container">
                        Товар
                    </th>
                    <th class="table__head-container">
                        Рейтинг
                    </th>
                    <th class="table__head-container">
                        Статус
                    </th>
                    <th class="table__head-container">
                        Дата
                    </th>
                </tr>
                <tr class="table__row"
                    v-for="review in reviews"
                    :key="review.id"
                    @click="select(review)"
                >
                    <td class="table__cell">
                        <div class="table__cell-container">
                        {{review.id}}
                        </div>
                    </td>
                    <td class="table__cell">
                        <div class="table__cell-container">
                        {{review.user|userFilter}}
                        </div>
                    </td>
                    <td class="table__cell">
                        <div class="table__cell-container">
                        {{review.product.id}}
                        </div>
                    </td>
                    <td class="table__cell">
                        <div class="table__cell-container">
                        {{review.rating}}
                        </div>
                    </td>
                    <td class="table__cell">
                        <div class="table__cell-container blue"
                            v-if="review.status==='новый'"
                        >
                            <md-icon class="icon blue">hourglass_empty</md-icon>
                            новый
                        </div>
                        <div class="table__cell-container success"
                            v-else-if="review.status==='одобрен'"
                        >
                            <md-icon class="icon success">done</md-icon>
                            одобрен
                        </div>
                        <div class="table__cell-container red"
                            v-else
                        >
                            <md-icon class="icon red">cancel</md-icon>
                            отклонен
                        </div>
                    </td>
                    <td class="table__cell">
                        <div class="table__cell-container">
                        {{review.created_at|dateFilter}}
                        </div>
                    </td>
                </tr>
            </table>
        </div>
        <div class="reviews__error"
            v-else
        >
            <div class="md-display-3">
                Во время соедиения с сервером произошла ошибка
            </div>
        </div>
    </md-content>
</template>

<script>
    import normalizeNumber from '../../core/normalizeNumber'

    import store from './../../store';

    export default {
        name: 'reviews',
        store,
        data: () => ({
            reviews: [],
            initialized: false,
            responseError: false,
            count: 0,
            limit: 25,
            offset: 0,
        }),
        computed: {
            apiListUrl() {
                return `/api/reviews/?limit=${this.limit}&offset=${this.offset}`
            },
            totalCount() {
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
                return this.totalCount < this.count;
            }
        },
        created() {
            this.initialize();
        },
        methods: {
            initialize() {
                this.getReviews();
            },
            getReviews() {
                this.$http.get(this.apiListUrl).then(
                    response => {
                        this.handleSuccessfulGetListApiResponse(response);
                    },
                    response => {
                        this.handleFailedGetListApiResponse(response);
                    }
                )
            },
            handleSuccessfulGetListApiResponse(response) {
                this.reviews = response.body.results;
                this.count = response.body.count;
                this.initialized = true;
                this.responseError = false;
            },
            handleFailedGetListApiResponse(response) {
                this.initialized = true;
                this.responseError = true;
            },
            previousPage() {
                this.offset -= this.limit;
                this.getReviews();
            },
            nextPage() {
                this.offset += this.limit;
                this.getReviews();
            },
            select(review) {
                let path = `/reviews/${review.id}`;
                this.$router.push({path: path});
            }
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
            userFilter(user) {
                if (user.profile.phone_number!="") {
                    return user.profile.phone_number
                } else if (user.email!="") {
                    return user.email
                }
                return `ID: ${user.id}`
            }
        }
    }
</script>

<style lang="scss" scoped>
    $primary: #448aff;
    $accent: #F44336;
    $success: #00BFA5;

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
    .reviews {
        height: 100%;
    }
    .reviews__placeholder {
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .reviews__error {
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .table__head-container {
        padding: 6px 32px 6px 24px;
    }
    .icon {
        font-size: 18px !important;
        margin: 0px !important;
    }
    .red {
        color: $accent !important;
    }
    .success {
        color: $success !important;
    }
    .blue {
        color: $primary !important;
    }
    .cell-aling-center {
        display: flex;
        justify-content: flex-start;
        align-items: center;
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
</style>