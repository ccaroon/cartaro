<template>
  <div :id="editorId" :style="'height: ' + height + 'vh'"></div>
</template>

<script>
// COMPS
import { minimalSetup } from 'codemirror'
import { indentWithTab } from '@codemirror/commands'
import { LanguageDescription, StreamLanguage, bracketMatching } from '@codemirror/language'
import { EditorView, highlightActiveLine, keymap } from '@codemirror/view'
import { highlightSelectionMatches } from '@codemirror/search'

// LANGS
import { javascript } from '@codemirror/lang-javascript'
import { json } from '@codemirror/lang-json'
import { markdown } from '@codemirror/lang-markdown'
import { python } from '@codemirror/lang-python'
import { yaml } from '@codemirror/legacy-modes/mode/yaml'

// THEMES (In order of how I like them for Markdown)
import { basicDark } from 'cm6-theme-basic-dark'
// import { oneDark } from '@codemirror/theme-one-dark'
// import { materialDark } from 'cm6-theme-material-dark'
// import { dracula } from '@uiw/codemirror-theme-dracula'
// -----

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
      '&': {
        height: '100%',
        'font-size': '16px'
      },
      '.cm-scroller': { overflow: 'auto' }
    })

    const updateListener = EditorView.updateListener.of(self.contentUpdate)

    this.editor = new EditorView({
      doc: this.content,
      extensions: [
        EditorView.lineWrapping,
        fixedHeight,
        updateListener,
        minimalSetup,
        highlightActiveLine(),
        bracketMatching(),
        highlightSelectionMatches(),
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
        basicDark
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
        const setContent = this.editor.state.update({
          changes: {
            from: 0,
            to: this.editor.state.doc.length,
            insert: newContent
          }
        })

        this.editor.dispatch(setContent)
        // Move cursor to end of document
        // this.editor.dispatch({
        //   selection: {
        //     // anchor: this.editor.state.doc.length,
        //     // head: this.editor.state.doc.length
        //     anchor: 0,
        //     head: 0
        //   }
        // })
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
