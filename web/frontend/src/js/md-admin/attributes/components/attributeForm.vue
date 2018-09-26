<template>
    <md-content class="attribute">
        <div class="form"
            v-if="showForm"
        >
            <div class="toolbar">
                <div class="controls">
                    <div class="controls__left">
                        <md-button class="md-primary"
                            @click="back"
                        >
                            <md-icon>keyboard_backspace</md-icon>
                            НАЗАД
                        </md-button>
                    </div>
                    <div class="controls__right">
                        <md-button
                            class="md-raised md-primary"
                            @click="saveChanges"
                            :disabled="!hasChanged"
                        >
                            <md-icon>done</md-icon>
                            СОХРАНИТЬ
                        </md-button>
                        <md-button
                            class="md-raised md-accent"
                            @click="rollbackChanges"
                            :disabled="!hasChanged"
                        >
                            <md-icon>settings_backup_restore</md-icon>
                            ОТМЕНИТЬ
                        </md-button>
                        <md-button class="md-raised md-accent"
                            @click="showDeleteAttributeDialog = true"
                            disabled
                        >
                            <md-icon>delete</md-icon>
                            УДАЛИТЬ
                        </md-button>
                    </div>
                </div>
            </div>
            <md-tabs class="tabs">
                <md-tab md-label="Главное">
                    <div class="md-layout">
                        <div class="md-layout-item">
                            <md-field>
                                <label>Название</label>
                                <md-input
                                    v-model="attribute.name"
                                    @input="handleNewAttributeNameInput"
                                >
                                </md-input>
                            </md-field>
                            <md-field>
                                <label>Key</label>
                                <md-input
                                    v-model="attribute.key"
                                >
                                </md-input>
                            </md-field>
                            <md-field>
                                <label>Тип</label>
                                <md-select
                                    v-model="attribute.attribute_type"
                                    name="attribute-type"
                                    id="attribute-type"
                                    @change="handleAttributeTypeChange"
                                >
                                    <md-option value="1">Choice</md-option>
                                    <md-option value="2">Multi-choice</md-option>
                                    <md-option value="3">Numeric</md-option>
                                </md-select>
                            </md-field>
                        </div>
                        <div class="md-layout-item">
                        </div>
                    </div>
                </md-tab>
                <md-tab md-label="Значения">
                    <div class="values__placeholder values_placeholder_type"
                        v-if="showNumericPlaceholder"
                    >
                        <span class="md-display-1">
                        Для численных атрибутов не предусмотрено добавление отдельных значений
                        </span>
                    </div>
                    <table class="table"
                        v-else-if="showValuesForm"
                    >
                        <tr class="table__row">
                            <th class="table__head">
                                ID
                            </th>
                            <th class="table__head text_left">
                                Название
                            </th>
                            <th class="table__head text_left">
                                Slug
                            </th>
                            <th class="table__head">
                            </th>
                            <th class="table__head">
                            </th>
                        </tr>
                        <tr class="table__row">
                            <td class="table__cell">
                            </td>
                            <td class="table__cell table__cell_dense">
                                <md-field md-inline
                                    class="edit-field"
                                >
                                    <label>name</label>
                                    <md-input
                                        v-model="newValue.name"
                                        @input="handleNewValueNameInput"
                                    >
                                    </md-input>
                                </md-field>
                            </td>
                            <td class="table__cell table__cell_dense">
                                <md-field md-inline
                                    class="edit-field"
                                >
                                    <label>slug</label>
                                    <md-input
                                        v-model="newValue.slug"
                                    >
                                    </md-input>
                                </md-field>
                            </td>
                            <td class="table__cell"
                                colspan="2"
                            >
                                <md-button class="md-primary md-raised"
                                    :disabled="!newAttributeIsValid"
                                    @click="addValue"
                                >
                                    <md-icon>done</md-icon>
                                    ДОБАВИТЬ   
                                </md-button>
                            </td>
                        </tr>
                        <tr class="table__row"
                            v-for="value in sortedValues"
                            :key="value.id"
                        >
                            <td class="table__cell text_center">
                                {{value.id}}
                            </td>
                            <td class="table__cell">
                                {{value.name}}
                            </td>
                            <td class="table__cell">
                                {{value.slug}}
                            </td>
                            <td class="table__cell">
                                <md-button class="md-fab md-mini md-primary" disabled>
                                    <md-icon>edit</md-icon>
                                </md-button>
                            </td>
                            <td class="table__cell">
                                <md-button class="md-fab md-mini"
                                    disabled
                                    @click="triggerDelete(value)"
                                >
                                    <md-icon>delete</md-icon>
                                </md-button>
                            </td>
                        </tr>
                    </table>
                    <div class="values__placeholder"
                        v-else
                    >
                        <span class="md-display-1">
                        Атрибут ещё не создан
                        </span>
                    </div>
                </md-tab>
            </md-tabs>
        </div>
        <div class="error"
            v-else-if="initialized"
        >
            Во время обращения к серверу произошла ошибка
        </div>
        <div class="placeholder"
            v-else
        >
            <md-progress-spinner :md-diameter="100" :md-stroke="10" md-mode="indeterminate">
            </md-progress-spinner>
        </div>
        <md-dialog :md-active.sync="showDeleteDialog" class="dialog">
            <md-dialog-title>Подтверждение</md-dialog-title>
            <md-dialog-content>
                <p>
                    Удаление AttributeValue может привести к удалению так же связанных и категорий. Вы уверены, что хотите продолжить?
                </p>
                <md-button class="md-raised md-accent"
                    @click="deleteValue"
                >
                    УДАЛИТЬ
                </md-button>
                <md-button class="md-raised md-primary"
                    @click="showDeleteDialog=false"
                >
                    ОТМЕНА
                </md-button>
            </md-dialog-content>
        </md-dialog>
        <md-dialog :md-active.sync="showDeleteAttributeDialog" class="dialog">
            <md-dialog-title>Подтверждение</md-dialog-title>
            <md-dialog-content>
                <p>
                    Удаление Attribute может привести к удалению так же связанных и категорий. Вы уверены, что хотите продолжить?
                </p>
                <md-button class="md-raised md-accent"
                    @click="deleteAttribute"
                >
                    УДАЛИТЬ
                </md-button>
                <md-button class="md-raised md-primary"
                    @click="showDeleteAttributeDialog=false"
                >
                    ОТМЕНА
                </md-button>
            </md-dialog-content>
        </md-dialog>
        <md-snackbar 
            md-position="center" 
            :md-duration="snackbarDuration" 
            :md-active.sync="showSnackbar" 
            md-persistent>
            <span>{{snackbarText}}</span>
        </md-snackbar>
    </md-content>
