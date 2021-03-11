<template>
  <v-sheet outlined>
    <codemirror :value="content" @input="onContentChange" :options="cmOption" />
  </v-sheet>
</template>

<script>
  import { codemirror } from 'vue-codemirror'

  // Base CSS
  import 'codemirror/lib/codemirror.css'

  // Languages
  import 'codemirror/mode/clike/clike.js'
  import 'codemirror/mode/go/go.js'
  import 'codemirror/mode/groovy/groovy.js'
  import 'codemirror/mode/javascript/javascript.js'
  import 'codemirror/mode/markdown/markdown.js'
  import 'codemirror/mode/python/python.js'
  import 'codemirror/mode/shell/shell.js'
  import 'codemirror/mode/yaml/yaml.js'

  // AddOns
  import 'codemirror/addon/selection/active-line'

  // Themes
  // import 'codemirror/theme/lesser-dark.css'
  // import 'codemirror/theme/material-darker.css'
  // import 'codemirror/theme/material.css'
  // import 'codemirror/theme/panda-syntax.css'
  import 'codemirror/theme/yonce.css'

  export default {
    name: 'shared-markdown',
    components: { codemirror },
    props: ['content'],
    mounted () {},
    methods: {
      onContentChange: function (newContent) {
        this.$emit('update', newContent)
      }
    },
    watch: { },
    data () {
      return {
        cmOption: {
          tabSize: 4,
          styleActiveLine: true,
          lineNumbers: false,
          lineWrapping: false,
          mode: 'text/x-markdown',
          theme: 'yonce'
        }
      }
    }
  }
</script>
