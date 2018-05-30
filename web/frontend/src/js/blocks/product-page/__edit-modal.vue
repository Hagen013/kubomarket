<template>
    <transition name="fade-fast">
    <div class="edit-modal__wrap" @click.self="hideModal">
        <div class="edit-modal">
            <div class="edit-modal__headline-area">
                <div class="edit-modal__headline">
                    {{headline}}
                </div>
            </div>
            <div class="edit-modal__content" v-if="requestSucceded">
                Удалено связей: {{response.body.deleted}}<br>
                Добавлено связей: {{response.body.added}}
            </div>
            <div class="edit-modal__content edit-modal__content_failed" v-else>
                Во время обращения к серверу произошла ошибка (код ответа: {{response.request.status}}).
                Пожалуйста, сообщите специалисту по произошедшей ситуации.
            </div>
            <div class="edit-modal__controls">
                <button class="edit-modal__button" @click="hideModal">
                    Закрыть
                </button>
                <button class="edit-modal__button" @click="productCardRedirect">
                    На страницу товара
                </button>
            </div>
        </div>
    </div>
    </transition>
</template>

<script>
    export default {
        name: 'edit-modal',
        data: () => ({
            headline: '',
            requestSucceded: false,
        }),
        props: [
            'response',
            'url'
        ],
        created: function () {
            if ( this.response.status == 200 ) {
                this.requestSucceded = true;
                this.headline = 'Товар успешно обновлён';
            } else {
                this.headline = 'Во время обновления произошла ошибка';
            }
        },
        methods: {
            hideModal() {
                this.$emit('close-modal');
            },
            productCardRedirect() {
                console.log(this.url);
                window.location.href = this.url;
            }
        }
    }
</script>

<style lang="scss" scoped>
    .edit-modal__wrap {
        position: fixed;
        display: flex;
        align-items: center;
        justify-content: center;
        top: 0px;
        height: 100%;
        width: 100%;
        z-index: 20000;
    }
    .edit-modal {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: absolute;
        height: 350px;
        width: 500px;
        padding: 16px;
        background: white;
        box-shadow: 0 10px 13px -6px rgba(0,0,0,.2), 0 20px 31px 3px rgba(0,0,0,.14), 0 8px 38px 7px rgba(0,0,0,.12);
    }
    .edit-modal__headline {
        font-size: 22px;
        font-family: PFDinDisplayPro-Bold !important;
        margin: 16px 0px 16px 0px;
    }
    .edit-modal__content {
        flex-grow: 1;
    }
    .edit-modal__controls {
        font-family: PFDinDisplayPro-Bold !important;
    }
    .edit-modal__button {
        float: right;
        display: block !important;
        height: 40px;
        margin-left: 16px;
        padding: 0px 8px 0px 8px;
        line-height: 40px;
        font-size: 14px;
        color: white;
        cursor: pointer;
        background: #448aff;
        border-radius: 3px;
        transition-duration: 0.2s;
        transition-property: background, box-shadow;
        transition-timing-function: cubic-bezier(.4,0,.2,1);
        box-shadow: 0 3px 1px -2px rgba(0,0,0,.2), 0 2px 2px 0 rgba(0,0,0,.14), 0 1px 5px 0 rgba(0,0,0,.12);
        &:hover {
            box-shadow: 0 5px 5px -3px rgba(0,0,0,.2), 0 8px 10px 1px rgba(0,0,0,.14), 0 3px 14px 2px rgba(0,0,0,.12);
        }
    }
    .edit-modal__content_failed {
        color: #ff5252;
    }
</style>