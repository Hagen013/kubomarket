<template>
    <div class="review-form__wrap"
        @click.self="hide"
    >
        <div class="review-form">
            <div class="review-form__content"
                v-if="isEditing"
            >
                <div class="review-form__top">
                    <h2>Оставить отзыв</h2>
                </div>
                <div class="review-form__bottom">
                    <div class="review-form__rating">
                        <div class="review-form__rating-caption">
                            Оценка товара:
                        </div>
                        <star-rating
                            v-model="rating"
                            :increment="0.5"
                            :star-size="24"
                            text-class="reivew-form__stars-text"
                        >
                        </star-rating>
                    </div>
                    <div class="review-form__text">
                        <textarea class="review__textarea textarea"
                            v-model="review.content"
                            placeholder="Ваш отзыв"
                        >
                        </textarea>
                    </div>
                </div>
                <div class="review__controls">
                    <div class="button button_blue"
                        @click="create"
                    >
                        Отправить
                    </div>
                </div>
            </div>
            <div class="review-form__success"
                v-if="reviewCreated"
            >
                Спасибо! Ваш отзыв успешно отправлен. Мы рассмотрим Ваш отзыв течении нескольких для
                соответствия с законами РФ относительно публикации информации в интернете и он будет
                опубликован на странице данного товара.
            </div>
            <div class="review-form__error"
                v-if="responseError"
            >
                <p>
                    Ваш отзыв не удалось отправить по неизвестной причине :( 
                </p>
                <p>
                    Пожалуйста, свяжитесь с оператором магазина, если данное сообщение будет повторятся.
                </p>
            </div>
        </div>
    </div>
</template>

<script>
    import StarRating from 'vue-star-rating'

    export default {
        name: 'review-form',
        components: {
            "star-rating": StarRating
        },
        data: () => ({
            review: {
                content: "",
                rating: 10
            },
            reviewCreated: false,
            responseError: false,
            rating: 5,
        }),
        props: [
            'pk',
            'user'
        ],
        created() {
            this.review.product = this.pk;
            this.review.user = this.user;
        },
        computed: {
            isEditing() {
                return ( (this.reviewCreated===false) && (this.responseError===false) )
            }
        },
        methods: {
            create() {
                this.$http.post(`/api/products/${this.pk}/reviews/`, this.review).then(
                    response => {
                        this.handleSuccessfulResponse(response);
                    },
                    response => {
                        this.handleFailedResponse(response);
                    }
                )
            },
            handleSuccessfulResponse(response) {
                this.reviewCreated = true;
            },
            handleFailedResponse(response) {
                //console.log(response);
                this.responseError = true;
            },
            hide() {
                this.$store.commit('showReviewForm/hide');
            }
        },
        watch: {
            rating() {
                this.review.rating = this.rating * 2;
            }
        }
    }
</script>

<style lang="scss" scoped>
</style>