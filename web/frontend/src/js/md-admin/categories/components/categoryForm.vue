<template>
    <md-content class="form"
        v-if="ready"
    >
        <div class="md-layout">
            <div class="md-layout-item">
                <md-button
                    class="md-primary"
                    @click="back"
                >
                    <md-icon>keyboard_backspace</md-icon>
                    НАЗАД
                </md-button>
            </div>
            <div class="md-layout-item form__buttons">
                <md-button
                    class="md-raised md-accent"
                    :disabled="categoryID===undefined"
                    @click="displayDeleteDialog = true"
                >
                    <md-icon>done</md-icon>
                    УДАЛИТЬ 
                </md-button>
                <md-button
                    class="md-raised md-accent"
                    :disabled="!hasChanged"
                    @click="rollback"
                >
                    <md-icon>settings_backup_restore</md-icon>
                    ОТМЕНИТЬ
                </md-button>
                <md-button
                    class="md-raised md-primary"
                    :disabled="!hasChanged"
                    @click="save"
                >
                    <md-icon>done</md-icon>
                    СОХРАНИТЬ
                </md-button>
            </div>
        </div>
        <div class="md-layout form__data"
            v-if="!categoryResponseError"
        >
            <div class="md-layout-item">
                <md-tabs>
                    <md-tab md-label="Основные данные">
                        <div class="md-layout">
                            <div class="md-layout-item">
                                <md-field>
                                    <label>ID</label>
                                    <md-input
                                        v-model="category.id"
                                        disabled
                                    >
                                    </md-input>
                                </md-field>
                                <md-field>
                                    <label>Название</label>
                                    <md-input
                                        v-model="category.name"
                                    >
                                    </md-input>
                                </md-field>
                                <md-field>
                                    <label>H1 Title</label>
                                    <md-input
                                        v-model="category._title"
                                    >
                                    </md-input>
                                </md-field>
                                <md-field>
                                    <label>URL (формируется автоматически)</label>
                                    <md-input
                                        v-model="category.url"
                                        disabled
                                    >
                                    </md-input>
                                </md-field>
                                <md-field>
                                    <label>Число запросов в месяц</label>
                                    <md-input
                                        v-model="category.scoring"
                                    >
                                    </md-input>
                                </md-field>
                                <md-field>
                                    <label>Поисковый рейтинг (для поиска на сайте)</label>
                                    <md-input
                                        v-model="category.search_scoring"
                                    >
                                    </md-input>
                                </md-field>
                            </div>
                            <div class="md-layout-item">
                            </div>
                        </div>
                    </md-tab>
                    <md-tab md-label="Атрибуты">
                        <attributes
                            :category="category"
                            :savingIteration="savingIteration"
                            :rollbackIteration="rollbackIteration"
                            v-on:change-option="changeOption"
                            v-on:add-active-option="addActiveOption"
                            v-on:remove-active-option="removeActiveOption"
                        >
                        </attributes>
                    </md-tab>
                    <md-tab md-label="Мета-теги">
                        <div class="md-layout">
                            <div class="md-layout-item">
                                <md-field>
                                    <label>
                                        meta-title
                                    </label>
                                    <md-input 
                                        v-model="category._meta_title"
                                        md-counter="256"
                                        max-length="256"
                                    >
                                    </md-input>
                                </md-field>
                                <md-field>
                                    <label>
                                        meta-keywords
                                    </label>
                                    <md-textarea 
                                        v-model="category._meta_keywords"
                                        md-counter="256"
                                        max-length="256"
                                    >
                                    </md-textarea>
                                </md-field>
                                <md-field>
                                    <label>
                                        meta-description
                                    </label>
                                    <md-textarea 
                                        v-model="category._meta_description"
                                        md-counter="256"
                                        max-length="256"
                                    >
                                    </md-textarea>
                                </md-field>
                            </div>
                            <div class="md-layout-item">
                            </div>
                        </div>
                        <div class="md-layout">
                        </div>
                    </md-tab>
                    <md-tab md-label="Описание">
                        <div class="form__description-wrap">
                            <editor
                                api-key="01cvgst8dh28i7irbbw1k430b4mi12q4pfb7sksuk67kkqpz"
                                :init="{
                                    height: 500,
                                    toolbar: 'formatselect | bold italic removeformat | bullist numlist | link | alignleft alignright aligncenter alignjustify',
                                    block_formats: 'параграф=p;Заголовок 2=h2;Заголовок 3=h3;Заголовок 4=h4;',
                                    plugins: 'lists, link'
                                }"
                                v-model="category.description"
                            >
                            </editor>
                        </div>
                    </md-tab>
                </md-tabs>
            </div>
        </div>

        <md-dialog :md-active.sync="displayDeleteDialog">
            <md-dialog-title>Подтверждение</md-dialog-title>
            <md-content class="dialog__content">
                Вы уверены что хотите удалить категорию {{category.name}}?
            </md-content>
            <md-dialog-actions>
                <md-button class="md-primary" @click="displayDeleteDialog = false">Отмена</md-button>
                <md-button class="md-accent" @click="deleteCategory">Удалить</md-button>
            </md-dialog-actions>
        </md-dialog>

    </md-content>
    <md-content
        v-else
        class="form__placeholder"
    >
        <md-progress-spinner :md-diameter="100" :md-stroke="10" md-mode="indeterminate">
        </md-progress-spinner>
    </md-content>
