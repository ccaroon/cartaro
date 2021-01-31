<template>
  <v-dialog v-model="value" persistent scrollable max-width="75%">
    <v-card>
      <v-card-title>
        {{ secret.name }}
        <v-spacer></v-spacer>
        <v-chip
          small
          label
          class="mr-1"
          v-for="(tag, idx) in secret.tags"
          :key="idx"
          >{{ tag }}</v-chip
        >
      </v-card-title>
      <v-card-subtitle>
        {{ secret.system }} / {{ secret.sub_system }}
      </v-card-subtitle>
      <v-divider></v-divider>
      <v-card-title>{{ formatType(secret.type) }}</v-card-title>
      <v-card-text>
        <v-row
          v-for="(val, fld) in decrypt(secret)"
          :key="fld"
          no-gutters
          dense
        >
          <v-col>
            <v-icon @click.stop="utils.copyToClipboard(fld.toUpperCase(), val)"
              >mdi-{{ constants.ICONS.secrets[fld] }}</v-icon
            >&nbsp;
            <template v-if="hideData">**********</template>
            <template v-else>{{ val }}</template>
          </v-col>
        </v-row>
      </v-card-text>
      <v-divider></v-divider>
      <v-card-title>Notes</v-card-title>
      <v-card-text
        v-html="md.render(secret.note || '')"
        class="body-1 pt-3"
        style="height: 250px"
      ></v-card-text>
      <v-card-actions>
        <v-btn fab small
          ><v-icon
            :color="hideData ? 'red' : 'green'"
            @click="hideData = !hideData"
            >mdi-{{ hideData ? "lock" : "lock-open" }}</v-icon
          ></v-btn
        >
        <v-spacer></v-spacer>
        <v-btn color="success" @click="close()">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import Format from '../../lib/Format'
import Constants from '../../lib/Constants'
import Utils from '../../lib/Utils'
import MarkdownIt from 'markdown-it'
import MDEmoji from 'markdown-it-emoji'

export default {
  name: 'secret-viewer',
  components: {},
  props: ['secret', 'isHidden', 'decrypt', 'value'],

  methods: {
    formatType: function (type = ' ') {
      var parts = type.split('-')
      var prettyParts = parts.map(p => {
        return `${p[0].toUpperCase()}${p.slice(1)}`
      })

      return prettyParts.join('/')
    },
    close: function () {
      this.$emit('close')
    }
  },

  watch: {
    // Triggered when click to view a different secret
    secret: function () {
      this.hideData = this.isHidden
    }
  },

  data () {
    return {
      constants: Constants,
      format: Format,
      utils: Utils,
      hideData: true,
      md: new MarkdownIt().use(MDEmoji)
    }
  }
}
</script>
