import Resource from './Resource'
// -----------------------------------------------------------------------------
class Note extends Resource {
  static RESOURCE_NAME = 'notes'

  toString () {
    return this.title
  }
}
// -----------------------------------------------------------------------------
export default Note
