import Moment from 'moment'
import format from '../lib/format'
import Icon from '../lib/Icon'
import Resource from './Resource'
// -----------------------------------------------------------------------------
class WorkDay extends Resource {
  static RESOURCE_NAME = 'work_days'

  static DEFAULT_IN = '09:00'
  static DEFAULT_OUT = '16:30'

  static HOURS_PER_DAY = 7.5

  static TYPE_NORMAL = 'normal'
  static TYPE_VACATION = 'vacation'
  static TYPE_SICK = 'sick'
  static TYPE_HOLIDAY = 'holiday'

  static color (dayType, hint = null, alt = false) {
    let color = 'blue'

    if (dayType === WorkDay.TYPE_VACATION) {
      color = 'green'
    } else if (dayType === WorkDay.TYPE_SICK) {
      color = 'red'
    } else if (dayType === WorkDay.TYPE_HOLIDAY) {
      color = 'deep-purple'
    }

    if (hint === 'accent') {
      color += alt ? ' accent-4' : ' accent-2'
    } else if (hint === 'light') {
      color += alt ? ' lighten-4' : ' lighten-3'
    }

    return color
  }

  color (hint = null, alt = false) {
    return WorkDay.color(this.type, hint, alt)
  }

  icon () {
    return Icon.get(this.type, 'mdi-calendar')
  }

  typeCode (asEmoji = false) {
    let code = '???'
    let emoji = ''
    if (this.type === WorkDay.TYPE_NORMAL) {
      code = 'NRM'
      emoji = '😐'
    } else if (this.type === WorkDay.TYPE_VACATION) {
      code = 'VAC'
      emoji = '😴'
    } else if (this.type === WorkDay.TYPE_SICK) {
      code = 'SCK'
      emoji = '🤒'
    } else if (this.type === WorkDay.TYPE_HOLIDAY) {
      code = 'HDY'
      emoji = '🥳'
    }

    return (asEmoji ? emoji : code)
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

  isNormal () {
    return this.type === WorkDay.TYPE_NORMAL
  }

  toString () {
    return format.formatDate(this.date)
  }
}
// -----------------------------------------------------------------------------
export default WorkDay
