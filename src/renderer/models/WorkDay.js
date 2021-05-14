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

  typeCode () {
    let code = '???'
    if (this.type === WorkDay.TYPE_NORMAL) {
      code = 'NRM'
    } else if (this.type === WorkDay.TYPE_PTO) {
      code = 'PTO'
    } else if (this.type === WorkDay.TYPE_SICK) {
      code = 'SCK'
    } else if (this.type === WorkDay.TYPE_HOLIDAY) {
      code = 'HDY'
    }

    return code
  }

  start () {
    const inTime = this.time_in.split(':')
    const dayStart = Moment(this.date * 1000).startOf('day').hours(inTime[0]).minutes(inTime[1])

    return dayStart
  }

  end () {
    const outTime = this.time_out.split(':')
    const dayEnd = Moment(this.date * 1000).startOf('day').hours(outTime[0]).minutes(outTime[1])

    return dayEnd
  }

  allDay () {
    let allDay = false

    if (this.time_in === '00:00' && this.time_out === '00:00') {
      allDay = true
    }

    return allDay
  }

  hoursWorked () {
    const dayStart = this.start()
    const dayEnd = this.end()

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
