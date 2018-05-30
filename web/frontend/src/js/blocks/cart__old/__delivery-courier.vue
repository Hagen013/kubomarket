<template>
    <div class="delivery-courier__wrap">
        <div class="delivery-courier">    
            <div 
            v-if="isCurierAvailable" 
            class="delivery-courier__form"
            @input="changeCustomerAddress"
            >
                <div 
                    class="input input_block input_asterisk delivery-courier__city" 
                    placeholder="Населенный пункт" 
                    @click="showModal"
                    >
                    {{cityName}}
                </div>
                <input class="input input_block delivery-courier__building" placeholder="Дом, строение" v-model="address.building">
                <input class="input input_block delivery-courier__app-number" placeholder="Кв. или Офис" v-model="address.apartment">
    
                <input class="input input_block delivery-courier__pass-number" placeholder="Домофон или код" v-model="address.pass_number">
                <input class="input input_block delivery-courier__street" placeholder="Улица" v-model="address.street">
    
                <input class="input input_block delivery-courier__entrance" placeholder="Подъезд" v-model="address.entrance">
                <input class="input input_block delivery-courier__floor" placeholder="Этаж" v-model="address.floor">
                <textarea class="input delivery-courier__additional-info" placeholder="Пожелания" v-model="address.note">
                </textarea>
            </div>
            <div v-else class="delivery-courier__form cart__text">
                К сожалению, доставку курьером в {{ cityName }}  осуществить невозможно.
            </div>

        </div>
    </div>
</template>

<script>
import { Vue } from '../../vue.js';;

import store from '../../store'

export default {
    name: "delivery-courier",
    store,
    data: function () {
        return {
            // address: {
            //     building: "",
            //     apartment: "",
            //     street: "",
            //     entrance: "",
            //     floor: "",
            //     pass_number: "",
            //     note: "",
            // }
        }
    },
    props: [
        'deliveryData',
        'cityName',
        'isCurierAvailable',
        'customerAddress'
    ],
    methods: {
        changeCustomerAddress() {
            this.$parent.$emit('changeCustomerAddress', this.address);
        },
        showModal() {
            this.$store.commit('showModalCityChoice/show');
        },
    },
    computed: {
        address: {
            get() {
                return this.customerAddress;
            },
            set(value) {
                this.address = new Object(this.$store.state.customer.address);
            }

        }
    },
}
</script>
