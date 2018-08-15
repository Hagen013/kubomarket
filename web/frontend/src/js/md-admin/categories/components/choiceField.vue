<template>
    <div class="choice-field">
        <div class="title-area">
            <div class="title">
            {{attribute.name}}
            </div>
            <transition name="fade-fast">
                <div class="choice-field__changed" v-if="hasChanged">
                изменено
                </div>
            </transition>
        </div>
        <div class="value" :class="{ valueFocused: isFocused }">
            <input class="value__field"
                @focus="showDropDown"
                @blur="hideDropDown"
                readonly
                v-model="selectedOption"
            >
            <i class="dropdown__icon">
                <svg height="24" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="M7 10l5 5 5-5z"></path> <path d="M0 0h24v24H0z" fill="none"></path></svg>
            </i>
        </div>
        <transition name='fade-fast'>
        <div class="dropdown" v-if="dropdownIsActive">
            <div class="dropdown__option" @click="changeActiveOption('Не выбрано', -1)">
                Не выбрано
            </div>
            <div class="dropdown__option"
                v-for="(option, index) in attribute.values"
                :key="option.id"
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
        name: 'choice-field',
        data: () => ({
            selectedOption: '',
            isFocused: false,
            dropdownIsActive: false,
            initialValue: '',
        }),
        props: [
            "attribute",
            "selected_values",
            "savingIteraion",
            "rollbackIteration"
        ],
        created() {
            if ( this.selected_values.length > 0 ) {
                this.selectedOption = this.selected_values[0].name;
            } else {
                this.selectedOption = 'Не выбрано';
            }
            this.initialValue = this.selectedOption;
        },
        computed: {
            hasChanged() {
                return this.selectedOption !== this.initialValue;
            }
        },
        methods: {
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
            },
            rollback() {
                this.selectedOption = this.initialValue;
            },
            save() {
                this.initialValue = this.selectedOption;
            }
        },
        watch: {
            savingIteration() {
                this.save();
            },
            rollbackIteration() {
                this.rollback;
            }
        }
    }
</script>

<style lang="scss" scoped>
    input {
        outline: none !important;
        -webkit-box-shadow: none !important;
        box-shadow: none !important;
        border-radius: 0px;
        font-size: 16px;
        border: none;
    }
    .choice-field {
        margin-bottom: 24px;
    }
    .title {
        font-size: 13px;
        color: rgba(0,0,0,.54);
    }
    .value {
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
    .value__field {
        height: 32px;
        line-height: 32px;
        width: 100%;
        cursor: pointer;
    }
    .dropdown__icon {
        position: absolute;
        top: 6px;
        right: 0px;
        svg {
            height: 24px;
            width: 24px;
        }
    }
    .dropdown {
        position: absolute;
        max-height: 280px;
        max-width: 568px;
        overflow: hidden;
        overflow-y: scroll;
        width: 100%;
        top: 80px;
        background: white;
        box-shadow: 0 3px 5px -1px rgba(0,0,0,.2), 0 6px 10px 0 rgba(0,0,0,.14), 0 1px 18px 0 rgba(0,0,0,.12);
        z-index: 1000;
    }
    .dropdown__option {
        padding: 8px 8px 8px 8px;
        cursor: pointer;
        transition-duration: 0.2s;
        transition-property: background;
        &:hover {
            background: #e0e0e0;
        }
    }
    .valueFocused {
        &:before {
            opacity: 1;
            transform: scaleX(1);
        }
    }
    .title-area {
        display: flex;
        justify-content: space-between;
        height: 19px;
        max-width: 568px;
    }
    .choice-field__changed {
        color: #ff5252;
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
