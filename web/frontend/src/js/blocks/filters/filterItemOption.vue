<template>
    <li class="filter-item__value">
        <div class="checkbox coloured">
            <label>
                <input type="checkbox"
                    v-model="selected"
                    @change="triggerOptionChange"
                >
                <span class="checkbox-material">
                    <span class="check"></span>
                </span>
                {{title}}
            </label>
        </div>

        <label class="checkbox__wrap"
            v-if="!disabled"
        >
            <input class="checkbox"
                type="checkbox"
                @change="triggerOptionChange"
                v-model="selected"
            >
            <span class="checkbox-custom"></span>
            <span class="checkbox__label">{{title}}</span>
        </label>

        <label class="checkbox__wrap checkbox__wrap_disabled"
            v-else
        >
            <input class="checkbox"
                type="checkbox"
                disabled="disabled"
            >
            <span class="checkbox-custom checkbox-custom_disabled"></span>
            <span class="checkbox__label">{{title}}</span>
        </label>

        <div class="filter-item__value-count">
            {{count}}
        </div>
    </li>
</template>

<script>
export default {
    name: 'filter-item-option',
    data: () => {
        return {
            selected: false,
        }
    },
    props: [
        "title",
        "id",
        "count",
        "active"
    ],
    created() {
        if (this.active === true) {
            this.selected = true;
        }
    },
    computed: {
        disabled() {
            if (this.count === 0) {
                return true
            } else {
                return false
            }
        }
    },
    methods: {
        triggerOptionChange() {
            this.$emit('option-changed', this.selected, this.id);
        }
    }
}
</script>