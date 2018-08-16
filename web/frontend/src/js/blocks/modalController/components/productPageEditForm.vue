<template>

    <div class="edit-form edit-form_product">
        <div class="edit-form__title-area">
            <div class="edit-form__title">
            Редактирование товара: {{uuid}}
            </div>
            <div class="edit-form__close" @click="hideEditForm">
                <svg height="32" viewBox="0 0 24 24" width="32" xmlns="http://www.w3.org/2000/svg"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"></path> <path d="M0 0h24v24H0z" fill="none"></path></svg>
            </div>
        </div>
        <div class="edit-form__content-wrap">
            <el-tabs class="edit-form__nav">
                <el-tab-pane label="Основное">

        <div class="edit-form__main">
        <div class="edit-form__controls">
            <button class="edit-form__controls-button edit-form__controls-button-accept"
                :class="{ eidtForm__controlsButton_disabled: !hasChanged }"
                :disabled="!hasChanged"
                @click="saveChanges"
            >
                Принять изменения
            </button>
            <button class="edit-form__controls-button edit-form__controls-button-cancel"
                :class="{ eidtForm__controlsButton_disabled: !hasChanged }"
                :disabled="!hasChanged"
                @click="cancelChanges"
            >
                Отменить
            </button>
        </div>
        <div class="edit-form__content" v-if="apiResponsesRecieved">
            <div class="edit-form__top-content">
                <div class="edit-form__main-info">
                    <div class="edit-form__title-block">
                        <div class="edit-form__headline">
                            Основная информация
                        </div>
                        <div class="edit-form__title-block-button"
                            @click="toggleMainInfo"
                        >
                            <span v-if="mainInfoIsDisplayed">[ СКРЫТЬ ]</span>
                            <span v-if="!mainInfoIsDisplayed">[РАСКРЫТЬ]</span>
                        </div>
                    </div>
                    <div class="edit-form__main-content" v-if="mainInfoIsDisplayed">
                        <div class="field">
                            <div class="field__label">
                                Наименование
                            </div>
                            <div class="field__value">
                                {{name}}
                            </div>
                        </div>
                        <div class="field">
                            <div class="field__label">
                                vendor_code
                            </div>
                            <div class="field__value">
                                {{uuid}}
                            </div>
                        </div>
                        <div class="field">
                            <div class="md-checkbox">
                                <input
                                    type="checkbox"
                                    name="is-in-stock"
                                    id="is-in-stock"
                                    v-model="isInStock"
                                    @change="checkChanges"
                                >
                                <label for="is-in-stock">В наличии</label>
                            </div>
                        </div>
                        <div class="field">
                            <div class="field__label">
                                Цена
                            </div>
                            <div class="field__value">
                                {{price}} рублей
                            </div>
                        </div>
                        <div class="field">
                            <div class="field__label">
                            Slug
                            </div>
                            <div class="field__value">
                                {{slug}}
                            </div>
                        </div>
                    </div>
                    <div class="edit-form__dimensions">
                        <div class="edit-form__title-block">
                            <div class="edit-form__headline">
                                Габариты
                            </div>
                            <div class="edit-form__title-block-button"
                                @click="toggleDimensionsInfo"
                            >
                                <span v-if="dimensionsInfoIsDisplayed">[ СКРЫТЬ ]</span>
                                <span v-if="!dimensionsInfoIsDisplayed">[РАСКРЫТЬ]</span>
                            </div>
                        </div>
                        <div class="edit-form__dimensions-content" v-if="dimensionsInfoIsDisplayed">
                            <div class="edit-form__dimension-info">
                                <field :value="heightValue" label="Высота" :numerical="true"
                                    v-on:value-changed="setHeight"
                                >
                                </field>
                                <field :value="widthValue" label="Ширина" :numerical="true"
                                    v-on:value-changed="setWidth"
                                >
                                </field>
                                <field :value="depthValue" label="Глубина" :numerical="true"
                                    v-on:value-changed="setDepth"
                                >
                                </field>
                            </div>
                            <div class="edit-form__dimension-img-wrap">
                                <img src="/static/img/cubes/cube.jpg">
                                <div class="edit-form__height-label">{{heightValue}} см</div>
                                <div class="edit-form__width-label">{{widthValue}} см</div>
                                <div class="edit-form__depth-label">{{depthValue}} см</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="edit-form__attributes" v-if="attrsValuesApiResponseRecieved">
                <div class="edit-form__title-block">
                    <div class="edit-form__headline">
                        Атрибуты
                    </div>
                </div>
                <div class="edit-form__attr" v-for="(attribute, index) in attributes">
                    <choice-form v-if="attribute.attribute_type==1"
                        :attribute="attribute"
                        :selected_values="attribute.selected_values"
                        :saving_iteration="savingIteration"
                        v-on:option-changed="changeAttributeValue"
                    >
                    </choice-form>
                    <multi-choice-form v-else-if="attribute.attribute_type==2"
                        :attribute="attribute"
                        :selected_values="attribute.selected_values"
                        :saving_iteration="savingIteration"
                        v-on:add-active-option="addActiveOption"
                        v-on:remove-active-option="removeActiveOption"
                    >
                    </multi-choice-form>
                    <numeric-form v-else-if="attribute.attribute_type==3"
                        :attribute="attribute"
                        :selected_values="attribute.selected_values"
                        :saving_iteration="savingIteration"
                        v-on:value-changed="changeAttributeValue"
                    >
                    </numeric-form>
                    <boolean-form v-else-if="attribute.attribute_type==4"
                        :attribute="attribute"
                        :selected_values="attribute.selected_values"
                        :saving_iteration="savingIteration"
                        v-on:toggled="changeAttributeValue"
                    >
                    </boolean-form>
                </div>
            </div>

            <description
                :descriptionText=proxyDescription
                :id=id
                :saving_iteration=savingIteration
                :product_name=name
                v-on:changed=changeDescription
            >
            </description>

        </div>
        <images-gallery
            :id="id"
            :slug="slug"
            :saving_iteration="imagesSavingIteraion"
            v-on:has-changed="processImagesChange"
        >
        </images-gallery>
        </div>
        <edit-modal v-if="showResponseModal"
            :response="serverResponse"
            :url="url"
            v-on:close-modal="showResponseModal=false"
        >
        </edit-modal>


                </el-tab-pane>
                <el-tab-pane label="Видеобзоры">
                    <video-reviews
                        :pk="id"
                    >
                    </video-reviews>
                </el-tab-pane>
            </el-tabs>
        </div>
    </div>

