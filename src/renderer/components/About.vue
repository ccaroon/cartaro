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
                      <v-icon>mdi-{{ item.icon }}</v-icon>
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
                      <v-icon>mdi-{{ item.icon }}</v-icon>
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
        { name: 'Electron', value: process.versions.electron, icon: 'atom' },
        { name: 'NodeJS', value: process.versions.node, icon: 'nodejs' },
        { name: 'Python', value: '3.8.2', icon: 'language-python' },
        { name: 'Chrome', value: process.versions.chrome, icon: 'google-chrome' },
        { name: 'Vue Version', value: require('vue/package.json').version, icon: 'vuejs' }
      ],
      systemInfo: [
        { name: 'Cartaro', value: `v${pkgJson.version} | ${pkgJson.codename}`, icon: 'map-legend' },
        { name: 'Platform', value: require('os').platform(), icon: 'laptop' },
        { name: 'Mode', value: process.env.NODE_ENV, icon: 'cogs' },
        { name: 'Server', value: RestClient.baseUrl(), icon: 'ip-network' }
      ]
    }

    if (process.platform === 'darwin') {
      data.systemInfo[1].icon = 'apple'
    } else if (process.platform === 'win32') {
      data.systemInfo[1].icon = 'windows'
    } else if (process.platform === 'linux') {
      data.systemInfo[1].icon = 'linux'
    }

    return (data)
  }
}
</script>
