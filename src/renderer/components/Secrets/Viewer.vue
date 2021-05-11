<template>
  <v-dialog :value="value" persistent scrollable max-width="75%">
    <v-card>
      <v-app-bar dense flat>
        <v-toolbar-title>{{ secret.name }}</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn small icon @click="close()">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-app-bar>
      <v-card-subtitle class="pl-4 pb-1">
        {{ secret.system }} / {{ secret.sub_system }}
      </v-card-subtitle>
      <v-divider></v-divider>
      <v-card-title>{{ formatType(secret.type) }}</v-card-title>
      <v-card-text>
        <v-row v-for="fld in secret.fieldNames()" :key="fld" no-gutters dense>
          <v-col>
            <v-icon
              @click.stop="
                utils.copyToClipboard(fld.toUpperCase(), secret.data[fld])
              "
              >{{ secret.icon(fld) }}</v-icon
            >&nbsp;
            <template v-if="hideData">**********</template>
            <template v-else>{{ secret.data[fld] }}</template>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-title>Notes</v-card-title>
      <v-card-text
        v-html="$markdown.render(secret.note || '')"
        class="pt-3"
        style="height: 250px"
      ></v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <v-chip
          small
          label
          class="pa-1 mr-1"
          v-for="(tag, idx) in secret.tags"
          :key="idx"
          >{{ tag }}</v-chip
        >
        <v-spacer></v-spacer>
        <v-btn fab small
          ><v-icon
            :color="hideData ? 'red' : 'green'"
            @click="hideData = !hideData"
            >mdi-{{ hideData ? "lock" : "lock-open" }}</v-icon
          ></v-btn
        >
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import Format from '../../lib/Format'
import Constants from '../../lib/Constants'
import Utils from '../../lib/Utils'

export default {
  name: 'secret-viewer',
  components: {},
  props: ['secret', 'isHidden', 'value'],

  methods: {
    formatType: function (type = ' ') {
      const parts = type.split('-')
      const prettyParts = parts.map(p => {
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
      hideData: true
    }
  }
}
</script>
