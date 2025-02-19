// -----------------------------------------------------------------------------
class Icon {
  static MIN_MATCH_LEN = 3
  static SKIP_WORDS = [
    'a', 'the', 'but', 'and', 'or', 'do', 'then', 'of', 'to', 'for', 'in', 'as'
  ]

  static ICONS = [
    //  -- A --
    { icon: new Icon('Account', 'mdi-credit-card-details'), keywords: [] },
    { icon: new Icon('Alien', 'mdi-alien'), keywords: [] },
    { icon: new Icon('Amazon', 'mdi-aws'), keywords: ['aws'] },
    { icon: new Icon('Ansible', 'mdi-ansible'), keywords: [] },
    { icon: new Icon('API', 'mdi-api'), keywords: [] },
    { icon: new Icon('Apple', 'mdi-apple'), keywords: [] },
    { icon: new Icon('Application', 'mdi-application-outline'), keywords: ['app'] },
    { icon: new Icon('Artifactory', 'mdi-package'), keywords: [] },

    // -- B --
    { icon: new Icon('Banzai', 'mdi-surfing'), keywords: ['surf', 'surfing'] },
    { icon: new Icon('Bash', 'mdi-bash'), keywords: ['shell'] },
    { icon: new Icon('BitBucket', 'mdi-bitbucket'), keywords: ['stash'] },
    { icon: new Icon('Books', 'mdi-book-open-variant'), keywords: ['book'] },
    { icon: new Icon('Brain', 'mdi-brain'), keywords: ['mindtap', 'think'] },
    { icon: new Icon('Branch', 'mdi-source-branch'), keywords: ['branches'] },
    { icon: new Icon('Bug', 'mdi-bug'), keywords: ['bugs'] },
    { icon: new Icon('Cake', 'mdi-cake-variant'), keywords: ['birthday'] },

    // -- C --
    { icon: new Icon('C', 'mdi-language-c'), keywords: [] },
    { icon: new Icon('C++', 'mdi-language-cpp'), keywords: [] },
    { icon: new Icon('Cake', 'mdi-cake-variant'), keywords: ['birthday'] },
    { icon: new Icon('Cancel', 'mdi-cancel'), keywords: ['blocked'] },
    { icon: new Icon('Celebration', 'mdi-party-popper'), keywords: ['celebrate', 'anniversary', 'party'] },
    { icon: new Icon('CentOS', 'mdi-centos'), keywords: ['centos7'] },
    { icon: new Icon('Cloud', 'mdi-cloud'), keywords: [] },
    { icon: new Icon('Code', 'mdi-code-braces'), keywords: ['coding', 'development', 'programming'] },
    { icon: new Icon('Coffee', 'mdi-coffee'), keywords: ['cuppa'] },
    { icon: new Icon('Cog', 'mdi-cog'), keywords: ['configs', 'settings', 'operational'] },
    { icon: new Icon('Contacts', 'mdi-contacts'), keywords: ['ldap', 'ad', 'active directory'] },
    { icon: new Icon('Content', 'mdi-card-text'), keywords: ['text', 'blot'] },
    { icon: new Icon('Credentials', 'mdi-credit-card'), keywords: ['creds'] },
    { icon: new Icon('CSS', 'mdi-language-css3'), keywords: ['css3'] },

    // -- D --
    { icon: new Icon('Databases', 'mdi-database'), keywords: ['DB', 'sql', 'mysql', 'postgresql', 'redis', 'mongodb'] },
    { icon: new Icon('Debian', 'mdi-debian'), keywords: [] },
    { icon: new Icon('Deleted', 'mdi-close-octagon'), keywords: ['removed'] },
    { icon: new Icon('Disaster', 'mdi-flash-alert'), keywords: ['dr', 'disaster-recovery'] },
    { icon: new Icon('DNS', 'mdi-dns'), keywords: ['infoblox', 'route53'] },
    { icon: new Icon('Docker', 'mdi-docker'), keywords: [] },
    { icon: new Icon('Dots', 'mdi-dots-horizontal'), keywords: ['other', 'misc'] },
    { icon: new Icon('DST', 'mdi-brightness-6'), keywords: ['daylight-savings-time'] },

    // -- E --
    { icon: new Icon('Earth', 'mdi-earth'), keywords: ['world', 'planet'] },
    { icon: new Icon('Education Book', 'mdi-book-education'), keywords: ['cengage'] },
    { icon: new Icon('Electronics', 'mdi-raspberrypi'), keywords: ['raspi'] },
    { icon: new Icon('Employee', 'mdi-card-account-details'), keywords: [] },
    { icon: new Icon('Errors', 'mdi-alert-octagon'), keywords: [] },
    { icon: new Icon('Events', 'mdi-calendar-star'), keywords: [] },

    // -- F --
    { icon: new Icon('F5', 'mdi-keyboard-f5'), keywords: ['bigip'] },
    { icon: new Icon('Fishing', 'mdi-fish'), keywords: ['fish', 'ghoti'] },
    { icon: new Icon('Flag', 'mdi-flag-variant'), keywords: ['independence'] },
    { icon: new Icon('Flower', 'mdi-flower'), keywords: ['spring'] },
    { icon: new Icon('Food', 'mdi-food-fork-drink'), keywords: ['lunch', 'drink', 'snack'] },
    { icon: new Icon('Frog', 'fa-frog'), keywords: ['jfrog'] },
    { icon: new Icon('Function', 'mdi-function-variant'), keywords: ['method', 'algorithm', 'algorithms'] },

    // -- G --
    { icon: new Icon('Git', 'mdi-git'), keywords: [] },
    { icon: new Icon('GitHub', 'mdi-github'), keywords: [] },
    { icon: new Icon('Goal', 'mdi-flag-checkered'), keywords: ['goals'] },
    { icon: new Icon('GoLang', 'mdi-language-go'), keywords: [] },
    { icon: new Icon('Google', 'mdi-google'), keywords: [] },

    // --H --
    { icon: new Icon('Halloween', 'mdi-halloween'), keywords: ['jack-o-lantern'] },
    { icon: new Icon('Harddrives', 'mdi-harddisk'), keywords: ['harddisks', 'hard-disks', 'HD', 'HDD', 'hard-drives'] },
    { icon: new Icon('Health-Check', 'mdi-heart-pulse'), keywords: ['healthcheck'] },
    { icon: new Icon('Health', 'mdi-bottle-tonic-plus-outline'), keywords: ['wellness'] },
    { icon: new Icon('Heart', 'mdi-heart'), keywords: ['love', 'valentine', 'valentine\'s'] },
    { icon: new Icon('Hello', 'mdi-human-greeting-variant'), keywords: [] },
    { icon: new Icon('Holiday', 'mdi-flag-variant'), keywords: [] },
    { icon: new Icon('HTML', 'mdi-language-html5'), keywords: ['html5'] },

    // -- I --

    // -- J --
    { icon: new Icon('Java', 'mdi-language-java'), keywords: [] },
    { icon: new Icon('JavaScript', 'mdi-language-javascript'), keywords: ['ecma'] },
    { icon: new Icon('Jira', 'mdi-jira'), keywords: [] },
    { icon: new Icon('jQuery', 'mdi-jquery'), keywords: [] },
    { icon: new Icon('JSON', 'mdi-code-json'), keywords: ['json'] },

    // -- K --
    { icon: new Icon('Key', 'mdi-key'), keywords: [] },
    { icon: new Icon('King', 'mdi-chess-king'), keywords: ['mlk'] },

    // -- L --
    { icon: new Icon('Laptop', 'mdi-laptop'), keywords: ['computer'] },
    { icon: new Icon('Leaf', 'mdi-leaf-maple'), keywords: ['fall'] },
    { icon: new Icon('Learn', 'mdi-school'), keywords: ['learning'] },
    { icon: new Icon('License', 'mdi-license'), keywords: [] },
    { icon: new Icon('Log', 'mdi-math-log'), keywords: ['splunk'] },

    // -- M --
    { icon: new Icon('MacIntosh', 'mdi-apple-finder'), keywords: ['macos'] },
    { icon: new Icon('Magic', 'mdi-magic-staff'), keywords: [] },
    {
      icon: new Icon('Managers', 'mdi-account-tie'), keywords: ['boss', 'cto', 'cfo', 'ceo', 'manager', 'leader']
    },
    { icon: new Icon('Map', 'mdi-map-legend'), keywords: ['cartaro'] },
    { icon: new Icon('Markdown', 'mdi-language-markdown'), keywords: [] },
    { icon: new Icon('Marked Off', 'mdi-check-decagram'), keywords: [] },
    { icon: new Icon('Medical', 'mdi-medical-bag'), keywords: ['doctor', 'dr', 'open enrollment'] },
    { icon: new Icon('Medicine', 'mdi-pill'), keywords: [] },
    { icon: new Icon('Meeting', 'mdi-calendar-star'), keywords: [] },
    { icon: new Icon('Memory', 'mdi-memory'), keywords: ['mem', 'ram'] },
    { icon: new Icon('Misc', 'mdi-dots-horizontal'), keywords: [] },
    { icon: new Icon('Monitoring', 'mdi-monitor-dashboard'), keywords: ['logicmonitor', 'dashboard'] },
    { icon: new Icon('Moon', 'mdi-moon-waning-crescent'), keywords: [] },
    { icon: new Icon('Mostly Harmless', 'mdi-earth-off'), keywords: ['mostly harmless'] },
    { icon: new Icon('Mother', 'mdi-mother-heart'), keywords: ['mother', 'mother-s', 'mom', 'mum'] },

    // -- N --
    { icon: new Icon('Network', 'mdi-lan-connect'), keywords: ['internet'] },
    { icon: new Icon('NodeJS', 'mdi-nodejs'), keywords: ['node.js'] },
    { icon: new Icon('Notebook', 'mdi-notebook-outline'), keywords: [] },
    { icon: new Icon('Notes', 'mdi-note'), keywords: [] },
    { icon: new Icon('NPM', 'mdi-npm'), keywords: ['package.json'] },

    // -- O --
    { icon: new Icon('One up', 'mdi-one-up'), keywords: ['bonus', 'extra'] },
    { icon: new Icon('Outlook', 'mdi-microsoft-outlook'), keywords: [] },

    // -- P --
    { icon: new Icon('Package', 'mdi-package-variant'), keywords: ['yum', 'rpm', 'deb', 'apt', 'tar', 'tgz', 'zip'] },
    { icon: new Icon('Party', 'mdi-party-popper'), keywords: ['new year\'s'] },
    { icon: new Icon('Password', 'mdi-form-textbox-password'), keywords: [] },
    { icon: new Icon('Penguin', 'mdi-penguin'), keywords: ['linux'] },
    { icon: new Icon('People', 'mdi-account-group'), keywords: ['team', 'presidents\''] },
    { icon: new Icon('Phone', 'mdi-cellphone'), keywords: ['cellphone', 'iphone'] },
    { icon: new Icon('PHP', 'mdi-language-php'), keywords: [] },
    { icon: new Icon('Pipeline', 'mdi-pipe'), keywords: ['harness'] },
    { icon: new Icon('Python', 'mdi-language-python'), keywords: ['python2', 'python3'] },

    // -- Q --

    // -- R --
    { icon: new Icon('RedHat', 'mdi-redhat'), keywords: [] },
    { icon: new Icon('Reports', 'mdi-file-chart'), keywords: ['reporting', 'chart'] },
    { icon: new Icon('Rolling Deployment', 'mdi-rotate-right'), keywords: ['rolling', 'inplace'] },

    // -- S --
    { icon: new Icon('Safe', 'mdi-safe-square-outline'), keywords: ['vault', 'hashicorp-vault'] },
    { icon: new Icon('Script', 'mdi-script-text-outline'), keywords: ['perl'] },
    { icon: new Icon('Search', 'mdi-magnify'), keywords: ['find', 'lookup', 'solr'] },
    { icon: new Icon('Secret', 'mdi-eye-off'), keywords: [] },
    { icon: new Icon('Server', 'mdi-server'), keywords: ['instance'] },
    { icon: new Icon('Sick', 'mdi-emoticon-sick'), keywords: [] },
    { icon: new Icon('Skull', 'mdi-skull'), keywords: ['friday-the-13th'] },
    { icon: new Icon('Slack', 'mdi-slack'), keywords: [] },
    { icon: new Icon('Snowflake', 'mdi-snowflake'), keywords: ['snow', 'winter', 'unique'] },
    { icon: new Icon('Space Invaders', 'mdi-space-invaders'), keywords: ['space invaders', 'space-invaders', 'spacelift'] },
    { icon: new Icon('Space Station', 'mdi-space-station'), keywords: ['space station', 'space-station'] },
    { icon: new Icon('SSH', 'mdi-ssh'), keywords: ['scp'] },
    { icon: new Icon('Story', 'mdi-bookmark'), keywords: [] },
    { icon: new Icon('Sun', 'mdi-weather-sunny'), keywords: ['summer'] },
    { icon: new Icon('Support', 'mdi-face-agent'), keywords: [] },
    { icon: new Icon('Surfing', 'mdi-surfing'), keywords: ['banzai'] },
    { icon: new Icon('Swap', 'mdi-swap-horizontal-circle-outline'), keywords: ['blue-green'] },

    // -- T --
    { icon: new Icon('Task', 'mdi-checkbox-marked'), keywords: ['todo'] },
    { icon: new Icon('Teams', 'mdi-account-multiple'), keywords: ['team'] },
    { icon: new Icon('Terraform', 'mdi-terraform'), keywords: ['hashicorp-terraform'] },
    { icon: new Icon('Ticket', 'mdi-ticket-outline'), keywords: [] },
    { icon: new Icon('Token', 'mdi-star-circle'), keywords: ['token'] },
    { icon: new Icon('Tooth', 'mdi-tooth-outline'), keywords: ['dentist', 'teeth', 'dental'] },
    { icon: new Icon('Transfer', 'mdi-transfer'), keywords: ['xfer'] },
    { icon: new Icon('Tree', 'mdi-pine-tree'), keywords: ['christmas'] },
    { icon: new Icon('Tsunami', 'mdi-tsunami'), keywords: [] },
    { icon: new Icon('Turkey', 'mdi-turkey'), keywords: ['thanksgiving'] },

    // -- U --
    { icon: new Icon('Ubuntu', 'mdi-ubuntu'), keywords: [] },
    { icon: new Icon('UFO', 'mdi-ufo-outline'), keywords: ['spaceship'] },
    { icon: new Icon('Users', 'mdi-account-box'), keywords: ['user', 'username'] },

    // -- V --
    { icon: new Icon('Vacation', 'mdi-island'), keywords: ['island', 'pto'] },
    { icon: new Icon('Virus', 'mdi-virus'), keywords: ['covid', 'covid-19'] },
    { icon: new Icon('VPN', 'mdi-vpn'), keywords: [] },

    // -- W --
    { icon: new Icon('Weekly', 'mdi-calendar-range'), keywords: ['weeks', 'week'] },
    {
      icon: new Icon('Weekday', 'mdi-calendar-range'),
      keywords: [
        'monday', 'tuesday', 'wednesday', 'thursday',
        'friday', 'saturday', 'sunday'
      ]
    },
    { icon: new Icon('WiFi', 'mdi-wifi'), keywords: [] },
    { icon: new Icon('Wizard', 'mdi-wizard-hat'), keywords: [] },
    { icon: new Icon('Workday', 'mdi-calendar'), keywords: [] },
    { icon: new Icon('Workflow', 'mdi-sitemap'), keywords: [] },

    // -- X --
    { icon: new Icon('XRay', 'mdi-radiology-box'), keywords: [] },

    // -- Y --
    { icon: new Icon('YAML', 'mdi-language-xaml'), keywords: ['yaml', 'yml'] },
    { icon: new Icon('Year', 'mdi-calendar-multiple'), keywords: ['yearly'] }

    // -- Z --
  ]

