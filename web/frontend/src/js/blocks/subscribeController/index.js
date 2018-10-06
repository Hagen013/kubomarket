import { Vue } from "../../vue.js";
import store from "../../store"


var registerForm = new Vue({
    name: 'subsribe',
    el: '#subscribe',
    store,
    data: {
        email: "",
        apiUrl: "/api/users/subscribes/"
    },
    computed: {
        emailIsValid() {

        }
    },
    methods: {
        submit() {
            let data = {
                "email": this.email
            }
            this.$http.post(this.apiUrl, data).then(
                response => {
                    this.handleSuccessfulResponse(response);
                },
                response => {
                    this.handleFailedResponse(response);
                }
            )
        },
        handleSuccessfulResponse(response) {
            console.log("success");
            this.$store.commit("showSubscribeModal/show");
        },
        handleFailedResponse(response) {
        }
    }
});
