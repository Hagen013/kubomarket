<template>
    <div class="filter-item">
        <div class="filter-item__btn" @click="showDropdown">
            <slot>
            </slot>
            <div class="filter-item__active-count" v-if="activeOptionsCount > 0">
                {{activeOptionsCount}}
            </div>
        </div>

        <div class="filter-item__dropdown" v-if="displayDropdown"
            @click.self="hideDropdown"
            :style="{ left:  dropdownOffset + 'px' }"
        >

        <div class="filter-item__dropdown-content"
            v-if="apiResponseRecieved"
        >

            <div class="filter-item__search-box" v-if="showSearchInput">
                <input type="text"
                    class="filter-item__search-input"
                    placeholder="Поиск"
                    v-model="searchQuery"
                >
                <i class="filter-item__search-icon icon icon_search-blue"></i>
            </div>

            <ul class="filter-item__values-list" 
                :class="{ filterItem__valuesList_scrollable : scrollable }"
            >
                <filter-item-option v-for="option in sortedOptions"
                    :title="option.name"
                    :id="option.id"
                    :key="option.id"
                    :count="option.count"
                    :active="option.active"
                    v-on:option-changed="handleOptionChange"
                >
                </filter-item-option>
            </ul>

            <div class="filter-item__controls" v-if="activeOptionsCount > 0">
                <div class="filter-item__submit filter-item__submit_half" @click="submit">
                    ПРИМЕНИТЬ
                </div>
                <div class="filter-item__clear" @click="clear">
                    СБРОСИТЬ
                </div>
            </div>

            <div class="filter-item__controls" v-else>
                <div class="filter-item__submit" @click="submit">
                    ПРИМЕНИТЬ
                </div>
            </div>

        </div>

        <div class="filter-item__response-placeholder"
            v-else
        >
            <div class="filter-item__loader icon icon_rolling">
            </div>
        </div>

        </div>
    </div>
</template>

<script>
import filterItemOption from "./filterItemOption.vue"

import updateQueryString from '../../core/updateQueryString'
import getParameterByName from '../../core/getParameterByName'
import removeQueryParameter from '../../core/removeQueryParameter'

import fuzzy from 'fuzzysearch'


