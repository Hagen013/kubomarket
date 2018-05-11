<template>
    <md-content>
        <div class="md-layout">
            <div class="md-layout-item">
                <md-card>
                    <md-card-header>
                        <div class="md-title">Подгрузка новых атрибутов</div>
                    </md-card-header>
                    <md-card-content>
                        <md-field>
                            <label>Файл атрибутов</label>
                            <md-file placeholder="выберите файл" v-on:md-change="setUploadFile"/>
                        </md-field>
                        <md-button class="md-primary md-raised" :disabled="uploadDisabled" @click="uploadFileTriggered">
                            <md-icon>file_upload</md-icon>
                            Загрузить файл
                        </md-button>
                        <div class="upload__info">
                            <span v-if="uploadFile == null" class="md-caption caption_upload caption-accent">Файл не выбран</span>
                        </div>
                        <transition name="fadeIn">
                            <div class="upload__progress" v-if="uploadInProgress">
                                <span class="md-caption caption_upload">Обработка файла...</span>
                                <md-progress-bar md-mode="indeterminate"></md-progress-bar>
                            </div>
                        </transition>
                        <transition name="fadeIn">
                            <div class="upload__progress" v-if="uploadingFinished">
                                <span class="md-caption caption_upload">Файл обработан</span>
                                <md-progress-bar md-mode="determinate" :md-value="100"></md-progress-bar>
                            </div>
                        </transition>
                    </md-card-content>
                </md-card>
            </div>
            <div class="md-layout-item">
            </div>
        </div>
    </md-content>
</template>

<script>
    export default {
        name: 'sync-attributes',
        data: () => ({
            uploadFile: null,
            uploadDisabled: true,
            uploadInProgress: false,
            uploadStatusTimer: null,
            uploadingFinished: false
        }),
        computed: {
        },
        methods: {
            setUploadFile(fileList) {
                this.uploadFile = fileList[0];
                if ( this.uploadFile ) {
                    this.uploadDisabled = false;
                }    
            },
            uploadFileTriggered() {
                let formData = new FormData();

                formData.append('file', this.uploadFile);

                this.uploadingFinished = false;
                this.uploadDisabled = true;

                this.$http.post('/controls/attrbiute-values/upload/', formData).then(
                    response => {
                        this.uploadInProgress = true;
                    },
                    response => {
                    }
                )          
            },
            getUploadStatus() {
                this.$http.get('/controls/attrbiute-values/upload/').then(
                    response => {
                        if ( response.data.is_ready ) {
                            this.uploadInProgress = false;
                            this.uploadingFinished = true;
                            this.uploadDisabled = false;
                        }
                    },
                    response => {
                    },
                );
            },
        },
        watch: {
            uploadInProgress: function () {
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
    .md-card__content {
        padding: 16px;
    }
    .caption-accent {
        color: #ff5252;
    }
    .upload__info {
        padding: 16px;
    }
</style>