  name = null
  code = null
  constructor (name, code) {
    this.name = name
    this.code = code
  }

  static superSearch (searchTerms, defaultIcon = null, options = {}) {
    let foundIcon = null
    let termsIsArray = false
    let parts = null

    if (searchTerms instanceof Array) {
      termsIsArray = true
    }

    // --Longest String Match--
    // Check entire searchTerms string for a match...
    // ...if not found decrease searchTerms length by 1 word
    // ...keep trying until it's just a single word
    // ** Example **
    // Start: "Open Enrollment 2021"
    // -----> "Open Enrollment"
    // -----> "Open"
    // -----> END
    // I.e. Find a match for the longest possible "whole" string
    if (!termsIsArray) {
      parts = searchTerms.split(options.sep || ' ')
      do {
        const searchTerm = parts.join(options.sep || ' ')
        foundIcon = this.search(searchTerm)
        parts.pop()
      } while (parts.length >= 1 && !foundIcon)
    }

    // --Keyword Match--
    // Look for a match by using each word in the
    // searchTerms as a keyword
    if (!foundIcon) {
      parts = termsIsArray ? searchTerms : searchTerms.split(options.sep || ' ')
      for (let i = 0; i < parts.length; i++) {
        foundIcon = this.search(parts[i])
        if (foundIcon) {
          break
        }
      }
    }

    // --No Match--
    // Use default
    if (!foundIcon && defaultIcon) {
      foundIcon = new Icon('Default', defaultIcon)
    }

    return foundIcon
  }

