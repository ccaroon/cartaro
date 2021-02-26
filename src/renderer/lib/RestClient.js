import axios from 'axios'

const BASE_URL = 'http://127.0.0.1:4242'

function RestClient (resource) {
  this.resource = resource
}

RestClient.prototype.create = function (obj, handlers) {
  var p = axios.post(`${BASE_URL}/${this.resource}/`, obj)
  this.__resolve(p, handlers)
}

RestClient.prototype.update = function (obj, handlers) {
  var p = axios.put(`${BASE_URL}/${this.resource}/${obj.id}`, obj)
  this.__resolve(p, handlers)
}

RestClient.prototype.fetch = function (query, endpoint = '/', handlers) {
  var filters = []
  for (const [key, value] of Object.entries(query)) {
    filters.push(`${key}=${value}`)
  }
  var qs = filters.join('&')

  var p = axios.get(`${BASE_URL}/${this.resource}${endpoint}?${qs}`)
  this.__resolve(p, handlers)
}

RestClient.prototype.delete = function (obj, handlers) {
  var p = axios.delete(`${BASE_URL}/${this.resource}/${obj.id}`)
  this.__resolve(p, handlers)
}

RestClient.prototype.__resolve = function (promise, handlers) {
  promise
    .then(resp => {
      if (handlers.onSuccess) {
        handlers.onSuccess(resp)
      }
    })
    .catch(err => {
      if (handlers.onError) {
        handlers.onError(err)
      }
      this.handleError(err)
    })
}

RestClient.prototype.handleError = function (err) {
  if (err.response) {
    console.log(`${err.response.status} - ${err.response.data.error}`)
  } else {
    console.log(err)
  }
}

export default RestClient
