<template>
    <md-content class="profile">
        <transition name="fade-fast"
            v-if="show"
        >
            <div class="profile__content">
                <div class="profile__controls">
                    <md-button class="md-primary"
                        @click="back"
                    >
                        <md-icon>keyboard_backspace</md-icon>
                        НАЗАД
                    </md-button>
                </div>
                <div class="md-layout">
                    <div class="md-layout-item">
                        <div class="profile__info">
                            <h2>Данные:</h2>
                            <md-field>
                                <label>ID</label>
                                <md-input v-model="user.id" readonly></md-input>
                            </md-field>
                            <md-field>
                                <label>email</label>
                                <md-input v-model="user.email" readonly></md-input>
                            </md-field>
                            <md-field>
                                <label>Телефон</label>
                                <md-input v-model="user.profile.phone_number" readonly></md-input>
                            </md-field>
                            <md-field>
                                <label>Имя</label>
                                <md-input v-model="user.profile.name" readonly></md-input>
                            </md-field>
                            <md-field>
                                <label>Фамилия</label>
                                <md-input v-model="user.profile.surname" readonly></md-input>
                            </md-field>
                            <md-field>
                                <label>Отчество</label>
                                <md-input v-model="user.profile.patronymic" readonly></md-input>
                            </md-field>
                        </div>
                    </div>
                    <div class="md-layout-item">
                        <div class="profile__orders-wrap">
                            <h2>Заказы:</h2>
                            <md-card class="profile__orders-card">
                                <div class="profile__orders"
                                    v-if="hasOrders"
                                >
                                    <div class="order"
                                        v-for="order in userOrders"
                                        :key="order.id"
                                        @click="selectOrder(order.id)"
                                    >
                                        <div class="order__id">
                                            №{{order.public}}
                                        </div>
                                        <div class="order__price">
                                            {{order.data.cart.total_price}} ₽
                                        </div>
                                        <div class="order__date">
                                            {{order.created_at|dataFilter}}
                                        </div>
                                    </div>
                                </div>
                                <div class="profile__orders-placeholder"
                                    v-else
                                >
                                    Нет заказов
                                </div>
                            </md-card>
                        </div>
                    </div>
                </div>
            </div>
        </transition>
        <div class="placeholder"
            v-else
        >
            <md-progress-spinner
                class="md-primary"
                md-mode="indeterminate"
                :md-diameter="128"
            >
            </md-progress-spinner>
        </div>
    </md-content>
</template>

<script>
    import store from './../../../store';
    import normalizeNumber from '../../../core/normalizeNumber'


    export default {
        name: "userProfile",
        store,
        data: () => ({
            userID: null,
            userProfileApiUrl: "/api/users/",
            userOrdersApiUrl: "/api/users/",
            userProfileGetResponseReceived: false,
            userProfileGetResponseError: false,
            userOrdersGetResponseReceived: false,
            userOrdersGetResponseError: false,
            user: null,
            userProxy: null,
            userOrders: []
        }),
        created() {
            this.initialize();
            this.getUserProfile();
            this.getUserOrders();
        },
        computed: {
            profileAvailable() {
                return ( (this.userProfileGetResponseReceived) && (!this.userProfileGetResponseError) )
            },
            ordersAvailable() {
                return ( (this.userOrdersGetResponseReceived) && (!this.userOrdersGetResponseError) )
            },
            show() {
                return (this.profileAvailable && this.ordersAvailable);
            },
            hasOrders() {
                return (this.userOrders.length > 0)
            }
        },
        methods: {
            initialize() {
                this.userID = this.$route.params.id;
                let title = `Пользователь: ${this.userID}`;
                this.$store.commit('admin/changeAppTitle', title);
                this.userProfileApiUrl += `${this.userID}/`;
                this.userOrdersApiUrl += `${this.userID}/orders`;
            },
            getUserProfile() {
                this.$http.get(this.userProfileApiUrl).then(
                    response => {
                        this.handleSuccessfulUserProfileGetResponse(response);
                    },
                    response => {
                        this.handleFailedUserProfileGetResponse(response);
                    }
                )
            },
            getUserOrders() {
                this.$http.get(this.userOrdersApiUrl).then(
                    response => {
                        this.handleSuccessfulOrdersGetResponse(response);
                    },
                    response => {
                        this.handleFailedOrdersGetResponse(response);
                    }
                )
            },
            handleSuccessfulUserProfileGetResponse(response) {
                this.user = response.body;
                this.userProfileGetResponseReceived = true;
                this.userProfileGetResponseError = false;
            },
            handleFailedUserProfileGetResponse(response) {
                this.userProfileGetResponseReceived = true;
                this.userProfileGetResponseError = true;
            },
            handleSuccessfulOrdersGetResponse(response) {
                this.userOrders = response.body;
                this.userOrdersGetResponseReceived = true;
                this.userOrdersGetResponseError = false;
            },
            handleFailedOrdersGetResponse(response) {
                this.userOrdersGetResponseReceived = true;
                this.userOrdersGetResponseError = true;
            },
            selectOrder(orderID) {
                let orderPath = `/order/${orderID}`;
                this.$router.push({path: orderPath});
            },
            back() {
                this.$router.go(-1);
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
    .profile {
        height: 100%;
    }
    .profile__info {
        padding: 0px 16px;
    }
    .profile__orders {
    }
    .profile__orders-wrap {
        padding: 0px 16px;
    }
    .order__button {
        width: 100%;
    }
    .profile__orders-card {
        margin: 0px !important;
    }
    .order {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px;
        transition: .3s cubic-bezier(.4,0,.2,1);
        transition-property: background-color,font-weight;
        will-change: background-color,font-weight;
        cursor: pointer;
        &:hover {
            background-color: rgba(0,0,0,.08);
        }
    }
    .order__id {

    }
    .order__price {

    }
    .order__date {

    }
    .profile__orders-placeholder {
        padding: 32px 16px;
        font-weight: 900;
        font-size: 18px;
        color: rgba(0,0,0,.32);
        text-align: center;
    }
    .placeholder {
        height: 100%;
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .fade-fast {
        opacity: 1 !important;
        transition: opacity 0.2s
    }
    .fade-fast-enter-active, .fade-fast-leave-active{
        transition: opacity 0.2s
    }
    .fade-fast-enter, .fade-fast-leave-to  {
        opacity: 0
    }
</style>