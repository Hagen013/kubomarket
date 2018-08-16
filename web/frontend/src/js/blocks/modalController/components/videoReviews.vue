<template>
    <div class="video-reviews"
    >
        <div class="video-reviews__content"
            v-if="getListApiResponseReceived"
            v-loading="synchronizing"

        >
            <div class="video-reviews__list">
                <div class="video-reviews__item"
                    v-for="review in reviews"
                    :key="review.id"
                >
                    <el-input placeholder="" :disabled="true" v-model="review.youtube_code"></el-input>
                    <el-button 
                        type="danger"
                        class="item-button"
                        @click="deleteReview(review)"
                    >
                        Удалить
                    </el-button>
                </div>
                <div class="video-reviews__item">
                    <el-input placeholder="Введите ссылку" v-model="newCode"></el-input>
                    <el-button 
                        type="primary"
                        class="item-button"
                        :disabled="!codeIsValid"
                        @click="postReview"
                    >
                        Добавить
                    </el-button>
                </div>
            </div>
        </div>
        <div class="video-revies__placeholder"
            v-else
        >
        </div>
    </div>
</template>

<script>
import store from "../../../store";

export default {
    name: "video-reviews",
    store,
    data: () => ({
        reviews: [],
        getListApiResponseReceived: false,
        getListApiResponseError: false,
        newCode: "",
        codeRegexp: /^.*(youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/,
        synchronizing: false
    }),
    computed: {
        apiListUrl() {
            return `/api/products/${this.pk}/video-reviews/`
        },
        videoCode() {
            let matches = Array(this.newCode.match(this.codeRegexp));
            let group = matches[0];
            if ((group !== null) && (group.length === 3)) {
                return group[2]
            }
            return null
        },
        codeIsValid() {
            return this.videoCode !== null
        }
    },
    props: [
        "pk"
    ],
    created() {
        this.initialize();
    },
    methods: {
        initialize() {
            this.getReviews();
        },
        getReviews() {
            this.$http.get(this.apiListUrl).then(
                response => {
                    this.handleSuccessfulGetListResponse(response); 
                },
                response => {
                    this.handleFailedGetListResponse(response);
                }
            )
        },
        handleSuccessfulGetListResponse(response) {
            this.reviews = response.body;
            this.synchronizing = false;
            this.getListApiResponseError = false;
            this.getListApiResponseReceived = true;
        },
        handleFailedGetListResponse(response) {
            this.synchronizing = false;
            this.getListApiResponseError = true;
            this.getListApiResponseReceived = true;
        },
        postReview() {
            this.synchronizing = true;
            let data = {
                "youtube_code": this.videoCode,
                "product": this.pk
            }
            this.$http.post(this.apiListUrl, data).then(
                response => {
                    this.handleSuccessfulPostResponse(response);
                },
                response => {
                    this.handleFailedPostResponse(response);
                }
            )
        },
        deleteReview(review) {
            let url = `${this.apiListUrl}${review.id}`;
            this.synchronizing = true;
            this.$http.delete(url).then(
                response => {
                    this.handleSuccessfulDeleteResponse(response);
                },
                response => {
                    this.handleFailedDeleteResponse(response)
                }
            )
        },
        putReview(review) {
        },
        handleSuccessfulPostResponse(response) {
            this.getReviews();
        },
        handleFailedPostResponse(response) {
        },
        handleSuccessfulDeleteResponse(response) {
            this.getReviews();
        },
        handleFailedDeleteResponse(response) {
        }
    }
}
</script>

<style lang="scss" scoped>
    .video-reviews__content {
        padding: 32px 0px;
    }
    .video-reviews__list {
        max-width: 750px;
    }
    .video-reviews__item {
        display: flex;
        flex-direction: row;
        margin-bottom: 15px;
    }
    .item-button {
        min-width: 108px !important;
        margin-left: 15px !important;
    }
</style>