import Moment from 'moment'

import Constants from '../lib/Constants'
import RestClient from '../lib/RestClient'
// -----------------------------------------------------------------------------
class Todo {
  static CLIENT = new RestClient('todos')

  constructor(data) {
    Object.assign(this, data)
  }

  markUncomplete () {
    if (this.repeat > 0) {
      alert('Cannot Mark Repeatable Todos as Uncompleted.')
    } else {
      this.is_complete = false
      this.completed_at = null
    }
  }

  markComplete () {
    var promises = []

    if (this.repeat > 0) {
      var repeatDuper = new Promise((resolve, reject) => {
        var newTodo = new Todo(this)
        delete newTodo.id
        newTodo.due_at = Moment(this.due_at * 1000).add(this.repeat, 'days').unix()
        newTodo.save({
          onSuccess: resolve,
          onError: reject
        })
      })
      promises.push(repeatDuper)
    }

    // **MUST** come last in promises list
    var always = new Promise((resolve) => {
      this.is_complete = true
      this.completed_at = Moment().unix()
      resolve()
    })
    promises.push(always)

    return Promise.all(promises)
  }

  toggleCompleted () {
    var promise = new Promise((resolve) => { resolve(true) })
    if (this.is_complete) {
      this.markUncomplete()
    } else {
      promise = this.markComplete()
    }
    return promise
  }

  priorityColor () {
    var key = `PRIORITY_${this.priority}`
    return Constants.COLORS[key]
  }

  color (idx) {
    var colors = {
      default: [Constants.COLORS.GREY, Constants.COLORS.GREY_ALT],
      dueSoon: ['yellow lighten-2', 'yellow lighten-4'],
      overdue: ['red lighten-2', 'red lighten-4']
    }
    var colorKey = 'default'
    var color = null

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

  save (options = {}) {
    if (this.id) {
      return Todo.CLIENT.update(this, options)
    } else {
      return Todo.CLIENT.create(this, options)
    }
  }

  delete (options = {}) {
    return Todo.CLIENT.delete(this, options)
  }

  static fetch (query, options) {
    return Todo.CLIENT.fetch(query, '/', {
      handlers: {
        onSuccess: (resp) => {
          var todos = []
          resp.data.todos.forEach(todo => {
            todos.push(new Todo(todo))
          })
          options.handlers.onSuccess(todos, resp.data.total)
        },
        onError: options.handlers.onError
      }
    })
  }
}
// -----------------------------------------------------------------------------
export default Todo
