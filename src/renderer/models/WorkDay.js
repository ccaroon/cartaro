import Moment from 'moment'

import RestClient from '../lib/RestClient'
// -----------------------------------------------------------------------------
class WorkDay {
  static CLIENT = new RestClient('work_days')

  static DEFAULT_IN = '09:00'
  static DEFAULT_OUT = '16:30'

  static TYPE_NORMAL = 'normal'
  static TYPE_PTO = 'pto'
  static TYPE_SICK = 'sick'
  static TYPE_HOLIDAY = 'holiday'

  constructor(data) {
    Object.assign(this, data)
  }

  hoursWorked () {
    var inTime = this.time_in.split(':')
    var dayStart = Moment(this.date * 1000).startOf('day').hours(inTime[0]).minutes(inTime[1])

    var outTime = this.time_out.split(':')
    var dayEnd = Moment(this.date * 1000).startOf('day').hours(outTime[0]).minutes(outTime[1])

    var duration = Moment.duration(dayEnd.diff(dayStart))

    return duration
  }

  clearInOut () {
    this.time_in = '00:00'
    this.time_out = '00:00'
  }

  save (options = {}) {
    if (this.id) {
      return WorkDay.CLIENT.update(this, options)
    } else {
      return WorkDay.CLIENT.create(this, options)
    }
  }

  delete (options = {}) {
    return WorkDay.CLIENT.delete(this, options)
  }

  static fetch (query, endpoint = '/', options = {}) {
    return WorkDay.CLIENT.fetch(query, endpoint, {
      handlers: {
        onSuccess: (resp) => {
          var workDays = []
          resp.data.work_days.forEach(day => {
            workDays.push(new WorkDay(day))
          })
          options.handlers.onSuccess(workDays, resp.data.total)
        },
        onError: options.handlers.onError
      }
    })
  }
}
// -----------------------------------------------------------------------------
export default WorkDay
