# 08c. Hiring manager answers, and Terraform `count` → `for_each`

The hiring-manager round was testing ownership and judgment. The Terraform questions were testing whether you can change **addresses in state** without recreating machines. Syntax was the prop. The signal was safe production change.

Resume facts used here: Impact Analytics from **May 2026** (this interview is a few months in). Uber is **via EPAM**, July 2024–May 2026. You owned specific systems. You did not own every adjacent pipeline. Reviewers existed.

<div class="callout warn">
<b>Notice period.</b> Do not invent a number of days in the interview if you have not read the clause. The script below says you will confirm it. 26 May, from an October interview, is the <b>next</b> 26 May, which is enough calendar time for a normal notice once you have checked the letter.
</div>

---

## HM1. Introduction

**What they want:** 60–90 seconds, current role first, one proof, why this loop. Not a biography from college.

**Say this**

> I'm a backend engineer, about five years in, mostly Python and Go. I joined Impact Analytics in May 2026. I work on AssortSmart, a retail planning product. The two things I own there are the Go platform that serves planner APIs, and a batch scoring system that decides keep-or-drop for articles.
>
> On the platform side I moved the heavy planner pivots onto ClickHouse rollups. The same query on 250 million rows went from 189 seconds to 12. On the scoring side the runs are built to finish even when the model provider fails: timeouts, a circuit breaker, and checkpoints, so we don't recompute work that's already done.
>
> Before that I was at Uber via EPAM, for almost two years. I owned the Finance risk-scoping backend. Reconciliation for the quarterly audit went from 14 days to 3, on a $340 million materiality threshold. That was FastAPI and MySQL, with a small team of three on the ORM migration.
>
> Earlier I led a PHP-to-FastAPI migration at a GST invoicing company, and I started at GeeksforGeeks on a Django product.
>
> I'm here because this role is that same work at cloud scale: services that stay up, fail in a controlled way, and can be changed without a maintenance window. That's the part I want to go deeper on.

**If they cut you off at 30 seconds,** stop after the ClickHouse sentence and the Uber sentence. Do not keep listing companies.

**Assumptions:** they have the resume. Don't re-read it. Don't open with "I'm passionate."

---

## HM2. Why are you looking outside so soon after joining?

**What they are testing:** flight risk. They want to know if you will leave OCI in five months as well, and whether you are running from a problem you caused.

**The situation, said plainly.** You joined Impact Analytics in May 2026. Looking now is early. Acknowledge that in the first sentence. People who dodge the word "soon" sound like they are hiding a bad review.

**Say this**

> It's early, and I don't pretend otherwise. I joined Impact Analytics in May, and the work is real. The ClickHouse path and the scoring runs are in production. I'm not leaving because the role collapsed or because of a manager.
>
> What changed is the kind of system I want to be responsible for next. This team runs a cloud data plane: failover, deployments without a window, incidents, the boring correctness. That is the work I already reach for inside a product company, and it is the actual job here, not a side task.
>
> I didn't start the search in week two. I looked when this role was concrete. If I join, I'm not shopping again in six months. I want a longer run on one platform, which is the opposite of collecting logos.
>
> I will also not disappear on the current team. I'll finish the handover against whatever notice my contract actually specifies. I don't want to quote a day count in this room and then discover the letter says something else.

**Do not say:** the company is chaotic, the stack is boring, you were promised a title, you are underpaid, or "I'm always exploring." Do not invent a grievance.

**If they ask "does your manager know?":** "Not yet. I don't start a resignation conversation before I have a decision. I won't accept an offer and then stall the current team."

### Can you join by 26 May?

**Say this**

> Yes, I can plan around 26 May. Before I sign a start date I need to read the notice clause and tell you the exact last day in writing. If the notice is the usual 30, 60, or 90 days, 26 May is comfortable, and I would rather join earlier than make you wait until May. If something in the letter is longer, I will tell you this week, not on the day you send the offer.

**Why this shape.** "Yes" without a fake precision. A date you have not checked is how people miss a start date. Offering to come **earlier** if notice allows is the opposite of dragging it out.

**Do not** resign, give notice, or tell the current manager until there is a written offer you intend to accept.

### Likely follow-up: why OCI, not another product company?

> The job description is operability: timeouts, failover, runbooks, change management. I have been doing the application version of that. I want the platform version, where a bad default hits every tenant. Product companies will still need features first. This team is measured on the system staying up.

### Likely follow-up: why should we believe you won't do this again?

> You shouldn't believe a slogan. Look at the tenure before this: almost two years at Uber via EPAM, a year and a half at Masters, a year at GeeksforGeeks. The short one is the current role, and I'm being explicit about why this move is different. I'm also not going to pretend five months is a long stay.

