<template>
    <div class="delivery-courier__wrap">
        <div class="delivery-courier">    
            <div 
            v-if="isPostalServiceAvailable" 
            class="delivery-courier__form" 
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
                <textarea class="input delivery-courier__additional-info" placeholder="Почтовый индекс и ваши пожелания" v-model="address.note">
                </textarea>
            </div>
            <div v-else class="delivery-courier__form cart__text">
                <br/>
                К сожалению, доставку Почтой России в {{ cityName }}  осуществить невозможно.
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
        }
    },
    props: [
        'deliveryData',
        'cityName',
        'isPostalServiceAvailable',
        'customerAddress'
    ],
    methods: {
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
    created: function () {
        // this.building = this.$store.state.orders.address.building;
        // this.appNumber = this.$store.state.orders.address.appNumber;
        // this.street = this.$store.state.orders.address.street;
        // this.entrance = this.$store.state.orders.address.entrance;
        // this.floor = this.$store.state.orders.address.floor;
        // this.passNumber = this.$store.state.orders.address.passNumber;
        // this.note = this.$store.state.orders.address.note;
    }
}
</script>
