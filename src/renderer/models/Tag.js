import Resource from './Resource'

// -----------------------------------------------------------------------------
class Tag extends Resource {
  static RESOURCE_NAME = 'tags'

  static loadAll (handlers) {
    this.fetch({}, '/', {
      handlers: {
        onSuccess: (objs) => {
          // Want a list of tag names, not full Tag objects
          var tags = objs.map(tag => tag.name)
          handlers.onSuccess(tags)
        },
        onError: handlers.onError
      }
    })
  }
}
// -----------------------------------------------------------------------------
export default Tag
