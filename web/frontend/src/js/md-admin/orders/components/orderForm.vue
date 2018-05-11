<template>
    <div class="md-layout" v-if="order !== null">
        <div class="md-layout-item">
            <md-button class="md-primary"
                @click="ordersListRedirect"
            >
                <md-icon>keyboard_backspace</md-icon>
                К СПИСКУ
            </md-button>

            <div class="order-main">
                <md-field>
                    <label for="status">Статус</label>
                    <md-select v-model="order.state" name="status" id="status">
                        <md-option value="новый">Новый</md-option>
                        <md-option value="недозвон">Недозвон</md-option>
                        <md-option value="доставка">Доставка</md-option>
                        <md-option value="выполнен">Выполнен</md-option>
                        <md-option value="согласован">Согласован</md-option>
                        <md-option value="отменён">Отменён</md-option>
                        <md-option value="отменён: недозвон">Отменён: недозвон</md-option>
                    </md-select>
                </md-field>
                <md-field>
                    <label>Служебные заметки</label>
                    <md-textarea v-model="order.manager_notes"></md-textarea>
                </md-field>

                <md-field>
                    <label>ФИО</label>
                    <md-input v-model="order.data.customer.name"></md-input>
                </md-field>
                <md-field>
                    <label>Телефон</label>
                    <md-input v-model="order.data.customer.phone"></md-input>
                </md-field>
                <md-field>
                    <label>Email</label>
                    <md-input v-model="order.data.customer.email"></md-input>
                </md-field>
                <md-field>
                    <label>Город (автоматически)</label>
                    <md-input v-model="order.data['geo']['city']"></md-input>
                </md-field>
                <md-field>
                    <label for="source">Источник</label>
                    <md-select v-model="order.source" name="source" id="source">
                        <md-option value="cart">Корзина</md-option>
                        <md-option value="callback">Обратный звонок</md-option>
                        <md-option value="product-page">Страница товара</md-option>
                    </md-select>
                </md-field>

            </div>

        </div>
        <div class="md-layout-item second-column">
            <div class="total-price">
                <span class="md-display-2">{{totalPrice}} ₽</span>
            </div>
            <md-field>
                <label>Время создания</label>
                <md-input v-model="createdAtFormated" readonly></md-input>
            </md-field>
            <md-field>
                <label>Адрес доставки</label>
                <md-textarea v-model="order.data.customer.address"></md-textarea>
            </md-field>
            <md-field>
                <label for="delivery-type">Способ доставки</label>
                <md-select v-model="order.data['delivery']['mod']['type']" name="delivery-type" id="delivery-type">
                    <md-option value=null>Не выбрано</md-option>
                    <md-option value="curier">Курьер</md-option>
                    <md-option value="delivery_points">Пункт выдачи</md-option>
                    <md-option value="postal_service">Почта</md-option>
                </md-select>
            </md-field>
            <md-field>
                <label>Код</label>
                <md-input v-model="order.data['delivery']['mod']['code']"></md-input>
            </md-field>
            <md-field>
                <label>Цена доставки</label>
                <md-input v-model="order.data['delivery']['mod']['price']" type="number"></md-input>
            </md-field>
        </div>
        <div class="md-layout-item third-column">
            <div class="save-button-wrap">
                <md-button class="md-primary md-raised"
                    @click="rollBack"
                    :disabled="!hasChanged"
                >
                    <md-icon>settings_backup_restore</md-icon>
                    отменить
                </md-button>
                <md-button class="md-accent md-raised" 
                    @click="updateOrder"
                    :disabled="!hasChanged"
                >
                    <md-icon>done</md-icon>
                    Сохранить
                </md-button>
            </div>

            <search-field
                v-on:item-selected="addItemToCart"
            >
            </search-field>

            <md-list>
                <div class="cart-item md-elevation-2"
                    v-for="(item, key) of cartItems"
                    :data="item"
                    :key="item['url']"
                >
                    <div class="cart-item-image">
                        <img :src="item['image']">
                    </div>
                    <div class="cart-item-content">
                        <a class="cart-item-link" :href="item['url']">
                            {{item['name']}}
                        </a>
                        <div class="cart-item-code">
                            {{item['vendor_code']}}
                        </div>
                        <div class="cart-item-price">
                            {{item['total_price']}} ₽
                        </div>
                        <div class="cart-item-quantity">
                            {{item['quantity']}} шт.
                        </div>
                    </div>

                    <md-button class="md-icon-button md-list-action delete-button"
                        @click="deleteItem(key)"
                    >
                        <md-icon class="md-accent">
                            delete
                        </md-icon>
                    </md-button>

                    <transition name="fade-fast">
                    <md-button class="md-icon-button decrement-button"
                        @click="decrementItem(key)"
                        v-if="item['quantity']>1"
                    >
                        <md-icon class="md-primary">
                            remove
                        </md-icon>
                    </md-button>
                    </transition>


                    <md-button class="md-icon-button increment-button"
                        @click="incrementItem(key)"
                    >
                        <md-icon class="md-primary">
                            add
                        </md-icon>
                    </md-button>

                </div>
            </md-list>

        </div>
    </div>

    <div class="md-layout" v-else-if="apiError === true">
    </div>

