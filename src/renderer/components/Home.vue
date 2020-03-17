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
