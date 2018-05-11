<template>

    
    <div class="main__wrapper">
        <div class="md-layout">

            <div class="md-layout-item">
                <md-card>
                    <md-card-header>
                        <div class="md-title">Загрузка остатков</div>
                    </md-card-header>
                    <div class="md-card__content">
                        <md-field>
                            <label>Файл остатков</label>
                            <md-file placeholder="выберите файл" v-on:md-change="setUploadFile"/>
                        </md-field>
                        <md-button class="md-primary md-raised"
                            @click="uploadFileTriggered"
                        >
                            <md-icon>file_upload</md-icon>
                            Загрузить остатки
                        </md-button>
                        <transition name="fadeIn">
                            <div class="upload__progress" v-if="uploadInProgress">
                                <span class="md-caption caption_upload">Обработка файлов остатков...</span>
                                <md-progress-bar md-mode="indeterminate"></md-progress-bar>
                            </div>
                        </transition>
                        <transition name="fadeIn">
                            <div class="upload__progress" v-if="uploadSucceded">
                                <span class="md-caption caption_upload">Файл обработан</span>
                                <md-progress-bar md-mode="determinate" :md-value="100"></md-progress-bar>
                                <span v-if="uploadFailed" class="md-caption caption_upload caption-accent">Во время обработки произошла ошибка</span>
                            </div>
                        </transition>
                    </div>
                </md-card>
            </div>

            <div class="md-layout-item">
                <md-card>
                    <md-card-header>
                        <div class="md-title">Выгрузка остатков с сайта</div>
                    </md-card-header>
                    <div class="md-card__content">
                        <md-button class="md-accent md-raised"
                            @click="downloadFileTriggered"
                        >
                            <md-icon>file_download</md-icon>
                            Скачать файл
                        </md-button>
                        <transition name="fadeIn">
                            <div class="upload__progress" v-if="downloadInProgress">
                                <span class="md-caption caption_upload">Формирование файла остатков...</span>
                                <md-progress-bar md-mode="indeterminate"></md-progress-bar>
                            </div>
                        </transition>
                        <transition name="fadeIn">
                            <div class="upload__progress" v-if="downloadSucceded">
                                <span class="md-caption caption_upload">Файл сформирован</span>
                                <md-progress-bar md-mode="determinate" :md-value="100"></md-progress-bar>
                            </div>
                        </transition>
                    </div>
                </md-card>
            </div>
        </div>

	</div>

</template>

<script>
  export default {
    name: 'appmain',
    data: () => ({
        downloadInProgress: false,
        downloadSucceded: false,
        downloadTimer: null,
        uploadTimer: null,
        file: null,
        uploadFileSelected: false,
        uploadingFile: false,
        fileUploaded: false,
        uploadInProgress: false,
        uploadSucceded: false,
        uploadState: '',
    }),
    computed: {
        uploadFailed() {
            if ( this.uploadState == 'FAILURE' ) {
                return true
            }
            return false
        }
    },
    methods: {
        downloadFileTriggered() {
            this.downloadInProgress = true;
            this.downloadSucceded = false;
                this.$http.post('/controls/status/').then(
                    response => {
                    },
                    response => {
                    },
                );
        },
        uploadFileTriggered() {
            if (this.file) {
                let formData = new FormData();

                formData.append('file', this.file);

                this.uploadingFile = true;
                this.fileUploaded = false;

                this.$http.post('/controls/upload/', formData).then(
                    response => {
                        this.uploadInProgress = true;
                        this.uploadSucceded = false;
                    },
                    response => {
                    }
                )
            }
        },
        getDownloadStatus() {
            this.$http.get('/controls/status/').then(
                response => {
                    if ( response.data.is_ready ) {
                        this.downloadInProgress = false;
                        this.downloadSucceded = true;
                        document.location.assign('/controls/download/')
                    }
                },
                response => {
                },
            );
        },
        getUploadStatus() {
            this.$http.get('/controls/upload/').then(
                response => {
                    this.uploadProgress = response.data.progress;
                    this.uploadState = response.data.state;
                    if ( response.data.is_ready ) {
                        this.uploadInProgress = false;
                        this.uploadSucceded = true;
                    }
                },
                response => {
                },
            )
        },
        setUploadFile(fileList) {
            this.file = fileList[0];            
        },
    },
    watch: {
        downloadInProgress: function () {
            if ( this.downloadInProgress === true ) {
                this.downloadTimer = setInterval(this.getDownloadStatus, 250);
            } else {
                clearInterval(this.downloadTimer);
            }
        },
        uploadInProgress: function () {
            if ( this.uploadInProgress === true ) {
                this.uploadTimer = setInterval(this.getUploadStatus, 250);
            } else {
                clearInterval(this.uploadTimer);
            }
        }
    }
  }
</script>

<style lang="scss" scoped>
    .main-container {
        position: relative;
        padding: 16px;
    }

    .md-card__content {
        padding: 0px 16px 16px 16px;
    }

    .upload__progress {
        padding: 16px 0px 16px 0px;
    }

    .caption-accent {
        color: #ff5252;
    }
</style>
