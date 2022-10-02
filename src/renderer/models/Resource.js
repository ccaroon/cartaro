import RestClient from '../lib/RestClient'
// -----------------------------------------------------------------------------
class Resource {
  static CLIENT = null

  constructor (data) {
    Object.assign(this, data)

    this.client = this.constructor.getClient()
  }

  static getClient () {
    if (this.CLIENT === null) {
      this.CLIENT = new RestClient(this.RESOURCE_NAME)
    }
    return this.CLIENT
  }

  exists (fields, options = {}) {
    const query = {
      pp: 5,
      op: 'and'
    }

    fields.forEach((fld) => {
      query[fld] = this[fld]
    })

    this.constructor.fetch(query, '/', {
      handlers: {
        onSuccess: (_, count) => {
          const exists = count > 0
          options.handlers.onSuccess(exists)
        },
        onError: options.handlers.onError
      }
    })
  }

  static fetch (query, endpoint = '/', options = {}) {
    const client = this.getClient()
    const promise = client.fetch(query, endpoint)

    options.handlers = 'handlers' in options ? options.handlers : {}

    this.__resolve(promise, {
      handlers: {
        onSuccess: (resp) => {
          let items = null
          const itemData = resp.data[client.dataName()]
          if (itemData instanceof Array) {
            items = []
            itemData.forEach(data => {
              items.push(new this(data))
            })
          } else {
            // Assume itemData is a Hash (Object)
            items = {}
            for (const [name, group] of Object.entries(itemData)) {
              const itemList = []
              group.forEach(item => {
                itemList.push(new this(item))
              })
              items[name] = itemList
            }
          }
          if (options.handlers.onSuccess) {
            options.handlers.onSuccess(items, resp.data.total)
          }
        },
        onError: options.handlers.onError
      }
    })
  }

  create (options = {}) {
    const promise = this.client.create(this)
    return this.constructor.__resolve(promise, options, (resp) => {
      this.id = resp.data.id
    })
  }

  update (options = {}) {
    const promise = this.client.update(this)
    return this.constructor.__resolve(promise, options)
  }

  save (options = {}) {
    if (this.id) {
      return this.update(options)
    } else {
      return this.create(options)
    }
  }

  delete (options = {}) {
    const promise = this.client.delete(this, options.safe)
    return this.constructor.__resolve(promise, options)
  }

  undelete (options = {}) {
    const promise = this.client.undelete(this)
    return this.constructor.__resolve(promise, options)
  }

  isDeleted () {
    return this.deleted_at !== null
  }

  static __resolve (promise, options, privateCB = null) {
    const handlers = options.handlers

    if (options.asPromise) {
      return promise
    } else {
      promise
        .then(resp => {
          if (privateCB) {
            privateCB(resp)
          }

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
  }

  static __handleError (err) {
    if (err.response) {
      console.log(`${err.response.status} - ${err.response.data.error}`)
    } else {
      console.log(err)
    }
  }
}
// -----------------------------------------------------------------------------
export default Resource
