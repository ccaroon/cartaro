<template>
  <span>
    <v-chip
      x-small
      label
      :class="tagClass"
      :color="color"
      v-for="(tag, tgIdx) in getTags()"
      :key="tgIdx"
      >{{ tag }}</v-chip
    >
  </span>
</template>
<script>
export default {
  name: 'shared-tags',
  components: {},
  props: ['tags', 'color', 'tagClassOverride', 'maxDisplay'],

  methods: {
    getTags: function () {
      return this.maxDisplay ? this.tags.slice(0, this.maxDisplay) : this.tags
    }
  },

  data () {
    return {
      tagClass: this.tagClassOverride || 'mr-1 float-right'
    }
  }
}
</script>
