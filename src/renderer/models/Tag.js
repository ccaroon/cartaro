import Resource from './Resource'

// -----------------------------------------------------------------------------
class Tag extends Resource {
  static RESOURCE_NAME = 'tags'

  static loadAll (handlers) {
    this.fetch({}, '/', {
      handlers: {
        onSuccess: (objs) => {
          // Want a list of tag names, not full Tag objects
          const tags = objs.map(tag => tag.name)
          handlers.onSuccess(tags)
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
export default Tag
