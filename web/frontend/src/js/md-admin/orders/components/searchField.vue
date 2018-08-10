<template>
    <div class="search-field">
        <div class="search-field__wrap">
            <div class="search-field__input-box">
                <input
                    placeholder="Добавить"
                    class="search-field__input"
                    v-model="searchQuery"
                    @focus="handleFocus"
                    @input="handleInput"
                    @blur="handleBlur"
                >
                <md-icon class="md-primary">search</md-icon>
            </div>
            <transition name="fade-fast">
            <ul class="search-field__content"
                v-if="showContent"
            >
                <li class="search-field__item"
                    v-for="item in searchResults"
                    :key=item.id
                    @click="selectItem(item)"
                >
                    <div class="search-field__item-img">
                        <img :src="item['image']">
                    </div>
                    <div class="search-field__item-name">
                        {{item.name}}
                    </div>
                    <div class="search-field__hover-overlay">
                    </div>
                </li>
            </ul>
            </transition>
        </div>
    </div>
</template>

<script>
    import debounce from 'debounce'

    export default {
        name: 'search-field',
        data: () => ({
            searchQuery: '',
            focused: false,
            searchApiUrl: '/api/search/?safe=true&line=',
            searchResults: [],
        }),
        computed: {
            showContent() {
                return ( (this.searchQuery.length > 0) && (this.focused) )
            },
            codeMatches() {
                let codePattern = /^[0-9]*$/;
                return ( codePattern.exec(this.searchQuery) !== null ) 
            },
        },
        methods: {
            handleInput() {
                this.searchTriggered();
            },
            handleBlur() {
                this.focused=false;
            },
            handleFocus() {
                this.focused=true;
            },
            searchTriggered: debounce(function () {
                let url = null;
                if (this.codeMatches) {
                    url = `/api/search/by-code/?line=${this.searchQuery}`;
                } else {
                    url = this.searchApiUrl + this.searchQuery;
                }
                this.$http.get(url).then(
                    response => {
                        this.handleSuccessfulSearchResponse(response);
                    },
                    response => {
                        this.handleFailedSearchResponse(response);
                    }
                )
            }, 500),
            handleSuccessfulSearchResponse(response) {
                this.searchResults = response.body['results_standard'];
            },
            handleFailedSearchResponse(response) {
            },
            selectItem(item) {
                this.$emit('item-selected', item);
                this.focused = false;
            }
        },
    }
</script>

<style lang="scss" scoped>
    $primary: #448aff;
    $border: #949494;

    .search-field {
        width: 100%;
        padding: 16px 0px 0px 0px;
    }
    .search-field__wrap {
        position: relative;
        width: 100%;
    }
    .search-field__input-box {
        position: relative;
        margin: 4px 0px 24px 0px;
        .md-icon {
            position: absolute;
            top: 5px;
            right: 8px;
        }
    }
    .search-field__input {
        height: 32px;
        width: 100%;
        padding-left: 12px;
        line-height: 100%;
        font-size: 16px;
        font-family: Roboto,Noto Sans,-apple-system,BlinkMacSystemFont,sans-serif;
        outline: none !important;
        border: 1px solid lighten($primary, 20%);
        transition-duration: .2s;
        transition-property: border;
        transition-timing-function: cubic-bezier;
        &:hover {
            border: 1px solid lighten($primary, 20%);
        }
        &:focus {
            border: 1px solid $primary;
        }
    }
    .search-field__content {
        position: absolute;
        margin: 0px;
        padding: 0px 0px 16px 0px;
        top: 32px;
        width: 100%;
        background: white;
        box-shadow: 0 3px 5px -1px rgba(0,0,0,.2), 0 6px 10px 0 rgba(0,0,0,.14), 0 1px 18px 0 rgba(0,0,0,.12);
        z-index: 1000;
    }
    .search-field__item-img {
        height: 64px;
        width: 64px;
        img {
            height: 100%;
            width: auto;
        }
    }
    .search-field__item-name {
        height: 100%;
        padding: 0px 0px 0px 0px;
        display: flex;
        align-items: center;
        overflow: hidden;
    }
    .search-field__item {
        position: relative;
        display: flex;
        height: 64px;
        width: 100%;
        list-style: none;
        cursor: pointer;
        transition-duration: .2s;
        transition-property: background;
        transition-timing-function: cubic-bezier;
        &:hover {
            .search-field__hover-overlay {
                opacity: 0.1;
            }
        }
    }
    .search-field__hover-overlay {
        position: absolute;
        top: 0px;
        left: 0px;
        height: 100%;
        width: 100%;
        background: black;
        opacity: 0;
        will-change: opacity;
        transition-duration: .2s;
        transition-property: opacity;
        transition-timing-function: cubic-bezier;
    }
</style>