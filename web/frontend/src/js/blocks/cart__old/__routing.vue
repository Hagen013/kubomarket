<template>
    <div class="routing cart__routing">
        <div @click="$emit('selectTab', 0)" 
            :class="{routing__item_active:(curentTabKey==0)}" 
            class="routing__item float-item">
            <div class="routing__skewx-top"></div>
            <div class="routing__skewx-bottom"></div>
            <div class="routing__caption routing__caption_items">
                Корзина
            </div>
        </div>
        <div @click="$emit('selectTab', 1)" 
            :class="{routing__item_active:(curentTabKey==1)}" 
            class="routing__item float-item">
            <div class="routing__skewx-top"></div>
            <div class="routing__skewx-bottom"></div>
            <div class="routing__caption routing__caption_delivery">
                Доставка
            </div>
        </div>
        <div @click="$emit('selectTab', 2)" 
            :class="{routing__item_active:(curentTabKey==2)}" 
            class="routing__item float-item">
            <div class="routing__skewx-top"></div>
            <div class="routing__skewx-bottom"></div>
            <div class="routing__caption routing__caption_payment">
                Оплата
            </div>
        </div>
        <div class="clearfix">
        </div>
    </div>
</template>

<script>

export default {
    name: "cart-routing",
    props:[
        'curentTabKey',
    ]
}
</script>