</template>

<script>
    import searchField from './searchField.vue'
    import debounce from 'debounce'
    import normalizeNumber from '../../../core/normalizeNumber.js'

    var equal = require('fast-deep-equal');

    export default {
        name: 'order-form',
        components: {
            'search-field': searchField,
        },
        data: () => ({
            componentTitle: null,
            orderApiUrl: '/api/order/',
            originalOrder: null,
            order: null,
            apiError: false,
            monthsMap: {
                0: 'Января',
                1: 'Февраля',
                2: 'Марта',
                3: 'Апреля',
                4: 'Мая',
                5: 'Июня',
                6: 'Июля',
                7: 'Авгутса',
                8: 'Сентября',
                9: 'Октября',
                10: 'Ноября',
                11: 'Декабря'
            },
            itemsChanged: false
        }),
        created() {
            this.orderId = this.$route.params.id;
            this.componentTitle = `Заказ № ${this.orderId}`;
            this.$store.commit('admin/changeAppTitle', this.componentTitle);
            this.getOrder(this.orderId);
        },
        computed: {
            createdAtFormated() {
                if (this.order !== null) {
                    return this.formatDate(this.order.created_at);
                }
            },
            stateChanged() {
                if (this.order !== null) {
                    return (this.order.state !== this.originalOrder.state)
                } else {
                    return false
                }
            },
            sourceChanged() {
                if (this.order !== null) {
                    return (this.order.source !== this.originalOrder.source)
                } else {
                    return false
                }
            },
            notesChanged() {
                if (this.order !== null) {
                    return (this.order.manager_notes !== this.originalOrder.manager_notes)
                } else {
                    return false
                }
            },
            customerChanged() {
                if (this.order !== null) {
                    let customer = JSON.stringify(this.order.data['customer']);
                    let originalCustomer = JSON.stringify(this.originalOrder.data['customer']);
                    return customer !== originalCustomer
                } else {
                    return false
                }
            },
            deliveryChanged() {
                if (this.order !== null) {
                    let delivery = JSON.stringify(this.order.data['delivery']['mod']);
                    let originalDelivery = JSON.stringify(this.originalOrder.data['delivery']['mod']);
                    return delivery !== originalDelivery
                } else {
                    return false
                }
            },
            geoChanged() {
                if (this.order !== null) {
                    let geo = JSON.stringify(this.order.data['geo']);
                    let originalGeo = JSON.stringify(this.originalOrder.data['geo']);
                    return geo !== originalGeo
                } else {
                    return false
                }
            },
            hasChanged() {
                return (
                    this.stateChanged ||
                    this.sourceChanged ||
                    this.notesChanged ||
                    this.itemsChanged ||
                    this.deliveryChanged ||
                    this.customerChanged ||
                    this.geoChanged
                )
            },
            cartItems() {
                if (this.order !== null) {
                    return this.order.data['cart']['items']
                } else {
                    return []
                }
            },
            totalPrice() {
                if (this.order !== null) {
                    let deliveryPrice = Number(this.order.data['delivery']['mod']['price']);
                    return this.order.data['cart']['total_price'] + deliveryPrice
                }
            }
        },
        methods: {
            getOrder(orderId) {
                let url = `${this.orderApiUrl}${this.orderId}/`;
                this.$http.get(url).then(
                    response => {
                        this.handleSuccesfulGETResponse(response);
                    },
                    response => {
                        this.handleErrorGETResponse(response);
                    }
                )
            },
            handleSuccesfulGETResponse(response) {
                this.order = response.body;
                this.originalOrder = JSON.parse(JSON.stringify(this.order));
            },
            handleErrorGETResponse(response) {
                this.apiError = true;
            },
            ordersListRedirect() {
                this.$router.replace({path: '/orders'});
            },
            formatDate(dateString) {
                let date = new Date(dateString);
                let year = date.getFullYear();
                let month = this.monthsMap[date.getMonth()];
                let day = normalizeNumber(date.getDate());
                let minutes = normalizeNumber(date.getMinutes());
                let hours = normalizeNumber(date.getHours());
                let seconds = normalizeNumber(date.getSeconds());

                return `${day} ${month} ${year}   ${hours}:${minutes}:${seconds}`
            },
            updateOrder() {
                let url = `${this.orderApiUrl}${this.orderId}/`;
                this.$http.put(url, this.order).then(
                    response => {
                        this.handleSuccesfulPUTResponse(response);
                    },
                    response => {
                        this.handleErrorPUTResponse(response);
                    }
                )
            },
            handleSuccesfulPUTResponse(response) {
                this.ordersListRedirect();
            },
            handleErrorPUTesponse(response) {

            },
            deleteItem(itemKey) {
                delete this.order.data['cart']['items'][itemKey];
                this.checkItemsChange();
                this.$forceUpdate();
            },
            addItemToCart(item) {
                let cartItem = {
                    image: item.image,
                    name: item.name,
                    price: item.price,
                    quantity: 1,
                    total_price: item.price*1,
                    vendor_code: item.vendor_code,
                    url: item.absolute_url
                }
                this.order.data['cart']['items'][item.offer_identifier] = cartItem;
                this.checkItemsChange();
                this.$forceUpdate();
            },
            checkItemsChange() {
                this.calculatePrices();
                let items = JSON.stringify(this.order.data['cart']['items']);
                let originalItems = JSON.stringify(this.originalOrder.data['cart']['items']);
                if ( items !== originalItems )  {
                    this.itemsChanged = true;
                } else {
                    this.itemsChanged = false;
                }
            },
            rollBack() {
                this.order = JSON.parse(JSON.stringify(this.originalOrder));
                this.checkItemsChange();
            },
            incrementItem(itemKey) {
                let item  = this.order.data['cart']['items'][itemKey];
                let quantity = item['quantity'];
                item['quantity'] += 1;
                this.checkItemsChange();
            },
            decrementItem(itemKey) {
                let item  = this.order.data['cart']['items'][itemKey];
                let quantity = item['quantity'];
                if (quantity > 1) {
                    item['quantity'] -= 1;
                }
                this.checkItemsChange();
            },
            calculatePrices() {
                let totalPrice = 0;
                //let deliveryPrice = Number(this.order.data['delivery']['mod']['price']);
                for (let key in this.cartItems) {
                    let item = this.order.data['cart']['items'][key]
                    let quantity = item['quantity'];
                    let price = item['price'];
                    item['total_price'] = price * quantity;
                    totalPrice += item['total_price']
                }
                //totalPrice += deliveryPrice;
                this.order.data['cart']['total_price'] = totalPrice;
            }
        },
    }
