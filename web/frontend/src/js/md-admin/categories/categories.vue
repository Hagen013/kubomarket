<template>
    <md-content class="categories">
        <div class="categories__content"
            v-if="showContent"
        >
            <div class="categories__controls">
                <div class="categories__controls-item">
                    <md-field>
                        <md-icon>search</md-icon>
                        <label>Поиск</label>
                        <md-input v-model="query"></md-input>
                    </md-field>
                </div>
                <div class="categories__controls-item">
                    <md-button class="md-raised md-primary"
                        @click="create"
                    >
                        <md-icon>add</md-icon>
                        Создать категорию
                    </md-button>
                </div>
            </div>
            <div class="categories__wrap">
                <ul class="categories__tree"
                    v-if="displayModeTree"
                >
                </ul>
                <table class="table"
                    v-else
                >
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
                                    Parent ID
                                </div>
                            </div>
                        </th>
                        <th class="table__head">
                            <div class="table__head-container">
                                <div class="table__label">
                                    Название
                                </div>
                            </div>
                        </th>
                        <th class="table__head numeric">
                            <div class="table__head-container">
                                <div class="table__label">
                                    Глубина в каталоге
                                </div>
                            </div>
                        </th>
                        <th class="table__head">
                            <div class="table__head-container">
                                <div class="table__label">
                                    URL
                                </div>
                            </div>
                        </th>
                        <th class="table__head numeric">
                            <div class="table__head-container">
                                <div class="table__label">
                                    Скоринг
                                </div>
                            </div>
                        </th>
                    </tr>
                    <tr class="table__row"
                        v-for="node of filteredCategories"
                        :key="node.id"
                        @click="showCategory(node)"
                    >
                        <td class="table__cell">
                            <div class="table__cell-container">
                                {{node.id}}
                            </div>
                        </td>
                        <td class="table__cell">
                            <div class="table__cell-container">
                                {{node.parent}}
                            </div>
                        </td>
                        <td class="table__cell">
                            <div class="table__cell-container">
                                {{node.name}}
                            </div>
                        </td>
                        <td class="table__cell">
                            <div class="table__cell-container">
                                {{node.depth}}
                            </div>
                        </td>
                        <td class="table__cell">
                            <div class="table__cell-container">
                                /catalog/{{node.url}}
                            </div>
                        </td>
                        <td class="table__cell">
                            <div class="table__cell-container">
                                {{node.scoring}}
                            </div>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="categories__placeholder"
            v-else
        >
            <md-progress-spinner :md-diameter="80" :md-stroke="10" md-mode="indeterminate">
            </md-progress-spinner>
        </div>
    </md-content>
</template>

<script>
    import store from './../../store'
    import debounce from 'debounce'
    import fuzzy from 'fuzzysearch'

    export default {
        name: 'categories',
        store,
        data: () => ({
            componentTitle: "Категории",
            limit: 100,
            offset: 0,
            count: 0,
            responseRecieved: false,
            responseError: false,
            listApiUrl: "/api/cubes/categories/",
            categories: [],
            displayModeTree: false,
            query: ""
        }),
        computed: {
            showContent() {
                return (this.responseRecieved && !this.responseError)
            },
            queryParams() {
                return {
                    "limit": this.limit,
                    "offset": this.offset
                }
            },
            sortedNodes() {
                return this.categories
            },
            displayModeCaption() {
                if (this.displayModeTree) {
                    return "Дерево"
                }
                return "Список"
            },
            filteredCategories() {
                return this.categories.filter(item => this.matchText(item.name))
            },
        },
        created() {
            this.$store.commit('admin/changeAppTitle', this.componentTitle);
            this.getCategories();
        },
        mounted() {
        },
        methods: {
            getCategories() {
                this.$http.get(this.listApiUrl, {params: this.params}).then(
                    response => {
                        this.handleSuccessfulGetResponse(response);
                    },
                    response => {
                        this.handleFailedGetResponse(response);
                    }
                )
            },
            handleSuccessfulGetResponse(response) {
                this.categories = response.body["results"];
                this.count = response.body["count"];
                this.responseError = false;
                this.responseRecieved = true;
            },
            handleFailedGetResponse(response) {
                this.responseError = true;
                this.responseRecieved = true;
            },
            showCategory(node) {
                let path = `category/${node.id}`;
                this.$router.push({path: path});
            },
            create() {
                let path = "/category"
                this.$router.push({path: path});
            },
            matchText(item) {
                const target = item.toLowerCase();
                const search = this.query.toLowerCase();
                return fuzzy(search, target)
            }
        }
    }
</script>

<style lang="scss" scoped>
    .categories__controls {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
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

    .categories__placeholder {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 400px;
        width: 100%;
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