import RestClient from '../lib/RestClient'
// -----------------------------------------------------------------------------
class Resource {
  static CLIENT = null

  constructor(data) {
    Object.assign(this, data)

    this.client = this.constructor.getClient()
  }

  static getClient () {
    if (this.CLIENT === null) {
      console.log(`Creating new RestClient(${this.RESOURCE_NAME})`)
      this.CLIENT = new RestClient(this.RESOURCE_NAME)
    }
    return this.CLIENT
  }

  static fetch (query, endpoint = '/', options = {}) {
    const client = this.getClient()

    return client.fetch(query, endpoint, {
      handlers: {
        onSuccess: (resp) => {
          var items = []
          resp.data[client.resource].forEach(data => {
            items.push(new this(data))
          })
          options.handlers.onSuccess(items, resp.data.total)
        },
        onError: options.handlers.onError
      }
    })
  }

  create (options = {}) {
    return this.client.create(this, options)
  }

  update (options = {}) {
    return this.client.update(this, options)
  }

  save (options = {}) {
    if (this.id) {
      return this.update(options)
    } else {
      return this.create(options)
    }
  }

  delete (options = {}) {
    return this.client.delete(this, options)
  }
}
// -----------------------------------------------------------------------------
export default Resource
