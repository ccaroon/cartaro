import Moment from 'moment'

import constants from '../lib/constants'
import Resource from './Resource'
// -----------------------------------------------------------------------------
class Todo extends Resource {
  static RESOURCE_NAME = 'todos'

  // constructor(data) {
  //   super(data)
  // }

  markUncomplete () {
    if (this.repeat > 0) {
      alert('Cannot Mark Repeatable Todos as Uncompleted.')
    } else {
      this.is_complete = false
      this.completed_at = null
    }
  }

  markComplete () {
    const promises = []

    if (this.repeat > 0) {
      const repeatDuper = new Promise((resolve, reject) => {
        const newTodo = new Todo(this)
        delete newTodo.id
        newTodo.due_at = Moment(this.due_at * 1000).add(this.repeat, 'days').unix()
        newTodo.save({
          handlers: {
            onSuccess: resolve,
            onError: reject
          }
        })
      })
      promises.push(repeatDuper)
    }

    // **MUST** come last in promises list
    const always = new Promise((resolve) => {
      this.is_complete = true
      this.completed_at = Moment().unix()
      resolve()
    })
    promises.push(always)

    return Promise.all(promises)
  }

  toggleCompleted () {
    let promise = new Promise((resolve) => { resolve(true) })
    if (this.is_complete) {
      this.markUncomplete()
    } else {
      promise = this.markComplete()
    }
    return promise
  }

  priorityColor () {
    const key = `PRIORITY_${this.priority}`
    return constants.COLORS[key]
  }

  color (idx) {
    const colors = {
      default: [constants.COLORS.GREY, constants.COLORS.GREY_ALT],
      dueSoon: ['yellow lighten-2', 'yellow lighten-4'],
      overdue: ['red lighten-2', 'red lighten-4']
    }
    let colorKey = 'default'
    let color = null

    const now = Moment()
    const due = Moment.unix(this.due_at)

    if (!this.is_complete && this.due_at) {
      if (due < now) {
        colorKey = 'overdue'
      } else if (due < now.add(7, 'days')) {
        colorKey = 'dueSoon'
      }
    }

    color = colors[colorKey][0]
    if (idx % 2 === 0) {
      color = colors[colorKey][1]
    }

    return color
  }

  toString () {
    return this.title
  }
}
// -----------------------------------------------------------------------------
export default Todo
