<template>
    <div class="multi-choice-form">
        <div class="multi-choice-form__title-area">
            <div class="multi-choice-form__title">
            {{attribute.name}}
            </div>
            <transition name="fade-fast">
                <div class="multi-choice-form__changed" v-if="hasChanged">
                изменено
                </div>
            </transition>
        </div>
        <div class="multi-choice-form__value"
            :class="{ multiChoiceForm__valueFocused: isFocused }"
        >
            <input placeholder="Поиск.." class="multi-choice-form__input"
                v-model="query"
                @focus="showDropdown"
                @blur="hideDropdown"
            >
        </div>
        <transition name='fade-fast'>
        <div class="multi-choice-form__dropdown" v-if="dropdownIsActive">
            <div class="multi-choice-form__dropdown-option" v-for="option of filteredOptions"
                @click="addActiveOption(attribute, option)"
            >
                {{option.name}}
            </div>
        </div>
        </transition>
        <div class="multi-choice-form__active-options">
            <div class="multi-choice-form__active-options-item" v-for="option in selected_values">
                <div class="multi-choice-form__active-option-item-name">{{option.name}}</div>
                <i class="multi-choice-form__delete-option"
                    @click="removeActiveOption(attribute, option)"
                >
                    <svg height="24" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"></path> <path d="M0 0h24v24H0z" fill="none"></path></svg>
                </i>
            </div>
        </div>
    </div>
</template>

<script>
    import fuzzy from 'fuzzysearch'

    export default {
        name: 'multi-choice-form',
        data: () => ({
            dropdownIsActive: false,
            dropdownItems: [],
            query: '',
            isFocused: false,
            addedValues: [],
            removedValues: [],
        }),
        props: [
            'attribute',
            'selected_values',
            'saving_iteration'
        ],
        computed: {
            filteredOptions() {
                return this.dropdownItems.filter(item => this.matchText(item.name))
            },
            hasChanged() {
                return ( (this.addedValues.length !== 0) || (this.removedValues.length) !== 0 )
            }
        },
        methods: {
            setDefaults() {
                this.addedValues = [];
                this.removedValues = [];
            },
            showDropdown() {
                this.isFocused = true;
                this.updateDropdownItems();
                this.dropdownIsActive = true;
            },
            hideDropdown() {
                this.isFocused = false;
                this.dropdownIsActive = false;
            },
            addActiveOption(attribute, option) {
                let index = this.removedValues.indexOf(option.id);
                this.focusLock = true;
                if ( index !== -1 ) {
                    this.removedValues.splice(index, 1);
                } else {
                    this.addedValues.push(option.id);
                }
                this.query = '';
                this.$emit('add-active-option', attribute.id, option, this.hasChanged);
                this.$forceUpdate();
            },
            removeActiveOption(attribute, option) {
                let index = this.addedValues.indexOf(option.id);
                if ( index !== -1 ) {
                    this.addedValues.splice(index, 1);
                } else {
                    this.removedValues.push(option.id);
                }
                this.$emit('remove-active-option', attribute.id, option, this.hasChanged);
                this.$forceUpdate();
            },
            updateDropdownItems() {
                let filtredValues = [];
                let idArray = this.selected_values.map((a) => a.id );
                for ( let i=0; i< this.attribute.values.length; i++ ) {
                    let value = this.attribute.values[i];
                    if ( idArray.indexOf(value.id) == -1 ) {
                        filtredValues.push(value);
                    }
                }
                this.dropdownItems = filtredValues;
            },
            matchText(item) {
                const target = item.toLowerCase();
                const search = this.query.toLowerCase();
                return fuzzy(search, target)
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
    .multi-choice-form {
        position: relative;
    }
    .multi-choice-form__input {
        height: 32px;
        width: 100%;
        line-height: 100%;
    }
    .multi-choice-form__title {
        font-size: 14px;
        font-family: PFDinDisplayPro-Bold !important;
    }
    .multi-choice-form__dropdown {
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
    .multi-choice-form__dropdown-option {
        padding: 8px 8px 8px 8px;
        cursor: pointer;
        transition-duration: 0.2s;
        transition-property: background;
        &:hover {
            background: #e0e0e0;
        }
    }
    .multi-choice-form__active-options {
        display: flex;
        flex-wrap: wrap;
        max-width: 568px;
        padding: 8px 0px 8px 0px;
    }
    .multi-choice-form__active-options-item {
        display: flex;
        align-items: center;
        height: 32px;
        margin-right: 16px;
        margin-bottom: 8px;
        padding: 0px 16px 0px 16px;
        text-align: center;
        border-radius: 32px;
        color: white;
        background: #448aff;
        transition-duration: 0.2s;
        transition-property: background;
        transition-timing-function: cubic-bezier(.25,.8,.25,1);
        cursor: default;
        &:hover {
            background: rgba(0,0,0,.54);
            .multi-choice-form__delete-option {
                background: hsla(0,0%,100%,.87);
            }
            svg {
                fill: rgba(16,16,16,.90);
            }
        }
    }
    .multi-choice-form__delete-option {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 20px;
        width: 20px;
        margin-left: 8px;
        padding: 2px;
        background: rgba(0,0,0,.26);
        border-radius: 16px;
        transition-duration: 0.2s;
        transition-property: opacity, background;
        transition-timing-function: cubic-bezier(.25,.8,.25,1);
        color: white;
        cursor: pointer;
        svg {
            transition-duration: 0.2s;
            transition-property: fill;
            transition-timing-function: cubic-bezier(.25,.8,.25,1);
            fill: rgba(255,255,255,.90);
        }
        &:hover {
            opacity: 0.7;
        }
    }
    .multi-choice-form__value {
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
    .multiChoiceForm__valueFocused {
        &:before {
            opacity: 1;
            transform: scaleX(1);
        }
    }
    .multi-choice-form__title-area {
        display: flex;
        justify-content: space-between;
        height: 19px;
        max-width: 568px;
    }
    .multi-choice-form__changed {
        color: #ff5252;
    }
</style>