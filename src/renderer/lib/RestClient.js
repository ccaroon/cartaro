import axios from 'axios'

import config from '../../Config'
// -----------------------------------------------------------------------------
class RestClient {
  resource = null

  static HOST = 'http://127.0.0.1'

  constructor(resource) {
    this.resource = resource
  }

  __baseUrl () {
    return `${RestClient.HOST}:${config.getTransient('serverPort')}`
  }

  create (obj, options = {}) {
    var p = axios.post(`${this.__baseUrl()}/${this.resource}/`, obj)
    return this.__resolve(p, options)
  }

  update (obj, options = {}) {
    var p = axios.put(`${this.__baseUrl()}/${this.resource}/${obj.id}`, obj)
    return this.__resolve(p, options)
  }

  fetch (query, endpoint = '/', options = {}) {
    var filters = []
    for (const [key, value] of Object.entries(query)) {
      filters.push(`${key}=${value}`)
    }
    var qs = filters.join('&')

    console.log(`baseUrl: ${this.__baseUrl()}`)

    var p = axios.get(`${this.__baseUrl()}/${this.resource}${endpoint}?${qs}`)
    return this.__resolve(p, options)
  }

  delete (obj, options) {
    var url = `${this.__baseUrl()}/${this.resource}/${obj.id}`
    if ('safe' in options) {
      url += `?safe=${options.safe}`
    }

    const p = axios.delete(url)
    return this.__resolve(p, options)
  }

  __resolve (promise, options) {
    var resolvedVal = true

    if (options.asPromise) {
      resolvedVal = promise
    } else {
      const handlers = 'handlers' in options ? options.handlers : {}
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
          this.__handleError(err)
        })
    }

    return resolvedVal
  }

  __handleError (err) {
    if (err.response) {
      console.log(`${err.response.status} - ${err.response.data.error}`)
    } else {
      console.log(err)
    }
  }
}
// -----------------------------------------------------------------------------
export default RestClient