</template>

<script>
    import { Vue } from '../../../vue'
    import multiChoiceForm from './__multi-choice-form.vue'
    import choiceForm from './__choice-form.vue'
    import booleanForm from './__boolean-form.vue'
    import numericForm from './__numeric-form.vue'
    import field from './__field.vue'
    import editModal from './__edit-modal.vue'
    import imagesGallery from './__images-gallery.vue'
    import description from './__description.vue'
    import store from "../../../store"
    import Element from 'element-ui'
    import "element-ui/lib/theme-chalk/index.css"
    import videoReviews from "./videoReviews.vue"
    Vue.use(Element)

    export default {
        name: 'edit-form',
        components: {
            'multi-choice-form': multiChoiceForm,
            'choice-form': choiceForm,
            'boolean-form': booleanForm,
            'numeric-form': numericForm,
            'field': field,
            'edit-modal': editModal,
            'images-gallery': imagesGallery,
            'description': description,
            'video-reviews': videoReviews
        },
        store,
        data: () => ({
            attributes: [],
            values: {},
            productAttributes: null,
            attrs_api_url: '/api/cubes/attributes/',
            product_api_url: '/api/products/',
            attrs_values_api_url: '/api/cubes/values/',
            attrsApiResponseRecieved: false,
            productApiResponseRecieved: false,
            attrsValuesApiResponseRecieved: false,
            connectionError: false,
            heightValue: 0,
            widthValue: 0,
            depthValue: 0,
            mainInfoIsDisplayed: true,
            dimensionsInfoIsDisplayed: true,
            imagesGalleryStuck: false,
            hasChanged: false,
            showResponseModal: false,
            savingIteration: 0,
            serverResponse: null,
            attributesChanged: false,
            imagesChanged: false,
            imagesSavingIteraion: 0,
            originalDescription: "",
            proxyDescription: "",
            isInStockInitial: true,
            isInStock: true,
        }),
        props: [
            'uuid',
            'id',
            'name',
            'price',
            'slug',
            'url',
            'height',
            'width',
            'depth',
            'description',
            'is_in_stock'
        ],
        computed: {
            apiResponsesRecieved() {
                return ( ( this.attrsApiResponseRecieved && this.productApiResponseRecieved ) && this.attrsValuesApiResponseRecieved )
            },
            dimensionsChanged() {
                return (
                    (Number(this.height) != this.heightValue) ||
                    (Number(this.width) != this.widthValue) ||
                    (Number(this.depth) != this.depthValue)
                )
            },
            descriptionChanged() {
                return this.proxyDescription !== this.originalDescription
            },
            availabilityChanged() {
                return (this.isInStockInitial !== this.isInStock)
            }
        },
        created: function () {
            this.product_api_url = `${this.product_api_url}${this.id}/attributes/`;
            this.getAttributesList();
            this.heightValue = Number(this.height);
            this.widthValue = Number(this.width);
            this.depthValue = Number(this.depth);
            this.originalDescription = String(this.description);
            this.proxyDescription = String(this.description);
            if (this.is_in_stock === "False") {
                this.isInStock = false;
                this.isInStockInitial = false;
            }
        },
        methods: {
            hideEditForm() {
                this.$store.commit("showProductPageEditForm/hide");
            },
            setDefaults() {
                this.savingIteration += 1;
                this.checkChanges();
            },
            getAttributesList() {
                this.$http.get(this.attrs_api_url).then(
                    response => {
                        this.attributes = response.body;
                        this.attrsApiResponseRecieved = true;
                        this.getProductAttributes();
                    },
                    response => {
                    }
                )
            },
            getProductAttributes() {
                this.$http.get(this.product_api_url).then(
                    response => {
                        this.productAttributes = response.body.attributes;
                        this.productApiResponseRecieved = true;
                        this.getAttributeValues();
                    },
                    response => {
                    }
                )
            },
            getAttributeValues() {
                this.$http.get(this.attrs_values_api_url).then(
                    response => {
                        this.values = response.body;
                        this.processRecievedValues();
                    },
                    response => {
                    }
                )
            },
            processRecievedValues() {
                for ( let key in this.attributes ) {
                    let id = Number(this.attributes[key].id);
                    this.attributes[key].values = this.values[id];
                    this.attributes[key].hasChanged = false;
                    if ( this.productAttributes[id] != undefined ) {
                        this.attributes[key].selected_values = this.productAttributes[id];
                    } else {
                        this.productAttributes[id] = new Array();
                        this.attributes[key].selected_values = this.productAttributes[id];
                    }
                }
                this.attrsValuesApiResponseRecieved = true;
            },
            addActiveOption(attributeID, option, hasChanged) {
                attributeID = Number(attributeID);
                for ( let i=0; i<this.attributes.length; i++ ) {
                    if ( this.attributes[i].id === attributeID ) {
                        this.attributes[i].selected_values.push(option);
                        this.attributes[i].hasChanged = hasChanged;
                        break
                    }
                }
                this.checkChanges();
                this.$forceUpdate();
            },
            removeActiveOption(attributeID, option, hasChanged) {
                for ( let i=0; i<this.attributes.length; i++ ) {
                    if ( this.attributes[i].id === attributeID ) {
                        let index = this.attributes[i].selected_values.indexOf(option);
                        if ( index > -1 ) {
                            this.attributes[i].selected_values.splice(index, 1);
                            this.attributes[i].hasChanged = hasChanged;
                            break
                        }
                    }
                }
                this.checkChanges();
                this.$forceUpdate();
            },
            changeAttributeValue(attributeID, valuesList, hasChanged) {
                for ( let i=0; i<this.attributes.length; i++ ) {
                    if ( this.attributes[i].id === attributeID ) {
                        this.attributes[i].selected_values = valuesList;
                        this.attributes[i].hasChanged = hasChanged;
                        break
                    }
                }
                this.checkChanges();
            },
            setHeight(value) {
                this.heightValue = value;
            },
            setWidth(value) {
                this.widthValue = value;
            },
            setDepth(value) {
                this.depthValue = value;
            },
            toggleMainInfo() {
                this.mainInfoIsDisplayed = !this.mainInfoIsDisplayed;
            },
            toggleDimensionsInfo() {
                this.dimensionsInfoIsDisplayed = !this.dimensionsInfoIsDisplayed;
            },
            checkChanges() {
                this.attributesChanged = this.attributes.some(function (currentValue, index, array) {
                    return currentValue.hasChanged
                })
                this.hasChanged = (this.attributesChanged || 
                                   this.dimensionsChanged ||
                                   this.descriptionChanged || 
                                   this.imagesChanged ||
                                   this.availabilityChanged
                                   );
            },
            saveChanges() {
                if (this.attributesChanged ||
                    this.dimensionsChanged ||
                    this.descriptionChanged ||
                    this.availabilityChanged) {
                    this.saveProductChanges();
                }
                if (this.imagesChanged) {
                    this.imagesSavingIteraion += 1;
                }
            },
            saveProductChanges() {
                let attributes = this.attributes.map((currentAttribute, index, array) => {
                    return {
                        "attribute_type": currentAttribute.attribute_type,
                        "id": currentAttribute.id,
                        "key": currentAttribute.key,
                        "name": currentAttribute.name,
                        "unit": currentAttribute.unit,
                        "selected_values": currentAttribute.selected_values,
                    }
                })
                let data = {
                    'attributes': attributes,
                    'height': this.heightValue,
                    'width': this.widthValue,
                    'depth': this.depthValue,
                    'is_in_stock': this.isInStock,
                    'description': this.proxyDescription
                }
                this.$http.put(this.product_api_url, data).then(
                    response => {
                        this.setDefaults();
                        this.hasChanged = false;
                        this.isInStockInitial = Boolean(this.isInStock);
                        this.serverResponse = response;
                        this.showResponseModal = true;
                    },
                    response => {
                    }
                )
            },
            saveImagesChanges() {

            },
            processImagesChange(value) {
                this.imagesChanged = value;
                this.checkChanges();
            },
            cancelChanges() {

            },
            changeDescription(payload) {
                this.proxyDescription = payload;
                this.checkChanges();
            }
        },
        watch: {
            heightValue() {
                this.checkChanges();
            },
            widthValue() {
                this.checkChanges();
            },
            depthValue() {
                this.checkChanges();
            },
        }
    }
