<template>
  <div>
    <v-dialog v-model="showArchiveDelete" persistent max-width="40%">
      <v-card>
        <v-card-title>{{ item }}</v-card-title>
        <v-card-actions>
          <v-btn color="red" rounded @click="doArchiveDelete(false)">
            <v-icon>mdi-delete</v-icon> Delete
          </v-btn>
          <v-btn color="green" rounded @click="unArchive()">
            <v-icon>mdi-archive-arrow-up</v-icon> Restore
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn @click="showArchiveDelete = false">Cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-list-item-action>
      <v-row no-gutters>
        <v-col class="mr-1" v-if="actions.hasOwnProperty('onEdit')">
          <v-btn
            icon
            outlined
            @click="actions['onEdit'](item)"
            :disabled="item.isDeleted()"
          >
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
        </v-col>
        <v-col class="mr-1" v-if="actions.hasOwnProperty('onArchiveDelete')">
          <v-btn icon outlined @click="archiveDelete()">
            <v-icon :color="archiveDeleteColor"
              >mdi-{{ archiveDeleteIcon }}</v-icon
            >
          </v-btn>
        </v-col>
      </v-row>
    </v-list-item-action>
  </div>
</template>
<script>
import Notification from '../../lib/Notification'

export default {
  name: 'shared-actions',
  components: {},
  props: ['item', 'actions'],

  computed: {
    archiveDeleteIcon: function () {
      return this.item.isDeleted() ? 'delete-restore' : 'archive-arrow-down'
    },

    archiveDeleteColor: function () {
      return this.item.isDeleted() ? 'red' : ''
    }
  },

  methods: {
    unArchive: function () {
      var self = this

      this.item.deleted_at = null
      this.item.undelete({
        handlers: {
          onSuccess: () => {
            this.showArchiveDelete = false
            self.actions.onArchiveDelete(self.item)
          },
          onError: (err) => { Notification.error(`SH.Actions.unArchive: ${err.toString()}`) }
        }
      })
    },

    archiveDelete: function () {
      if (this.item.isDeleted()) {
        this.showArchiveDelete = true
      } else {
        this.doArchiveDelete()
      }
    },

    doArchiveDelete: function (prompt = true) {
      var self = this
      var safe = 1
      var msg = `Archive "${this.item}"?`

      if (this.item.isDeleted()) {
        safe = 0
        msg = `Delete "${this.item}"?`
      }

      var doDelete = prompt ? confirm(msg) : true

      if (doDelete) {
        this.item.delete({
          safe: safe,
          handlers: {
            onSuccess: () => {
              this.showArchiveDelete = false
              self.actions.onArchiveDelete(self.item)
            },
            onError: (err) => { Notification.error(`SH.Actions.archiveDelete: ${err.toString()}`) }
          }
        })
      }
    }
  },

  data () {
    return {
      showArchiveDelete: false
    }
  }
}
</script>
