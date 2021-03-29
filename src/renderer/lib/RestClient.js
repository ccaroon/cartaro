import axios from 'axios'

import config from '../../Config'
// -----------------------------------------------------------------------------
class RestClient {
  resource = null

  static HOST = 'http://127.0.0.1'
  static PORT = config.get('serverPort', 4242)

  constructor(resource) {
    this.resource = resource
  }

  static baseUrl () {
    return `${this.HOST}:${this.PORT}`
  }

  create (obj, options = {}) {
    const p = axios.post(`${RestClient.baseUrl()}/${this.resource}/`, obj)
    return this.__resolve(p, options)
  }

  update (obj, options = {}) {
    const p = axios.put(`${RestClient.baseUrl()}/${this.resource}/${obj.id}`, obj)
    return this.__resolve(p, options)
  }

  fetch (query, endpoint = '/', options = {}) {
    const filters = []
    let key, value
    for ([key, value] of Object.entries(query)) {
      filters.push(`${key}=${value}`)
    }
    const qs = filters.join('&')

    const p = axios.get(`${RestClient.baseUrl()}/${this.resource}${endpoint}?${qs}`)
    return this.__resolve(p, options)
  }

  delete (obj, options) {
    let url = `${RestClient.baseUrl()}/${this.resource}/${obj.id}`
    if ('safe' in options) {
      url += `?safe=${options.safe}`
    }

    const p = axios.delete(url)
    return this.__resolve(p, options)
  }

  undelete (obj, options = {}) {
    const p = axios.put(`${RestClient.baseUrl()}/${this.resource}/undelete/${obj.id}`)
    return this.__resolve(p, options)
  }

  __resolve (promise, options) {
    let resolvedVal = true

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
