Tests {{build.number}} for repo {{repo.name}} on {{commit.branch}}:

{{#success build.status}}
Status: succeeded.
{{else}}
Status: failed.
{{/success}}

Results: {{build.link}}
