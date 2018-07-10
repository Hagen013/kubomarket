import { Vue } from '../../vue.js';
import store from '../../store'

import error from './components/error.vue'

var loginForm = new Vue({
    name: 'login-form',
    el: '#login-form',
    store,
    components: {
        "error": error
    },
    data: {
        loginApiUrl: "/api/users/auth/",
        redirectUrl: "/",
        username: "",
        password: "",
        errorDetails: "",
        authFailed: false,
        authResponseStatusCode: null
    },
    computed: {
    },
    methods: {
        submit() {
            this.authFailed = false;
            let data = new FormData();
            data.append("username", this.username);
            data.append("password", this.password);
            this.$http.post(this.loginApiUrl, data).then(
                response => {
                    this.handleSuccessfulAuthResponse(response);
                },
                response => {
                    this.handleFailedAuthResponse(response);
                }
            )
        },
        handleSuccessfulAuthResponse(response) {
            this.authResponseStatusCode = response.status;
            window.location.href = this.redirectUrl;
        },
        handleFailedAuthResponse(response) {
            console.log(response);
            this.authResponseStatusCode = response.status;
            this.authFailed = true;
            this.errorDetails = response.body["details"];
        },
        noop() {
            console.log("noop");
        }
    }
});