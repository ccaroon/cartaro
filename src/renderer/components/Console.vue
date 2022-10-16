<template>
  <v-textarea autofocus clearable dark dense no-resize solo class="cartaroConsole" background-color="black"
    clear-icon="mdi-nuke" rows="25" @keypress="handleKeyPress"></v-textarea>
</template>

<script>
import Mousetrap from 'mousetrap'

export default {
  name: 'app-quake-console',
  components: {},
  props: [],
  mounted () {
    this.bindShortcutKeys()
  },

  methods: {
    // Was unable to get Mousetrap to fire when the v-textarea is focused.
    // Tried several things as mentioned in the Mousetrap docs
    // Instead, using the `keypress` handler to trigger Mousetrap
    handleKeyPress: function (event) {
      const keyData = []

      if (event.altKey) keyData.unshift('alt')
      if (event.ctrlKey) keyData.unshift('ctrl')
      if (event.metaKey) keyData.unshift('meta')
      if (event.shiftKey) keyData.unshift('shift')
      keyData.sort()
      keyData.push(event.key.toLowerCase())

      Mousetrap.trigger(keyData.join('+'))
    },

    bindShortcutKeys: function () {
      Mousetrap.bind(['ctrl+enter'], (e) => {
        console.log('!!Execute!!')
        return false
      })
    }
  },

  data: () => ({
  })
}
</script>
<style>
.cartaroConsole textarea {
  /* light-green accent-3 */
  color: #76ff03 !important;
}
</style>
