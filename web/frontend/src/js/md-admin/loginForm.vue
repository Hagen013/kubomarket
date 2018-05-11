<template>
    <md-dialog :md-active="showDialog" v-on:keyup.enter="submit">
        <md-dialog-title>Вход</md-dialog-title>
        <div class="md-dialog__content">
            <md-field md-clearable :class="messageClass">
                <label>Логин</label>
                <md-input v-model="username" required></md-input>
            </md-field>
            <md-field :class="messageClass">
                <label>Пароль</label>
                <md-input v-model="password" type="password" required></md-input>
            </md-field>
            <div class="order-form__controls">
                <md-button class="md-primary md-raised"
                    @click="submit"
                >
                Далее
                </md-button>
            </div>
        </div>
    </md-dialog>
</template>

<script>
    export default {
        name: 'login-form',
        data: () => ({
            sessionLoginAPIViewUrl: '/api/users/login/',
            redirectUrl: '/md-admin/',
            showDialog: true,
            username: "",
            password: "",
            authFailed: false,
        }),
        computed: {
            messageClass() {
                return {
                    "md-invalid": this.authFailed
                }
            }
        },
        mounted() {
            this.$forceUpdate();
        },
        methods: {
            submit() {
                let data = new FormData();

                data.append("username", this.username);
                data.append("password", this.password);

                this.$http.post(this.sessionLoginAPIViewUrl, data).then(
                    response => {
                        this.handleSuccessfulResponse(response);
                    },
                    response => {
                        this.handleFailedResponse(response);
                    },
                )
            },
            handleSuccessfulResponse(response) {
                window.location.href = this.redirectUrl;
            },
            handleFailedResponse(response) {
                this.authFailed = true;
            }
        }
    }
</script>

<style lang="scss" scoped>
    .md-dialog__content {
        width: 500px;
        padding: 0px 24px 32px 24px;
    }
    .order-form__controls {
        display: flex;
        justify-content: flex-end;
    }
    input:-webkit-autofill {
        -webkit-box-shadow: 0 0 0 30px white inset;
    }
</style>