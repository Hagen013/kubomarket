<template>
    <md-app>

        <md-app-toolbar class="md-primary">
            <md-button class="md-icon-button" @click="toggleMenu" v-if="!menuVisible">
            <md-icon>menu</md-icon>
            </md-button>
            <span class="md-title">{{appTitle}}</span>
        </md-app-toolbar>

        <md-app-drawer
            :md-active.sync="menuVisible"
            md-persistent="full"
        >
            <md-toolbar class="md-transparent" md-elevation="0">
                <span class="md-title toolbar-title">Меню</span>
                <div class="md-toolbar-section-end">
                    <md-button class="md-icon-button md-dense" @click="toggleMenu">
                    <md-icon>keyboard_arrow_left</md-icon>
                    </md-button>
                </div>
            </md-toolbar>

            <md-list>
                <md-list-item @click="route('/orders')"
                    :class="{ 'md-list-item--active' : $router.currentRoute.fullPath=='/orders' }"
                >
                    <md-icon>shopping_cart</md-icon>
                    <span class="md-list-item-text">Заказы</span>
                </md-list-item>

                <md-list-item @click="route('/offers')"
                    :class="{ 'md-list-item--active' : $router.currentRoute.fullPath=='/offers' }"
                >
                    <md-icon>file_download</md-icon>
                    <span class="md-list-item-text">Остатки</span>
                </md-list-item>

                <md-list-item @click="route('/attributes')"
                    :class="{ 'md-list-item--active' : $router.currentRoute.fullPath=='/attributes' }"
                >
                    <md-icon>format_list_bulleted</md-icon>
                    <span class="md-list-item-text">Атрибуты</span>
                </md-list-item>

                <md-list-item @click="route('/upload')"
                    :class="{ 'md-list-item--active' : $router.currentRoute.fullPath=='/upload' }"
                >
                    <md-icon>add</md-icon>
                    <span class="md-list-item-text">Новые товары</span>
                </md-list-item>

                <md-list-item @click="route('/images')"
                    :class="{ 'md-list-item--active' : $router.currentRoute.fullPath=='/images' }"
                >
                    <md-icon>add_a_photo</md-icon>
                    <span class="md-list-item-text">Изображения</span>
                </md-list-item>

                <md-list-item @click="route('/categories')"
                    :class="{ 'md-list-item--active' : $router.currentRoute.fullPath=='/categories' }"
                >
                    <md-icon>device_hub</md-icon>
                    <span class="md-list-item-text">Категории</span>
                </md-list-item>

                <md-list-item @click="route('/users')"
                    :class="{ 'md-list-item--active' : $router.currentRoute.fullPath=='/users' }"
                >
                    <md-icon>people</md-icon>
                    <span class="md-list-item-text">Пользователи</span>
                </md-list-item>

            </md-list>

        </md-app-drawer>

        <md-app-content>
            <transition name="fade-fast" mode="out-in">
                <router-view></router-view>
            </transition>
        </md-app-content>

    </md-app>
</template>

