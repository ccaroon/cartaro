<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="auto">
        <img src="@/assets/logo.png" />
      </v-col>
    </v-row>
    <v-row class="black light-green--text">
      <v-col cols="auto">{{ data.id }} - {{ data.title }} - {{ data.content }}</v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'home',
  components: { },
  mounted: function () {
    this.getStuff()
  },

  methods: {
    getStuff: function () {
      var self = this
      this.$http.get('http://127.0.0.1:4242/notes/1')
        .then(resp => {
          self.data = resp.data
        })
    }
  },
  data () {
    return {
      data: {}
    }
  }
}
</script>
