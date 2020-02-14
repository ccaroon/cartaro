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
    methods: {
    }
  }
</script>
