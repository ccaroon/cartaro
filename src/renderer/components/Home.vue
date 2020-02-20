<template>
  <div>
    <v-responsive class="green lighten-1">
      <v-container fill-height>
        <v-row align="center">
          <v-col cols="auto">
            <img src="@/assets/logo.png" />
          </v-col>
          <v-col cols="auto">
            <p class="display-4">Ĉartaro</p>
            <p class="subtitle-1">Job Journal</p>
            <p class="subtitle-1">{{ thing1.name }} - {{ thing1.age }}</p>
          </v-col>
        </v-row>
      </v-container>
    </v-responsive>
    <v-container>
      <v-row align="center" justify="space-around" class="pa-1">
        <system-information></system-information>
      </v-row>
    </v-container>
  </div>
</template>

<script>
  import SystemInformation from './SystemInformation'

  export default {
    name: 'home',
    components: { SystemInformation },
    mounted: function () {
      this.getStuff()
    },

    methods: {
      getStuff: function () {
        var self = this

        // this.$http.get('http://api.open-notify.org/iss-now.json')
        //   .then(resp => {
        //     self.thing1 = resp.data.iss_position.latitude
        //   })
        this.$http.get('http://127.0.0.1:4242')
          .then(resp => {
            self.thing1 = resp.data
          })
      }
    },
    data () {
      return {
        thing1: {}
      }
    }
  }
</script>
