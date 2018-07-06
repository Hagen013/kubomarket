<template>
    <div class="profile-data">
        <div class="profile-data__title bold">
            Мои данные
        </div>
        <div class="profile-data__delimeter">
        </div>
        <div class="profile-data__block">
            <div class="profile-data__fullname">
                <div class="input-box">
                    <input class="input"
                        placeholder="Имя"
                    >
                </div>
                <div class="input-box">
                    <input class="input"
                        placeholder="Фамилия"
                    >
                </div>
                <div class="input-box">
                    <input class="input"
                        placeholder="Отчество"
                    >
                </div>
            </div>
            <div class="profile-data__email">
            </div>
            <div class="profile-data__password">
            </div>
        </div>
        <div class="profile-data__delimeter">
        </div>
        <div class="profile-data__block">
            <div class="profile-data__phone-wrap">
                <div class="input-box">
                    <input class="input"
                        placeholder="Телефон"
                    >
                </div>
            </div>
        </div>
        <div class="profile-data__delimeter">
        </div>
        <div class="profile-data__block">
            <div class="profile-data__button button button_blue">
                СОХРАНИТЬ ДАННЫЕ
            </div>
        </div>
    </div>
</template>

<script>
import store from "../../../store";

export default {
    name: "personal-data",
    store,
    data: () => ({
    }),
    methods: {
    }
}
</script>