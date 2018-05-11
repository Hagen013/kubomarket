<template>
    <transition name="fade-fast">
        <div class="images-gallery">
            <div class="images-gallery__main-img-wrap" id="main-image"
                :class="{ imagesGallery__mainImgWrapFixed: mainImageFixed }"
            >
                <div class="images-gallery__title-block">
                    <div class="images-gallery__headline">
                        Главное изображение
                    </div>
                    <div class="images-gallery__title-block-button images-gallery__hide-main-image" @click="toggleMainImage">
                        <span v-if="showMainImage">[ СКРЫТЬ ]</span>
                        <span v-else>[РАСКРЫТЬ]</span>
                    </div>
                    <button class="images-gallery__fab images-gallery__change-main"
                        @click="toggleMainImageEditModal"
                    >
                        <div class="icon icon_edit product-card__control-icon"></div>
                    </button>
                </div>
                <a class="images-gallery__main-img-link"
                    v-show="showMainImage"
                    data-fancybox="edit-form"
                    :href="mainImage"
                >
                    <img class="images-gallery__main-img" :src="mainImage">
                </a>
            </div>
            <div class="images-gallery__additional-imgs-wrap"
                :class="{ imagesGallery__additionalImgsWrapMainContentHidden : !showMainImage }"
            >
                <div class="images-gallery__title-block">
                    <div class="images-gallery__headline">
                        Дополнительные изображения
                    </div>
                    <button class="images-gallery__fab images-gallery__add-photo"
                        @click="toggleAddImageModal"
                    >
                    +
                    </button>
                </div>
                <div class="images-gallery__additional-images sortable" id="additional-images">
                </div>
            </div>
            <transition name="fade-fast">
                <div class="images-gallery__modal images-gallery__edit-main-image"
                    v-if="mainImageEditModalIsDisplayed"
                    @click.self="recoverMainImageModal"
                >
                    <div class="images-gallery__modal-card">
                        <div class="images-gallery__modal-title">
                        Изменить главное фото
                        </div>
                        <div class="images-gallery__modal-content">
                            <div class="images-gallery__modal-left-content">
                                <div class="images-gallery__modal-top">
                                    <div class="images-gallery__modal-caption">
                                    Выберите из фото:
                                    </div>
                                </div>
                                <div class="image-gallery__modal-img-choices">
                                    <div class="images-gallery__modal-choice-item"
                                        v-for="image in additionalImages"
                                        @click="setActiveChoiceItem(image)"
                                        :class="{ imagesGallery__modalChoiceItemActive: activeImageThumbnailId === image.id }"
                                    >
                                        <img :src="image.url">  
                                    </div>
                                </div>
                            </div>
                            <div class="images-gallery__modal-right-content">
                                <div class="images-gallery__modal-top">
                                    <div class="images-gallery__modal-caption">
                                    Или загрузите новое:
                                    </div>
                                    <label for="main-file-upload" class="images-gallery__button">
                                        Выберите файл
                                    </label>
                                    <input
                                        id="main-file-upload"
                                        type="file"
                                        @change="handleMainFile($event)"
                                    >
                                </div>
                                <div class="images-gallery__modal-right-content-img-wrap">
                                    <img :src="activeImageThumbnail" id="main-image-preview">
                                </div>
                            </div>
                        </div>
                        <div class="images-gallery__modal-close"
                            @click="recoverMainImageModal"
                        >
                            <svg height="32" viewBox="0 0 24 24" width="32" xmlns="http://www.w3.org/2000/svg"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"></path> <path d="M0 0h24v24H0z" fill="none"></path></svg>
                        </div>
                        <div class="images-gallery__bottom-controls">
                            <button class="images-gallery__button images-gallery__button_accent"
                                @click="saveMainImageChanges"
                                :disabled="!mainImageUploadActive"
                            >
                                Сохранить
                            </button>
                        </div>
                    </div>
                </div>
            </transition>
            <transition name="fade-fast">
                <div class="images-gallery__modal images-gallery__add-image"
                    v-if="addImageModalIsDisplayed"
                    @click.self="recoverAddImageModal"
                >
                    <div class="images-gallery__modal-card">
                        <div class="images-gallery__modal-title">
                        Добавить дополнительное изображение
                        </div>
                        <div class="images-gallery__add-image-content-wrap">
                            <div class="images-gallery__add-image-content">
                                <div class="images-gallery__image-placeholder">
                                    <div class="images-gallery__image-placeholder-caption"
                                        v-if="additionalImagesFile === null"
                                    >
                                    Не выбрано
                                    </div>
                                    <img id="placeholder-image" class="images-gallery__placeholder-image">
                                </div>
                            </div>
                            <div class="images-gallery__add-image-controls">
                                <div class="images-gallery__upload-status">
                                    {{addImageUploadMessage}}
                                </div>
                                <label for="file-upload" class="images-gallery__button">
                                    Выберите файл
                                </label>
                                <input
                                    id="file-upload"
                                    type="file"
                                    @change="handleFile($event)"
                                >
                                <button class="images-gallery__button images-gallery__button_accent images-gallery__upload-ad"
                                    @click="uploadAdditionalImage"
                                    :disabled="addImageUploadButtonIsActive"
                                >
                                    Загрузить
                                </button>
                            </div>
                        </div>
                        <div class="images-gallery__modal-close"
                            @click="recoverAddImageModal"
                        >
                            <svg height="32" viewBox="0 0 24 24" width="32" xmlns="http://www.w3.org/2000/svg"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"></path> <path d="M0 0h24v24H0z" fill="none"></path></svg>
                        </div>
                    </div>
                </div>
            </transition>
        </div>
    </transition>
