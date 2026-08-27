# Reviewing standard-name batches

Review the physics meaning first. You may edit names and documentation freely
in the pull request when a quantity is misidentified, underspecified, or
described inaccurately. Do not spend review time imitating the catalog's
spelling, grammar, link, or prose conventions: make the scientifically correct
change and let the Standard Names pipeline hold the style line.

Every reviewer edit passes back through the same grammar validation and
independent name or documentation review used before publication. A compliant
edit is approved. An edit that does not satisfy those rules is recorded as
contested for explicit human resolution; it is never silently accepted or
silently rewritten.

Approval has a precise provenance meaning. Merging the pull request says that
unchanged entries were reviewed and approved as presented, and that committed
edits express the reviewer's intended physics correction. The subsequent
approval operation records the pull-request URL and number, merge commit, and
approval time against each result. Entries untouched during review are
promoted from accepted to approved; edited entries earn approval only after
their pipeline re-review passes.

Keep commit subjects and the pull-request title short and human-readable: name
what the batch is in words. Use a brief prose body for its scope and review
intent. Do not paste an entry list into either surface; the diff is the
authoritative inventory.
