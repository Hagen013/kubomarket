import Vue from 'vue'

import store from '../../store'

//Components
import navItem from './__nav-item.vue'
import purchaseModal from '../added-to-cart-modal/purchase-modal.vue'

import delivery from './components/delivery.vue'
import modalCallback from './__modal-callback.vue'


const editForm = () => import('./__edit-form.vue')


var productCard = new Vue({
    name: 'product-page',
    el: '#product-page',
    store,
    components: {
        'nav-item': navItem,
        'delivery': delivery,
        'purchase-modal': purchaseModal,
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
            return (this.thumbnailsNumber - 3) * -150;
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
    },
    created: function () {
        // Initializing
        let thumbnails = document.getElementsByClassName('photo-gallery__nav-item');
        this.thumbnailsNumber = thumbnails.length;
        if (this.thumbnailsNumber < 3) {
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
        this.productDeliveryData = JSON.parse(this.$el.attributes['delivery_data'].value);

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
                this.currentTrackOffset += 150;
                this.setTrackOffset();
            }
        },
        nextSlide() {
            if (this.navNextIsActive) {
                this.currentTrackOffset -= 150;
                this.setTrackOffset();
            }
        },
        setTrackOffset() {
            let track = document.getElementById('photo-gallery__nav-track');
            track.style.marginLeft = `${this.currentTrackOffset}px`;
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
                //this.switchNavToTablet();
            } else {
                //this.switchNavToMobile();
            }
        },
        checkMediaQueryDesktop(mql) {
            if (mql.matches) {
                //this.switchNavToDesktop();
            } else {
                //this.switchNavToTablet()
            }
        },
        checkMediaQueryWide(mql) {
            if (mql.matches) {
                //this.switchNavToWide();
            } else {
                //this.switchNavToDesktop();
            }
        },
        // this.currentDisplayMode switching
        // switchNavToMobile() {
        //     this.currentDisplayMode = 'mobile';
        //     this.currentTrackOffset = 0;
        //     this.setTrackToPosition();
        // },
        // switchNavToTablet() {
        //     this.currentDisplayMode = 'tablet';
        //     this.currentTrackOffset = 0;
        //     this.setTrackToPosition();
        // },
        showModalCityChoice() {
            this.$store.commit('showModalCityChoice/show');
        },
        addOfferToCart() {
            if (this.is_in_stock) {
                this.$store.dispatch('addToCart', {offer_identifier:this.offer_identifier});
                this.$store.commit("showPurchaseModal/show");
                
            } else {
                console.log("addOfferToCart disable");
            }
        },
        // switchNavToDesktop() {
        //     this.currentDisplayMode = 'desktop';
        //     this.currentTrackOffset = 0;
        //     this.setTrackToPosition();
        // },
        // switchNavToWide() {
        //     this.currentDisplayMode = 'wide';
        // },
        // setTrackToPosition() {
        //     let track = document.getElementById('js-photo-gallery__nav-track');
        //     this.currentTrackOffset = 0;
        //     track.style.margin = '0px';
        // },
        isImageActive(image_key) {
            if (this.currentImageKey == image_key) {
                return true;
            }
            return false;
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
                    console.log(this.productDeliveryData);
                    console.log(response.body);
                    this.deliveryData=response.body;
                },
                (response)=>{
                    this.deliveryData = {};
                })
            } else {
                console.log('kladr not inited');
            }
        },
        hideCityChoiceModal() {
            this.$store.commit('showModalCityChoice/hide');
        },
        showCityChoiceModal() {
            this.$store.commit('showModalCityChoice/show');
        },
    }
})