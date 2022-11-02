<template>
  <div :id="editorId" :style="'height: ' + height + 'vh'"></div>
</template>

<script>
// COMPS
import { basicSetup } from 'codemirror'
import { indentWithTab } from '@codemirror/commands'
import { LanguageDescription, StreamLanguage } from '@codemirror/language'
import { EditorView, keymap } from '@codemirror/view'

// LANGS
import { javascript } from '@codemirror/lang-javascript'
import { json } from '@codemirror/lang-json'
import { markdown } from '@codemirror/lang-markdown'
import { python } from '@codemirror/lang-python'
import { yaml } from '@codemirror/legacy-modes/mode/yaml'

// THEMES
import { oneDark } from '@codemirror/theme-one-dark'

export default {
  name: 'shared-markdown',
  props: ['content', 'id', 'keyMap', 'height'],

  mounted () {
    const self = this
    const keyMappings = []

    // Tab key indents
    keyMappings.push(indentWithTab)
    // Ctl|Cmd-S saves
    keyMappings.push(
      {
        key: 'Mod-s',
        run () {
          self.contentSave()
          return true
        }
      }
    )
    // Custom key mappings
    if (this.keyMap) {
      this.keyMap.forEach(map => {
        keyMappings.push(map)
      })
    }

    const fixedHeight = EditorView.theme({
      '&': { height: '100%' },
      '.cm-scroller': { overflow: 'auto' }
    })

    const updateListener = EditorView.updateListener.of(self.contentUpdate)

    this.editor = new EditorView({
      doc: this.content,
      extensions: [
        EditorView.lineWrapping,
        fixedHeight,
        updateListener,
        basicSetup,
        keymap.of(keyMappings),
        markdown({
          // codeLanguages: [
          //   LanguageDescription.of({ name: 'javascript', support: javascript() }),
          //   LanguageDescription.of({ name: 'json', support: json() }),
          //   LanguageDescription.of({ name: 'python', support: python() })
          // ]
          // Have to use as a function b/c of the legacy YAML language.
          // Can't get a LanguageDescription of `yaml`
          codeLanguages: this.loadLang
        }),
        oneDark
      ],
      parent: document.getElementById(this.editorId)
    })
    this.editor.focus()
  },

  methods: {
    loadLang: function (info) {
      return this.languages[info]
    },

    contentUpdate: function (view) {
      if (view.docChanged) {
        this.$emit('update', this.editor.state.doc.toString())
      }
    },

    contentSave: function () {
      this.$emit('save', this.editor.state.doc.toString())
    }
  },

  watch: {
    content: function (newContent, oldContent) {
      if (newContent !== oldContent) {
        const transaction = this.editor.state.update({
          changes: {
            from: 0,
            to: this.editor.state.doc.length,
            insert: newContent
          }
        })
        console.log('...md updating editor...')
        this.editor.dispatch(transaction)
        this.editor.focus()
      }
    }

    // keyMap: function (newMap, oldMap) {
    //   if (newMap !== oldMap) {
    //     // Use Compartment.reconfigure()
    //     return true
    //   }
    // }
  },

  data () {
    return {
      editor: null,
      editorId: 'cartaro-md-editor-' + (this.id || 'X'),
      languages: {
        javascript: LanguageDescription.of({ name: 'javascript', support: javascript() }).support.language,
        json: LanguageDescription.of({ name: 'json', support: json() }).support.language,
        python: LanguageDescription.of({ name: 'python', support: python() }).support.language,
        yaml: StreamLanguage.define(yaml)
      }
    }
  }
}
</script>
