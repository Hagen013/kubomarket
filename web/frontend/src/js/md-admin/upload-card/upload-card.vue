<template>
    <md-content>
        <md-card>
            <md-card-header>
                <div class="md-title">{{cardTitle}}</div>
            </md-card-header>
            <md-card-content>
                <md-field>
                    <label>{{fileLabel}}</label>
                    <md-file placeholder="выберите файл" v-on:md-change="setUploadFile"/>
                </md-field>
                <md-button class="md-raised md-primary"
                    @click="triggerUpload"
                    :disabled="!uploadDisabled"
                >
                    <md-icon>file_upload</md-icon>
                    Загрузить файл
                </md-button>
                <div class="card__caption">
                    <transition name="fadeIn" mode="out-in">
                        <span class="md-caption warning" v-if="!uploadFileSelected">Файл не выбран</span>
                    </transition>
                    <transition name="fadeIn" mode="out-in">
                        <div v-if="uploadInProgress">
                            <span class="md-caption">Обработка файла...</span>
                            <md-progress-bar md-mode="indeterminate"></md-progress-bar>
                        </div>
                    </transition>
                    <transition name="fadeIn" mode="out-in">
                        <div v-if="uploadSucceded">
                            <span class="md-caption">Файл обработан</span>
                            <md-progress-bar md-mode="determinate" :md-value="100"></md-progress-bar>
                        </div>
                    </transition>
                    <transition name="fadeIn" mode="out-in">
                        <div v-if="connectionFailed">
                            <span class="md-caption warning">Во время обработки файла произошла ошибка!</span>
                        </div>
                    </transition>
                </div>
            </md-card-content>
        </md-card>
    </md-content>
</template>

<script>
    export default {
        name: 'upload-card',
        data: () => ({
            cardTitle: 'Загрузить',
            fileLabel: 'выбранный файл',
            uploadFile: null,
            uploadInProgress: false,
            uploadStatusTimer: null,
            uploadFileSelected: false,
            taskState: 'AWAITING',
            connectionFailed: false,
            uploadSucceded: false
        }),
        props: ['upload_url'],
        computed: {
            uploadDisabled: function () {
                return ( ( this.uploadFileSelected ) && ( !this.uploadInProgress ) )
            }
        },
        methods: {
            setUploadFile(fileList) {
                this.connectionFailed = false;
                this.uploadFile = fileList[0];
                if ( this.uploadFile ) {
                    this.uploadFileSelected = true;
                }    
            },
            triggerUpload() {
                if ( this.uploadFile ) {
                    this.connectionFailed = false;
                    let formData = new FormData();

                    formData.append('file', this.uploadFile);

                    this.uploadInProgress = true;

                    this.$http.post(this.upload_url, formData).then(
                        response => {
                            this.uploadInProgress = true;
                            this.uploadSucceded = false;
                        },
                        response => {
                            this.connectionFailed = true;
                        }
                    )
                }
            },
            getUploadStatus() {
                this.$http.get(this.upload_url).then(
                    response => {
                        this.taskState = response.data.state;
                        if ( response.data.is_ready ) {
                            this.uploadInProgress = false;
                            this.uploadSucceded = true;
                        }
                    },
                    response => {
                        this.uploadInProgress = false;
                        this.connectionFailed = true;
                    },
                )
            },
        },
        watch: {
            uploadInProgress() {
                if ( this.uploadInProgress ) {
                    this.uploadStatusTimer = setInterval(this.getUploadStatus, 250);
                } else {
                    clearInterval(this.uploadStatusTimer);
                }
            }
        }
    }
</script>

<style lang="scss" scoped>
    .card__caption {
        min-height: 46px;
        padding: 12px;
    }
    .warning {
        color: #ff5252;
    }
</style>