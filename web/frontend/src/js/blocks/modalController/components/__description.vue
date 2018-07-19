<template>
    <div class="description">
        <div class="description__title-block">
            <div class="description__headline">
                Описание
            </div>
            <div class="description-toolkit">
                <label for="main-file-upload" class="description__toolkit-button">
                    +
                </label>
                <input
                    id="main-file-upload"
                    type="file"
                    @change="handleDescriptionImageFile($event)"
                >
            </div>
        </div>
        <textarea class="description__textarea"
            @input=change
            v-model="proxyDescription">
        </textarea>
    </div>
</template>

<script>
    export default {
        name: 'description',
        data: () => ({
            proxyDescription: '',
            imageFile: null,
            connectionFailed: false,
            imagesApiUrl: '',
            uploadInProgress: false,
            uploadSucceded: false,
            taksId: '',
            statusTimer: null,
            fileName: null,
        }),
        props: [
            'id',
            'descriptionText',
            'saving_iteration',
            'product_name'
        ],
        created() {
            this.proxyDescription = String(this.descriptionText);
            this.imagesApiUrl = `/api/products/${this.id}/description/images/`;
        },
        methods: {
            change() {
                this.$emit('changed', this.proxyDescription);
            },
            handleDescriptionImageFile(event) {
                this.imageFile = event.target.files[0];
                this.saveImage();
            },
            saveImage() {
                let formData = new FormData();
                formData.append('file', this.imageFile);

                this.$http.post(this.imagesApiUrl, formData).then(
                    response => {
                        this.handleSuccessFulImageUpload(response);
                    },
                    response => {
                        this.handleFailedImageUpload(response);
                    }
                )
            },
            getImageUploadStatus(response) {
                this.$http.get(this.imagesApiUrl, {params: {'task_id': this.taksId}}).then(
                    response => {
                        if (response.data.is_ready) {
                            this.uploadInProgress = false;
                            this.uploadSucceded = true;
                            this.addImageToDescription();
                        }
                    },
                    response => {
                        this.uploadInProgress = false;
                        this.uploadSucceded = false;
                    }
                )
            },
            handleSuccessFulImageUpload(response) {
                this.uploadInProgress = true;
                this.uploadSucceded = false;
                this.taksId = response.body['task_id'];
                this.fileName = response.body['filename'];
            },
            handleFailedImageUpload(response) {
                this.uploadInProgress = false;
                this.connectionFailed = true;
            },
            addImageToDescription() {
                this.proxyDescription += `<p><div class="product-page__decription-image-wrap"><img src="/media/storage/${this.fileName}" alt="${this.product_name}"></div></p>`;
                this.change();
            }
        },
        watch: {
            uploadInProgress() {
                if (this.uploadInProgress) {
                    this.statusTimer = setInterval(this.getImageUploadStatus, 250);
                } else {
                    clearInterval(this.statusTimer);
                }
            }
        }
    }
</script>

<style lang="scss" scoped>
    .description {
        padding: 0px 16px 256px 16px;
    }
    .description-toolkit {
        display: flex;
        position: absolute;
        top: 0px;
        right: 0px;
        height: 100%;
        width: 200px;
        align-items: center;
        justify-content: flex-end;
    }
    .description__toolkit-button {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 40px;
        width: 40px;
        border-radius: 20px;
        background: #448aff;
        cursor: pointer;
        color: white;
        font-size: 20px;
        box-shadow: 0 3px 5px -1px rgba(0, 0, 0, 0.2), 0 6px 10px 0 rgba(0, 0, 0, 0.14), 0 1px 18px 0 rgba(0, 0, 0, 0.12);
        transition: .2s;
        &:hover {
            background: #5e9aff;
        }
    }
    .description__textarea {
        min-height: 400px;
        padding: 16px;
        width: 100%;
        line-height: 1.5;
        resize: vertical;
        border: 2px solid #448aff;
        border-radius: 4px;
    }
    .description__title-block {
        position: relative;
        display: flex;
        width: 100%;
        padding: 16px 0px 24px 0px;
        justify-content: space-between;
    }
    .description__headline {
        font-size: 22px;
        font-family: PFDinDisplayPro-Bold !important;
    }
</style>