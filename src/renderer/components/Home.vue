<template>
  <div>
    <v-responsive>
      <v-container>
        <v-row align="center" class="blue-grey lighten-1">
          <v-col cols="auto">
            <img src="@/assets/logo.png" />
          </v-col>
          <v-col cols="auto">
            <p class="display-4">Ĉartaro</p>
            <p class="subtitle-1">Job Journal</p>
          </v-col>
        </v-row>
        <v-row class="black light-green--text">
          <v-col cols="auto">{{ data.msg }}</v-col>
        </v-row>
      </v-container>
    </v-responsive>
  </div>
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
      this.$http.get('http://127.0.0.1:4242/hello')
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
