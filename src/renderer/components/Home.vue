<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="auto">
        <img src="@/assets/logo.png" />
      </v-col>
    </v-row>
    <v-row class="black light-green--text">
      <v-col cols="auto">{{ msg }}</v-col>
    </v-row>
    <v-row justify="center" class="grey" dense>
      <v-col cols="2">Scratch Area</v-col>
    </v-row>
    <v-row>
      <v-col>This is the way the world ends!</v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'home',
  components: { },

  mounted: function () {
  },

  methods: {
  },

  data () {
    return {
      msg: 'Here Be Dragons!'
    }
  }
}
</script>