---

## HM3. Was the work end-to-end yours? What was the ownership model? Who else was involved? How much autonomy?

**What they are testing:** "I" versus "we," and whether you inflate a team effort into a solo build. Senior people describe the boundary. Juniors say "I owned everything."

**The model, in one diagram**

```
you own                         shared                         not yours
---------                       ------                         ---------
design of the component         API review, PR review          HFM extract into MySQL
implementation                  on-call of the wider product   (Uber data pipeline)
the rollout of that component   prioritization with the PM     cluster-to-cluster
the numbers you can measure     security / SOX rules           allowlists at the cloud
                                                           provider (you worked
                                                           around them; you did
                                                           not own network policy)
```

**Say this**

> End to end for the component, not end to end for the company. I want to be precise about that.
>
> At Impact Analytics I own the design and the code for the planner read path on ClickHouse, the Go copy tool between clusters, and the scoring orchestration: timeouts, checkpoints, what happens when the model provider fails. I also shipped Ask Iris, the planner copilot, including the rule that tenant scope is fixed when the socket opens. I write the design, I implement it, I watch it in production. Other engineers review the PRs. I don't merge my own judgment with nobody looking.
>
> Autonomy is high on the technical choice and bounded by review and by production safety. Nobody handed me a class diagram for the rollups. I did have to justify ClickHouse against people who had measured the old system and didn't want a new database. I wrote the comparison on the same 250 million rows, and the team committed after the numbers, not before.
>
> At Uber, via EPAM, I owned the risk-scoping backend. The product already had a design doc and a finance stakeholder. I didn't invent the audit process. I replaced the spreadsheet path with a service: schema, APIs, the migration off raw SQL, and the SOX checks. I led three engineers on the SQLAlchemy migration. They owned pieces. I owned the approach, the review bar, and the rollout. The feed that loads general-ledger balances from the finance system was a data-pipeline team. I consumed that data. I didn't operate their extract.
>
> So the ownership model is: one owner for the service, reviewers on every change, and explicit edges where another team starts. I had room to choose the design. I did not have room to skip review, and I don't want that room.

**Edges to mention if they push**

| Claim | Honest boundary |
|---|---|
| ClickHouse 15.5× | Query time on a fixed harness. The 170 GB memory failure was a separate, load-time problem. |
| Go copy at ~344k rows/s | Rows per second, measured while a multi-billion-row copy was in flight. Not "the migration finished at that rate." |
| 80% accuracy | A CI gate on a 300-case set. Not live accuracy for every tenant. |
| Uber 14 days to 3 | The outcome on the reconciliation workflow I owned. Not "I did the auditors' job." |
| Led 3 / mentored 2 | FRM migration was three engineers. Masters was two people I mentored through a service extraction. Don't merge those numbers. |

### Likely follow-up: tell me about a decision you were not allowed to make alone

> Putting ClickHouse in as the system of record for planner reads. I could prototype alone. I could not commit the org alone. I separated the measured facts from the conclusion, showed that the objection was about in-place updates rather than about analytical reads, and we staged it. That is the autonomy I actually want: strong proposal, a recorded decision, then I go execute.

### Likely follow-up: conflict with a reviewer

Use the Uber repository-versus-model story, short. The team rule said all SQL lives in `repository/`. You put query methods on the ORM model so a column rename fails the type checker, after a bug where income-statement rows were read with balance-sheet column lists. You wrote the exception down, and you kept repository functions for queries that don't belong to one model. You disagreed, you didn't ignore the rule, and the exception is auditable.

---

## HM4. End-to-end ownership, from requirement to production

**Pick one story and walk the pipeline they named.** Don't switch projects in the middle. The ClickHouse pivot is the cleanest requirement-to-production arc. The Masters migration is the cleanest "no maintenance window" arc. Use ClickHouse unless they already spent the round on it.

**Requirement.** Planners run wide pivots. On Postgres those were hitting about 189 seconds at 250 million rows. The requirement was not "adopt ClickHouse." The requirement was a pivot a planner will wait for, without wrong numbers.

**Design.** Read path and write path are different. Postgres stays for roles and transactional rows. Analytical reads go to pre-aggregated ClickHouse tables, partitioned by season, so a query prunes instead of scanning the fact table. Writes are versioned inserts, not updates, because the objection to ClickHouse was its update behavior. I wrote that down before building the second table.

