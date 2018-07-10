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
        errorTextStatusMap: {
            401: "Неверный email или пароль",
            403: "Аккаунт не подтверждён. Перейдите по ссылке из письма, присланного Вам на почту"
        }
    }),
    props: [
        "status",
        "details"
    ],
    computed: {
        errorText() {
            return this.errorTextStatusMap[this.status]
        }
    }
}
</script>