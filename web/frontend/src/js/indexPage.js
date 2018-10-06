// Common VUE and store
import {Vue} from './vue.js'
import store from './store';

// Common
import header from './blocks/header'
import footer from './blocks/footer'
import mobileMenu from './blocks/mobileMenu/'
import mobileCatalog from './blocks/mobileCatalog/'
import modalController from './blocks/modalController/index.js';

//Page-specific
import subscribeController from './blocks/subscribeController';

//store.dispatch('geo/initGeo');
store.dispatch('initAll');


var initialized  = false;
let mqlMobile = window.matchMedia('screen and (min-width: 480px)');
let mqlTablet = window.matchMedia('screen and (min-width: 750px)');
let mqlDesktop = window.matchMedia('screen and (min-width: 970px)');
let mqlWide = window.matchMedia('screen and (min-width: 1170px)');

function handleResize(mql) {
    if (initialized) {
        vkGroupdWidgetInit();
    }
}

function vkGroupdWidgetInit(mql) {
    initialized = false;
    let container = document.getElementById("vk-group-widget-container");
    let width = container.clientWidth;
    let height = container.clientHeight;
    document.getElementById("vk-group-widget").innerHTML = "";
    VK.Widgets.Group("vk-group-widget", {mode: 0, width: width, height: height, color3: "00A651"}, 167697602);
    initialized = true;
}

mqlMobile.addListener(handleResize);
mqlTablet.addListener(handleResize);
mqlDesktop.addListener(handleResize);
mqlWide.addListener(handleResize);

vkGroupdWidgetInit();

$('#page-slider').owlCarousel({
    loop: true,
    margin: 10,
    nav: false,
    items: 1,
    autoplay: true,
    autoplayTimeout: 3000,
    autoplayHoverPause: true,
    responsive: {
        0: {

        },
        480: {

        },
        750: {

        },
        970: {

        },
        1170: {
            
        }
    }
})

$('#carousel-1').owlCarousel({
    loop: true,
    margin: 10,
    nav: true,
    dots: false,
    items: 1,
    autoplay: true,
    autoplayTimeout: 3000,
    autoplayHoverPause: true,
    navText: ['<i class="arrow-icon icon_arrow-left"></i>', '<i class="arrow-icon icon_arrow-right"></i>'],
    responsive: {
        0: {

        },
        480: {

        },
        750: {
            items: 2,
        },
        970: {
            items: 2,
        },
        1170: {
            items: 3
        }
    }
})

$('#carousel-2').owlCarousel({
    loop: true,
    margin: 10,
    nav: true,
    dots: false,
    items: 1,
    autoplay: true,
    autoplayTimeout: 4000,
    autoplayHoverPause: true,
    navText: ['<i class="arrow-icon icon_arrow-left"></i>', '<i class="arrow-icon icon_arrow-right"></i>'],
    responsive: {
        0: {

        },
        480: {

        },
        750: {
            items: 2,
        },
        970: {
            items: 2,
        },
        1170: {
            items: 3
        }
    }
})

$('#carousel-3').owlCarousel({
    loop: true,
    margin: 10,
    nav: true,
    dots: false,
    items: 1,
    autoplay: true,
    autoplayTimeout: 3000,
    autoplayHoverPause: true,
    navText: ['<i class="arrow-icon icon_arrow-left"></i>', '<i class="arrow-icon icon_arrow-right"></i>'],
    responsive: {
        0: {

        },
        480: {

        },
        750: {
            items: 2,
        },
        970: {
            items: 2,
        },
        1170: {
            items: 3
        }
    }
})
