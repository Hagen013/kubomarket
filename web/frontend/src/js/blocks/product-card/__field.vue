<template>
    <div class="field">
        <div class="field__label">
            {{label}}
        </div>
        <div class="field__value" :class="{ field__value_focused: isFocused }">
            <input class="field__input" v-if="numerical"
                v-model="innerValue"
                @focus="isFocused = true"
                @blur="isFocused = false"
                @input="setValueToNumber"
                onkeypress='return event.charCode >= 48 && event.charCode <= 57'
            >
            <input class="field__input" v-else
                v-model="innerValue"
                @focus="isFocused = true"
                @blur="isFocused = false"
                @input="checkInput"
            >
        </div>
    </div>
</template>

<script>
    export default {
        name: 'edit-form',
        data: () => ({
            innerValue: null,
            isFocused: false,
        }),
        props: {
            value: {

            },
            label: {
                type: String
            },
            numerical: {
                type: Boolean,
                default: false
            }
        },
        created: function () {
            this.innerValue = this.value;
            if ( ( this.numerical ) && ( isNaN(this.innerValue) ) ) {
                this.innerValue = 0;
            }
            if ( typeof(this.innerValue == Number) ) {
                this.numerical = true;
            }
        },
        methods: {
            setValueToNumber() {
                this.innerValue = parseInt(this.innerValue);
                if ( isNaN(this.innerValue) ) {
                    this.innerValue = 0;
                }
                this.$emit('value-changed', this.innerValue);
            },
            checkInput() {
                this.$emit('value-changed', this.innerValue);
            }
        }
    }
</script>

<style lang="scss" scoped>
    .field {
        margin: 4px 0px 24px 0px;
        padding: 16px 0px 0px 0px;
    }
    .field__label {
        font-size: 12px;
        color: rgba(0,0,0,.54);
    }
    .field__value {
        position: relative;
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
    .field__input {
        height: 32px;
        line-height: 100%;
    }
    .field__value_focused {
        &:before {
            opacity: 1;
            transform: scaleX(1);
        }
    }
</style>