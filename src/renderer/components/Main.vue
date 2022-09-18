<template>
  <v-container>
    <v-row>
      <v-col cols="3">
        <a href="https://en.wikipedia.org/wiki/Daikon" target="_blank">
          <v-img
            max-width="256"
            max-height="256"
            src="../assets/logo.png"
          ></v-img>
        </a>
      </v-col>
      <v-col>
        <div class="text-h1">Cartaro</div>
        <v-btn color="primary" @click="openGitHub">
          <v-icon left>mdi-github</v-icon>
          View on GitHub
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'MainScreen',

  methods: {
    openGitHub: function () {
      window.Main.newWindow('https://github.com/ccaroon/cartaro')
    }
  },

  data: () => ({})
}
</script>
