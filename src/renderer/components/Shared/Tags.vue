<template>
  <span>
    <v-chip
      x-small
      label
      class="mr-1 float-right"
      :color="color"
      v-for="(tag,tgIdx) in tags"
      :key="tgIdx"
    >{{ tag }}</v-chip>
  </span>
</template>
<script>
export default {
  name: 'shared-tags',
  components: {},
  props: ['tags', 'color'],

  methods: {},

  data () {
    return {}
  }
}
</script>