</script>

<style lang="scss" scoped>
    .edit-form {
        position: absolute;
        top: 0px;
        width: 0px;
        height: 100%;
        width: 100%;
        min-width: 1140px;
        z-index: 99000;
        background: white;
    }
    .edit-form__title-area {
        position: relative;
        display: flex;
        justify-content: space-between;
        height: 64px;
        padding: 0px 16px 0px 16px;
        line-height: 64px;
        color: white;
        background: #448aff;
        font-size: 24px;
        box-shadow: 0 2px 4px -1px rgba(0,0,0,.2), 0 4px 5px 0 rgba(0,0,0,.14), 0 1px 10px 0 rgba(0,0,0,.12);
        z-index: 2000;
    }
    .edit-form__close {
        position: absolute;
        display: flex;
        align-items: center;
        justify-content: center;
        top: 0px;
        right: 0px;
        height: 64px;
        width: 64px;
        background: darken(#448aff, 5);
        cursor: pointer;
        transition: .2s;
        &:hover {
            background: darken(#448aff, 10);
        }
        svg {
            fill: rgba(255,255,255,.90);
        }
    }
    .edit-form__content-wrap {
        padding: 16px;
    }
    .edit-form__content {
        position: relative;
        padding: 32px 0px 124px 0px;
        width: 50%;
        background: white;
    }
    .edit-form__attributes {
        max-width: 852px;
        padding: 0px 16px 16px 16px;
    }
    .field {
        margin: 4px 0px 24px 0px;
        padding: 16px 0px 0px 0px;
    }
    .field__label {
        color: rgba(0,0,0,.54);
        font-size: 12px;
    }
    .field__value {
        height: 32px;
        line-height: 32px;
        color: rgba(0,0,0,.87);
        &:after {
            display: block;
            height: 1px;
            content: '';
            background-color: rgba(0,0,0,.42);
        }
    }
    .edit-form__top-content {
        display: flex;
    }
    .edit-form__main-info {
        min-width: 600px;
        padding: 0px 8px 0px 0px;
    }
    .edit-form__attr {
        padding: 16px 0px 16px 0px;
    }
    .edit-form__dimensions-content {
        display: flex;
        flex-flow: row wrap;
    }
    .edit-form__title-block {
        position: relative;
        display: flex;
        width: 100%;
        padding: 16px 0px 24px 0px;
        justify-content: space-between;
    }
    .edit-form__headline {
        font-size: 22px;
        font-family: PFDinDisplayPro-Bold !important;
    }
    .edit-form__dimension {
        margin: 4px 0px 24px 0px;
        padding: 16px 0px 0px 0px;
    }
    .edit-form__dimenstion-title {
        color: rgba(0,0,0,.54);
        font-size: 12px;
    }
    .edit-form__dimension-value {
        &:after {
            display: block;
            height: 1px;
            content: '';
            background-color: rgba(0,0,0,.42);
        }
    }
    .edit-form__dimension-input {
        height: 32px;
        line-height: 32px;
    }
    .edit-form__dimension-img-wrap {
        position: relative;
        height: 400px;
        width: 399px;
        padding: 16px;
        text-align: center;
        img {
            height: 100%;
            width: auto;
        }
    }
    .edit-form__height-label {
        position: absolute;
        top: 162px;
        left: 46px;
    }
    .edit-form__width-label {
        position: absolute;
        bottom: 32px;
        right: 122px;
    }
    .edit-form__depth-label {
        position: absolute;
        bottom: 42px;
        left: 98px;
    }
    .edit-form__title-block-button {
        color: grey;
        cursor: pointer;
        padding-top: 6px;
        transition-duration: 0.2s;
        transition-property: color;
        &:hover {
            color: #ff5252;
        }
    }
    .edit-form__controls {
        display: flex;
        position: fixed;
        bottom: 64px;
        right: 64px;
        z-index: 10000;
    }
    .edit-form__controls-button {
        height: 40px;
        padding: 0px 8px 0px 8px;
        line-height: 40px;
        color: white;
        font-size: 14px;
        cursor: pointer;
        border-radius: 3px;
        transition-duration: 0.2s;
        transition-property: background, box-shadow;
        transition-timing-function: cubic-bezier(.4,0,.2,1);
        box-shadow: 0 3px 1px -2px rgba(0,0,0,.2), 0 2px 2px 0 rgba(0,0,0,.14), 0 1px 5px 0 rgba(0,0,0,.12);
        &:hover {
            box-shadow: 0 5px 5px -3px rgba(0,0,0,.2), 0 8px 10px 1px rgba(0,0,0,.14), 0 3px 14px 2px rgba(0,0,0,.12);
        }
    }
    .edit-form__controls-button-accept {
        background: #448aff;
        margin-right: 8px;
        &:hover {
            background: lighten(#448aff, 5);
        }
    }
    .edit-form__controls-button-cancel {
        background: #ff5252;
        &:hover {
            background: lighten(#ff5252, 5);
        }
    }
    .eidtForm__controlsButton_disabled {
        color: #212121;
        background: #F5F5F5;
        cursor: default;
        &:hover {
            box-shadow: 0 3px 1px -2px rgba(0,0,0,.2), 0 2px 2px 0 rgba(0,0,0,.14), 0 1px 5px 0 rgba(0,0,0,.12) !important;
            background: #F5F5F5;
        }
    }
    .edit-form__main {
        display: flex;
        flex-direction: row;
        background: white;
    }

    $md-checkbox-margin: 16px 0;
    $md-checkbox-checked-color: #448aff;
    $md-checkbox-border-color: rgba(0, 0, 0, 0.54);

    $md-checkbox-size: 18px;
    $md-checkbox-padding: 3px;

    $md-checkmark-width: 2px;
    $md-checkmark-color: #fff;

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

    label {
        user-select: none;
    }

</style>