export default {
    name: 'filter-item',
    data: () => {
        return {
            apiUrl: '/api/search/facetes/',
            apiResponseRecieved: false,
            displayDropdown: false,
            defaultOptions: [],
            options: [],
            hasChanged: false,
            searchQuery: "",
            showSearchInput: false,
            primarySortedIds: []
        }
    },
    components: {
        "filter-item-option": filterItemOption
    },
    props: [
        "title",
        "pk",
        "slug",
        "values"
    ],
    computed: {
        activeFacetesProxy() {
            return this.$store.state.facetes.active
        },
        baseFacetesProxy() {
            return this.$store.state.facetes.base
        },
        removedFacetesProxy() {
            return this.$store.state.facetes.removed
        },
        baseRemovedFacetesProxy() {
            return this.$store.state.facetes.removedBase
        },
        optionsChanged() {
            if (this.apiResponseRecieved === false) {
                return false
            } else {
                if ( JSON.stringify(this.defaultOptions) !== JSON.stringify(this.options) ) {
                    return true
                } else {
                    return false
                }
            }
        },
        sortedOptions() {
            if (!this.apiResponseRecieved) {
                return []
            } else {
                let self = this;
                let primaryOptions = this.options.filter(function(item) {
                    return self.primarySortedIds.indexOf(item.id) !== -1
                }).sort(function(a,b) {
                    return b.count - a.count
                });
                let secondaryOptions = this.options.filter(function(item) {
                    return self.primarySortedIds.indexOf(item.id) === -1
                }).sort(
                    (a, b) => b.count - a.count
                )
                let options = primaryOptions.concat(secondaryOptions);
                options = options.filter(
                    item => this.matchText(item.name)
                )
                return options
            }
        },
        activeOptionsCount() {
            return this.options.filter(option => option.active === true).length;
        },
        scrollable() {
            return this.sortedOptions.length > 8;
        },
        dropdownOffset() {
            let el = this.$el.parentNode;
            let parent = el.parentNode;
            let offsetDiff = el.offsetLeft - parent.offsetLeft;
            let offset = parent.offsetWidth - (offsetDiff + 300);
            if (offset < 0) {
                return offset
            }
            return 0
        }
    },
    created() {
        this.initialize();
    },
    methods: {
        initialize() {
            let parsedValues = getParameterByName(this.slug);

            this.options = JSON.parse(this.values);
            
            if (parsedValues !== null) {
                parsedValues = parsedValues.split(',');
                parsedValues = parsedValues.map(function(currentValue, index, array) {
                    return Number(currentValue);
                });
                for (let i=0; i<parsedValues.length; i++) {
                    let value = parsedValues[i];
                    let payload = {
                        "key": this.slug,
                        "value": value
                    }
                    this.$store.commit("facetes/addActiveOption", payload);
                }
            }

            if ( (this.activeFacetesProxy[this.slug] !== undefined) && (this.activeFacetesProxy[this.slug].length > 0)) {
                this.primarySortedIds = [];
                for (let i=0; i<this.options.length; i++) {
                    let optionId = this.options[i]["id"];
                    let index = this.activeFacetesProxy[this.slug].indexOf(optionId);
                    if (index !== -1) {
                        this.options[i]["active"] = true;
                        this.primarySortedIds.push(this.options[i].id);
                    }
                }
            }

        },
        hideDropdown() {
            this.displayDropdown = false;
            if (this.hasChanged) {
                this.filtersRedirect();
            }
            this.searchQuery = "";
            this.apiResponseRecieved = false;
        },
        showDropdown() {
            this.displayDropdown = true;
            this.getCounts();
        },
        getCounts() {
            let params = {slug: this.slug};
            for (let key in this.activeFacetesProxy) {
                params[key] = this.activeFacetesProxy[key].join(',');
            }

            this.$http.get(this.apiUrl, {params: params}).then(
                response => {
                    this.handleSuccessfulResponse(response);
                },
                response => {
                    this.handleFailedResponse(response);
                }
            )

            if (this.options.length > 8) {
                this.showSearchInput = true
            }

        },
        handleSuccessfulResponse(response) {
            let buckets = response.body['aggregations']['facet']['buckets'];
            let mapping = {};
            for (let i=0; i<buckets.length; i++) {
                let key = buckets[i]["key"];
                let value = buckets[i]["doc_count"];
                mapping[key] = value;
            }
            for (let i=0; i<this.options.length; i++) {
                let key = (this.options[i]['id']);
                let value = mapping[key];
                if (value === undefined) {
                    value = 0;
                }
                this.options[i]['count'] = value;
            }
            this.defaultOptions = this.options.slice();
            this.apiResponseRecieved = true;
        },
        handleFailedResponse(response) {
            console.log("request failed");
        },
        handleOptionChange(option, pk) {
            let payload = {
                "key": this.slug,
                "value": pk
            };
            this.hasChanged = true;
            for (let i=0; i<this.options.length; i++) {
                if (pk === this.options[i]["id"]) {
                    this.options[i]["active"] = option;
                }
            }
            if (option === true) {
                this.$store.commit("facetes/addActiveOption", payload);
            } else {
                this.$store.commit("facetes/removeActiveOption", payload);
            }
        },
        submit() {
            if (this.hasChanged) {
                this.filtersRedirect();
            }
        },
        clear() {
            let payload = {"key": this.slug}
            this.$store.commit("facetes/clearField", payload);
            for (let i=0; i<this.options.length; i++) {
                this.options[i].active = false;
            }
            this.filtersRedirect();
        },
        filtersRedirect() {
            let querystring = window.location.search;

            for (let key in this.removedFacetesProxy) {
                querystring = removeQueryParameter(querystring, key);
            }

            for (let key in this.activeFacetesProxy) {
                let values = [];
                let self = this;
                if (this.baseFacetesProxy[key] !== undefined) {
                    values = this.activeFacetesProxy[key].filter(function(value) {
                        return self.baseFacetesProxy[key].indexOf(value) === -1
                    })
                    values = values.join(',');
                } else {
                    values = this.activeFacetesProxy[key].join(',');
                }
                if (values.length > 0) {
                    querystring = updateQueryString(querystring, key, values);
                }
            }

            for (let key in this.baseRemovedFacetesProxy) {
                let values = this.baseRemovedFacetesProxy[key].join(',');
                let queryKey = "-" + key;
                querystring = updateQueryString(querystring, queryKey, values);
            }
            window.location.search = querystring;
        },
        matchText(item) {
            const target = item.toLowerCase();
            const search = this.searchQuery.toLowerCase();
            return fuzzy(search, target)
        }
    }
}
</script>
