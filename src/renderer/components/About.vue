<template>
  <v-dialog v-model="showDialog" max-width="768">
    <v-card>
      <v-card-title id="about-title" class="headline blue-grey lighten-1">
        <img width="64" src="../assets/logo.png" />
        &nbsp;
        {{ appInfo.name }} v{{ appInfo.version }} ({{ appInfo.codename }})
      </v-card-title>
      <v-card-text>
        {{ appInfo.description }} &mdash; &copy; {{ appInfo.author }} 2020-{{
          new Date().getFullYear()
        }}
        <v-divider></v-divider>
        <v-row>
          <v-col>
            <v-subheader>System Info</v-subheader>
            <v-data-table
              :items="systemInfo"
              hide-default-footer
              hide-default-header
              dark
            >
              <template v-slot:body="{ items }">
                <tbody>
                  <tr v-for="item in items" :key="item.name">
                    <td>
                      <v-icon>{{ item.icon }}</v-icon>
                      {{ item.name }}
                    </td>
                    <td
                      :id="
                        'about-sysinfo-' +
                        item.name.toLowerCase().replace(' ', '')
                      "
                    >
                      {{ item.value }}
                    </td>
                  </tr>
                </tbody>
              </template>
            </v-data-table>
          </v-col>
          <v-col>
            <v-subheader>Built With</v-subheader>
            <v-data-table
              :items="builtWith"
              hide-default-footer
              hide-default-header
              dark
            >
              <template v-slot:body="{ items }">
                <tbody>
                  <tr v-for="item in items" :key="item.name">
                    <td>
                      <v-icon>{{ item.icon }}</v-icon>
                      {{ item.name }}
                    </td>
                    <td
                      :id="
                        'about-tech-' + item.name.toLowerCase().replace(' ', '')
                      "
                    >
                      {{ item.value }}
                    </td>
                  </tr>
                </tbody>
              </template>
            </v-data-table>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
// import config from '../../Config'
import RestClient from '../lib/RestClient'

const { ipcRenderer } = require('electron')
const pkgJson = require('../../../package.json')

export default {
  mounted () {
    ipcRenderer.on('menu-help-about', (event, arg) => {
      this.showDialog = true
    })
  },

  data () {
    const data = {
      showDialog: false,
      appInfo: pkgJson,
      builtWith: [
        { name: 'Electron', value: process.versions.electron, icon: 'mdi-atom' },
        { name: 'NodeJS', value: process.versions.node, icon: 'mdi-nodejs' },
        { name: 'Python', value: '3.9.6', icon: 'mdi-language-python' },
        { name: 'Chrome', value: process.versions.chrome, icon: 'mdi-google-chrome' },
        { name: 'Vue Version', value: require('vue/package.json').version, icon: 'mdi-vuejs' }
      ],
      systemInfo: [
        { name: 'Cartaro', value: `v${pkgJson.version} | ${pkgJson.codename}`, icon: pkgJson.icon },
        { name: 'Platform', value: require('os').platform(), icon: 'mdi-laptop' },
        { name: 'Mode', value: process.env.NODE_ENV, icon: 'mdi-cogs' },
        { name: 'Server', value: RestClient.baseUrl(), icon: 'mdi-ip-network' },
        { name: 'Build Date', value: pkgJson.buildDate, icon: 'mdi-wrench' }
      ]
    }

    if (process.platform === 'darwin') {
      data.systemInfo[1].icon = 'mdi-apple'
    } else if (process.platform === 'win32') {
      data.systemInfo[1].icon = 'mdi-windows'
    } else if (process.platform === 'linux') {
      data.systemInfo[1].icon = 'mdi-linux'
    }

    return (data)
  }
}
</script>