</template>

<script>
    import transliterate from "../../../core/transliterate.js";
    const equal = require('fast-deep-equal');

    export default {
        name: "attribute",
        data: () => ({
            componentTitle: "Создание атрибута",
            attributeID: undefined,
            initialized: false,
            attribute: {
                name: "",
                key: "",
                attribute_type: "2",
                unit: "",
                values: []
            },
            proxyAttribute: {
                name: "",
                key: "",
                attribute_type: "2",
                unit: "",
                values: []
            },
            initialized: false,
            responseError: false,
            newAttribute: {
                name: "",
                key: "",
                attribute_type: "2"
            },
            newValue: {
                name: "",
                slug: "",
                value: ""
            },
            showDeleteDialog: false,
            valueToDelete: null,
            valueToUpdate: null,
            showSnackbar: false,
            snackbarText: "",
            snackbarDuration: 4000,
            apiListUrl: "/api/cubes/attributes/",
            showDeleteAttributeDialog: false
        }),
        computed: {
            instanceApiUrl() {
                return `/api/cubes/attributes/${this.attributeID}/`
            },
            instanceValuesListApiUrl() {
                return `/api/cubes/attributes/${this.attributeID}/values/`
            },
            showForm() {
                if (this.attributeID === undefined) {
                    return true
                }
                if (this.initialized && !this.responseError) {
                    return true
                }
                return false
            },
            newAttributeIsValid() {
                return ( (this.newValue.name !== "") && (this.newValue.slug !== "") )
            },
            sortedValues() {
                return this.attribute.values.sort(function(a, b) {
                    return b.id - a.id
                })
            },
            hasChanged() {
                return !equal(this.attribute, this.proxyAttribute);
            },
            showValuesForm() {
                if (this.attributeID === undefined) {
                    return false
                }
                return true
            },
            showNumericPlaceholder() {
                return this.proxyAttribute.attribute_type == 3;
            }
        },
        created() {
            this.initialize();
        },
        methods: {
            initialize() {
                this.attributeID = this.$route.params.id;
                if (this.attributeID === undefined) {
                    this.componentTitle = "Создание атрибута";
                    this.proxyAttribute = JSON.parse(JSON.stringify(this.attribute));
                } else {
                    this.componentTitle = `Редактирование атрибута: ${this.attributeID}`;
                    this.getAttribute();
                }
                this.$store.commit('admin/changeAppTitle', this.componentTitle);
                this.initialized = true;
            },
            getAttribute() {
                this.$http.get(this.instanceApiUrl).then(
                    response => {
                        this.handleSuccessfulGetResponse(response);
                    },
                    response => {
                        this.handleFailedGetResponse(response);
                    }
                )
            },
            create() {
                this.$http.post(this.apiListUrl, this.attribute).then(
                    response => {
                        this.handleSuccessfulPostResponse(response);
                    },
                    response => {
                        this.handleFailedPostResponse(response);
                    }
                )
            },
            update() {
                this.$http.put(this.instanceApiUrl, this.attribute).then(
                    response => {
                        this.handleSuccessfulPutResponse(response);
                    },
                    response => {
                        this.handleFailedPutResponse(response);
                    }
                )
            },
            deleteAttribute() {
                console.log(this.instanceApiUrl);
                this.$http.delete(this.instanceApiUrl, this.attribute).then(
                    response => {
                        this.handleSuccessfulDeleteResponse(response);
                    },
                    response => {
                        this.handleFailedDeleteResponse(response);
                    }
                )
            },
            processAttribute(attribute) {
                this.attribute = attribute;
                this.proxyAttribute = JSON.parse(JSON.stringify(this.attribute));
                this.componentTitle = `Редактирование атрибута: ${this.attributeID} (${this.attribute.name})`;
                this.$store.commit('admin/changeAppTitle', this.componentTitle);
            },
            handleSuccessfulGetResponse(response) {
                this.processAttribute(response.body);
                this.initialized = true;
                this.responseError = false;
            },
            handleFailedGetResponse(response) {
                this.initialized = true;
                this.responseError = true;
            },
            handleSuccessfulPutResponse(response) {
                this.attribute = response.body;
                this.attributeID = this.attribute.id;
                this.proxyAttribute = JSON.parse(JSON.stringify(this.attribute));
                this.snackbarText = "Изменения сохранены";
                this.showSnackbar = true;
            },
            handleFailedPutResponse(response) {
                this.snackbarText = "Не удалось сохранить изменения";
                this.showSnackbar = true;
            },
            handleSuccessfulPostResponse(response) {
                this.proxyAttribute = JSON.parse(JSON.stringify(this.attribute));
                this.attribute = response.body;
                this.attributeID = this.attribute.id;
                this.snackbarText = "Атрибут создан";
                this.showSnackbar = true;
            },
            handleFailedPostResponse(response) {
                this.snackbarText = "Не удалось создать атрибут";
                this.showSnackbar = true;
            },
            handleSuccessfulDeleteResponse(response) {
                this.showDeleteDialog = false;
                this.back();
            },
            handleFailedDeleteResponse(response) {
                this.snackbarText = "Не удалось удалить атрибут";
                this.showSnackbar = true;
            },
            saveChanges() {
                if (this.attributeID === undefined) {
                    this.create();
                } else {
                    this.update();
                }
            },
            rollbackChanges() {
                this.attribute = JSON.parse(JSON.stringify(this.proxyAttribute));
            },
            triggerDelete(value) {
                this.showDeleteDialog = true;
                this.valueToDelete = value;
            },
            back() {
                this.$router.go(-1);
            },
            addValue() {
                this.newValue.attribute = this.attributeID;
                this.newValue.attribute_type = this.attribute.attribute_type;
                this.newValue.value = this.newValue.slug;
                this.$http.post(this.instanceValuesListApiUrl, this.newValue).then(
                    response => {
                        this.handleSuccessfulCreateValueResponse(response)
                    },
                    response => {
                        this.handleFailedCreateValueResponse(response)
                    }
                )
            },
            deleteValue() {
                let url = `${this.instanceValuesListApiUrl}${this.valueToDelete.id}/`;
                this.$http.delete(url).then(
                    response => {
                        this.handleSuccessfulDeleteValueResponse(response);
                    },
                    response => {
                        this.handleFailedDeleteValueResponse(response);
                    }
                )
            },
            updateValue() {
                let url = `${this.instanceValuesListApiUrl}${this.valuesToUpdate.id}/`;
                this.$http.put(url).then(
                    response => {
                        this.handleSuccessfulUpdateValueResponse(response);
                    },
                    response => {
                        this.handleFailedUpdateValueResponse(response);
                    }
                )
            },
            handleSuccessfulCreateValueResponse(response) {
                this.getAttribute();
                this.snackbarText = "Значение успешно добавлено";
                this.showSnackbar = true;
            },
            handleFailedCreateValueResponse(response) {
                this.snackbarText = "Не удалось добавить значение";
                this.showSnackbar = true;
            },
            handleSuccessfulUpdateValueResponse(response) {
            },
            handleFailedUpdateValueResponse(response) {
            },
            handleSuccessfulDeleteValueResponse(response) {
                this.getAttribute();
                this.showDeleteDialog = false;
                this.snackbarText = "Значение успешно удалено";
                this.showSnackbar = true;
            },
            handleFailedDeleteValueResponse(response) {
                this.snackbarText = "Не удалось удалить значение";
                this.showSnackbar = true;
            },
            handleNewValueNameInput(name) {
                this.newValue.slug = transliterate(name).toLowerCase();
            },
            handleNewAttributeNameInput(name) {
                this.attribute.key = transliterate(name).toLowerCase();
            },
            back() {
                this.$router.go(-1);
            },
            handleAttributeTypeChange() {
                this.attribute.attribute_type = Number(this.attribute.attribute_type);
            }
        }
    }
