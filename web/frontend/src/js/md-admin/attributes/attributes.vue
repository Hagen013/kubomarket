<template>
    <md-content class="attributes">
        <div class="toolbar">
            <div class="search-box">
                <md-field>
                    <md-icon>search</md-icon>
                    <label>Поиск</label>
                    <md-input v-model="query"></md-input>
                </md-field>
            </div>
            <md-button class="md-primary md-raised"
                @click="createAttribute"
            >
                <md-icon>
                add
                </md-icon>
                Создать атрибут
            </md-button>
        </div>
        <table class="table">
            <tr>
                <th class="table__head">
                    ID
                </th>
                <th class="table__head text_left">
                    Название
                </th>
                <th class="table__head text_left">
                    Тип
                </th>
                <th class="table__head text_left">
                    Количество значений
                </th>
            </tr>
            <tr class="table__row"
                v-for="attribute in filteredAttributes"
                :key="attribute.id"
                @click="selectAttribute(attribute)"
            >
                <td class="table__cell text_center">
                    {{attribute.id}}
                </td>
                <td class="table__cell">
                    {{attribute.name}}
                </td>
                <td class="table__cell">
                    {{attribute.attribute_type|attributeTypeFilter}}
                </td>
                <td class="table__cell">
                    {{attribute|countValues}}
                </td>
            </tr>
        </table>
    </md-content>
</template>

<script>
    import fuzzy from 'fuzzysearch'

    export default {
        name: "attributes",
        data: () => ({
            apiListUrl: "/api/cubes/attributes/",
            attributes: [],
            query: "",
        }),
        computed: {
            filteredAttributes() {
                return this.attributes.filter(item => this.matchText(item.name))
            },
        },
        created() {
            this.getAttributes();
        },
        methods: {
            getAttributes() {
                this.$http.get(this.apiListUrl).then(
                    response => {
                        this.handleSuccessfulGetListAttributes(response);
                    },
                    response => {
                        this.handleFailedGetListAttributes(response);
                    }
                )
            },
            createAttribute() {
                let path = "/attribute"
                this.$router.push({path: path});
            },
            handleSuccessfulGetListAttributes(response) {
                this.attributes = response.body;
            },
            handleFailedGetListAttributes(response) {
            },
            selectAttribute(attribute) {
                let path = `attribute/${attribute.id}`;
                this.$router.push({path: path});
            },
            matchText(item) {
                const target = item.toLowerCase();
                const search = this.query.toLowerCase();
                return fuzzy(search, target)
            },
        },
        filters: {
            attributeTypeFilter(typeId) {
                if (typeId === 1) {
                    return "Choice"
                } else if (typeId === 2) {
                    return "Multi-choice"
                } else if (typeId === 3) {
                    return "Numeric"
                }
            },
            countValues(attribute) {
                let count = 0;
                if (attribute.attribute_type === 3) {
                    return "[ ... ]"
                }
                for (let value in attribute.values) {
                    count += 1;
                }
                return String(count)
            }
        }
    }
</script>

<style lang="scss" scoped>
    .table {
        width: 100%;
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
    .table__head {
        padding: 12px;
    }
    .table__cell {
        padding: 12px;
        border-top-color: rgba(0,0,0,.12);
        border-top: 1px solid rgba(0,0,0,.12);
    }
    .text_center {
        text-align: center;
    }
    .text_left {
        text-align: left;
    }
    .text_right {
        text-align: right;
    }
    .toolbar {
        display: flex;
        justify-content: space-between;
    }
    .search-box {
        max-width: 400px;
    }
</style>
