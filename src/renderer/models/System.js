import Resource from './Resource'

// -----------------------------------------------------------------------------
class System extends Resource {
  static RESOURCE_NAME = 'sys'

  static versionInfo (handlers) {
    this.fetch({}, '/version', {
      handlers: {
        onSuccess: (data) => {
          handlers.onSuccess(data)
        },
        onError: handlers.onError
      }
    })
  }

  toString () {
    return this.name
  }
}
// -----------------------------------------------------------------------------
export default System
