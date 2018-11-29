<template>
    <div class="filter-item">
        <div class="filter-item__btn"
            @click="showDropdown"
        >
            <slot>
            </slot>
            <div class="filter-item__active-count"
                v-if="activeOptionsCount > 0"
            >
                {{activeOptionsCount}}
            </div>
        </div>

        <div class="filter-item__dropdown"
            v-if="displayDropdown"
            @click.self="hideDropDown"
            :style="{ left: dropdownOffset + 'px' }"
        >
            <div class="filter-item__dropdown-content"
                v-if="apiResponseReceived"
            >
                <div class="filter-item__search-box"
                    v-if="showSearchInput"
                >
                    <input type="text"
                        class="filter-item__search-input"
                        placeholder="Поиск"
                        v-model="searchQuery"
                    >
                    <i class="filter-item__search-icon icon icon_search"></i>
                </div>

                <ul class="filter-item__values-list green_scrollbar"
                    :class="{ filterItem__valuesList_scrollable : scrollable }"
                    v-if="!displayPlaceholder"
                >
                    <filter-item-option v-for="option in sortedOptions"
                        :title="option.name"
                        :id="option.id"
                        :key="option.id"
                        :count="option.count"
                        :active="option.active"
                        v-on:option-changed="handleOptionsChange"
                    >
                    </filter-item-option>
                </ul>

                <div class="filter-item__response-placeholder"
                    v-else
                >
                    <div class="filter-item__loader icon icon_rolling">
                    </div>
                </div>

                <div class="filter-item__controls"
                    v-if="!displayPlaceholder"
                >
                    <div class="filter-item__submit bold"
                        @click="submit"
                        :class="{ 'filter-item__submit_half' : activeOptionsCount > 0 }"
                    >
                        ПРИМЕНИТЬ
                    </div>
                    <div class="filter-item__clear bold"
                        @click="clear"
                        v-if="activeOptionsCount > 0"
                    >
                        СБРОСИТЬ
                    </div>
                </div>

            </div>
        </div>

    </div>
</template>

<script>
import filterItemOption from './filterItemOption.vue'

import updateQueryString from '../../../core/updateQueryString'
import getParameterByName from '../../../core/getParameterByName'
import removeQueryParameter from '../../../core/removeQueryParameter'

import fuzzy from 'fuzzysearch'


