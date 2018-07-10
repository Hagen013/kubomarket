<template>
    <transition name="fade-fast">
    <div class="profile" v-if=pageReady>
        <h1 class="profile__greeting">
            Здравствуйте {{profile.greeting_name}}
        </h1>
        <div class="profile__content">
            <nav class="profile__nav">
                <li class="profile__nav-item"
                    @click="currentItem = 0"
                    :class="{ profile__navItem_active : currentItem === 0 }"
                >
                    Мои заказы
                </li>
                <li class="profile__nav-item"
                    @click="currentItem = 1"
                    :class="{ profile__navItem_active : currentItem === 1 }"
                >
                    Мои данные
                </li>
                <li class="profile__nav-item"
                    @click="currentItem = 2"
                    :class="{ profile__navItem_active : currentItem === 2 }"
                >
                    Мои отзывы
                </li>
            </nav>
            <div class="profile__outlet">
                <orders
                    :orders=orders
                    :recieved=ordersResponseRecieved
                    :failed=ordersRequestFailed
                    v-if="currentItem === 0"
                    v-on:dataRequest="getOrders"
                >
                </orders>
                <personal-data
                    :profile=profile
                    :recieved=profileResponseRecieved
                    :failed=profileRequestFailed
                    v-if="currentItem === 1"
                >
                </personal-data>
                <comments
                    :comments=comments
                    :recieved=commentsResponseRecieved
                    :failed=commentsRequestFailed
                    v-if="currentItem === 2"
                >
                </comments>
            </div>
        </div>
    </div>
    </transition>
</template>

<script>
import store from "../../../store";

import orders from "./orders.vue";
import personalData from "./personalData.vue";
import comments from "./comments.vue";


export default {
    name: "profile",
    store,
    components: {
        "orders": orders,
        "personal-data": personalData,
        "comments": comments
    },
    data: () => ({
        baseApiUrl: "/api/users/",
        ordersUrl: null,
        commentsUrl: null,
        profileUrl: null,
        orders: null,
        profile: null,
        comments: null,
        ordersResponseRecieved: false,
        profileResponseRecieved: false,
        commentsResponseRecieved: false,
        ordersRequestFailed: false,
        profileRequestFailed: false,
        commentsRequestFailed: false,
        currentItem: 1
    }),
    props: [
        "user_id"
    ],
    created() {
        this.modifyApiUrls();
        this.getInitialData();
    },
    computed: {
        pageReady() {
            return ( (this.profileResponseRecieved) && (!this.profileRequestFailed) )
        }
    },
    methods: {
        modifyApiUrls() {
            this.ordersUrl = `${this.baseApiUrl}${this.user_id}/orders/`;
            this.commentsUrl = `${this.baseApiUrl}${this.user_id}/comments/`;
            this.profileUrl = `${this.baseApiUrl}${this.user_id}/profile/`;
        },
        getInitialData() {
            this.getProfile();
        },
        getProfile() {
            this.$http.get(this.profileUrl).then(
                response => {
                    this.handleSuccessfulProfileResponse(response);
                },
                response => {
                    this.handleFailedProfileResponse(response);
                }
            )
        },
        getOrders() {
            this.$http.get(this.ordersUrl).then(
                response => {
                    this.handleSuccessfulOrdersResponse(response);
                },
                response => {
                    this.handleFailedOrdersResponse(response);
                }
            )
        },
        getComments() {
            this.$http.get(this.commentsUrl).then(
                response => {
                    this.handleSuccessfulProfileResponse(response);
                },
                response => {
                    this.handleFailedCommentsResponse(response);
                }
            )
        },
        handleSuccessfulProfileResponse(response) {
            this.profileResponseRecieved = true;
            this.profile = response.body;
        },
        handleSuccessfulOrdersResponse(response) {
            this.ordersResponseRecieved = true;
            this.orders = response.body;
        },
        handleSuccessfulCommentsResponse(response) {
            this.commentsResponseRecieved = true;
            this.comments = response.body;
        },
        handleFailedProfileResponse(response) {
            this.profileResponseRecieved = true;
            this.profileRequestFailed = true;
        },
        handleFailedOrdersResponse(response) {
            this.ordersResponseRecieved = true;
            this.ordersRequestFailed = true;
        },
        handleFailedCommentsResponse(response)  {
            this.commentsResponseRecieved = true;
            this.commentsRequestFailed = true;
        }
    }
}
</script>