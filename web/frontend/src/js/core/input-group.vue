<template>
    <div class="input-group">
        <div class="input-group__placeholder" v-if="isInputActive">
            <label v-bind:for="input_id">{{placeholder}}</label>
            <span class="input-group__asterisk" v-if="is_obligatory">*</span>
        </div>
        <input class="input"
            v-model='inputText'
            @input="changeTriggered"
        >
    </div>
</template>

<script>
export default {
    name: 'input-group',
    data: function () {
        return {
            inputText: ''
        }
    },
    props: {
        placeholder: String,
        input_id: String,
        is_obligatory: {
            type: Boolean,
            default: false
        },
        init_text: {
            type:String,
            default: "",
        }
    },
    methods: {
        changeTriggered() {
            this.$emit('input-changed', this.inputText);
        }
    },
    computed: {
        isInputActive() {
            if ( this.inputText.length > 0 ) {
                return false
            }
            return true
        }
    },
    mounted: function () {
        this.inputText = this.init_text;
    }
}
</script>