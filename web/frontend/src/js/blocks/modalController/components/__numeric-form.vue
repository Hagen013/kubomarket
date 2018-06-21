<template>
    <div class="numeric-form">
        <div class="numeric-form__title-area">
            <div class="numeric-form__title">
            {{attribute.name}}
            </div>
            <transition name="fade-fast">
                <div class="numeric-form__changed" v-if="hasChanged">
                изменено
                </div>
            </transition>
        </div>
        <div class="numeric-form__value" :class="{ numericForm__valueFocused: isFocused }">
            <div class="value-label" v-if="isEmpty">не указано</div>
            <input class="numeric-form__value-field"
                type="text"
                @click="isFocused=true"
                @blur="isFocused=false"
                @input="changeValue"
                onkeypress="return event.charCode >= 48 && event.charCode <= 57"
                v-model="proxyValue"
            >
        </div>
    </div>
</template>

<script>
    export default {
        name: 'numeric-form',
        data: () => ({
            isFocused: false,
            dropdownIsActive: false,
            initialValue: '',
            proxyValue: '',
        }),
        props: [
            'attribute',
            'selected_values',
            'saving_iteration'
        ],
        created() {
            if (this.selected_values.length > 0) {
                this.initialValue = this.selected_values[0].value;
                this.proxyValue = String(this.initialValue);
            }
        },
        computed: {
            isEmpty() {
                return (this.proxyValue === '')
            },
            hasChanged() {
            }
        },
        methods: {
            setDefaults() {
            },
            clearActiveOption() {
            },
            changeActiveOption(optionName, index) {
            },
            changeValue() {
                console.log('change value');
            }
        },
        watch: {
            saving_iteration() {
                this.setDefaults();
            },
        }
    }
</script>

<style lang="scss" scoped>
    .value-label {
        position: absolute;
        top: 6px;
        left: 0px;
        font-size: 12px;
        color: rgba(0, 0, 0, 0.54);
    }
    .numeric-form {
        position: relative;
    }
    .numeric-form__title {
        font-size: 14px;
        font-family: PFDinDisplayPro-Bold !important;
    }
    .numeric-form__value {
        position: relative;
        max-width: 568px;
        margin-bottom: 8px;
        &:before {
            display: block;
            position: absolute;
            bottom: 0px;
            height: 2px;
            width: 100%;
            opacity: 0;
            content: '';
            background-color: #448aff;
            z-index: 2;
            will-change: border,opacity,transform;
            transition: .3s;
            transition-timing-function: cubic-bezier(.4,0,.2,1);
            transition-property: border, opacity, transform, -webkit-transform;
            transform: scaleX(.12);
        }
        &:after {
            display: block;
            height: 1px;
            content: '';
            background-color: rgba(0,0,0,.42);
            z-index: 1;
            will-change: border, opacity, transform;
            transition: border .3s cubic-bezier(.4,0,.2,1),opacity .3s cubic-bezier(.4,0,.2,1),transform 0s cubic-bezier(.4,0,.2,1) .3s,-webkit-transform 0s cubic-bezier(.4,0,.2,1) .3s;
        }
    }
    .numeric-form__value-field {
        height: 32px;
        line-height: 32px;
        width: 100%;
    }
    .numericForm__valueFocused {
        &:before {
            opacity: 1;
            transform: scaleX(1);
        }
    }
    .numeric-form__title-area {
        display: flex;
        justify-content: space-between;
        height: 19px;
        max-width: 568px;
    }
    .numeric-form__changed {
        color: #ff5252;
    }
</style>