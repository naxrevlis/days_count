
Tests {{build.number}} for repo {{repo.name}} on {{commit.branch}}:

{{#success build.status}}
Status: :white_check_mark: succeeded.
{{else}}
Status: :x: failed.
{{/success}}

Results: {{build.link}}