---
icon: lucide/wrench
---

# Manual Steps

This documentation includes a set of steps that do not have an automated CLI command, and must be performed manually in the UI. They are formatted as a list of QA-like problems and solutions.

## Mattermost In/Outgoing Webhooks

Typical users cannot create incoming or outgoing webhooks in Mattermost. Instead of enabling this for all, create them and share the information to the group. These steps are not rocket science, but I've included images since this information might be informative for the participants as well.

![alt text](images/manual_mattermost_incoming_webhooks.png)
/// caption
Webhooks are added in the Integrations > Incoming Webhooks section of the Mattermost System Console.
///

![alt text](images/manual_mattermost_incoming_webhook_add.png)
/// caption
There are not too many settings in the menu. Choose title, description, channel, and username that it will be posted as. The username can also be later on changed in the workflow using the `username` field in the JSON body of the webhook.
///

![alt text](images/manual_mattermost_incoming_webhook_successful.png)
/// caption
The URL shown here should be kept secret. Sending anything to that URI will post a message to the Mattermost channel.
///

Sending an HTTP POST request to that URL with a JSON body containing `text` field will post the content of that field as a message to the Mattermost channel. For example:

![alt text](images/manual_mattermost_incoming_webhook_with_curl.png)
/// caption
A command line tool `curl` has been used to send a POST request to the URL seen in the screenshot above.
///

![alt text](images/manual_mattermost_town_square_msg_received.png)
/// caption
The command appears in the Mattermost Town Square channel as a message. Note that anyone could've sent this message.
///

You can read more about this feature at Mattermost's [Incoming Webhooks documentation](https://developers.mattermost.com/integrate/webhooks/incoming/).

!!! info

    Now that you have created one, create another one with the same settings but with a Title ending in suffix `(prod)`.

    Copy these into your memo:

    ```
    MM-IN (test): https://mattermost-aika-agent-workshop.2.rahtiapp.fi/hooks/<webhook_id_test>
    MM-IN (prod): https://mattermost-aika-agent-workshop.2.rahtiapp.fi/hooks/<webhook_id_prd>
    ```

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
