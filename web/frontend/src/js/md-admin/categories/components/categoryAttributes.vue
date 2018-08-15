<template>
    <div class="attributes"
        v-if="apiResponseReceived"
    >
        <div class="attributes__content"
            v-if="!apiResponseError"
        >
            <div class="attributes__list">
                <div class="attribute"
                    v-for="(attribute, index) in attributes"
                    :key="attribute.id"
                >
                    <choice-field
                        v-if="attribute.attribute_type==1"
                        :attribute="attribute"
                        :selected_values="attribute.selected_values"
                        :savingIteration="savingIteration"
                        :rollbackIteration="rollbackIteration"
                        v-on:option-changed="changeAttributeValue"
                    >
                    </choice-field>
                    <multichoice-field
                        v-else-if="attribute.attribute_type==2"
                        :attribute="attribute"
                        :selected_values="attribute.selected_values"
                        v-on:add-active-option="addActiveOption"
                        v-on:remove-active-option="removeActiveOption"
                    >
                    </multichoice-field>
                </div>
            </div>
        </div>
        <div class="attributes__error">
        </div>
    </div>
    <div class="attributes__placeholder"
        v-else
    >
        <md-progress-spinner :md-diameter="100" :md-stroke="10" md-mode="indeterminate">
        </md-progress-spinner>
    </div>
</template>

<script>
    import choiceField from "./choiceField.vue"
    import multichoiceField from "./multichoiceField.vue"
    import numericField from "./numericField.vue"

    export default {
        name: 'categories-attributes',
        data: () => ({
            attributesApiUrl: "/api/cubes/attributes/",
            apiResponseReceived: false,
            apiResponseError: false,
            attributes: [],
            proxyAttributes: []
        }),
        components: {
            "choice-field": choiceField,
            "multichoice-field": multichoiceField,
            "numeric-field": numericField
        },
        props: [
            "category",
            "savingIteration",
            "rollbackIteration"
        ],
        computed: {
        },
        created() {
            this.initialize();
        },
        methods: {
            initialize() {
                this.getAttributes();
            },
            getAttributes() {
                this.$http.get(this.attributesApiUrl).then(
                    response => {
                        this.handleSuccessfulGetAttriubutesResponse(response);
                    },
                    response => {
                        this.handleFailedGetAttributesResponse(response);
                    }
                )
            },
            handleSuccessfulGetAttriubutesResponse(response) {
                this.attributes = response.body;
                for (let i=0; i<this.attributes.length; i++) {
                    this.attributes[i].selected_values = [];
                    for (let y=0; y<this.category.attribute_values.length; y++) {
                        if (this.attributes[i].id === this.category.attribute_values[y].attribute) {
                            this.attributes[i].selected_values.push(this.category.attribute_values[y]);
                        }
                    }
                }
                this.proxyAttributes = JSON.parse(JSON.stringify(this.attributes));
                this.apiResponseError = false;
                this.apiResponseReceived = true;
            },
            handleFailedGetAttributesResponse(response) {
                this.apiResponseError = true;
                this.apiResponseReceived = true;
            },
            changeAttributeValue(attributeId, valuesList, hasChanged) {
                for (let i=0; i<this.attributes.length; i++) {
                    if (this.attributes[i].id===attributeId) {
                        this.attributes[i].selected_values = valuesList;
                        this.$emit("change-option", attributeId, valuesList, hasChanged);
                        break
                    }
                }
            },
            addActiveOption(attributeId, option, hasChanged) {
                for (let i=0; i<this.attributes.length; i++) {
                    if (this.attributes[i].id===attributeId) {
                        this.attributes[i].selected_values.push(option);
                        this.$emit("add-active-option", attributeId, option, hasChanged);
                        break
                    }
                }
            },
            removeActiveOption(attributeId, option, hasChanged) {
                for (let i=0; i<this.attributes.length; i++) {
                    if (this.attributes[i].id==attributeId) {
                        let index = this.attributes[i].selected_values.indexOf(option);
                        this.attributes[i].selected_values.splice(index, 1);
                        this.$emit("remove-active-option", attributeId, option, hasChanged);
                        break
                    }
                }
            }
        },
        watch: {
            savingIteration() {
                this.proxyAttributes = JSON.parse(JSON.stringify(this.attributes));
            },
            rollbackIteration() {
                this.attributes = JSON.parse(JSON.stringify(this.proxyAttributes));
            }
        }
    }
</script>

<style lang="scss" scoped>
    .attributes {
        padding-bottom: 300px;
    }
    .attributes__placeholder {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 400px;
        width: 100%;
    }
    .fade-fast {
        opacity: 1 !important;
        transition: opacity 0.2s
    }
    .fade-fast-enter-active, .fade-fast-leave-active{
        transition: opacity 0.2s
    }
    .fade-fast-enter, .fade-fast-leave-to  {
        opacity: 0
    }
</style>
