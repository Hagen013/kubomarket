<template>
    <transition name="fade-fast">
    <div class="login__error">
        {{errorText}}
    </div>
    </transition>
</template>

<script>
export default {
    name: "error",
    data: () => ({
    }),
    props: [
        "email_is_valid",
        "password_is_valid",
        "passwords_match",
        "server_error"
    ],
    computed: {
        errorText() {
            let text = ""
            if (!this.email_is_valid) {
                text += "Неправильный email. "
            }
            if (!this.password_is_valid) {
                text += "Пароль должен быть длиной от 6 до 28 символов. "
            }
            if (!this.passwords_match) {
                text += "Пароли не совпадают. "
            }
            if (this.server_error) {
                text += "Неправильный email или пароль."
            }
            return text
        }
    }
}
</script>