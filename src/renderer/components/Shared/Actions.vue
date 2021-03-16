<template>
  <v-list-item-action>
    <v-row no-gutters>
      <v-col class="mr-1" v-if="actions.hasOwnProperty('edit')">
        <v-btn icon outlined @click="actions['edit'](item)">
          <v-icon>mdi-pencil</v-icon>
        </v-btn>
      </v-col>
      <v-col class="mr-1" v-if="actions.hasOwnProperty('remove')">
        <v-btn icon outlined @click="actions['remove'](item)">
          <v-icon :color="deleteIconColor()">mdi-delete</v-icon>
        </v-btn>
      </v-col>
    </v-row>
  </v-list-item-action>
</template>
<script>
export default {
  name: 'shared-actions',
  components: {},
  props: ['item', 'actions'],

  methods: {
    deleteIconColor: function () {
      return this.item.isDeleted() ? 'red' : null
    }
  },

  data () {
    return {}
  }
}
</script>
