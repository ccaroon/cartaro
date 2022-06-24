import axios from 'axios'

import config from '../../Config'
// -----------------------------------------------------------------------------
class RestClient {
  resource = null

  static HOST = 'http://127.0.0.1'
  static PORT = config.get('server:port', 4242)

  constructor(resource) {
    this.resource = resource
  }

  static baseUrl () {
    return `${this.HOST}:${this.PORT}`
  }

  dataName () {
    return this.resource.split('/').pop()
  }

  create (obj) {
    const p = axios.post(`${RestClient.baseUrl()}/${this.resource}/`, obj)
    return p
  }

  update (obj) {
    const p = axios.put(`${RestClient.baseUrl()}/${this.resource}/${obj.id}`, obj)
    return p
  }

  fetch (query, endpoint = '/') {
    const filters = []
    let key, value
    for ([key, value] of Object.entries(query)) {
      filters.push(`${key}=${value}`)
    }
    const qs = filters.join('&')

    const p = axios.get(`${RestClient.baseUrl()}/${this.resource}${endpoint}?${qs}`)
    return p
  }

  delete (obj, safe = false) {
    const safeDel = safe ? 1 : 0
    const p = axios.delete(`${RestClient.baseUrl()}/${this.resource}/${obj.id}?safe=${safeDel}`)
    return p
  }

  undelete (obj) {
    const p = axios.put(`${RestClient.baseUrl()}/${this.resource}/undelete/${obj.id}`)
    return p
  }
}
// -----------------------------------------------------------------------------
export default RestClient
