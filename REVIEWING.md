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

When the pull request merges, every entry that a reviewer did not edit is
approved as proposed. Every entry that a reviewer edited goes back through
the naming and review checks before it can be approved. If an edit fails
those checks, it is marked contested and resolved separately.

## What reviewers may change

You are invited to change the standard name itself and its description and
documentation prose. These are the parts that carry the physics judgement the
review exists to capture, so make them scientifically correct and complete.

Other fields are machine-owned and must not be edited by hand. The unit is
taken from the Data Dictionary, never from an author. The entry kind and status
are assigned by the catalog tools. Every source binding field is also
machine-owned: its kind, ref, and version preserve the exact source of the
entry. The identity roles are generated from the name. The file's structure
and formatting are generated too.
That includes entry ordering, blank-line separation, and key order.

If a machine-owned field is changed anyway, continuous integration flags the
pull request and the change is not carried into the graph. This protects you
from silently breaking provenance; it does not restrict your judgement about
the physics expressed by the standard name or its prose.

Keep commit subjects and the pull-request title short and human-readable: name
what the batch is in words. Use a brief prose body for its scope and review
intent. Do not paste an entry list into either surface; the diff is the
authoritative inventory.