</script>

<style lang="scss" scoped>
    .order-main {
        padding: 0px 16px 0px 16px;
    }
    .save-button-wrap {
        display: flex;
        justify-content: flex-end;
    }
    .third-column {
        padding: 0px 0px 0px 16px;
    }
    .decrement-button {
        position: absolute;
        bottom: 8px;
        right: 80px;
    }
    .increment-button {
        position: absolute;
        bottom: 8px;
        right: 40px;
    }
    .delete-button {
        position: absolute;
        bottom: 8px;
        right: 0px;
    }
    .total-price {
        display: flex;
        height: 48px;
        width: 100%;
        align-items: center;
        justify-content: center;
    }
    .md-layout-item {
        flex: 1;
        width: 0;
    }

    .cart-item {
        position: relative;
        display: flex;
        height: 104px;
        width: 100%;
        padding: 8px 0px 6px 8px;
        margin-bottom: 16px;
    }

    .cart-item-image {
        height: 88px;
        width: 88px;
        overflow: hidden;
        text-align: center;
        img {
            height: 100%;
            width: auto;
        }
    }

    .cart-item-content {
        display: flex;
        flex-direction: column;
    }








    .fade {
        opacity: 1 !important;
        transition: opacity 1s
    }

    .fade-fast, .fadeFast {
        opacity: 1 !important;
        transition: opacity 0.2s
    }

    .fade-fast-enter-active, .fade-fast-leave-active{
        transition: opacity 0.2s
    }

    .fade-enter-active, .fade-leave-active{
        transition: opacity 1s
    }

    .fade-enter, .fade-leave-to, 
    .fade-fast-enter, .fade-fast-leave-to  {
        opacity: 0
    }
</style>