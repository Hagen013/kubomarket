<template>
    <div class="page-form"
        v-if="!loading"
    >
        <el-header class="bg-green header">
            <h1 class="title">
                Категория: {{category.title}}
            </h1>
            <div class="close" @click="close">
                <i class="el-icon-close"></i>
            </div>
        </el-header>
        <el-main>
            <el-row class="page-form__interaction-area">
                <div class="buttons">
                    <el-button type="primary"
                        :disabled="!hasChanged"
                        @click="saveChanges"
                    >
                        <i class="el-icon-check"></i>
                        Сохранить
                    </el-button>
                    <el-button type="warning"
                        :disabled="!hasChanged"
                        @click="rollBack"
                    >
                        <i class="el-icon-close"></i>
                        Откатить
                    </el-button>
                </div>
            </el-row>
            <el-row class="field">
                <div class="sub-title">
                    meta title
                </div>
                <el-input
                    type="textarea"
                    :rows="2"
                    v-model="category._meta_title">
                </el-input>
            </el-row>
            <el-row class="field">
                <div class="sub-title">
                    meta keywords
                </div>
                <el-input
                    type="textarea"
                    :rows="3"
                    v-model="category._meta_keywords">
                </el-input>
            </el-row>
            <el-row class="field">
                <div class="sub-title">
                    meta description
                </div>
                <el-input
                    type="textarea"
                    :rows="5"
                    v-model="category._meta_description">
                </el-input>
            </el-row>
        </el-main>
    </div>
</template>

<script>
import { Vue } from '../../../vue'
import Element from 'element-ui'
import "element-ui/lib/theme-chalk/index.css";
var equal = require('fast-deep-equal');

Vue.use(Element)

import store from "../../../store";

export default Vue.component("category-node-edit-from", {
    name: "categoryNodeEditForm",
    store,
    data: () => ({
        categoryApiUrl: '/api/cubes/categories/',
        apiResponseRecieved: false,
        loading: true,
        proxyCategory: null,
        category: null,
        hasChanged: false
    }),
    props: [
        "id"
    ],
    created() {
        this.setInitialData();
        this.initializeCategory();
    },
    methods: {
        close() {
            this.$store.commit("showProductPageEditForm/hide");
        },
        setInitialData() {
            this.categoryApiUrl = `${this.categoryApiUrl}${this.id}/`;
        },
        initializeCategory() {
            this.$http.get(this.categoryApiUrl).then(
                response => {
                    this.handleSuccessfulGetResponse(response);
                },
                response => {
                    this.handleFailedGetResponse(response);
                }
            )
        },
        handleSuccessfulGetResponse(response) {
            this.proxyCategory = response.body;
            this.category = JSON.parse(JSON.stringify(this.proxyCategory));
            this.loading = false;
        },
        handleFailedGetResponse(response) {
            this.loading = false;
        },
        saveChanges() {
            this.$http.put(this.categoryApiUrl, this.category).then(
                response => {
                    this.handleSuccessfulUpdateResponse(response);
                },
                response => {
                    this.handleFailedUpdateResponse(response);
                }
            )
        },
        rollBack() {
            this.category = JSON.parse(JSON.stringify(this.proxyCategory));
        },
        checkCategoryChanges() {
            this.hasChanged = !equal(this.category, this.proxyCategory);
        },
        handleSuccessfulUpdateResponse(response) {
            this.proxyCategory = JSON.parse(JSON.stringify(this.category));
            this.hasChanged = false;
        },
        handleFailedUpdateResponse(response) {

        }
    },
    watch: {
        category: {
            handler() {
                if (this.proxyCategory !== null) {
                    this.checkCategoryChanges();
                }
            },
            deep: true
        }
    }
})
</script>

<style lang="scss" scoped>
    .page-form {
        position: fixed;
        top: 0px;
        left: 0px;
        height: 100%;
        width: 100%;
        z-index: 20000;
        background: white;
    }
    .header {
        position: relative;
        color: white;
    }
    .close {
        position: absolute;
        display: flex;
        justify-content: center;
        align-items: center;
        top: 0px;
        right: 0px;
        height: 60px;
        width: 60px;
        font-size: 24px;
        cursor: pointer;
    }
    .bg-green {
        background-color: #00a651;
    }
    .title {
        height: 100%;
        width: 100%;
        font-size: 22px;
        line-height: 60px;
    }
    .field {
        padding: 16px;
    }
    .sub-title {
        font-size: 18px;
        margin-bottom: 8px;
    }
    .buttons {
        display: flex;
        padding-right: 16px;
        justify-content: flex-end;
    }
</style>