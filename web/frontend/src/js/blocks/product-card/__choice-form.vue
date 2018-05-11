<template>
    <div class="choice-form">
        <div class="choice-form__title-area">
            <div class="choice-form__title">
            {{attribute.name}}
            </div>
            <transition name="fade-fast">
                <div class="choice-form__changed" v-if="hasChanged">
                изменено
                </div>
            </transition>
        </div>
        <div class="choice-form__value" :class="{ choiceForm__valueFocused: isFocused }">
            <input class="choice-form__value-field"
                @focus="showDropDown"
                @blur="hideDropDown"
                readonly
                v-model="selectedOption"
            >
            <i class="choice-form___dropdown-icon">
                <svg height="24" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="M7 10l5 5 5-5z"></path> <path d="M0 0h24v24H0z" fill="none"></path></svg>
            </i>
        </div>
        <transition name='fade-fast'>
        <div class="choice-form__dropdown" v-if="dropdownIsActive">
            <div class="choice-form__dropdown-option" @click="changeActiveOption('Не выбрано', -1)">
                Не выбрано
            </div>
            <div class="choice-form__dropdown-option"
                v-for="(option, index) in attribute.values"
                @click="changeActiveOption(option.name, index)"
            >
                {{option.name}}
            </div>
        </div>
        </transition>
    </div>
</template>

<script>
    export default {
        name: 'choice-form',
        data: () => ({
            selectedOption: '',
            isFocused: false,
            dropdownIsActive: false,
            initialValue: '',
        }),
        props: [
            'attribute',
            'selected_values',
            'saving_iteration'
        ],
        created: function () {
            if ( this.selected_values.length > 0 ) {
                this.selectedOption = this.selected_values[0].name;
            } else {
                this.selectedOption = 'Не выбрано';
            }
            this.initialValue = this.selectedOption;
        },
        computed: {
            hasChanged() {
                return ( this.initialValue !== this.selectedOption )
            }
        },
        methods: {
            setDefaults() {
                this.initialValue = this.selectedOption;
            },
            showDropDown() {
                this.isFocused = true;
                this.dropdownIsActive = true;
            },
            hideDropDown() {
                this.isFocused = false;
                this.dropdownIsActive = false;
            },
            clearActiveOption() {
                this.selectedOption = 'Не выбрано';
            },
            changeActiveOption(optionName, index) {
                let valuesList = null;
                if ( index !== -1 ) {
                    valuesList = [this.attribute.values[index]];
                } else {
                    valuesList = []
                }
                this.selectedOption = optionName;
                this.$emit('option-changed', this.attribute.id, valuesList, this.hasChanged);
            }
        },
        watch: {
            saving_iteration() {
                this.setDefaults();
            }
        }
    }
</script>

<style lang="scss" scoped>
    .choice-form {
        position: relative;
    }
    .choice-form__select {
        min-width: 200px;
        padding: 8px;
        background: white;
        border: 1px solid #e7eff4;
        cursor: pointer;
    }
    .choice-form__option {
        height: 20px !important;
        padding: 8px !important;
        color: red;
    }
    .choice-form__title {
        font-size: 14px;
        font-family: PFDinDisplayPro-Bold !important;
    }
    .choice-form__value {
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
    .choice-form__value-field {
        height: 32px;
        line-height: 32px;
        width: 100%;
        cursor: pointer;
    }
    .choice-form___dropdown-icon {
        position: absolute;
        top: 6px;
        right: 0px;
        svg {
            height: 24px;
            width: 24px;
        }
    }
    .choice-form__dropdown {
        position: absolute;
        max-height: 280px;
        max-width: 568px;
        overflow: hidden;
        overflow-y: scroll;
        width: 100%;
        top: 64px;
        background: white;
        box-shadow: 0 3px 5px -1px rgba(0,0,0,.2), 0 6px 10px 0 rgba(0,0,0,.14), 0 1px 18px 0 rgba(0,0,0,.12);
        z-index: 1000;
    }
    .choice-form__dropdown-option {
        padding: 8px 8px 8px 8px;
        cursor: pointer;
        transition-duration: 0.2s;
        transition-property: background;
        &:hover {
            background: #e0e0e0;
        }
    }
    .choiceForm__valueFocused {
        &:before {
            opacity: 1;
            transform: scaleX(1);
        }
    }
    .choice-form__title-area {
        display: flex;
        justify-content: space-between;
        height: 19px;
        max-width: 568px;
    }
    .choice-form__changed {
        color: #ff5252;
    }
</style>