<template>
    <div class="modal search-modal"
        @click.self="close"
    >
        <div class="modal__content search-modal__content">
            <div class="search-modal__search-box">
                <div class="input-box search-modal__input-box">
                    <input class="input search-modal__input"
                        placeholder="Поиск"
                        v-model="searchQuery"
                        v-on:keyup.enter="enterPressed"
                        @input="searchTriggered"
                    >
                    <div class="button_round search-modal__search-button"
                        @click="enterPressed"
                    >
                        <i class="icon icon_search"></i>
                    </div>
                </div>
            </div>
            <ul class="search-modal__search-results">
                <li class="search-modal__result"
                    v-for="(result, key) in resultsStandard"
                >
                    <a class="search-modal__result-link"
                        :href="result['absolute_url']"
                    >
                        {{result['name']}}
                    </a>
                </li>
                <li class="search-modal__result"
                    v-for="(result, key) in resultsAdvanced"
                >
                    <a class="search-modal__result-link"
                        :href="result['absolute_url']"
                    >
                        {{result['name']}}
                    </a>
                </li>
            </ul>
            <div class="button_round search-modal__close"
                @click="close"
            >
                <i class="icon icon_close"></i>
            </div>
        </div>
    </div>
</template>

<script>
import store from '../../store'
import debounce from 'debounce'

export default {
    name: 'search-modal',
    data: function () {
        return {
            searchQuery: "",
            searchApiUrl: '/api/search/?line=',
            resultsStandard: [],
            resultsAdvanced: []
        }
    },
    store,
    computed: {
    },
    methods: {
        searchRedirect() {
            let codePattern = /b-247-.*[0-9].*$/;
            if ( codePattern.exec(this.searchQuery) !== null ) {
                document.location = `/search/by-code/${this.searchQuery}`;
            } else if ( this.searchQuery.length > 0 ) {
                document.location = `/search/${this.searchQuery}`;
            }
        },
        enterPressed() {
            if ( this.searchQuery.length > 2 ) {
                this.searchRedirect();
            }
        },
        searchTriggered: debounce(function () {
            let apiURL = this.searchApiUrl;
            let codePattern = /b-247-.*[0-9].*$/;
            if ( codePattern.exec(this.searchQuery) !== null ) {
                apiURL = '/api/search/by-code/?line=';
            }
            this.$http.get(apiURL + this.searchQuery).then(
                response => {
                    this.handleSuccessfulSearchRequest(response);
                },
                response => {
                    this.handleFailedSearchRequest(response);
                }
            );
        }, 500),
        handleSuccessfulSearchRequest(response) {
            this.resultsStandard = response.body['results_standard'];
            this.resultsAdvanced = response.body['results_advanced'];
        },
        handleFailedSearchRequest(response) {

        },
        close() {
            this.$store.commit("showSearchModal/hide");
        },
    },
}

</script>
