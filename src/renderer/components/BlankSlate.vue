<template>
  <v-container>
    <div id="editor"></div>
  </v-container>
</template>

<script>
import { EditorState } from '@codemirror/state'
import { EditorView, keymap } from '@codemirror/view'
import { defaultKeymap } from '@codemirror/commands'

export default {
  name: 'blank-slate',

  mounted () {
    const startState = EditorState.create({
      doc: 'Hello World',
      extensions: [keymap.of(defaultKeymap)]
    })

    const view = new EditorView({
      state: startState,
      parent: document.getElementById('editor')
    })

    return view
  },

  methods: { },

  data: () => ({})
}
</script>
