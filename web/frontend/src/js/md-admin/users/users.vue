<template>
    <md-content class="users">
        <transition name="fade-fast">
            <div class="users--content"
                v-if="getListApiResponseRecieved"
            >
                <div class="users--table-wrap"
                    v-if="showUsersList"
                >
                    <div class="users--controls">
                        <div class="users--pagination pagination">
                            <div class="pagination__client-count">
                                {{clientCount}}
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
                        <tbody>
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
                                            Email
                                        </div>
                                    </div>
                                </th>
                                <th class="table__head numeric">
                                    <div class="table__head-container">
                                        <div class="table__label">
                                            Имя
                                        </div>
                                    </div>
                                </th>
                                <th class="table__head numeric">
                                    <div class="table__head-container">
                                        <div class="table__label">
                                            Фамилия
                                        </div>
                                    </div>
                                </th>
                                <th class="table__head numeric">
                                    <div class="table__head-container">
                                        <div class="table__label">
                                            Телефон
                                        </div>
                                    </div>
                                </th>
                            </tr>
                            <tr class="table__row"
                                v-for="user of users"
                                :key="user.id"
                                @click="select(user.id)"
                            >
                                <td class="table__cell">
                                    <div class="table__cell-container">
                                        {{user.id}}
                                    </div>
                                </td>
                                <td class="table__cell">
                                    <div class="table__cell-container">
                                        {{user.email}}
                                    </div>
                                </td>
                                <td class="table__cell">
                                    <div class="table__cell-container">
                                        {{user.profile.name}}
                                    </div>
                                </td>
                                <td class="table__cell">
                                    <div class="table__cell-container">
                                        {{user.profile.surname}}
                                    </div>
                                </td>
                                <td class="table__cell">
                                    <div class="table__cell-container">
                                        {{user.profile.phone_number}}
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="users--error"
                    v-else
                >
                </div>
            </div>
            <div class="users--placeholder"
                v-else
            >
            </div>
        </transition>
    </md-content>
</template>

<script>
    import store from './../../store';

    const toLower = text => {
        return text.toString().toLowerCase()
    }

    const searchByName = (items, term) => {
        if (term) {
            return items.filter(item => toLower(item.name).includes(toLower(term)))
        }

        return items
    }

    export default {
        name: "users",
        store,
        data: () => ({
            componentTitle: "Пользователи",
            users: [],
            getListApiResponseRecieved: false,
            getListApiResponseError: false,
            search: null,
            searched: [],
            limit: 20,
            offset: 0,
            count: 0,
        }),
        computed: {
            showUsersList() {
                return (this.getListApiResponseRecieved && !this.getListApiResponseError)
            },
            listApiUrl() {
                return `/api/users/?limit=${this.limit}&offset=${this.offset}`
            },
            clientCount() {
                return (this.offset + this.limit)
            },
            hasPreviousPage() {
                return this.offset > 0
            },
            hasNextPage() {
                return this.clientCount < this.count;
            }
        },
        created() {
            this.initializeData();
            this.$store.commit('admin/changeAppTitle', this.componentTitle);
        },
        methods: {
            initializeData() {
                this.getUsers();
            },
            getUsers() {
                this.$http.get(this.listApiUrl).then(
                    response => {
                        this.handleSuccessfulGetListApiResponse(response);
                    },
                    response => {
                        this.handleFailedGetListApiResponse(response);
                    }
                )
            },
            handleSuccessfulGetListApiResponse(response) {
                this.users = response.body.results;
                this.count = response.body.count;
                this.searched = this.users;
                this.getListApiResponseRecieved = true;
                this.getListApiResponseError = false;
            },
            handleFailedGetListApiResponse(response) {
                this.getListApiResponseRecieved = true;
                this.getListApiResponseError = false;
            },
            searchOnTable () {
                this.searched = searchByName(this.users, this.search)
            },
            select(userID) {
                let path = `users/${userID}`;
                this.$router.push({path: path});
            },
            nextPage() {
                this.offset += this.limit;
                this.getUsers();
            },
            previousPage() {
                this.offset -= this.limit;
                this.getUsers();
            }
        }
    }
</script>

<style lang="scss" scoped>
    .users {
        height: 100%;
    }
    .users--content {
        height: 100%;
    }
    .users--table-wrap {
        height: 100%;
    }
    .users--controls {
        justify-content: flex-end;
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
</style>