**Implementation.** Six rollup tables, season grain and weekly grain, for product, store, and attribute. A formula compiler so a new KPI is configuration, not a deploy: the expression is parsed, identifiers are allowlisted, and division is wrapped so a zero denominator is zero rather than an exception. The weekly build could not be one `INSERT` for a whole season. Aggregator state was around 170 GB and the query was killed. I changed the unit of work to one fiscal week, with a memory cap and disk spill. That is an implementation decision forced by a limit, not a new product feature.

**Testing.** A row-identical harness: same rows, same query, Postgres and ClickHouse, answers compared. The 189s to 12s number comes from that, not from a screenshot of one lucky query. Separately, store totals are re-weighted so they match the sum of SKUs, and I check those sums against each other.

**Deployment.** The new tables are filled per season. Readers move when a season is complete, not halfway through a load. A failed load must not look complete. I had a bug here: a half-written partition of about 64 million rows still "had rows," so a skip-if-present check would have served it. The fix is a ledger of finished seasons, and success is the server saying the query finished, not the client saying the HTTP call returned. Rollback of a bad season is drop that partition and rebuild it. I will not call that an atomic swap. A crash in the middle leaves a hole until the rebuild. The safer design is build into a side table and replace the partition. I have that written. I don't claim it is what ran.

**Production.** The read path is the one planners hit. I watch latency and whether the parity checks hold. The copy between clusters is a separate operational path, forced by network allowlists, with a checkpoint per season so a killed process resumes.

**One sentence on the other people.** Reviewers on the design and the PRs. My name is on the decision, the code, and the numbers above.

### A second walkthrough, if they want a service rollout (Masters)

Requirement: filing-week latency, p95 around 1.2s, a PHP monolith. Design: strangler, one endpoint group at a time, not a rewrite. Implementation: FastAPI behind the same gateway, async calls for the government portal, idempotency keys on bulk import. Testing: contract checks so the new response matched the old fields, plus a canary percentage. Deployment: config to shift traffic, config to shift it back. I froze cutovers on filing weeks. Production: p95 to about 300ms, and a canary where my 10-second timeout was wrong because the portal sometimes needs longer. I reverted with config, then moved that call off the request thread. That is the loop from requirement to "production disagreed with me" to a fix.

### Likely follow-up: how do you test something you cannot stage at full size?

> Compare on a slice that is identical, not on a toy. The 250 million row harness was the real shape. For the memory failure I measured one week of the heaviest tenant before I raised any limit. I would rather have one true number than a full-size run I cannot explain.

### Likely follow-up: what did you personally code versus design?

> On these, both. I don't use "owned" for a document I handed to someone else. The rollup build, the formula parser, the copy tool, and the scoring checkpoints are code I wrote. The three-engineer ORM migration at Uber was a design and a review bar, and I was in that code too. I say which is which if you ask about a line.

---

## TF5. Terraform `count` versus `for_each`

**What they are testing.** Resource **addresses**, and what happens to those addresses when the input changes. Not the syntax of a VM.

**Definitions**

- **Resource address:** the id Terraform uses in state. It is not the cloud OCID. State maps an address to an OCID (or an AWS id, or whatever the provider returns).
- **`count`:** create `count` copies. Addresses are **integers**: `oci_core_instance.app[0]`, `[1]`, `[2]`.
- **`for_each`:** create one instance per entry in a map or a set of strings. Addresses are **keys**: `oci_core_instance.app["app-1"]`.
- **State:** the JSON snapshot of address → remote object id, plus attributes. `terraform apply` reconciles the config to that snapshot, then to the cloud.
- **Plan:** a dry run. It tells you which addresses will be created, destroyed, or updated in place. If you don't read the plan, you don't know whether you are about to replace a VM.

**`count` with three instances**

```hcl
variable "app_count" {
  type    = number
  default = 3
}

resource "oci_core_instance" "app" {
  count               = var.app_count
  availability_domain = var.ad
  display_name        = "app-${count.index + 1}"   # app-1, app-2, app-3
  shape               = var.shape
  # image, subnet, metadata omitted
}
```

Addresses in state:

```
oci_core_instance.app[0]   ->  ocid1.instance...aaa     display name app-1
oci_core_instance.app[1]   ->  ocid1.instance...bbb     display name app-2
oci_core_instance.app[2]   ->  ocid1.instance...ccc     display name app-3
```

**The trap with `count`.** It is positional. Insert an element at the front, or delete `[0]`, and every later index shifts. Terraform does not know that `[1]` "is the same VM" after the shift. The plan shows **destroy and create** for instances you meant to keep. That is the production incident this question is about.

**`for_each` with the same three instances**

```hcl
variable "apps" {
  type    = set(string)
  default = ["app-1", "app-2", "app-3"]
}

resource "oci_core_instance" "app" {
  for_each            = var.apps
  availability_domain = var.ad
  display_name        = each.key
  shape               = var.shape
}
```

