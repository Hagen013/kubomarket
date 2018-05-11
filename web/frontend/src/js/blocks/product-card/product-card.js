import Vue from 'vue'

import store from '../../store'

//Components
import navItem from './__nav-item.vue'
import deliveryInner from './__delivery-inner.vue'
import addedToCartModal from '../added-to-cart-modal/added-to-cart-modal.vue'

import modalCallback from '../header-top/__modal-callback.vue'


const editForm = () => import('./__edit-form.vue')


var productCard = new Vue({
    name: 'product-card',
    el: '#js-product-card',
    store,
    components: {
        'nav-item': navItem,
        'delivery-inner': deliveryInner,
        'added-to-cart-modal' : addedToCartModal,
        editForm,
        modalCallback
    },
    data: {
        isMounted: false,

        currentDisplayMode: 'mobile',
        currentTrackOffset: 0,
        currentImageKey: 0,
        thumbnailsNumber: 0,
        descriptionMenuState: 0,
        showNavButtons: true,
        isMounted: false,
        showAddedToCartModal: false,
        showEditControls: false,
        isShowModalCallback: false,
        showEditForm: false,

        offer_identifier: undefined,
        is_in_stock: false,

        deliveryData: undefined,
        productDeliveryData: undefined
    },
    computed: {
        navTrackMaxOffset() {
            switch (this.currentDisplayMode) {
                case "mobile":
                    return (this.thumbnailsNumber - 4) * -100;
                case "tablet":
                    return (this.thumbnailsNumber - 7) * -100;
                case "desktop":
                    return (this.thumbnailsNumber - 4) * -100;
                case "wide":
                    return (this.thumbnailsNumber - 4) * -100;
            }
        },
        navPrevIsActive() {
            if (this.currentTrackOffset < 0) {
                return true;
            }
            return false;
        },
        navNextIsActive() {
            if (this.currentTrackOffset > this.navTrackMaxOffset) {
                return true;
            }
            return false;
        },
        isAttrbitesTabActive() {
            return this.descriptionMenuState == 0 ? true : false;
        },
        isDescriptionTabActive() {
            return this.descriptionMenuState == 1 ? true : false;
        },
        kladr() {
            return this.$store.state.geo.code;
        },
        cityName() {
            return this.$store.state.geo.city;
        },
        isDeliveryDataInited() {
            return this.$store.state.geo.isDataInited && this.deliveryData !== undefined;
        }
        // addOfferToCart() {
        //     if (this.is_in_stock) {
        //         this.$http.put(
        //             `/api/cart/items/${this.offer_identifier}/`)
        //             .then(response => {
        //                 this.showAddedToCartModal = true;
        //                 this.$store.dispatch('cart/items/syncCart');
        //             });
        //     } else {
        //         console.log("addOfferToCart disable");
        //     }
        // },

    },
    created: function () {
        // Initializing
        let thumbnails = document.getElementsByClassName('photo-gallery__nav-item');
        this.thumbnailsNumber = thumbnails.length;
        if (this.thumbnailsNumber < 5) {
            this.showNavButtons = false;
        }

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
    mounted() {
        this.offer_identifier = this.$el.attributes['offer_identifier'].value;
        this.is_in_stock = this.$el.attributes['is_in_stock'].value == "True";

        // обязательные productDeliveryData
        this.productDeliveryData = JSON.parse(this.$el.attributes['delivery_data'].value)

        this.getDeliveryData();

        this.isMounted = true;
        this.$http.get(
            '/api/admin/is_staff/')
            .then(response => {
                this.showEditControls = response.data['is_staff'];
            });
    },
    watch: {
        kladr: function(val) {
            this.deliveryData = undefined;
            this.getDeliveryData();
        }
    },
    methods: {
        // Thumbnails slider
        prevSlide() {
            if (this.navPrevIsActive) {
                this.currentTrackOffset += 100;
                this.setTrackOffset();
            }
        },
        nextSlide() {
            if (this.navNextIsActive) {
                this.currentTrackOffset -= 100;
                this.setTrackOffset();
            }
        },
        setTrackOffset() {
            let track = document.getElementById('js-photo-gallery__nav-track');
            switch (this.currentDisplayMode) {
                case 'mobile':
                    track.style.marginLeft = `${this.currentTrackOffset}px`;
                    break;
                case 'tablet':
                    track.style.marginLeft = `${this.currentTrackOffset}px`;
                    break;
                case 'desktop':
                    track.style.marginTop = `${this.currentTrackOffset}px`;
                    break;
                case 'wide':
                    track.style.marginTop = `${this.currentTrackOffset}px`;
                    break;
            }
        },
        changeImage(image_key) {
            this.currentImageKey = image_key;
        },
        // Media queries processing
        // getCurrentDisplayMode - needed to initialize this.currentDisplayMode
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
                //this.switchThumbGalleryToTablet();
            } else {
                // no further breakpoints 
            }
        },
        checkMediaQueryTablet(mql) {
            if (mql.matches) {
                this.switchNavToTablet();
            } else {
                this.switchNavToMobile();
            }
        },
        checkMediaQueryDesktop(mql) {
            if (mql.matches) {
                this.switchNavToDesktop();
            } else {
                this.switchNavToTablet()
            }
        },
        checkMediaQueryWide(mql) {
            if (mql.matches) {
                this.switchNavToWide();
            } else {
                this.switchNavToDesktop();
            }
        },
        // this.currentDisplayMode switching
        switchNavToMobile() {
            this.currentDisplayMode = 'mobile';
            this.currentTrackOffset = 0;
            this.setTrackToPosition();
        },
        switchNavToTablet() {
            this.currentDisplayMode = 'tablet';
            this.currentTrackOffset = 0;
            this.setTrackToPosition();
        },
        showModalCityChoice() {
            this.$store.commit('showModalCityChoice/show');
        },
        addOfferToCart() {
            if (this.is_in_stock) {
                this.$store.dispatch('addToCart', {offer_identifier:this.offer_identifier});
                this.showAddedToCartModal = true;
                // this.$store.dispatch('addToCart', {offer_identifier:this.offer_identifier}).this(
                //     ()=>{},
                //     ()=>{console.error('Error in adding to cart');}
                // );
                
            } else {
                console.log("addOfferToCart disable");
            }
        },
        switchNavToDesktop() {
            this.currentDisplayMode = 'desktop';
            this.currentTrackOffset = 0;
            this.setTrackToPosition();
        },
        switchNavToWide() {
            this.currentDisplayMode = 'wide';
        },
        setTrackToPosition() {
            let track = document.getElementById('js-photo-gallery__nav-track');
            this.currentTrackOffset = 0;
            track.style.margin = '0px';
        },
        isImageActive(image_key) {
            if (this.currentImageKey == image_key) {
                return true;
            }
            return false;
        },
        switchDescriptionMenu(newState) {
            if (this.descriptionMenuState != newState) {
                this.descriptionMenuState = newState;
            }
        },
        toggleEditForm() {
            this.showEditForm = this.showEditForm === true ? false : true;
        },
        getDeliveryData() {
            this.deliveryData = undefined;
            if (this.kladr) {
                this.$http.post(`${GEO_IP_HOST}/api/delivery/one_product/`, {
                    'kladr': this.$store.state.geo.code,
                    'product': this.productDeliveryData
                }).then(
                (response)=>{
                    this.deliveryData=response.body;
                },
                (response)=>{
                    this.deliveryData = {};
                })
            } else {
                console.log('kladr not inited');
            }
        }
    }
})