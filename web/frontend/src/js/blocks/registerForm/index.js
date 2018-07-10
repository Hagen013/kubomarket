import { Vue } from "../../vue.js";
import store from "../../store"

import errors from "./components/errors.vue"


var registerForm = new Vue({
    name: 'register-form',
    el: '#register-form',
    store,
    data: {
        apiUrl: "/api/users/",
        redirectUrl: "/u/registration-success/",
        username: "",
        password: "",
        password2: "",
        submitted: false,
        registrationFailed: false,
    },
    components: {
        "errors": errors
    },
    computed: {
        passwordsMatch() {
            return this.password===this.password2;
        },
        customerEmail: {
            get() {
                return this.$store.state.customer.email;
            },
            set(value) {
                this.$store.commit('customer/setData', {email:value})
            }
        },
        emailIsValid() {
            return this.$store.getters["customer/isEmailValid"];
        },
        passwordIsValid() {
            return (this.password.length > 6) && (this.password.length < 28)
        },
        emailError() {
            return ( (this.submitted) && (!this.emailIsValid) )
        },
        passwordError() {
            return ( (this.submitted) && (!this.passwordIsValid) )
        },
        isValid() {
            return ( this.emailIsValid && this.passwordIsValid && this.passwordsMatch )
        },
        showErrors() {
            return ( ((!this.isValid) && (this.submitted)) || this.registrationFailed  )
        }
    },
    methods: {
        submit() {
            this.submitted = true;
            if (this.isValid) {
                let data = new FormData();
                data.append("username", this.customerEmail);
                data.append("email", this.customerEmail);
                data.append("password", this.password);
                this.$http.post(this.apiUrl, data).then(
                    response => {
                        this.handleSuccessfulResponse(response);
                    },
                    response => {
                        this.handleFailedResponse(response);
                    }
                )
            }
        },
        handleSuccessfulResponse(response) {
            window.location.href = this.redirectUrl;
        },
        handleFailedResponse(response) {
            this.registrationFailed = true;
        } 
    }
});
