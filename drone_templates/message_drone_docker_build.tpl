Docker build {{build.number}} for repo {{repo.name}} on {{commit.branch}}:

{{#success build.status}}
Status: \xE2\x9C\x85 succeeded.
{{else}}
Status: \xE2\x9D\x8C failed.
{{/success}}

Results: {{build.link}}
