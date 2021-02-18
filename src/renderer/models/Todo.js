import Moment from 'moment'

import Constants from '../lib/Constants'
import RestClient from '../lib/RestClient'

const CLIENT = new RestClient('todos')
// -----------------------------------------------------------------------------
function Todo (data) {
  Object.assign(this, data)
  this.client = CLIENT
}
// -----------------------------------------------------------------------------
Todo.prototype.markUncomplete = function () {
  if (this.repeat > 0) {
    alert('Cannot Mark Repeatable Todos as Uncompleted.')
  } else {
    this.is_complete = false
    this.completed_at = null
  }
}

Todo.prototype.markComplete = function () {
  if (this.repeat > 0) {
    var newTodo = new Todo(this)
    delete newTodo.id
    newTodo.due_at = Moment(this.due_at * 1000).add(this.repeat, 'days').unix()
    newTodo.save()
  }

  this.is_complete = true
  this.completed_at = Moment().unix()
}

Todo.prototype.toggleCompleted = function () {
  if (this.is_complete) {
    this.markUncomplete()
  } else {
    this.markComplete()
  }
}

Todo.prototype.priorityColor = function () {
  var key = `PRIORITY_${this.priority}`
  return Constants.COLORS[key]
}

Todo.prototype.color = function (idx) {
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

Todo.prototype.save = function (handlers = {}) {
  if (this.id) {
    this.client.update(this, handlers)
  } else {
    this.client.create(this, handlers)
  }
}

Todo.prototype.delete = function (handlers = {}) {
  this.client.delete(this, handlers)
}
// -----------------------------------------------------------------------------
function fetchTodos (query, handlers) {
  CLIENT.fetch(query, {
    onSuccess: (resp) => {
      var todos = []
      resp.data.todos.forEach(todo => {
        todos.push(new Todo(todo))
      })
      handlers.onSuccess(todos, resp.data.total)
    },
    onError: handlers.onError
  })
}
// -----------------------------------------------------------------------------
export { Todo, fetchTodos }