</template>

<script>
    import sortable from 'html5sortable/dist/html.sortable.min.js'

    export default {
        name: 'edit-modal',
        data: () => ({
            mainImage: '',
            additionalImages: [],
            showMainImage: true,
            mainImageFixed: false,
            mainImageEditModalIsDisplayed: false,
            addImageModalIsDisplayed:  false,
            activeImageThumbnailId: null,
            activeImageThumbnail: null,
            activeImageThumbnailObject: null,
            originalMainImage: '',
            originalAdditionalImages: [],
            hasChanged: false,
            additionalImageApiURL: '/api/cubes/images/',
            additionalImagesFile: null,
            addImageUploadURL: '/api/cubes/images/upload/',
            addImageUploadInProgess: false,
            addImageConnectionFailed: false,
            addImageUploadSucceded: false,
            addImageUploadStatusTimer: null,
            addImageTaskId: null,
            mainImageFile: null,
            mainImageUploadInProgress: false,
            mainImageConnectionFailed: false,
            mainImageUploadSucceded: false,
            mainImageUploadStatusTimer: null,
            mainImageTaskId: null,
            productImagesApiUrl: '/api/product/{slug}/image/',
        }),
        props: [
            'id',
            'slug',
            'saving_iteration'
        ],
        computed: {
            addImageUploadMessage() {
                if (this.addImageConnectionFailed) {
                    return "При соединении с сервером произошла ошибка"
                }
                if (this.addImageUploadSucceded) {
                    return "Изображение успешно добавлено"
                }
                if (this.addImageUploadInProgess) {
                    return "Загрузка изображения..."
                }    
                if (this.additionalImagesFile !== null) {
                    return this.additionalImagesFile.name
                }
            },
            addImageUploadButtonIsActive() {
                if ((this.additionalImagesFile === null) || this.addImageUploadInProgess) {
                    return true
                } else {
                    return false
                }
            },
            mainImageHasChanged() {
                return this.activeImageThumbnail !== this.originalMainImage
            },
            mainImageUploadButtonIsActive() {
                if ((this.activeImageThumbnail === null) || this.mainImageUploadInProgress || this.mainImageHasChanged) {
                    return false
                } else {
                    return true
                }
            },
            mainImageUploadActive() {
                if (this.activeImageThumbnailId || this.mainImageFile) {
                    return true
                } else {
                    return false
                }
            }
        },
        created: function () {
            this.mainImageUploadAPIUrl = `/api/products/${this.id}/image/`;
            this.productImagesApiUrl = `/api/products/${this.id}/images/`;
            console.log()
            window.onscroll = this.scrollFunction;
            this.getImages();
        },
        mounted: function () {
            this.scrollFunction();
        },
        methods: {
            getImages() {
                this.$http.get(this.productImagesApiUrl).then(
                    response => {
                        this.fillImagesGallery(response);
                    },
                    response => {
                    }
                )
            },
            fillImagesGallery(response) {
                this.mainImage = response.body['main'];
                this.activeImageThumbnail = this.mainImage;
                this.additionalImages = response.body['additional'];
                this.additionalImages = this.additionalImages.sort(function(a, b) {
                    return a.order - b.order
                })
                this.originalMainImage = this.mainImage;
                this.originalAdditionalImages = this.additionalImages.slice();
                this.renderGallery();
            },
            renderGallery() {
                let imagesGallery = document.getElementById('additional-images');

                while (imagesGallery.firstChild) {
                    imagesGallery.removeChild(imagesGallery.firstChild);
                }

                for (let i=0; i<this.additionalImages.length; i++) {
                    let element = document.createElement('div');
                    let deleteButton = document.createElement('div');
                    let imageId = this.additionalImages[i].id;
                    let deleteFunction = this.deleteItem;

                    element.className = 'images-gallery__item';
                    element.setAttribute('imageId', imageId);
                    deleteButton.className = 'image-gallery__item-close';
                    element.innerHTML = `<a class="images-gallery__item-link"
                                            data-fancybox="edit-form"
                                            href="${this.additionalImages[i].url}"
                                        >
                                            <img src=${this.additionalImages[i].url}>
                                        </a>`;
                    deleteButton.innerHTML = `<svg height="16" viewBox="0 0 24 24" width="16" xmlns="http://www.w3.org/2000/svg"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"></path> <path d="M0 0h24v24H0z" fill="none"></path></svg>`
                    deleteButton.addEventListener('click', function (e) {
                        deleteFunction(e, imageId);
                    });
                    element.appendChild(deleteButton);
                    imagesGallery.appendChild(element);
                }

                let clearfix = document.createElement('div');
                clearfix.className = 'clearfix';
                imagesGallery.appendChild(clearfix);

                sortable('.sortable', {

                });

                sortable('.sortable')[0].addEventListener('sortstop', this.sortEnd);

            },
            showAddModal() {
                console.log('show add modal');
            },
            showEditModal() {
                console.log('show edit modal');
            },
            scrollFunction(e) {
                let mainImage = document.getElementById('main-image');
                let imageOffset = mainImage.offsetTop;
                let offset = window.pageYOffset;
                let distance = imageOffset - offset;
                
                if ( (distance <= 0) && (!this.mainImageFixed) ) {
                    this.mainImageFixed = true;
                } else if ( (this.mainImageFixed)  && (distance >= -64) ) {
                    this.mainImageFixed = false;
                }
            },
            toggleMainImage() {
                this.showMainImage = !this.showMainImage;
            },
            sortEnd() {
                let imageItems = Array.prototype.slice.call(document.getElementsByClassName('images-gallery__item'));
                let imageIds = imageItems.map(function (currentValue, index, array) {
                    return Number(currentValue.getAttribute('imageid'))
                });
                this.additionalImages = this.additionalImages.sort(function (a, b) {
                    return imageIds.indexOf(a.id) - imageIds.indexOf(b.id)
                })
                for (let i=0; i<this.additionalImages.length; i++) {
                    this.additionalImages[i].order = i;
                }
                this.checkForChanges();
            },
            deleteItem(e, id) {
                let index = 0;
                let apiURL = `${this.additionalImageApiURL}${id}/`;

                for (let i=0; i<this.additionalImages.length; i++) {
                    if ( this.additionalImages[i].id === id ) {
                        index = i;
                        break
                    }
                }
                this.additionalImages.splice(index, 1);
                this.$http.delete(apiURL).then(
                    response => {
                        console.log(response);
                    },
                    response => {
                        console.log(response);
                    }
                );
                this.renderGallery();
                this.checkForChanges();
            },
            toggleMainImageEditModal() {
                this.mainImageEditModalIsDisplayed = !this.mainImageEditModalIsDisplayed;
            },
            toggleAddImageModal() {
                this.addImageModalIsDisplayed = !this.addImageModalIsDisplayed;
            },
            setActiveChoiceItem(image) {
                this.activeImageThumbnailId = image.id;
                this.activeImageThumbnail = image.url;
                this.activeImageThumbnailObject = image;
                this.mainImageFile = null;
            },
            checkForChanges() {
                let changesFound = false;

                if (this.mainImage !== this.originalMainImage) {
                    this.hasChanged = true;
                    changesFound = true;
                }
                if (this.additionalImages.length !== this.originalAdditionalImages.length) {
                    this.hasChanged = true;
                    changesFound = true;
                } else {
                    for (let i=0; i<this.additionalImages.length; i++) {
                        if (this.additionalImages[i].id !== this.originalAdditionalImages[i].id) {
                            this.hasChanged = true;
                            changesFound = true;
                            break
                        }
                    }
                }
                if (!changesFound) {
                    this.hasChanged = false;
                }
            },
            handleFile(event) {
                let reader = new FileReader();
                let placeholderImage = document.getElementById("placeholder-image");
                let fileInput = document.getElementById("file-upload");

                reader.onload = function(e) {
                    placeholderImage.setAttribute('src', e.target.result);
                }
                this.additionalImagesFile = event.target.files[0];
                reader.readAsDataURL(event.target.files[0]);
            },
            handleMainFile(event) {
                let reader = new FileReader();
                let mainImage = document.getElementById('main-image-preview');
                let fileInput = document.getElementById('main-file-upload');

                console.log(mainImage);
                console.log(fileInput);

                reader.onload = function(e) {
                    mainImage.setAttribute('src', e.target.result);
                }
                this.mainImageFile = event.target.files[0];
                reader.readAsDataURL(event.target.files[0]);
                this.activeImageThumbnailId = null;
            },
            saveMainImageChanges() {
                let formData = new FormData();
                this.mainImageConnectionFailed = false;
                

                if (this.mainImageFile !== null) {
                    formData.append('file', this.mainImageFile);
                } else {
                    let image = {
                        'id': this.activeImageThumbnailObject.id,
                        'url': this.activeImageThumbnailObject.url,
                        'order': this.activeImageThumbnailObject.order,
                        'thumbnail': this.activeImageThumbnailObject.thumbnail,
                    }
                    formData = {
                        "image": image,
                    }
                }
                this.$http.put(this.mainImageUploadAPIUrl, formData).then(
                    response => {
                        this.mainImageUploadInProgress = true;
                        this.mainImageUploadSucceded = false;
                        this.mainImageTaskId = response.body['task_id'];
                    },
                    response => {
                        this.mainImageConnectionFailed = true;
                    }
                )
            },
            getMainImageUploadStatus() {
                this.$http.get(this.mainImageUploadAPIUrl, {params: {'task_id': this.mainImageTaskId}}).then(
                    response => {
                        if ( response.data.is_ready ) {
                            this.mainImageUploadInProgress = false;
                            this.mainImageUploadSucceded = true;
                            this.mainImageEditModalIsDisplayed = false;
                            this.getImages();
                        }
                    },
                    response => {
                        this.mainImageUploadInProgress = false;
                        this.mainImageConnectionFailed = true;
                    }
                )
            },
            uploadAdditionalImage() {
                if ( this.additionalImagesFile ) {
                    let formData = new FormData();

                    formData.append('file', this.additionalImagesFile);
                    formData.append('product_slug', this.slug);
                    this.addImageConnectionFailed = false;

                    this.$http.post(this.addImageUploadURL, formData).then(
                        response => {
                            this.addImageUploadInProgess = true;
                            this.addImageUploadSucceded = false;
                            this.addImageTaskId = response.body['task_id'];
                        },
                        response => {
                            this.addImageConnectionFailed = true;
                        }
                    )
                }
            },
            getAdditionalImageUploadStatus() {
                this.$http.get(this.addImageUploadURL, {params: {'task_id': this.addImageTaskId}}).then(
                    response => {
                        if ( response.data.is_ready ) {
                            this.addImageUploadInProgess = false;
                            this.addImageUploadSucceded = true;
                            this.recoverMainImageModal();
                            this.getImages();
                        }
                    },
                    response => {
                        this.addImageUploadInProgess = false;
                        this.addImageConnectionFailed = true;
                    }
                )
            },
            recoverMainImageModal() {
                this.mainImageEditModalIsDisplayed = false;
                this.mainImageUploadSucceded = false;
                this.mainImageFile = null;
                this.mainImageTaskId = null;
                this.activeImageThumbnailId = null;
                this.activeImageThumbnail = this.mainImage;
            },
            recoverAddImageModal() {
                this.addImageModalIsDisplayed = false;
                this.addImageUploadSucceded = false;
                this.additionalImagesFile = null;
                this.addImageTaskId = null;
            },
            updateImages() {
                let data = {}

                for (let i=0; i<this.additionalImages.length; i++) {
                    var item = this.additionalImages[i];
                    data[item['id']] = item;
                }

                this.$http.put(this.productImagesApiUrl, data).then(
                    response => {

                    },
                    response => {

                    }
                )
            }
        },
        watch: {
            addImageUploadInProgess() {
                if ( this.addImageUploadInProgess ) {
                    this.addImageUploadStatusTimer = setInterval(this.getAdditionalImageUploadStatus, 250);
                } else {
                    clearInterval(this.addImageUploadStatusTimer);
                }
            },
            mainImageUploadInProgress() {
                if (this.mainImageUploadInProgress) {
                    this.mainImageUploadStatusTimer = setInterval(this.getMainImageUploadStatus, 250);
                } else {
                    clearInterval(this.mainImageUploadStatusTimer);
                }
            },
            hasChanged() {
                this.$emit('has-changed', this.hasChanged);
            },
            saving_iteration() {
                this.updateImages();
                this.hasChanged = false;
            }
        },
    }
