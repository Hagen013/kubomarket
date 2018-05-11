<template>
    <div class="category-form">
        <div class="md-layout top-nav">
            <div class="md-layout-item">
                <md-button class="md-primary"
                    @click="categoriesListRedirect"
                >
                    <md-icon>keyboard_backspace</md-icon>
                    К СПИСКУ
                </md-button>
            </div>
            <div class="md-layout-item">
            </div>
            <div class="md-layout-item">
                <div class="controls">
                    <md-button class="md-accent md-raised">
                        <md-icon>
                        settings_backup_restore
                        </md-icon>
                        ОТМЕНИТЬ
                    </md-button>
                    <md-button class="md-primary md-raised">
                        СОХРАНИТЬ
                        <md-icon>
                        done
                        </md-icon>
                    </md-button>
                </div>
            </div>
        </div>
        <div class="md-layout">
            <div class="md-layout-item first-column md-size-30">
                <md-card>
                    <md-card-header>
                        <div class="md-title">
                        Основная информация
                        </div>
                    </md-card-header>
                    <md-card-content>
                        <md-field>
                            <label>Name</label>
                            <md-input v-model="category.name"></md-input>
                        </md-field>
                        <md-field>
                            <label>Title</label>
                            <md-input v-model="category.title"></md-input>
                        </md-field>
                        <md-field>
                            <label>Meta title</label>
                            <md-input v-model="category._meta_title"></md-input>
                        </md-field>
                        <md-field>
                            <label>Meta keywords</label>
                            <md-textarea v-model="category._meta_keywords"></md-textarea>
                        </md-field>
                        <md-field>
                            <label>Meta description</label>
                            <md-textarea v-model="category._meta_description"></md-textarea>
                        </md-field>
                    </md-card-content>
                </md-card>
            </div>
            <div class="md-layout-item second-column">
                <md-card>
                    <md-card-header>
                        <div class="md-title">
                            Атрибуты
                        </div>
                    </md-card-header>
                    <md-card-content>
                    </md-card-content>
                </md-card>
            </div>
        </div>
        <md-snackbar :md-active.sync="connectionFailed" md-persistent>
        <span>Во время соединения с сервером произошла ошибка!</span>
        <md-button class="md-primary" @click="connectionFailed = false">ЗАКРЫТЬ</md-button>
        </md-snackbar>
    </div>
</template>

<script>
    export default {
        name: 'category-form',
        data: () => ({
            attributesApiURL: '/api/attributes/',
            categoryApiURL: '/api/category/',
            componentTitle: null,
            categoryId: null,
            connectionFailed: false,
            category: {
                id: null,
                name: '',
                title: '',
                parent: null,
                _meta_title: '',
                _meta_keywords: '',
                _meta_description: '',
                url: '',
                absolute_url: '',
                level: 0,
                depth: 0,
                scoring: 0,
                search_scoring: 0,
            },
            attributes: null
        }),
        created() {
            this.categoryId = this.$route.params.id;
            if ( this.categoryId !== undefined ) {
                this.componentTitle = `Редактирование категории ${this.categoryId}`;
                this.categoryApiURL += String(categoryId);
                this.getCategory();
            } else {
                this.componentTitle = 'Создание новой категории';
            }
            this.$store.commit('admin/changeAppTitle', this.componentTitle);
            this.getAttributes();
        },
        computed: {
        },
        methods: {
            categoriesListRedirect() {
                this.$router.replace({path: '/categories'});
            },
            getCategory() {
                this.$http.get(this.categoryApiURL).thne(
                    response => {
                        this.handleSuccessfulCategoryResponse(response);                        
                    },
                    response => {
                        this.handleFailedCategoryResponse(response);
                    }
                )
            },
            getAttributes() {
                this.$http.get(this.attributesApiURL).then(
                    response => {
                        this.handleSuccessfulAttributesResponse(response);
                    },
                    response => {
                        this.handleFailedAttributesResponse(response);
                    }
                )
            },
            handleSuccessfulAttributesResponse(response) {
                this.attributes = response.body;
            },
            handleFailedAttributesResponse(response) {
                this.connectionFailed = true;
            },
            handleSuccessfulCategoryResponse(response) {
                this.category = response.body;
            },
            handleFailedCategoryResponse(response) {
                this.connectionFailed = true;
            }
        }
    }
</script>

<style lang="scss" scoped>
    .controls {
        display: flex;
        width: 100%;
        justify-content: flex-end;
    }
    .top-nav {
        padding: 0px 0px 16px 0px;
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