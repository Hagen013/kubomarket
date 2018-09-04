<template>
    <div class="order" v-if="order!=null">
        <div class="md-layout">
            <div class="md-layout-item"
            >
                <md-button class="md-primary"
                    @click="ordersListRedirect"
                >
                    <md-icon>keyboard_backspace</md-icon>
                    НАЗАД
                </md-button>
            </div>
            <div class="md-layout-item"
            >
                <div class="total-price">
                    <span class="md-display-2">
                        {{totalPrice}} ₽
                    </span>
                </div>
            </div>
            <div class="md-layout-item"
            >
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
            </div>
        </div>
        <md-tabs md-sync-route>
            <md-tab id="tab-home" md-label="Заказ">
                <div class="md-layout tab__content">
                    <div class="md-layout-item col-1">
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
                                <md-option value="вручен">Вручен</md-option>
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
                    <div class="md-layout-item col-2">
                        <md-field>
                            <label>Время создания</label>
                            <md-input v-model="createdAtFormated" readonly></md-input>
                        </md-field>
                        <md-field>
                            <label>Адрес доставки</label>
                            <md-textarea v-model="order.data.customer.address"></md-textarea>
                        </md-field>
                        <md-field>
                            <label>Примечания</label>
                            <md-textarea v-model="order.client_notes"></md-textarea>
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
                    <div class="md-layout-item col-3">
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
                                        {{item['price']}} ₽ x {{item['quantity']}} = {{item['total_price']}} ₽
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
            </md-tab>
            <md-tab id="tab-pages" md-label="Доставка">
                <div class="tab__content">
                    <div class="md-layout">
                        <div class="md-layout-item">
                            <div class="md-title">
                                Текущий статус
                            </div>
                            <md-field>
                                <md-select
                                    v-model="order.delivery_status['service']"
                                    id="service"
                                >
                                    <md-option value="sdek">
                                        СДЭК
                                    </md-option>
                                    <md-option value="pickpoint">
                                        PickPoint
                                    </md-option>
                                    <md-option value="rupost">
                                        Почта России
                                    </md-option>
                                </md-select>
                            </md-field>
                            <md-field>
                                <label>Дата последнего изменения</label>
                                <md-input v-model="order.delivery_status['change_date']"
                                    disabled
                                >
                                </md-input>
                            </md-field>
                            <md-field>
                                <label>Внутренний номер отправления</label>
                                <md-input v-model="order.delivery_status['dispatch_number']"></md-input>
                            </md-field>
                            <md-field>
                                <label>Статус</label>
                                <md-input v-model="order.delivery_status['state_description']"></md-input>
                            </md-field>
                            <md-field>
                                <label>Код статуса</label>
                                <md-input v-model="order.delivery_status['service_status_code']"></md-input>
                            </md-field>
                        </div>
                        <div class="md-layout-item">
                            <div class="delivery-history"
                                v-if="showHistory"
                            >
                                <div class="md-title">
                                    История
                                </div>
                                <md-list class="md-triple-line">
                                    <md-list-item
                                        v-for="(item, key, index) in order.delivery_status['history']"
                                        :key="key"
                                    >
                                        <div class="md-list-item-text">
                                            <span>{{item['change_date']}}</span>
                                            <span>{{item['state_description']}}</span>
                                            <p>Код статуса: {{item['service_status_code']}}</p>
                                        </div>
                                    </md-list-item>
                                </md-list>
                            </div>
                        </div>
                    </div>
                </div>
            </md-tab>
            <md-tab id="tab-user" md-label="Клиент">
                <div class="tab__content">
                    <div class="md-layout">
                        <div class="md-layout-item col-1">
                            <div class="profile__wrap"
                                v-if="user !== null"
                            >
                                <div class="md-title">
                                    Профиль
                                </div>
                                <div class="profile__link">
                                    <md-button
                                        class="md-primary"
                                        @click="profileRedirect"
                                    >
                                        {{profileName}}
                                    </md-button>
                                </div>
                            </div>
                            <div class="feedback">
                                <div class="md-title">
                                    Обратная связь
                                </div>
                                <div class="feedback__forms">
                                    <div class="message-form">
                                        <md-field>
                                            <label>SMS</label>
                                            <md-textarea v-model="smsText">
                                            </md-textarea>
                                        </md-field>
                                        <md-button
                                            class="md-primary md-raised"
                                            disabled
                                        >
                                            Отправить
                                        </md-button>
                                    </div>
                                    <div class="message-form">
                                        <md-field>
                                            <label>Email</label>
                                            <md-textarea v-model="emailText">
                                            </md-textarea>
                                        </md-field>
                                        <md-button
                                            class="md-primary md-raised"
                                            disabled
                                        >
                                            Отправить
                                        </md-button>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="md-layout-item col-2">
                            <div class="orders"
                                v-if="hasOrders"
                            >
                                <div class="md-title">
                                    История заказов
                                </div>
                                <div class="orders__list">
                                    <div class="order__item"
                                        v-for="order in orders"
                                        :key="order.id"
                                    >
                                        <div class="order__id">
                                            №{{order.id}}
                                        </div>
                                        <div class="order__price">
                                            {{order.data.cart.total_price}} ₽
                                        </div>
                                        <div class="order__date">
                                            {{order.created_at|dataFilter}}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </md-tab>
        </md-tabs>
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
            userApiUrl: '/api/users/',
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
            itemsChanged: false,
            smsText: "",
            emailText: "",
            userId: null,
            user: null,
            userProfile: null,
            userOrders: []
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
            clientNotesChanged() {
                if (this.order !== null) {
                    return (this.order.client_notes !== this.originalOrder.client_notes)
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
            deliveryStatusServiceChanged() {
                return this.order.delivery_status['service'] !== this.originalOrder.delivery_status['service']        
            },
            deliveryStatusDescriptionChanged() {
                return this.order.delivery_status['state_description'] !== this.originalOrder.delivery_status['state_description']
            },
            deliveryStatusDispatchNumberChanged() {
                return this.order.delivery_status['dispatch_number'] !== this.originalOrder.delivery_status['dispatch_number']
            },
            deliveryServiceStatusCodeChanged() {
                return this.order.delivery_status['service_status_code'] !== this.originalOrder.delivery_status['service_status_code']
            },
            deliveryStatusChanged() {
                return (
                    this.deliveryStatusDescriptionChanged ||
                    this.deliveryStatusDispatchNumberChanged ||
                    this.deliveryServiceStatusCodeChanged ||
                    this.deliveryStatusServiceChanged
                )
            },
            hasChanged() {
                return (
                    this.stateChanged ||
                    this.sourceChanged ||
                    this.notesChanged ||
                    this.clientNotesChanged ||
                    this.itemsChanged ||
                    this.deliveryChanged ||
                    this.customerChanged ||
                    this.geoChanged ||
                    this.deliveryStatusChanged
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
            },
            showHistory() {
                if (this.order !== null) {
                    return this.order.delivery_status['history'].length > 0
                } else {
                    return false
                }
            },
            emailIsAvailable() {
                if (this.user )
                return false
            },
            hasOrders() {
                if (this.user !== null) {
                    return this.orders.length > 0
                }
                return false
            },
            profileName() {
                if (this.user !== null) {
                    let name = this.user.profile.name;
                    let surname = this.user.profile.surname;
                    return `${name} ${surname} (№ ${this.userId})`
                }
                return ""
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
                let orderData = response.body;
                if ((this.userId === null) && (orderData.user !== null) ) {
                    this.userId = orderData.user;
                    this.getUser();
                }
                this.order = orderData;
                this.originalOrder = JSON.parse(JSON.stringify(this.order));
            },
            handleErrorGETResponse(response) {
                this.apiError = true;
            },
            ordersListRedirect() {
                this.$router.go(-1);
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
            },
            sendEmailMessage() {

            },
            sendSmsMessage() {

            },
            getUser() {
                let url = `${this.userApiUrl}${this.userId}`;
                this.$http.get(url).then(
                    response => {
                        this.handleSuccessfulGETUserResponse(response);
                    },
                    response => {
                        this.handleFailedGETUserResponse(response);
                    }
                )
                this.getUserOrders();
            },
            getUserOrders() {
                let url = `${this.userApiUrl}${this.userId}/orders/`;
                this.$http.get(url).then(
                    response => {
                        this.handleSuccessfulGetOrdersResponse(response);
                    },
                    response => {
                        this.handleFailedGetOrdersResponse(response)
                    }
                )
            },
            handleSuccessfulGetOrdersResponse(response) {
                this.orders = response.body;
            },
            handleFailedGetOrdersResponse(response) {
            },
            handleSuccessfulGETUserResponse(response) {
                this.user = response.body;
            },
            handleFailedGETUserResponse(response) {
            },
            profileRedirect() {
                let path = `/users/${this.userId}`;
                this.$router.push({path: path});
            }
        },
        filters: {
            dataFilter(dataString) {
                let date = new Date(dataString);
                let year = date.getFullYear();
                let month = normalizeNumber(date.getMonth()+1);
                let day = normalizeNumber(date.getDate());
                let minutes = normalizeNumber(date.getMinutes());
                let hours = normalizeNumber(date.getHours());
                let seconds = normalizeNumber(date.getSeconds());
                return `${day}.${month}.${year} ${hours}:${minutes}:${seconds}`
            },
            capitalize(value) {
                if (!value) return ''
                value = value.toString()
                return value.charAt(0).toUpperCase() + value.slice(1)
            },
        }
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
    .tab__content {
        padding-top: 32px;
    }
    .col-1 {
        padding-right: 16px;
    }
    .col-2 {
        padding-right: 16px;
    }
    .delivery-history {
        padding-left: 32px;
    }
    .message-form {
        margin-bottom: 32px;
    }
    .orders__list {
        padding: 16px 0px;
    }
    .order__item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px;
        transition: .3s cubic-bezier(.4,0,.2,1);
        transition-property: background-color,font-weight;
        will-change: background-color,font-weight;
        cursor: pointer;
        &:hover {
            background-color: rgba(0,0,0,.08);
        }
        border-top: 1px solid rgba(0, 0, 0, 0.12);
    }
    .feedback {
        padding: 32px 0px;
    }
    .feedback__forms {
        padding-top: 16px;
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