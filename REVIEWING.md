# Reviewing standard-name batches

Review the physics meaning first. When a quantity is misidentified,
underspecified, or described inaccurately, say so — in whichever of the four
forms below is least effort for you. Do not spend review time imitating the
catalog's spelling, grammar, link, or prose conventions: make the
scientifically correct point and let the Standard Names pipeline hold the
style line.

An edit you commit to the branch is only one of the accepted review forms. A
sentence typed into a comment box carries exactly the same weight and reaches
the graph by the same route. Choose the form that is quickest for you; never
suppress an objection because editing the YAML looks like work.

## The four review forms

Each form binds a comment to the standard name it concerns in a different
way. The binding is what lets the maintainer route it without guessing.

| Review form | Where you leave it | How it binds to a name |
|---|---|---|
| **Edit in the diff** | the entry in `standard_names/<domain>.yml`, edited on the review branch or by accepting a suggestion | by position — the entry whose block you changed |
| **Comment on one entry line** | a review comment anchored to a line of the diff | by anchor — the entry whose block contains that line |
| **Comment on a whole domain file** | a file-level review comment on `standard_names/<domain>.yml` | by [the naming line](#the-naming-line) you write first |
| **General comment on the pull request** | the pull-request conversation | by [the naming line](#the-naming-line); without one it addresses the batch |

An anchored line comment needs no naming line: the anchor already identifies
the entry. Write one anyway if you are commenting from deep inside a
documentation block and want to be certain which entry you meant.

## The naming line

A file-level or pull-request-level comment has no line anchor, so it must
carry the name itself. Open the comment with exactly this line:

```
name: <standard name>
```

Standard names are unique across the whole catalog, so the name alone
identifies the entry. You never need the file, the domain, or a line number.

To raise several names in one comment, start a new paragraph for each and
repeat the naming line at the top of it. For example:

```
name: electron_temperature_at_plasma_boundary
The description says separatrix but the source binding is the outermost
closed flux surface only in limited configurations. Say which one is meant.

name: line_integrated_electron_density
Line integrated along what chord? The path has to be in the description.
```

A pull-request comment with no naming line is read as a comment on the batch
as a whole — its scope, its cut, its exclusions — and is answered by the
maintainer in the thread rather than routed to any entry.

## When the objection is to the name, not the prose

Say so explicitly, and propose the replacement spelling when you can:

```
name: <current standard name>
rename to: <proposed standard name>
```

Follow it with one or two sentences on the physics distinction the proposed
spelling carries that the current one does not. That sentence is the part
that survives; the spelling can be adjusted around it.

If you know the name is wrong but cannot supply a better one, write the
naming line and then say what the name must distinguish — for example, *this
name must distinguish the volume-averaged value from the magnetic-axis
value*. The maintainer drafts the successor spelling and brings it back to
you in the same thread.

A rename is not a prose fix. It changes the entry's identity, so it re-enters
grammar validation and the independent naming review, and it may be refused
where a prose correction would not be. A refused proposal is not discarded:
it is recorded contested with the rejected spelling written beside the
accepted one and the semantic distinction stated in plain language, and it is
resolved with you rather than around you.

## How a comment reaches the graph

No bot reads your comments. A maintainer does, and turns each one into either
a governed edit on the review branch or a review request against the named
entry. They then reply in your thread saying which, so you can see what your
comment became.

Every route converges: an edit you made yourself and an edit a maintainer
made from your comment both pass through the same grammar validation and the
same independent name-or-documentation review used before publication. A
compliant edit is approved. An edit that does not satisfy those rules is
recorded as contested for explicit human resolution; it is never silently
accepted and never silently rewritten. The four forms therefore differ only
in where you type them.

## What happens to a comment that cannot be acted on

Nothing is dropped in silence. A comment the maintainer cannot act on ends in
one of three visible outcomes, each written into your thread:

- **Out of scope for this batch.** The point is right but the fix reaches
  past this cut — a source binding to repair, a name not in this batch, a
  Data Dictionary defect. The comment is recorded as a follow-on against the
  named entry and the entry is held back from approval rather than approved
  over your objection. The reply carries the pointer to that follow-on.
- **Machine-owned field.** The reply names the authority that owns the value
  (see [what reviewers may change](#what-reviewers-may-change)). If the value
  itself is wrong, the objection is carried upstream against that authority
  and the reply says where it went. Your judgement about the name and the
  prose is untouched.
- **Cannot be routed.** No naming line, and no entry can be inferred from the
  text. The maintainer asks once in the thread for the naming line. If the
  batch merges before you answer, the comment is copied verbatim into the
  merge record and the entries it might have concerned are approved as
  proposed — the objection survives the merge and can be reopened against the
  named entry at any time.

## What reviewers may change

You are invited to change the standard name itself and its description and
documentation prose. These are the parts that carry the physics judgement the
review exists to capture, so make them scientifically correct and complete.

The entry you are reading holds four fields and no more: the name, the
description, the documentation, and the unit. Three of them are yours. The
unit is machine-owned — it is taken from the Data Dictionary, never from an
author — and it is in the file so that you can judge the prose against the
physical quantity it describes.

Every other field the catalog holds about a name is machine-owned, and none of
it is in the file you edit. It is carried per name in the `catalog.yml` sidecar
beside the domain files: the entry kind and its lifecycle status, its physics
domain, its source bindings (whose kind, ref, and version preserve the exact
source of the entry), its cross-reference links, and the identity roles
generated from the name. The sidecar is regenerated in full by every export, so
a hand edit to it is overwritten rather than reviewed. If one of those values
looks wrong, say so in a comment: the reply names the authority that owns the
value and the objection is carried there.

The domain file's structure and formatting are generated too. That includes
entry ordering, blank-line separation, and key order.

If a machine-owned field is changed anyway, continuous integration flags the
pull request and the change is not carried into the graph — the check that
does this is
[`.github/scripts/review_edit_guard.py`](.github/scripts/review_edit_guard.py).
This protects you from silently breaking provenance; it does not restrict
your judgement about the physics expressed by the standard name or its prose.

Prefer a comment to an edit whenever the correct value is not obvious to you.
A comment costs the review nothing and cannot break the guard.

## What merging means

When the pull request merges, every entry that no reviewer edited and no
reviewer commented on is approved as proposed. Every entry that a reviewer
edited goes back through the naming and review checks before it can be
approved. Every entry a reviewer commented on is dispositioned first, by one
of the routes above, and its comment thread records the outcome. If an edit
fails those checks, it is marked contested and resolved separately.

Keep commit subjects and the pull-request title short and human-readable:
name what the batch is in words. Use a brief prose body for its scope and
review intent. Do not paste an entry list into either surface; the diff is
the authoritative inventory.

## Where the pieces live

The published catalog and every entry's rendered page are on the
[catalog site](https://simon-mcintosh.github.io/imas-standard-names-catalog/);
each review pull request carries its own preview address in its body. The
repository layout and the CI workflows are described in
[`README.md`](README.md), and the rules for the catalog data itself in
[`AGENTS.md`](AGENTS.md). The YAML in this repository is generated from the
[imas-codex](https://github.com/Simon-McIntosh/imas-codex) knowledge graph,
which is where reviewed names and reviewed prose are folded back.
