<template>
    <md-content class="categories">
        <transition name="fade-fast">
            <div class="content-overlay" v-if="!responseRecieved">
                <md-progress-spinner md-mode="indeterminate">
                </md-progress-spinner>
            </div>
        </transition>
        <transition name="fade">
            <md-card>
                <div class="top-nav">
                    <md-button class="md-primary md-raised"
                        @click="categoryFormRedirect"
                    >
                        <md-icon>add</md-icon>
                        СОЗДАТЬ
                    </md-button>
                    <md-field md-inline class="search-field">
                        <label>Найти</label>
                        <md-input v-model="searchQuery">
                        </md-input>
                        <md-icon>
                        search
                        </md-icon>
                    </md-field>
                    <div class="pagination">
                        <span>Отображать по</span>
                        <md-field>
                            <md-select v-model="pageSize" name="pagesize" id="pagesize"
                                md-dense md-class="md-pagination-select"
                            >
                                <md-option value="50">50</md-option>
                                <md-option value="100">100</md-option>
                                <md-option value="200">200</md-option>
                            </md-select>
                        </md-field>
                        <span>{{listOffset}}-{{listLimit}} из {{count}}</span>
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
                <md-table class="table" v-model="proxyCategories">
                    <md-table-row 
                        slot="md-table-row"
                        slot-scope="{ item }"
                        @click.native="categoryFormRedirect(item)"
                    >
                        <md-table-cell md-label="ID" md-numeric class="item-id">{{ item.id }}</md-table-cell>
                        <md-table-cell md-label="Название">{{ item.name }}</md-table-cell>
                        <md-table-cell md-label="Глубина" md-numeric>{{ item.depth }}</md-table-cell>
                    </md-table-row>
                </md-table>
            </md-card>
        </transition>
    </md-content>
</template>

<script>
    import store from './../../store';
    import debounce from 'debounce'

    export default {
        name: 'categories',
        store,
        data: () => ({
            componentTitle: 'Редактирование категорий',
            apiListUrl: '/api/categories/',
            pageSize: 100,
            count: 0,
            currentPage: 0,
            listOrdering: '_depth',
            categories: [],
            searchQuery: '',
            responseRecieved: false,
            requestError: false,
            selected: {},
        }),
        computed: {
            listOffset() {
                return (this.pageSize * this.currentPage)
            },
            listLimit() {
                let limit = (this.listOffset + Number(this.pageSize));
                if ( (this.count !== 0) && (limit > this.count) ) {
                    limit = this.count;
                }
                return limit
            },
            requestSucceded() {
                return (this.responseRecieved && !this.responseError)
            },
            requestFailed() {
                return (this.responseRecieved && this.responseError)
            },
            proxyCategories() {
                return this.categories;
            },
            hasPreviousPage() {
                return this.listOffset > 0
            },
            hasNextPage() {
                return this.listLimit < this.count
            }
        },
        created() {
            this.$store.commit('admin/changeAppTitle', this.componentTitle);
            this.getCategoriesList();
        },
        mounted() {
        },
        methods: {
            getCategoriesList() {
                let query = `?offset=${this.listOffset}&limit=${this.listLimit}&ordering=${this.listOrdering}`;
                if (this.searchQuery !== '') {
                    query += `&search=${this.searchQuery}`;
                }
                let url = this.apiListUrl + query
                this.$http.get(url).then(
                    response => {
                        this.handleSuccessfulListResponse(response);
                    },
                    response => {
                        this.handleFailedListResponse(response);
                    }
                )
            },
            handleSuccessfulListResponse(response) {
                this.categories = response.body.results;
                this.count = response.body.count;
                this.responseRecieved = true;
                this.requestError = false;
            },
            handleFailedListResponse(response) {
                this.responseRecieved = true;
                this.requestError = true;
            },
            getClass: ({ id }) => ({
                'md-primary': id === 2,
                'md-accent': id === 3
            }),
            previousPage() {
                this.currentPage -= 1;
            },
            nextPage() {
                this.currentPage += 1;
            },
            categoryFormRedirect(category) {
                let id = category.id;
                let path = '';
                if (id !== undefined) {
                    path = `category/${id}`;
                } else {
                    path = `category/`
                }
                this.$router.replace({path: path});
            },
        },
        watch: {
            currentPage() {
                this.getCategoriesList();
            },
            pageSize() {
                this.getCategoriesList();
            },
            searchQuery: debounce(function() {
                this.currentPage = 0;
                this.responseRecieved = false;
                this.getCategoriesList();
            }, 1000),
        }
    }
</script>

<style lang="scss" scoped>
    .content-overlay {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        width: 100%;
        position: fixed;
        top: 0px;
        left: 0px;
        z-index: 10000;
        background: rgba(255,255,255,0.5);
    }
    .item-id {
        width: 100px !important;
    }
    .top-nav {
        display: flex;
        width: 100%;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(0,0,0,0.12);
    }
    .pagination {
        display: flex;
        height: 56px;
        max-width: 400px;
        min-width: 400px;
        flex: 1;
        align-items: center;
        justify-content: flex-end;
        font-size: 12px !important;
        .md-field {
            width: 52px;
            min-width: 36px;
            margin: -16px 24px 0 32px;
            &:after,
            &:before {
                display: none;
            }
            .md-select-value {
                font-size: 13px;
            }
        }
    }
    .md-pagination-select {
        max-width: 82px;
        min-width: 56px;
        margin-top: 5px;
        font-size: 12px;
    }
    .search-field {
        min-width: 250px;
        max-width: 500px;
    }
    .search-icon {
        position: absolute;
        top: 17px;
        right: 14px;
    }
    .md-table-row {
        cursor: pointer;
    }




    .fade-fast, .fadeFast {
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