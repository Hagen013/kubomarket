import validateEmail from '../../core/validate-email.js'

let PHONE_MASK = ['+', '7',' ','(', /\d/, /\d/, /\d/, ')', ' ', /\d/, /\d/, /\d/, '-', /\d/, /\d/, /\d/, /\d/];
import { conformToMask } from 'vue-text-mask';

export default {
    namespaced: true,
    state: {
        name: "",
        phone: "",
        email: "",
        address: ""
    },
    mutations: {
        name(state, payload) {
            state.name = payload;
        },
        phone(state, payload) {
            state.phone = payload;
        },
        maskedPhone(state, payload) {
            state.phone =  (payload.match(/\d/g)||[]).slice(1).join('');
        },
        email(state, payload) {
            state.email = payload;
        },
        address(state, payload) {
            state.address = payload;
        },
        setData(state, payload) {
            for (let prop in payload) {
                if (prop in state) {
                    state[prop] = payload[prop];
                } else {
                    console.error(`Error in setData - state has not ${prop} field;`);
                }
            }
        }
    },
    getters: {
        isEmailValid: state => {
            return validateEmail(state.email);
        },
        isPhoneValid: state => {
            return /\d{10}/.test(state.phone);
        },
        isEnoughForOrder: (state, getters) => {
            return (
                getters.isPhoneValid
            );
        },
        fullAddress: (state, getters) => {
            let not_entered = "незаполненно";
            return(
            `
            Строение: ${state.address.building || not_entered};
            Квартира: ${state.address.apartment || not_entered};
            Улица: ${state.address.street || not_entered};
            Подъезд: ${state.address.entrance || not_entered};
            Этаж: ${state.address.floor || not_entered};
            Пароль: ${state.address.pass_number || not_entered};
            Заметка клиента: ${state.address.note || not_entered};
            `.replace(/\s{2,}/g, ' ')
            );
        },
        phoneMask: (state, getters) => {
            return PHONE_MASK;
        },
        maskedPhone: (state, getters) => {
            if (state.phone == "") {
                return ""
            } else {
                return conformToMask(
                    state.phone,
                    PHONE_MASK,
                )['conformedValue'];

            }
        }
    }
}