<script>
    import 'vue2-animate/dist/vue2-animate.min.css'
    import VueRouter from 'vue-router'
    import store from './../store';

    import syncOffers from './sync-offers/sync-offers.vue'
    import syncAttributes from './sync-attributes/sync-attributes.vue'
    import syncImages from './sync-images/sync-images.vue'
    import uploadOffers from './upload-offers/upload-offers.vue'
    import orders from './orders/orders.vue'
    import orderForm from './orders/components/orderForm.vue'
    import categories from './categories/categories.vue'
    import categoryForm from './categories/components/categoryForm.vue'
    import users from './users/users.vue'
    import userProfile from './users/components/userProfile.vue'

    const routes = [
        { path: '/', redirect: "/orders" },
        { path: '/offers', component: syncOffers },
        { path: '/attributes', component: syncAttributes },
        { path: '/images', component: syncImages },
        { path: '/upload', component: uploadOffers },
        { path: '/orders', component: orders },
        { path: '/order/:id', component: orderForm },
        { path: '/categories', component: categories },
        { path: '/category/', component: categoryForm },
        { path: '/category/:id', component: categoryForm },
        { path: '/users', component: users },
        { path: '/users/:id', component: userProfile }
    ]

    const router = new VueRouter({
        routes
    })

    export default {
        name: 'app',
        router,
        components: {
        },
        data: () => ({
            menuVisible: true,
            currentDisplayMode: 'wide'
        }),
        computed: {
            appTitle() {
                return this.$store.state.admin.appTitle
            }
        },
        created() {
            let mqlMobile = window.matchMedia('screen and (min-width: 480px)');
            let mqlTablet = window.matchMedia('screen and (min-width: 750px)');
            let mqlDesktop = window.matchMedia('screen and (min-width: 970px)');
            let mqlWide = window.matchMedia('screen and (min-width: 1170px)');

            mqlMobile.addListener(this.checkMediaQueryMobile);
            mqlTablet.addListener(this.checkMediaQueryTablet);
            mqlDesktop.addListener(this.checkMediaQueryDesktop);
            mqlWide.addListener(this.checkMediaQueryWide);

            this.currentDisplayMode = this.getCurrentDisplayMode();
        },
        methods: {
            toggleMenu() {
                this.menuVisible = !this.menuVisible;
            },
            route(arg) {
                router.replace({ path: arg })
            },
            hideNavigation() {
                if ( this.menuVisible ) {
                    this.menuVisible = false;
                }
            },
            getCurrentDisplayMode() {
                let width = window.innerWidth;
                if (width < 970) {
                    if (width >= 750) {
                        return 'tablet'
                    } else {
                        return 'mobile'
                    }
                } else if (width < 1170) {
                    return 'desktop'
                } else {
                    return 'wide'
                }
            },
            checkMediaQueryMobile(mql) {
                if (mql.matches) {
                } else {
                }
            },
            checkMediaQueryTablet(mql) {
                if (mql.matches) {
                    this.switchToTablet();
                } else {
                    this.switchToMobile();
                }
            },
            checkMediaQueryDesktop(mql) {
                if (mql.matches) {
                    this.switchToDesktop();
                } else {
                    this.switchToTablet()
                }
            },
            checkMediaQueryWide(mql) {
                if (mql.matches) {
                    this.switchToWide();
                } else {
                    this.switchToDesktop();
                }
            },
            switchToMobile() {
                this.currentDisplayMode = 'mobile';
                this.$forceUpdate();
            },
            switchToTablet() {
                this.currentDisplayMode = 'tablet';
                this.$forceUpdate();
            },
            switchToDesktop() {
                this.currentDisplayMode = 'desktop';
                this.menuVisible = false;
                this.$forceUpdate();
            },
            switchToWide() {
                this.currentDisplayMode = 'wide';
                this.menuVisible = true;
                this.$forceUpdate();
            },
        },
        watch: {
        }
    }


</script>

<style lang="scss" scoped>
    @import 'node_modules/sass-mq/mq';

    $mq-breakpoints: (
        mobile:  480px,
        tablet:  750px,
        desktop: 970px,
        wide:    1170px
    );
    .md-app {
        min-height: 100vh;
        min-width: 850px;
    }
    .md-drawer {
        width: 230px;
        max-width: calc(100vw - 125px);
    }
    .md-list-item--active {
        background: rgba(27,54,100,0.08);
        border-left: 6px solid var(--md-theme-default-primary);
    }
    .md-content {
        width: 100% !important;
    }
    .md-app-drawer {
        width: 54px;
        @include mq($from: wide) {
            width: 230px;
        }
    }
    .md-list-item-text {
        display: none;
        @include mq($from: wide) {
            display: block;
        }
    }
    .toolbar-title {
        display: none;
        @include mq($from: wide) {
            display: block;
        }
    }
</style>