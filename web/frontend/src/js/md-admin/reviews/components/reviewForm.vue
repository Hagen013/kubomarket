<template>
    <md-content class="review instance-editor">
        <div class="review__placeholder placeholder"
            v-if="!initialized"
        >
            <md-progress-spinner :md-diameter="100" :md-stroke="10" md-mode="indeterminate">
            </md-progress-spinner>
        </div>
        <div class="review__content instance-form"
            v-else-if="!apiResponseError"
        >
            <div class="instance-form__controls">
                <div class="instance-form__controls-left">
                    <md-button class="md-primary"
                        @click="back"
                    >
                        <md-icon>keyboard_backspace</md-icon>
                        НАЗАД
                    </md-button>
                </div>
                <div class="instance-form__controls-right">
                    <md-button class="md-primary md-raised"
                        :disabled="!hasChanged"
                        @click="saveChanges"
                    >
                        <md-icon>
                            done
                        </md-icon>
                        СОХРАНИТЬ
                    </md-button>
                    <md-button class="md-accent md-raised"
                        :disabled="!hasChanged"
                        @click="rollbackChanges"
                    >
                        <md-icon>
                            settings_backup_restore
                        </md-icon>
                        ОТМЕНИТЬ ИЗМЕНЕНИЯ
                    </md-button>
                    <md-button class="md-accent md-raised"
                        @click="showDeleteDialog=true"
                    >
                        <md-icon>
                            delete
                        </md-icon>
                        УДАЛИТЬ
                    </md-button>
                </div>
            </div>
            <md-tabs>
                <md-tab md-label="Отзыв">
                    <div class="md-layout tabs__content">
                        <div class="md-layout-item">
                            <md-field>
                                <label></label>
                                <md-select
                                    v-model="instance.status"
                                >
                                    <md-option value="новый">Новый</md-option>
                                    <md-option value="одобрен">Одобрен</md-option>
                                    <md-option value="отклонен">Отклонен</md-option>
                                </md-select>
                            </md-field>
                            <md-field>
                                <label>Оценка</label>
                                <md-select
                                    v-model="instance.rating"
                                >
                                    <md-option value="1">0.5</md-option>
                                    <md-option value="2">1</md-option>
                                    <md-option value="3">1.5</md-option>
                                    <md-option value="4">2</md-option>
                                    <md-option value="5">2.5</md-option>
                                    <md-option value="6">3</md-option>
                                    <md-option value="7">3.5</md-option>
                                    <md-option value="8">4</md-option>
                                    <md-option value="9">4.5</md-option>
                                    <md-option value="10">5</md-option>
                                </md-select>
                            </md-field>
                            <md-field>
                                <label>Текст</label>
                                <md-textarea
                                    v-model="instance.content"
                                >
                                </md-textarea>
                            </md-field>
                        </div>
                        <div class="md-layout-item">
                        </div>
                    </div>
                </md-tab>
                <md-tab md-label="Клиент">
                    <div class="md-layout">
                        <div class="md-layout-item">
                            <md-field>
                                <label>ID</label>
                                <md-input v-model="instance.user.id" disabled>
                                </md-input>
                            </md-field>
                            <md-field>
                                <label>Email</label>
                                <md-input v-model="instance.user.email" disabled>
                                </md-input>
                            </md-field>
                            <md-field>
                                <label>Телефон</label>
                                <md-input v-model="instance.user.profile.phone_number" disabled></md-input>
                            </md-field>
                            <md-field>
                                <label>Имя</label>
                                <md-input v-model="instance.user.profile.name" disabled></md-input>
                            </md-field>
                            <md-field>
                                <label>Фамилия</label>
                                <md-input v-model="instance.user.profile.surname" disabled></md-input>
                            </md-field>
                            <md-field>
                                <label>Отчество</label>
                                <md-input v-model="instance.user.profile.patronymic" disabled></md-input>
                            </md-field>
                        </div>
                        <div class="md-layout-item">
                        </div>
                    </div>
                </md-tab>
            </md-tabs>
        </div>
        <div class="review__error placeholder placeholder_error"
            v-else
        >
            <div class="md-display-2">
                Во время соединения с сервером произошла ошибка
            </div>
        </div>
        <md-snackbar
            md-position="center"
            :md-duration="snackbarDuration"
            :md-active.sync="showSnackbar"
            md-persistent>
            <span>{{snackbarText}}</span>
        </md-snackbar>
        <md-dialog
            :md-active.sync="showDeleteDialog"
        >
            <md-dialog-title>
                Необходимо подтверждение
            </md-dialog-title>
            <md-dialog-content>
                Вы действительно хотите удалить данный отзыв?
                <div class="delete-dialog__controls">
                    <md-button class="md-raised md-accent"
                        @click="deleteInstance"
                    >
                        <md-icon>delete</md-icon>
                        УДАЛИТЬ
                    </md-button>
                    <md-button class="md-raised md-primary"
                        @click="showDeleteDialog=false"
                    >
                        <md-icon>cancel</md-icon>
                        ОТМЕНА
                    </md-button>
                </div>
            </md-dialog-content>
        </md-dialog>
    </md-content>
