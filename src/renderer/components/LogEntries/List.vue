<template>
  <v-container>
    <v-list dense>
      <v-list-item
        v-for="(logEntry, idx) in logEntries"
        :key="logEntry.id"
        :class="utils.rowColor(idx)"
        @click.stop
      >
        <v-list-item-avatar>
          <v-icon>{{ logEntry.icon() }}</v-icon>
        </v-list-item-avatar>
        <v-list-item-content @click="view(logEntry)">
          <v-list-item-title
            :class="
              logEntry.isDeleted()
                ? 'subtitle-1 text-decoration-line-through'
                : 'subtitle-1'
            "
            >{{ logEntry.subject }}</v-list-item-title
          >
          <v-list-item-subtitle>
            {{ logEntry.category }} |
            {{
              logEntry.logged_at
                ? format.formatDate(logEntry.logged_at * 1000)
                : "--"
            }}
            <Tags
              v-bind:tags="logEntry.tags"
              v-bind:color="utils.rowColor(idx + 1)"
            ></Tags>
          </v-list-item-subtitle>
        </v-list-item-content>
        <Actions
          v-bind:actions="{
            onEdit: (item) => {
              edit(item);
            },
            onArchiveDelete: (event, item) => {
              if (event.startsWith('post-')) {
                refresh();
              }
            },
          }"
          v-bind:item="logEntry"
        ></Actions>
      </v-list-item>
    </v-list>
  </v-container>
</template>
<script>
import format from '../../lib/format'
import utils from '../../lib/utils'

import Actions from '../Shared/Actions'
import Tags from '../Shared/Tags'

export default {
  name: 'log-entries-list',
  props: ['logEntries'],
  components: { Actions, Tags },
  mounted: function () {
  },

  methods: {
    view: function (logEntry) {
      this.$emit('view', logEntry)
    },

    edit: function (logEntry) {
      this.$emit('edit', logEntry)
    },

    refresh: function () {
      this.$emit('refresh')
    }
  },

  data () {
    return {
      format: format,
      utils: utils
    }
  }
}
</script>
