import Moment from 'moment'
import Format from '../lib/Format'
import Icon from '../lib/Icon'
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

  icon () {
    return Icon.get(this.type, 'mdi-calendar')
  }

  hoursWorked () {
    const inTime = this.time_in.split(':')
    const dayStart = Moment(this.date * 1000).startOf('day').hours(inTime[0]).minutes(inTime[1])

    const outTime = this.time_out.split(':')
    const dayEnd = Moment(this.date * 1000).startOf('day').hours(outTime[0]).minutes(outTime[1])

    const duration = Moment.duration(dayEnd.diff(dayStart))

    return duration
  }

  clearInOut () {
    this.time_in = '00:00'
    this.time_out = '00:00'
  }

  toString () {
    return Format.formatDate(this.date)
  }
}
// -----------------------------------------------------------------------------
export default WorkDay
