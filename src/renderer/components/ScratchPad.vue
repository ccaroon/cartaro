<template>
  <v-sheet class="scratch-pad">
    <Markdown
      :content="content.tab1"
      @update="contentUpdate"
      theme="yonce"
    ></Markdown>
  </v-sheet>
</template>
<script>
import Markdown from './Shared/Markdown'

export default {
  name: 'scratch-pad',
  components: { Markdown },
  mounted: function () {
  },

  methods: {
    contentUpdate: function (newContent) {
      this.content.tab1 = newContent
    }
  },

  data () {
    return {
      content: {
        tab1: '',
        tab2: ''
      }
    }
  }
}
</script>
<style lang="css" scoped>
/* >>> -means- that this style should effect child components */
>>> .CodeMirror {
  border: 1px solid rgb(52, 253, 34);
  height: 975px;
}
</style>
