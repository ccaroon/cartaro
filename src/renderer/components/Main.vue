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
        <div class="text-h1">Daikon</div>
        <v-btn color="primary" @click="openGitHub">
          <v-icon left>mdi-github</v-icon>
          View on GitHub
        </v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6">
        <v-text-field
          outlined
          label="message1"
          v-model="message1"
        ></v-text-field>
      </v-col>
      <v-col cols="6">
        <v-text-field
          outlined
          label="message2"
          v-model="message2"
        ></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col offset="5">
        <v-btn color="success" @click="transmogrify">Transmogrify</v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-alert icon="mdi-console" color="black" outlined>{{
          output
        }}</v-alert>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'MainScreen',

  methods: {
    transmogrify: function () {
      window.Napiform.transmogrify(this.message1, this.message2)
        .then((data) => {
          this.output = data
        })
    },

    openGitHub: function () {
      window.Main.newWindow('https://github.com/ccaroon/daikon')
    }
  },

  data: () => ({
    message1: 'Hello, World!',
    message2: 'This is the way the World Ends!',
    output: null
  })
}
</script>
