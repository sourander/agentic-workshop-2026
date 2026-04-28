---
icon: lucide/wrench
---

# Manual Steps

This documentation includes a set of steps that do not have an automated CLI command, and must be performed manually in the UI. They are formatted as a list of QA-like problems and solutions.

## Allow Users to Create Webhooks

If it is intended that users will use the **Outgoing** webhooks, the System Console setting `EnableOnlyAdminIntegrations` must be disabled. Sadly, as of 2026, this no longer exists. This is stated in the [Mattermost 4.9.0](https://docs.mattermost.com/administration-guide/upgrade/important-upgrade-notes.html) upgrade notes. Thus, what need to be done, is:

* Go to `System Console > User Management -> Permissions`
* Click `Edit Scheme`.
* Enable the following:

* Manage Incoming Webhooks
    * Manage Own
* Manage Outgoing Webhooks
    * Manage Own

This will enable both in- and outgoing webhooks, so that users can practice during Workshop as they wish.
