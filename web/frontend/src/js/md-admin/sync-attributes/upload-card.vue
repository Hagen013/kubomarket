<script>
    import defaultUploadCard from '../upload-card/upload-card.vue'

    export default {
        name: 'upload-card',
        extends: defaultUploadCard,
        data: () => ({
            reportFileApiUrl: '/controls/upload-attrs/report/'
        }),
        computed: {
        },
        methods: {
            getUploadStatus() {
                this.$http.get(this.upload_url).then(
                    response => {
                        this.taskState = response.data.state;
                        if ( response.data.is_ready ) {
                            this.uploadInProgress = false;
                            this.uploadSucceded = true;
                            document.location.assign(this.reportFileApiUrl);
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
        }
    }
</script>
