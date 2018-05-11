<template>

    <md-card>
        <md-card-header>
            <div class="md-title">{{cardTitle}}</div>
        </md-card-header>
        <md-card-content>
            <md-button class="md-raised md-accent" @click="downloadTriggered">
                <md-icon>file_download</md-icon>
                Скачать файл
            </md-button>
            <transition name="fadeIn" mode="out-in">
                <div class="upload__progress" v-if="downloadInProgress">
                    <span class="md-caption caption_upload">Формирование файла остатков...</span>
                    <md-progress-bar md-mode="indeterminate"></md-progress-bar>
                </div>
            </transition>
            <transition name="fadeIn" mode="out-in">
                <div class="upload__progress" v-if="downloadSucceded">
                    <span class="md-caption caption_upload">Файл сформирован</span>
                    <md-progress-bar md-mode="determinate" :md-value="100"></md-progress-bar>
                </div>
            </transition>
        </md-card-content>
    </md-card>

</template>

<script>
    export default {
        name: 'download-card',
        data: () => ({
            cardTitle: 'Скачать',
            downloadInProgress: false,
            downloadStatusTimer: null,
            taskState: 'AWAITING',
            connectionFailed: false,
            downloadSucceded: false,
        }),
        props: ['download_url', 'download_status_url'],
        computed: {
        },
        methods: {
            downloadTriggered() {
                this.downloadInProgress = true;
                this.downloadSucceded = false;
                this.$http.post(this.download_status_url).then(
                    response => {
                    },
                    response => {
                    },
                );
            },
            getDownloadStatus() {
                this.$http.get(this.download_status_url).then(
                    response => {
                        if ( response.data.is_ready ) {
                            this.downloadInProgress = false;
                            this.downloadSucceded = true;
                            this.downloadRequest();
                        }
                    },
                    response => {
                    },
                );
            },
            downloadRequest() {
                this.downloadInProgress = false;
                this.downloadSucceded = true;
                document.location.assign(this.download_url);
            }
        },
        watch: {
            downloadInProgress: function () {
                if ( this.downloadInProgress === true ) {
                    this.downloadStatusTimer = setInterval(this.getDownloadStatus, 250);
                } else {
                    clearInterval(this.downloadStatusTimer);
                }
            }
        }
    }
</script>

<style lang="scss" scoped>
</style>