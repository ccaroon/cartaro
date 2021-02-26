# Release Process

0. In working branch
1. Update CHANGELOG.MD entry
   - Version
   - Release Date
   - Entry Contents
2. Update package.json
   - codename
3. `git commit -a`
4. Squash commits, if desired.
5. GitHub: Create PR from working branch --> `master`
6. GitHub: Merge PR to `master`
7. `git checkout master`
8. `git up origin`
9.  `npm version <patch|minor|fullVersion>` (As appropriate)
10. `git push origin master`
11. `git push --tags`