</template>

<script>
    const equal = require('fast-deep-equal');

    export default {
        name: "review",
        data: () => ({
            baseApiUrl: "/api/reviews/",
            instanceId: null,
            showSnackbar: false,
            snackbarText: "",
            snackbarDuration: 4000,
            initialized: false,
            apiResponseError: false,
            instance: null,
            proxyInstance: null,
            showDeleteDialog: false
        }),
        computed: {
            instanceApiUrl() {
                return `${this.baseApiUrl}${this.instanceId}/`
            },
            hasChanged() {
                return !equal(this.instance, this.proxyInstance)
            }
        },
        created() {
            this.initialize();
        },
        methods: {
            initialize() {
                this.instanceId = this.$route.params.id;
                this.getInstance();
            },
            getInstance() {
                this.$http.get(this.instanceApiUrl).then(
                    response => {
                        this.handleSuccessfulGetApiResponse(response);
                    },
                    response => {
                        this.handleFailedGetApiResponse(response);
                    }
                )
            },
            saveChanges() {
                this.$http.put(this.instanceApiUrl, this.instance).then(
                    response => {
                        this.handleSuccessfulPutApiResponse(response);
                    },
                    response => {
                        this.handleFailedPutApiResponse(response);
                    }
                )
            },
            rollbackChanges() {
                this.instance = JSON.parse(JSON.stringify(this.proxyInstance));
            },
            updateInstance() {
                this.$http.put(this.instanceApiUrl, this.instance).then(
                    response => {
                        this.handleSuccessfulPutApiResponse(response);
                    },
                    response => {
                        this.handleFailedPutApiResponse(response);
                    }
                )
            },
            deleteInstance() {
                this.$http.delete(this.instanceApiUrl).then(
                    response => {
                        this.handleSuccessfulDeleteApiResponse(response);
                    },
                    response => {
                        this.handleFailedDeleteApiResponse(response);
                    }
                )
            },
            back() {
                let path = `/reviews/`;
                this.$router.go(-1);
                this.$router.push({path: path});
            },
            proceedReceivedInstanceData(receivedInstance) {
                this.instance = receivedInstance;
                this.proxyInstance = JSON.parse(JSON.stringify(this.instance));
            },
            // Response handling
            handleSuccessfulGetApiResponse(response) {
                this.proceedReceivedInstanceData(response.body);
                this.apiResponseError = false;
                this.initialized = true;
            },
            handleFailedGetApiResponse(response) {
                this.apiResponseError = true;
                this.initialized = true;
            },
            handleSuccessfulPutApiResponse(response) {
                this.proceedReceivedInstanceData(response.body);
                this.snackbarText = "Отзыв успешно сохранён";
                this.showSnackbar = true;
            },
            handleFailedPutApiResponse(response) {
                this.snackbarText = "Не удалось сохранить отзыв";
                this.showSnackbar = true;
            },
            handleSuccessfulDeleteApiResponse(response) {
                this.back();
            },
            handleFailedDeleteApiResponse(response) {
                this.snackbarText = "Не удалось удалить отзыв";
                this.showSnackbar = true;
            }
        }
    }
</script>

<style lang="scss" scoped>
    .instance-editor {
        height: 100%;
    }
    .placeholder {
        height: 100%;
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .instance-form__controls {
        display: flex;
        justify-content: space-between;
    }
    .tabs__content {
        padding: 60px 0px;
    }
    .delete-dialog__controls {
        padding: 40px 0px 0px 0px;
        display: flex;
        justify-content: flex-end;
    }
</style>