</script>

<style lang="scss" scoped>
    .controls {
        display: flex;
        justify-content: space-between;
    }
    .main {
        max-width: 400px;
    }
    .input-row-box {
        margin-right: 32px;
    }
    .tabs {
        padding: 24px 0px 0px 0px;
    }
    .table {
        margin-top: 32px;
        width: 100%;
    }
    .table__head {
        padding: 12px 0px;
    }
    .table__cell {
        border-top-color: rgba(0,0,0,.12);
        border-top: 1px solid rgba(0,0,0,.12);
    }
    .table__cell_dense {
        padding: 0px 32px 0px 0px;
    }
    .text_left {
        text-align: left;
    }
    .text_right {
        text-align: right;
    }
    .text_center {
        text-align: center;
    }
    .values {
        margin: 32px 0px 0px 0px;
        width: 700px;
        min-height: 100%;
        display: flex;
        flex-direction: column;
    }
    .value {
        display: flex;
        align-items: center;
        border-top-color: rgba(0,0,0,.12);
        border-top: 1px solid rgba(0,0,0,.12);
    }
    .value__id {
        width: 80px;
        text-align: left;
    }
    .value__name {
        width: 520px;
    }
    .value__delete {

    }
    .save-fab {
        background: #00e676 !important;
    }
    .dialog {
        max-width: 768px;
    }
    .values__placeholder {
        padding: 60px 0px;
        display: flex;
        justify-content: center;
        align-items: center;
    }
</style>
