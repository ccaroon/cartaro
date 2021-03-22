import Resource from './Resource'
// -----------------------------------------------------------------------------
class LogEntry extends Resource {
  static RESOURCE_NAME = 'log_entries'

  toString () {
    return this.subject
  }
}
// -----------------------------------------------------------------------------
export default LogEntry
