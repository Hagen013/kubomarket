<template>
    <div class="search-list">

        <div class="search-list__content">
            <div v-if="showStandard">
                <ul class="search-list__sub-list">
                    <li v-for="(result, key) in results_standard"
                        class="search-list__item"
                    >
                        <a class="search-list__item-link"
                            :href="result['absolute_url']"
                        >
                            {{result['name']}}
                        </a>
                    </li>
                </ul>
                <div class="search-list__content-delimeter">
                </div>
            </div>

            <div v-if="showAdvanced">
                <ul class="search-list__sub-list">
                    <li v-for="(result, key) in results_advanced"
                        class="search-list__item"
                    >
                        <a class="search-list__item-link"
                            :href="result['absolute_url']"
                        >
                            {{result['name']}}
                        </a>
                    </li>
                </ul>
            </div>

        </div>
    </div>
</template>
<script>

export default {
    name: 'search-list',
    data: function() {
        return {
        }
    },
    props: [
        'results_standard',
        'results_advanced'
    ],
    created() {
        console.log('created');
    },
    computed: {
        showStandard() {
            return (this.results_standard.length > 0)
        },
        showAdvanced() {
            return (this.results_advanced.length > 0)
        }
    }
}
</script>
