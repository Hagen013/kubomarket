<template>
    <div class="photo-gallery__nav-item-wrap" 
        @click="triggerImageChange"
        v-bind:class="{ photoGallery__navItemWrap_active : isActive }"
    >
        <slot>
        </slot>
    </div>
</template>

<script>
export default {
  name: 'image-carousel-item',
  data: function() {
      return {
      }
	},
  props:['image_key', 'active_key'],
  computed: {
      isActive: function() {
          if ( this.active_key == this.image_key ) {
              return true
          } else {
              return false
          }
      }
  },
  methods: {
      triggerImageChange: function() {
          this.$emit('selected', this.image_key);
      }
  }
}

</script>