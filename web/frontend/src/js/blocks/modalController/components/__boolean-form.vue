<template>
    <div class="boolean-form">
        <div class="boolean-form__title-area">
            <div class="boolean-form__title">
            {{attribute.name}}
            </div>
            <div class="boolean-form__changed" v-if="hasChanged">
            изменено
            </div>
        </div>
        <div class="md-checkbox">
            <input
                type="checkbox"
                name="subscribe"
                value="newsletter"
                :id="attribute.id"
                v-model="innerValue"
                @change="toggle"
            >
            <label :for="attribute.id">Да</label>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'boolean-form',
        data: () => ({
            innerValue: false,
            initialValue: null
        }),
        props: [
            'attribute',
            'selected_values',
            'saving_iteration'
        ],
        created: function () {
            if ( this.selected_values.length > 0 ) {
                this.innerValue = true;
                this.initialValue = true;
            } else {
                this.initialValue = false;
            }
        },
        computed: {
            hasChanged() {
                return ( this.initialValue !== this.innerValue )
            }
        },
        methods: {
            setDefaults() {
                this.initialValue = this.innerValue;
            },
            toggle() {
                let valuesList = [];
                if ( this.innerValue === true ) {
                    valuesList = this.attribute.values;
                }
                this.$emit('toggled', this.attribute.id, valuesList, this.hasChanged);
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
    $md-checkbox-margin: 16px 0;
    $md-checkbox-checked-color: #448aff;
    $md-checkbox-border-color: rgba(0, 0, 0, 0.54);

    $md-checkbox-size: 18px;
    $md-checkbox-padding: 3px;

    $md-checkmark-width: 2px;
    $md-checkmark-color: #fff;

    .boolean-form__title {
        font-size: 14px;
        font-family: PFDinDisplayPro-Bold !important;
    }

.md-checkbox {
    position: relative;
    box-sizing: border-box;
    margin: $md-checkbox-margin;
    padding-top: 3px;

    label {
    cursor: pointer;
    box-sizing: border-box;
    margin-left: 8px;
    &:before, &:after {
        content: "";
        position: absolute;
        left:0;
        top: 0;
    }
    
    &:before {
        width: $md-checkbox-size;
        height: $md-checkbox-size;
        background: #fff;
        border: 2px solid $md-checkbox-border-color;
        border-radius: 2px;
        cursor: pointer;
        transition: background .3s;
    }
    &:after {
    }    
  }
  
    input[type="checkbox"] {
        outline: 0;
        margin-right: $md-checkbox-size - 10px;
        box-sizing: border-box;
    
    &:checked {
       + label:before{
        background: $md-checkbox-checked-color;
        height: 22px;
        width: 22px;
        border:none;
      }
      + label:after {
        
        $md-checkmark-size: $md-checkbox-size - 2*$md-checkbox-padding;

        transform: rotate(-45deg);

        top: ($md-checkbox-size / 2) - ($md-checkmark-size / 4) - $md-checkbox-size/10;
        left: $md-checkbox-padding+2;
        width: $md-checkmark-size;
        height: $md-checkmark-size / 2;
        
        border: $md-checkmark-width solid $md-checkmark-color;
        border-top-style: none;
        border-right-style: none;
      } 
    }
  }
}

    .boolean-form__title-area {
        display: flex;
        justify-content: space-between;
        height: 19px;
        max-width: 568px;
    }
    .boolean-form__changed {
        color: #ff5252;
    }
</style>