</script>

<style lang="scss">
    .images-gallery {
        width: 50%;
        padding: 32px 16px 16px 0px;
    }
    .images-gallery__title-block {
        position: relative;
        display: flex;
        width: 100%;
        padding: 16px 0px 24px 0px;
        justify-content: space-between;
    }
    .images-gallery__headline {
        font-size: 22px;
        font-family: PFDinDisplayPro-Bold !important;
    }
    .images-gallery__main-img-link {
        display: flex;
        height: 260px;
        width: 100%;
        align-items: center;
        justify-content: center;
        &:focus {
            outline: none;
        }
    }
    .images-gallery__main-img {
        height: 100%;
        width: auto;
    }
    .images-gallery__item {
        position: relative;
        float: left;
        height: 100px;
        width: 100px;
        margin-top: -1px;
        margin-right: -1px;
        padding: 8px;
        cursor: move;
        border: 1px solid #e7eff4;
        &:hover {
            .image-gallery__item-close {
                display: flex;
            }
        }
    }
    .image-gallery__item-close {
        position: absolute;
        display: none;
        justify-content: center;
        align-items: center;
        top: 8px;
        right: 8px;
        height: 20px;
        width: 20px;
        border-radius: 10px;
        background: #ff5252;
        cursor: pointer;
        transition-duration: 0.2s;
        transition-property: background;
        svg {
            fill: rgba(255,255,255,.90);
        }
        &:hover {
            background: lighten(#448aff, 8)
        }
    }
    .images-gallery__item-link {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
        width: 100%;
        img {
            height: 100%;
            width: auto;
        }
    }
    .sortable-placeholder {
        float: left;
        height: 100px;
        width: 100px;
        margin-top: -1px;
        margin-left: -1px;
        border: 3px dashed grey;
    }
    .sortable-dragging {
        opacity: 0.7;
    }
    .images-gallery__additional-images {

    }
    .images-gallery__fab {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 56px;
        width: 56px;
        border-radius: 28px;
        cursor: pointer;
        transition-property: background, box-shadow;
        transition-duration: 0.3s;
        transition-timing-function: cubic-bezier;
        box-shadow: 0 3px 5px -1px rgba(0, 0, 0, 0.2), 0 6px 10px 0 rgba(0, 0, 0, 0.14), 0 1px 18px 0 rgba(0, 0, 0, 0.12);
    }
    .images-gallery__add-photo {
        position: absolute;
        top: 0px;
        right: 16px;
        color: white;
        background: #448aff;
        font-size: 24px;
        &:hover {
            background: lighten(#448aff, 5);
        }
    }
    .images-gallery__change-main {
        position: absolute;
        top: 0px;
        right: 0px;
        background: #448aff;
        &:hover {
            background: lighten(#448aff, 5);
        }
    }
    .images-gallery__main-img-wrap {
        position: absolute;
        top: 64px;
        right: 0px;
        width: 50%;
        min-width: 455px;
        padding: 32px 32px 16px 32px;
        background: white;
        z-index: 1000;
        transition-property: box-shadow, width;
        transition-duration: 0.2s;
        .images-gallery__title-block {
            padding-left: 0px;
        }
    }
    .images-gallery__title-block-button {
        margin-right: 92px;
        color: grey;
        cursor: pointer;
        padding-top: 6px;
        transition-duration: 0.2s;
        transition-property: color;
        &:hover {
            color: #ff5252;
        }
    }
    .imagesGallery__mainImgWrapFixed {
        position: fixed;
        top: 0px;
        right: 0px;
        padding: 32px 32px 16px 32px;
        box-shadow: 0 2px 4px -1px rgba(0,0,0,.2), 0 4px 5px 0 rgba(0,0,0,.14), 0 1px 10px 0 rgba(0,0,0,.12);
        .images-gallery__title-block {
            padding-left: 0px;
        }
    }
    .images-gallery__additional-imgs-wrap {
        padding-left: 32px;
        margin-top: 359px;
    }
    .imagesGallery__additionalImgsWrapMainContentHidden {
        margin-top: 115px !important;
    }
    .images-gallery__modal {
        display: flex;
        position: fixed;
        align-items: center;
        justify-content: center;
        top: 0px;
        left: 0px;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.3);
        z-index: 20000;
    }
    .images-gallery__modal-card {
        position: relative;
        min-height: 500px;
        width: 970px;
        padding: 16px;
        background: white;
        box-shadow: 0 7px 9px -4px rgba(0,0,0,.2), 0 14px 21px 2px rgba(0,0,0,.14), 0 5px 26px 4px rgba(0,0,0,.12);
    }
    .images-gallery__modal-title {
        font-size: 32px;
        font-family: PFDinDisplayPro-Bold !important;
        padding: 8px 0px 16px 0px;
    }
    .images-gallery__modal-content {
        display: flex;
        height: 360px;
        width: 100%;
    }
    .images-gallery__modal-left-content {
        height: 100%;
        width: 50%;
    }
    .images-gallery__modal-right-content {
        height: 100%;
        width: 50%;
    }
    .images-gallery__modal-close {
        position: absolute;
        display: flex;
        justify-content: center;
        align-items: center;
        top: 20px;
        right: 20px;
        height: 40px;
        width: 40px;
        border-radius: 20px;
        background: rgba(0,0,0,0);
        transition-property: background;
        transition-duration: 0.2s;
        transition-timing-function: cubic-bezier;
        cursor: pointer;
        &:hover {
            background: rgba(0,0,0,0.2);
        }
    }
    .images-gallery__modal-right-content-img-wrap {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 300px;
        border: 1px solid #e7eff4;
        img {
            height: 100%;
            width: auto;
        }
    }
    .images-gallery__modal-choice-item {
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
        float: left;
        height: 100px;
        width: 100px;
        margin-bottom: -1px;
        margin-left: -1px;
        padding: 8px;
        border: 1px solid #e7eff4;
        transition-duration: 0.2s;
        transition-property: border;
        z-index: 1;
        cursor: pointer;
        img {
            height: 100%;
            width: auto;
        }
        &:hover {
            border: 1px solid lighten(#448aff, 20);
            z-index: 90;
        }
    }
    .image-gallery__modal-img-choices {
        padding-left: 1px;
        min-height: 301px;
        max-height: 301px;
        width: 420px;
        overflow-y: scroll;
    }
    .imagesGallery__modalChoiceItemActive {
        border: 1px solid #448aff;
        z-index: 100;
        cursor: default;
        &:hover {
            border: 1px solid #448aff;
            z-index: 100;
        }
    }
    .images-gallery__modal-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 0px 16px 0px;
    }
    .images-gallery__modal-caption {
        padding: 8px 0px 8px 0px;
        color: rgba(0,0,0,.54);
    }
    .images-gallery__button {
        display: block;
        height: 40px;
        padding: 0px 8px 0px 8px;
        line-height: 40px;
        color: white;
        font-size: 14px;
        cursor: pointer;
        background: #448aff;
        border-radius: 3px;
        transition-duration: 0.2s;
        transition-property: background, box-shadow, color;
        transition-timing-function: cubic-bezier(.4,0,.2,1);
        box-shadow: 0 3px 1px -2px rgba(0,0,0,.2), 0 2px 2px 0 rgba(0,0,0,.14), 0 1px 5px 0 rgba(0,0,0,.12);
        &:hover {
            box-shadow: 0 5px 5px -3px rgba(0,0,0,.2), 0 8px 10px 1px rgba(0,0,0,.14), 0 3px 14px 2px rgba(0,0,0,.12);
        }
        &:disabled {
            cursor: default;
            color: grey;
            background: #e7eff4;
            &:hover {
                box-shadow: 0 3px 1px -2px rgba(0,0,0,.2), 0 2px 2px 0 rgba(0,0,0,.14), 0 1px 5px 0 rgba(0,0,0,.12);
            }
        }
    }
    .images-gallery__button_accent {
        background-color: #ff5252;
    }
    .images-gallery__bottom-controls {
        display: flex;
        flex-direction: row;
        justify-content: flex-end;
        padding: 16px 0px 16px 0px;
    }
    .images-gallery__add-image-content-wrap {
        display: flex;
        flex-direction: column;
        position: relative;
        padding-top: 32px;
        justify-content: center;
        align-items: center;
        width: 100%;
    }
    .images-gallery__add-image-content {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        width: 300px;
    }
    .images-gallery__image-placeholder {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 280px;
        width: 200px;
        margin-bottom: 16px;
        color: grey;
    }
    input[type="file"] {
        display: none;
    }
    .images-gallery__placeholder-image {
        height: 100%;
        width: auto;
    }
    .images-gallery__image-placeholder-caption {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
        width: 100%;
        background: #e7eff4;
    }
    .images-gallery__add-image-controls {
        display: flex;
        width: 100%;
        justify-content: flex-end;
    }
    .images-gallery__upload-ad {
        margin-left: 16px;
    }
    .images-gallery__upload-status {
        display: flex;
        float: left;
        justify-content: center;
        align-items: center;
        min-width: 500px;
        height: 40px;
        margin-right: 16px;
        line-height: 40px;
    }
</style>