export default {
    name: 'filter-item',
    components: {
        "filter-item-option": filterItemOption
    },
    data: () => ({
        apiUrl: '/api/search/facetes/',
        apiResponseReceived: false,
        displayDropdown: false,
        defaultOptions: [],
        options: [],
        hasChanged: false,
        searchQuery: '',
        showSearchInput: false,
        primarySortedIds: [],
        displayPlaceholder: true
    }),
    props: [
        'title',
        'pk',
        'slug',
        'values'
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
            if (this.apiResponseReceived === false) {
                return false
            } else {
                if ( JSON.stringify(this.defaultOptions) !== JSON.stringify(this.options) ) {
                    return true
                } else {
                    return false
                }
            }
        },
        showContent() {
            return (this.apiResponseReceived && !this.displayPlaceholder)
        },
        sortedOptions() {
            let sortedOptions = []
            if (!this.apiResponseReceived) {
                return sortedOptions
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
                sortedOptions = primaryOptions.concat(secondaryOptions);
                sortedOptions = sortedOptions.filter(
                    item => this.matchText(item.name)
                )
            }
            return sortedOptions
        },
        activeOptionsCount() {
            return this.options.filter(option => option.active == true).length
        },
        scrollable() {
            return this.sortedOptions.length > 0;
        },
        dropdownOffset() {
            if (window.innerWidth < 340) {
                return 0
            }
            let el = this.$el.parentNode;
            let parent = el.parentNode;
            let offsetDiff = el.offsetLeft - parent.offsetLeft;
            let offset = parent.offsetWidth - (offsetDiff + 320);
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
                    return Number(currentValue)
                })
                for (let i=0; i<parsedValues.length; i++) {
                    let value = parsedValues[i];
                    let payload = {
                        "key": this.slug,
                        "value": value
                    }
                    this.$store.commit("facetes/addActiveOption", payload);
                }
            }

            if ( (this.activeFacetesProxy[this.slug] !== undefined) && (this.activeFacetesProxy[this.slug].length > 0) ) {
                this.primarySortedIds = [];
                for (let i=0; i<this.options.length; i++) {
                    let optionId = this.options[i]['id'];
                    let index = this.activeFacetesProxy[this.slug].indexOf(optionId);
                    if (index !== -1) {
                        this.options[i]['active'] = true;
                        this.primarySortedIds.push(this.options[i].id);
                    }
                }
            }
        },
        hideDropDown() {
            this.displayDropdown = false;
            if (this.hasChanged) {
                this.filtersRedirect()
            }
            this.searchQuery = '';
            this.apiResponseReceived = false;
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

            if (this.options.length > 0) {
                this.showSearchInput = true;
            }
        },
        handleSuccessfulResponse(response) {
            let buckets = response.body['aggregations']['facet']['buckets'];
            let mapping = [];
            for (let i=0; i<buckets.length; i++) {
                let key = buckets[i]['key'];
                let value = buckets[i]['doc_count'];
                mapping[key] = value;
            }
            for (let i=0; i<this.options.length; i++) {
                let key = this.options[i]['id'];
                let value = mapping[key];
                if (value === undefined) {
                    value = 0;
                }
                this.options[i]['count'] = value;
                if (key === 93) {
                    console.log(value);
                    console.log(this.options[i]['count']);
                }
            }
            this.defaultOptions = this.options.slice();
            this.displayPlaceholder = false;
            this.apiResponseReceived = true;
            for (let i=0; i<this.options.length; i++) {
                let key = this.options[i]['id'];
                if (key === 93) {
                    console.log(this.options[i]['count']);
                }
            }
        },
        handleFailedResponse(response) {
            this.apiResponseReceived = true;
            this.displayPlaceholder = true;
        },
        handleOptionsChange(option, pk) {
            let payload = {
                "key": this.slug,
                "value": pk
            };
            this.hasChanged = true;
            for (let i=0; i<this.options.length; i++) {
                if (pk === this.options[i]['id']) {
                    this.options[i]['active'] = option;
                }
            }
            if (option === true) {
                this.$store.commit('facetes/addActiveOption', payload);
            } else {
                this.$store.commit('facetes/removeActiveOption', payload);
            }
        },
        submit() {
            if (this.hasChanged) {
                this.filtersRedirect();
            } else {
                this.displayDropdown = false;
            }
        },
        clear() {
           let payload = {"key": this.slug};
           this.$store.commit("facetes/clearField", payload);
           for (let i=0; i<this.options.length; i++) {
               this.options[i].active = false;
           }
           this.filtersRedirect();
        },
        filtersRedirect() {
            let queryString = window.location.search;

            for (let key in this.removedFacetesProxy) {
                queryString = removeQueryParameter(queryString, key);
            }

            for (let key in this.activeFacetesProxy) {
                let values = [];
                let self = this;
                if (this.baseFacetesProxy[key] !== undefined) {
                    values = this.activeFacetesProxy[key].filter(function(value) {
                        return self.baseFacetesProxy[key].indexOf(value) === -1
                    })
                    values = values.join(',')
                } else {
                    values = this.activeFacetesProxy[key].join(',');
                }
                if (values.length > 0) {
                    queryString = updateQueryString(queryString, key, values)
                }
            }

            for (let key in this.baseRemovedFacetesProxy) {
                let values = this.baseRemovedFacetesProxy[key].join(',');
                let queryKey = '-' + key;
                queryString = updateQueryString(queryString, queryKey, values);
            }
            window.location.search = queryString;
        },
        matchText(item) {
            const target = item.toLowerCase();
            const search = this.searchQuery.toLowerCase();
            return fuzzy(search, target)
        }
    }
}
</script>
