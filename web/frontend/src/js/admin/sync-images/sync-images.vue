<template>
    <md-content>
        <div class="md-layout">
            <div class="md-layout-item">
                <md-card>
                    <md-card-header>
                        <div class="md-title">Обновление изображений</div>
                    </md-card-header>
                    <md-card-content>
                        <md-field>
                            <label>Файл изображений</label>
                            <md-file placeholder="выберите файл" v-on:md-change="setUploadFile"/>
                        </md-field>
                        <md-button class="md-raised md-primary" 
                            :disabled="uploadDisabled"
                            @click="uploadFileTriggered"
                        >
                            <md-icon>file_upload</md-icon>
                            Загрузить файл
                        </md-button>
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
        name: 'sync-images',
        data: () => ({
            uploadFile: null,
            uploadDisabled: true,
            uploadInProgress: false,
            uploadingFinished: false,
            uploadStatusTimer: null,
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

                this.$http.post('/controls/images-sync/', formData).then(
                    response => {
                        this.uploadInProgress = true;
                    },
                    response => {
                    }
                )
            },
            getUploadStatus() {
                this.$http.get('/controls/images-sync/').then(
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
            }
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
</style>