</template>

<script>
    import attributes from './categoryAttributes.vue'
    import Editor from '@tinymce/tinymce-vue';
    let equal = require('fast-deep-equal');

    export default {
        name: 'category-form',
        components: {
            "editor": Editor,
            "attributes": attributes
        },
        data: () => ({
            componentTitle: "",
            categoryID: undefined,
            categoryApiUrl: "/api/cubes/categories/",
            listApiUrl: "/api/cubes/categories/",
            categoryResponseReceived: false,
            categoryResponseError: false,
            initialized: false,
            displayDeleteDialog: false,
            category: {
                absolute_url: "",
                depth: 0,
                description: "",
                id: "",
                level: 0,
                name: "",
                parent: null,
                scoring: 0,
                search_scoring: 10,
                url: "",
                _meta_description: "",
                _meta_keywords: "",
                _meta_title: "",
                _title: "",
                attribute_values: []
            },
            proxyCategory: null,
            hasChanged: false,
            savingIteration: 0,
            rollbackIteration: 0,
        }),
        computed: {
            ready() {
                if (this.initialized) {
                    if (this.categoryID === undefined) {
                        return true
                    }
                    else {
                        return this.categoryResponseReceived
                    }
                }
                else {
                    return false
                }
            }
        },
        created() {
            this.initialize();
        },
        methods: {
            initialize() {
                this.categoryID = this.$route.params.id;
                if (this.categoryID === undefined) {
                    this.componentTitle = "Содание категории";
                    this.proxyCategory = JSON.parse(JSON.stringify(this.category));
                }
                else {
                    this.componentTitle = `Редактирование категории: ${this.categoryID}`;
                    this.categoryApiUrl = `/api/cubes/categories/${this.categoryID}/`;
                    this.getCategory();
                }
                this.$store.commit('admin/changeAppTitle', this.componentTitle);
                this.initialized = true;
            },
            getCategory() {
                this.$http.get(this.categoryApiUrl).then(
                    response => {
                        this.handleSuccessfulGetCategoryApiResponse(response);
                    },
                    response => {
                        this.handleFailedGetCategoryApiResponse(response);
                    }
                )
            },
            back() {
                this.$router.go(-1);
            },
            checkCategoryChanges() {
                this.hasChanged = !equal(this.category, this.proxyCategory);
            },
            changeOption(attributeId, valuesList, hasChanged) {
                let optionHasChanged = false;
                let option = valuesList[0];
                for (let i=0; i<this.category.attribute_values.length; i++) {
                    if (this.category.attribute_values[i].parent===attributeId) {
                        this.category.attribute_values[i] = option;
                        break
                    }
                }
                if (!optionHasChanged) {
                    this.category.attribute_values.push(option);
                }
            },
            addActiveOption(attributeId, option, hasChanged) {
                this.category.attribute_values.push(option);
            },
            removeActiveOption(attributeId, option, hasChanged) {
                let index = this.category.attribute_values.indexOf(option);
                if (index !== -1) {
                    this.category.attribute_values.splice(index, 1);
                }
            },
            save() {
                if (this.categoryID===undefined) {
                    this.createCategory();
                }
                else {
                    this.updateCategory();
                }
            },
            rollback() {
                this.category = JSON.parse(JSON.stringify(this.proxyCategory));
                this.rollbackIteration += 1;
            },
            createCategory() {
                let data = this.category;
                this.$http.post(this.listApiUrl, data).then(
                    response => {
                        this.handleSuccessfulCreateCategoryResponse(response);
                    },
                    response => {
                        this.handleFailedCreateCategoryResponse(response);
                    }
                )
            },
            updateCategory() {
                let data = this.category;
                this.$http.put(this.categoryApiUrl, data).then(
                    response => {
                        this.handleSuccessfulUpdateCategoryResponse(response);
                    },
                    response => {
                        this.handleFailedUpdateCategoryResponse(response);
                    }
                )
            },
            deleteCategory() {
                this.$http.delete(this.categoryApiUrl).then(
                    response => {
                        this.handleSuccessfulDeleteCategoryResponse(response);
                    },
                    response => {
                        this.handleFailedDeleteCategoryResponse(response);
                    }
                )
            },
            processCategory(category) {
                this.category = category;
                this.proxyCategory = JSON.parse(JSON.stringify(this.category));
                this.componentTitle = `Редактирование категории: ${this.categoryID} (${this.category.name})`;
                this.$store.commit('admin/changeAppTitle', this.componentTitle);
            },
            handleSuccessfulGetCategoryApiResponse(response) {
                this.processCategory(response.body);
                this.categoryResponseError = false;
                this.categoryResponseReceived = true;
            },
            handleFailedGetCategoryApiResponse(response) {
                this.categoryResponseError = true;
                this.categoryResponseReceived = true;
            },
            handleSuccessfulCreateCategoryResponse(response) {
                this.processCategory(response.body);
            },
            handleFailedCreateCategoryResponse(response) {
                console.log(response);
            },
            handleSuccessfulUpdateCategoryResponse(response) {
                this.processCategory(response.body);
            },
            handleFailedUpdateCategoryResponse(response) {
                console.log(response);
            },
            handleSuccessfulDeleteCategoryResponse(response) {
                this.$router.go(-1);
            },
            handleFailedDeleteCategoryResponse(response) {
                console.log(response);
            },
        },
        watch: {
            category: {
                handler() {
                    if (this.initialized) {
                        this.checkCategoryChanges();
                    }
                },
                deep: true
            }
        }
    }
</script>

<style lang="scss" scoped>
    .controls {
        display: flex;
        width: 100%;
        justify-content: flex-end;
    }
    .form__buttons {
        display: flex;
        justify-content: flex-end !important;
    }
    .form__placeholder {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 400px;
        width: 100%;
    }
    .dialog__content {
        padding: 16px;
    }
    .top-nav {
        padding: 0px 0px 16px 0px;
    }
    .fade {
        opacity: 1 !important;
        transition: opacity 1s
    }
    .fade-fast {
        opacity: 1 !important;
        transition: opacity 0.2s
    }
    .fade-fast-enter-active, .fade-fast-leave-active{
        transition: opacity 0.2s
    }
    .fade-enter-active, .fade-leave-active{
        transition: opacity 1s
    }
    .fade-enter, .fade-leave-to, 
    .fade-fast-enter, .fade-fast-leave-to  {
        opacity: 0
    }
</style>