# Release Flow

## Stages

1. Plan: set release date
2. Freeze: freeze codes into a public release branch e.g.: "release/v0.3.0", based on develop branch
3. Test: test & bug-fix, prepare changelog & release nodes
4. Release: merge release branch into master and push tags
5. Announcements: send mail to the mailing lists

## Release Checklist

1. Create a release branch: `$ git flow release start v0.3.0` (required [git-flow](https://github.com/nviE/gitflow/wiki/Installation))
2. Bump version file: `$ make bump-version-file part=[major|minor|patch]`
3. Update changelog: `$ make changelog-auto` and edit CHANGELOG.md
4. Commit version file and changelog: `$ make commit-release-notes`
5. Publish the release branch: `$ git flow release publish v0.3.0`
6. Send a WIP PR: `$ make send-pull-request` and wait for feedback
7. Merge WIP PR into master branch
8. Create a version tag on master branch： `$ make add-release-tag`
9. Push tags: `$ git push origin --tags`
All done !
