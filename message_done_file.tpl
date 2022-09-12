Build {{build.number}} for {{repo.name}} on {{commit.branch}}

{{#success build.status}}
  Status: succeeded.
{{else}}
  Status: failed.
{{/success}}

Results: {{build.link}}