Addresses:

```
oci_core_instance.app["app-1"]  ->  ocid...
oci_core_instance.app["app-2"]  ->  ocid...
oci_core_instance.app["app-3"]  ->  ocid...
```

Remove `"app-2"` from the set and only `app["app-2"]` is destroyed. `app-1` and `app-3` stay. Keys are identity. Indexes are not.

**When `count` is still the right tool.** The replicas are identical and you only scale the number, and you accept that you will not delete from the middle. Even then, `for_each` over a set of names is safer the moment anyone will ever remove one specific instance.

**Sets versus maps.** `for_each` on a **set of strings** uses the string as the key. `for_each` on a **map** uses the map key. `for_each` cannot be a list of objects directly; you convert with `for_each = { for name in var.apps : name => name }` or `toset()`. Don't use a list index as the key or you have reinvented `count`.

**Referring to them**

```hcl
# count
oci_core_instance.app[0].id

# for_each
oci_core_instance.app["app-1"].id

# all of them
[for i in oci_core_instance.app : i.id]
```

**Both in one resource is illegal.** `count` and `for_each` on the same resource block conflict. The migration is a change from one meta-argument to the other, which **changes every address**. Terraform's default reading of an address change is "this object went away, that object is new."

---

## TF6. Migrate `count` to `for_each` without destroying the instances

**The goal.** Same three VMs, same disks, same OCIDs. Only the state address changes. The cloud must not see a delete.

**What has to be true**