  static get (name, defaultIcon = null) {
    let foundData = this.ICONS.find((iconData) => {
      if (iconData.icon.name.toLowerCase() === name.toLowerCase()) {
        return true
      } else {
        return false
      }
    })

    if (!foundData && defaultIcon) {
      foundData = { icon: new Icon('Default', defaultIcon) }
    }

    return foundData ? foundData.icon : null
  }

  static normalize (name) {
    return name.replaceAll(/\W/g, '-')
  }

  static search (name, defaultIcon = null) {
    let foundData = null
    const searchName = this.normalize(name)

    if (searchName.length >= this.MIN_MATCH_LEN && !this.SKIP_WORDS.includes(searchName.toLowerCase())) {
      const pattern = new RegExp(`^${searchName}$`, 'i')
      foundData = this.ICONS.find((iconData) => {
        if (iconData.icon.name.match(pattern)) {
          return true
        } else {
          let foundInKw = false
          for (let j = 0; j < iconData.keywords.length; j++) {
            const keyword = this.normalize(iconData.keywords[j])
            if (keyword.match(pattern)) {
              foundInKw = true
              break
            }
          }
          return foundInKw
        }
      })
    }

    if (!foundData && defaultIcon) {
      foundData = { icon: new Icon(name, defaultIcon) }
    }

    return foundData ? foundData.icon : null
  }

  toString () {
    return this.code
  }
}
// -----------------------------------------------------------------------------
export default Icon
