<template>
  <v-dialog :value="value" persistent max-width="75%" max-height="90%">
    <v-card>
      <v-app-bar dense flat>
        <v-toolbar-title>PTO Editor</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn small icon @click="close()">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-app-bar>
      <v-card-text>
        <v-form ref="ptoForm">
          <v-container>
            <v-row dense>
              <v-col cols="4">
                <v-text-field
                  label="Type"
                  v-model="pto.type"
                  outlined
                  dense
                  hide-details
                  :rules="rules.type"
                  >{{ pto.type }}</v-text-field
                >
              </v-col>
              <v-col cols="4">
                <v-select
                  :items="populateYears()"
                  label="Year"
                  v-model="pto.year"
                  outlined
                  dense
                ></v-select>
              </v-col>
              <v-col cols="4">
                <v-text-field
                  v-model="pto.starting_balance"
                  type="number"
                  dense
                  outlined
                  label="Starting Balance"
                  suffix="Hours"
                  :rules="rules.startingBalance"
                />
              </v-col>
            </v-row>
            <v-row dense v-if="pto.accrual">
              <v-col cols="4">
                <v-text-field
                  v-model="pto.accrual.rate"
                  type="number"
                  dense
                  outlined
                  label="Accrual Rate"
                  suffix="Hours"
                  :rules="rules.accrualRate"
                />
              </v-col>
              <v-col cols="4">
                <v-text-field
                  v-model="pto.accrual.period"
                  type="number"
                  dense
                  outlined
                  label="Accrual Period"
                  suffix="Months"
                  :rules="rules.accrualPeriod"
                />
              </v-col>
            </v-row>
          </v-container>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-alert v-show="errorMsg" dense color="error">{{
          this.errorMsg
        }}</v-alert>
        <v-spacer></v-spacer>
        <v-btn color="success" @click="save()">Save</v-btn>
        <v-btn color="red" text @click="close()">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
import Moment from 'moment'
// import Format from '../../lib/Format'
// import Notification from '../../lib/Notification'

// import Config from '../../../Config'

export default {
  name: 'pto-editor',
  components: { },
  props: ['pto', 'value'],

  mounted: function () {},

  methods: {
    populateYears: function () {
      const currYear = Moment().year()
      const yearList = []

      for (let i = -1; i < 5; i++) {
        yearList.push(currYear + i)
      }

      return yearList
    },

    save: function () {
      const self = this

      if (this.$refs.ptoForm.validate()) {
        this.pto.save({
          handlers: {
            onSuccess: () => { self.close() },
            onError: (err) => { self.errorMsg = err }
          }
        })
      } else {
        this.errorMsg = 'Please fill in the required fields.'
      }
    },

    cleanup: function () {
      this.errorMsg = null
      this.$refs.ptoForm.resetValidation()
    },

    close: function () {
      this.cleanup()
      this.$emit('close')
    }
  },

  data () {
    return {
      errorMsg: null,
      rules: {
        type: [
          type => !!type || 'Type is required'
        ],
        startingBalance: [
          startingBalance => startingBalance >= 0 || 'Starting Balance must be >= 0'
        ],
        accrualRate: [
          rate => (rate === null || rate > 0) || 'Accrual Rate must be greater than 0'
        ],
        accrualPeriod: [
          period => (period === null || period > 0) || 'Accrual Period must be greater than 0'
        ]
      }
    }
  }
}
</script>
