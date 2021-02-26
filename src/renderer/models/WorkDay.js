import Moment from 'moment'

import RestClient from '../lib/RestClient'

const CLIENT = new RestClient('work_days')
// -----------------------------------------------------------------------------
function WorkDay (data) {
  Object.assign(this, data)
  this.client = CLIENT
}
// -----------------------------------------------------------------------------
WorkDay.prototype.hoursWorked = function () {
  var inTime = this.time_in.split(':')
  var dayStart = Moment(this.date * 1000).startOf('day').hours(inTime[0]).minutes(inTime[1])

  var outTime = this.time_out.split(':')
  var dayEnd = Moment(this.date * 1000).startOf('day').hours(outTime[0]).minutes(outTime[1])

  var duration = Moment.duration(dayEnd.diff(dayStart))

  return duration
}
// WorkDay.prototype.save = function (handlers = {}) {
//   if (this.id) {
//     this.client.update(this, handlers)
//   } else {
//     this.client.create(this, handlers)
//   }
// }

// WorkDay.prototype.delete = function (handlers = {}) {
//   this.client.delete(this, handlers)
// }
// // -----------------------------------------------------------------------------
function fetchWorkDays (query, endpoint = '/', handlers) {
  CLIENT.fetch(query, endpoint, {
    onSuccess: (resp) => {
      var workDays = []
      resp.data.work_days.forEach(day => {
        workDays.push(new WorkDay(day))
      })
      handlers.onSuccess(workDays, resp.data.total)
    },
    onError: handlers.onError
  })
}
// -----------------------------------------------------------------------------
export { WorkDay, fetchWorkDays }
