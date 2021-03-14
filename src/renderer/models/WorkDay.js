import Moment from 'moment'

import Resource from './Resource'
// -----------------------------------------------------------------------------
class WorkDay extends Resource {
  static RESOURCE_NAME = 'work_days'

  static DEFAULT_IN = '09:00'
  static DEFAULT_OUT = '16:30'

  static TYPE_NORMAL = 'normal'
  static TYPE_PTO = 'pto'
  static TYPE_SICK = 'sick'
  static TYPE_HOLIDAY = 'holiday'

  // constructor(data) {
  //   super(data)
  // }

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
}
// -----------------------------------------------------------------------------
export default WorkDay