1. The new key is stable and matches the instance you intend (`"app-1"` ↔ today's `[0]`).
2. State is rewritten so the OCID currently stored at `[0]` is stored at `["app-1"]`.
3. `terraform plan` shows **no destroy, no create**, or only in-place attribute updates you expected (for example a tag).
4. You apply only after that plan. You do not "apply and see."

**How Terraform wants you to do it today: `moved` blocks** (Terraform 1.1+)

`moved` is config, reviewed in git, applied by the next plan. It is better than a one-off CLI command because the next person can see why the address changed.

```hcl
resource "oci_core_instance" "app" {
  for_each            = toset(["app-1", "app-2", "app-3"])
  availability_domain = var.ad
  display_name        = each.key
  shape               = var.shape
}

moved {
  from = oci_core_instance.app[0]
  to   = oci_core_instance.app["app-1"]
}

moved {
  from = oci_core_instance.app[1]
  to   = oci_core_instance.app["app-2"]
}

moved {
  from = oci_core_instance.app[2]
  to   = oci_core_instance.app["app-3"]
}
```

```
state before                         state after
oci_core_instance.app[0]  ocid aaa    oci_core_instance.app["app-1"]  ocid aaa
oci_core_instance.app[1]  ocid bbb    oci_core_instance.app["app-2"]  ocid bbb
oci_core_instance.app[2]  ocid ccc    oci_core_instance.app["app-3"]  ocid ccc

cloud: nothing. The OCID does not change.
```

**The sequence**

```bash
# 1. see the current addresses
terraform state list | grep oci_core_instance.app

# 2. edit config: count -> for_each, add moved blocks
# 3. plan. Read every line.
terraform plan -out=tfplan

#    You want:
#      # oci_core_instance.app[0] has moved to oci_core_instance.app["app-1"]
#      (and the same for 1 and 2)
#    You do not want:
#      -/+ destroy and then create
#      forces replacement

# 4. only if the plan is moves and in-place updates
terraform apply tfplan
```

`terraform plan -out=tfplan` then `apply tfplan` applies **that** plan, not a new one computed later. That matters if someone else is changing the same state.

**Older equivalent, still valid:** `terraform state mv` edits state immediately, before plan. It is easier to get wrong, and it is not reviewed as a diff. Prefer `moved`.

```bash
terraform state mv 'oci_core_instance.app[0]' 'oci_core_instance.app["app-1"]'
terraform state mv 'oci_core_instance.app[1]' 'oci_core_instance.app["app-2"]'
terraform state mv 'oci_core_instance.app[2]' 'oci_core_instance.app["app-3"]'
terraform plan    # should be empty, or only drift you already understood
```

Quotes matter. The shell will eat `["app-1"]` if you don't quote the whole address.

**After a clean apply,** delete the `moved` blocks in a follow-up PR. Leaving them forever is harmless and noisy. Removing them in the **same** apply as the move is wrong: the move has to be in the configuration for the plan that performs it.

**If the plan shows destroy/create anyway,** stop. Typical causes:

| Plan says replace | Why |
|---|---|
| You changed a **ForceNew** attribute in the same edit (image id, availability domain, some shape changes) | The address move is fine, and a field you touched cannot be updated in place. Split the PRs. Move first. Change the image later, on purpose. |
| The `moved` key points at the wrong index | `app-1` would now track the OCID that used to be `[2]`. Plan may show a display-name change in place, or a replace if name is ForceNew. Fix the mapping. Look at `terraform state show 'oci_core_instance.app[0]'` and match on OCID, not on memory. |
| `for_each` key is different from `to` | Address in `moved.to` must equal the address `for_each` will produce. |
| You removed `count` and forgot a `moved` for one index | That index is a destroy. The new key is a create. |
| Provider version treats a field as ForceNew that you thought was mutable | Read the plan's "forces replacement" line. It names the field. |

**State locking.** Remote state (OCI Object Storage backend, or Terraform Cloud, or S3) with a lock. Two applies at once corrupt state. A `moved` migration is exactly when you don't want a second pipeline running.

**Prove it before production.** Same pattern I use for a schema change: the plan is the canary. If I cannot explain every destroy line, I do not apply. On Masters, traffic shifts were a config change I could undo. Here, the undo for a mistaken destroy is a restore from backup, which is not an undo.

### Likely follow-up: `terraform import` versus `moved`

`import` adopts an object that Terraform does **not** yet have in state. You use it for a VM someone created in the console. `moved` renames an object Terraform **already** manages. Using `import` for this migration would create a second state object or collide. Don't.

```bash
terraform import 'oci_core_instance.app["app-4"]' ocid1.instance.oc1...
```

Then `plan`. Imported attributes often don't match the config, so the first plan wants to change tags or metadata. Read it.

### Likely follow-up: `create_before_destroy` and `prevent_destroy`

```hcl
lifecycle {
  prevent_destroy       = true
  create_before_destroy = true
}
```

- `prevent_destroy`: apply fails if the plan would destroy this resource. A seatbelt during a refactor. It does not help you if you remove the resource block entirely in some Terraform versions without care; it **does** fail an accidental destroy caused by an address change. I would turn it on for the database and for anything with data, before the `count` migration, so a bad plan errors instead of deleting.
- `create_before_destroy`: for replacements you **intend** (a new instance, then delete the old). It needs a name or an id that can exist twice, or the create collides. It is not how you avoid a replacement. `moved` is.

### Likely follow-up: modules and indexes

If the instances live in a module, the address includes the module:

```
module.compute.oci_core_instance.app[0]
  -> module.compute.oci_core_instance.app["app-1"]
```

`moved` can also rename a whole module (`from = module.old` / `to = module.new`). Same rule: plan must be moves, not creates.

### Likely follow-up: what does a bad plan look like versus a good one?

Good:

```
# oci_core_instance.app[0] has moved to oci_core_instance.app["app-1"]
  ~ display_name = "app-0" -> "app-1"     # only if you also renamed, and only if in-place
Plan: 0 to add, 0 to change, 0 to destroy.
```

A pure move with identical attributes is 0 add, 0 change, 0 destroy, plus the "has moved" note.

Bad:

```
# oci_core_instance.app[0] will be destroyed
# oci_core_instance.app["app-1"] will be created
Plan: 1 to add, 0 to change, 1 to destroy.
```

That plan replaces the VM. You do not apply it. You add the missing `moved` block.

### Likely follow-up: drift, refresh, and `-replace`

- **Drift:** someone resized the VM in the console. The next plan wants to change it back or adopt the new size, depending on config. Run plan and read it. Don't apply a migration plan that also "fixes" a pile of drift you haven't looked at. Split them.
- **`terraform apply -replace='oci_core_instance.app["app-1"]'`** forces replacement of that one address. It is the opposite of this migration. Know the flag so you don't pass it by habit.
- **Targeted apply** (`-target`) can apply a move while leaving a broken graph half-done. Avoid it for a state migration. The whole plan should already be small.

### Likely follow-up: workspaces and backends

A workspace is a separate state for the same config (dev vs prod). A `moved` block applies to whichever state you have selected. Migrating prod while your shell is pointed at dev does nothing to prod and can destroy dev. `terraform workspace show` before plan. Say that out loud. It is the same class of mistake as running a script on the wrong cluster.

---

## How the two halves of this round connect

They asked about ownership, then about Terraform state. The link you can close with:

> I treat a state migration the way I treat a schema change. The identity of the object stays. The name in the tool changes. I want the dry run to say "moved" and nothing else, and I want a seatbelt like `prevent_destroy` on anything that holds data. Applying a plan I haven't read is how you get a maintenance window you didn't schedule.
