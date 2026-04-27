---
icon: lucide/workflow
---

# Phase 4: Capstone

In this capstone phase, we connect n8n, Mattermost, and MinIO into one end‑to‑end workflow:

* Mattermost is the user interface (chat).
* n8n orchestrates the logic.
* MinIO acts as a simple document store (TXT files, RAG‑like).

The workflow listens to messages in a Mattermost channel, retrieves relevant TXT files from MinIO, passes them to an LLM for extraction/summarization, and posts a response back to Mattermost.


!!! warning

    This is not a full RAG implementation. We skip embeddings and similarity search. Instead, we read all TXT files from a bucket and let the LLM reason over them. This is intentional for workshop simplicity.

## Prerequisites (Already Provided)

Each attendee already has:

- ✅ A Mattermost account
- ✅ Permission to create Mattermost Integrations
- ✅ A MinIO username and password

In this documentation, we will use the example alias: `fit-dassie`. You should replace it with your own alias where applicable.

## Architecture

High‑Level Architecture

```
Mattermost (Channel Message)
        ↓
   n8n Workflow
        ↓
   MinIO (TXT files)
        ↓
   OpenAI (via proxy)
        ↓
Mattermost (Bot Reply)
```


## Step 1: Prepare MinIO Storage

### Log in to MinIO

Open the MinIO web UI. Default is: [minio-console-aika-agent-workshop.2.rahtiapp.fi](https://minio-console-aika-agent-workshop.2.rahtiapp.fi)

Log in using: 

* Username: your minio_username (e.g. `fit-dassie`)
* Password: your minio_password (e.g. `Fit-Dassie-42`)

### Create a Bucket

Create a bucket named after your alias. This can be done using the `+ Create Bucket` in Minio Console's left side navigation. Note that the buckets are shared, so do not place any sensitive information in them. The bucket name must be unique across all participants, so use your alias to ensure that.

* e.g. `fit-dassie`

!!! warning

    When you do add files to the bucket, notice that there are some naming rules that will make your life easy when referencing them in n8n:

    * lowercase (`a-z`)
    * no spaces
    * no special characters (except dash `-`)

    Thus, prefer file names like `colors.txt` or `menu.txt`.

### Upload TXT Files

Create a few simple TXT files that you will want your LLM to be able to use as reference documents. For example:

* menu.txt
* projects.txt

Let's imagine a use case where some information arrives in a non-JSON format. It can be mostly machine-readable, but not fully structured. Parsing this sort of content without LLM, using only rules and regexes, can be a nightmare. But LLMs can easily extract relevant information from such content if prompted correctly. Let's see how we can get this working.

??? info "Example content of menu.txt"

    ```
    Monday
    - Starter: Potato Soup
    - Main: Pasta
    - Dessert: Cookies

    Tuesday
    - Salad for starters
    - Mac and Cheese as main course
    - Ice Cream to finish

    Wednesday
    - 1: Cale Soup
    - 2: Reindeer Stew
    - 3: Chocolate Cake

    Thursday
    Our offering includes Grated Salad, Pea Soup, Pan Cakes and also some levain bread.

    Friday
    - Tom Yum Soup
    - Thai Curry
    - Mango Sticky Rice
    - Remember that it is a bring your kid to work day, so we have some fun snacks for the kids as well!
    ```

??? info "Example content of projects.txt"

    ```
    Active Projects as of 2026/Q1

    - Title: FIT Dassie
      Description: A project to build a simple RAG‑like workflow using n8n, Mattermost, and MinIO.
      Status: Active
    - Title: FIT Capybara
      Description: A project to explore agentic capabilities of LLMs using n8n and custom APIs.
      Status: Planning
    - Title: FIT Otter
      Description: A project to create a knowledge graph from unstructured data using n8n and Neo4j.
      Status: Completed
    ```

## Step 2: n8n Workflow

Create a new workflow in n8n and name it something like `My Capstone Workflow`. We will build the workflow step by step in the next sections. To start, we will only add the trigger, which will be a **Webhook** node that listens for incoming messages from Mattermost.

Now, ==this is important==. Change the HTTP Method to `POST`. Otherwise, the integration has no change of working.

Copy the URIs to your MEMO text file, as you will need them later. They look like...

* Test URL: `https://n8n-aika-agent-workshop.2.rahtiapp.fi/webhook-test/<uuid>`
* Production URL: `https://n8n-aika-agent-workshop.2.rahtiapp.fi/webhook/<uuid>`

!!! warning

    Leave the Authentication to None and Response to "Immediately". Later on, the Mattermost Outgoing Webook will give us token, looking like `xtzmfc18k3f5ixs1a61ap5551e`, which we *could* use for validation. We won't do it in this workshop to save some time. In product, you should validate it.

!!! tip

    Geeky note. You could now test it using e.g. CURL like this, assuming you press the `Listen for test event` button in n8n first:

    ```bash
    URI='https://n8n-aika-agent-workshop.2.rahtiapp.fi/webhook-test/<uuid>'
    curl -X POST $URI -d '{"text": "Hello from CURL!"}' -H "Content-Type: application/json"
    ```

## Step 3: Create a Mattermost Integration

### Create a channel

To avoid one ultra cluttered channel, create a new channel for this bot to operate in. You can name it after your alias, e.g. `fit-dassie`.

![alt text](images/04-mm-create-channel-dialog.png)
/// caption
When creating a new channel, you can set the name to match your alias.
///

### Go to Integrations

![alt text](images/04-mm-integrations-location.png)
/// caption
In Mattermost, the Integrations are in the top-left corner.
///

### Create an Outgoing Webhook

The *specific* names are not that important, but for consistency, you can use:

* Title: `fit-dassie-out-test`
* Content Type: `application/json`
* Channel: same channel as above (e.g. `fit-dassie`)
* Trigger Words: `ask-test`
* Trigger When: **First word matches a trigger word exactly**
* Callback URLs: `https://n8n-aika-agent-workshop.2.rahtiapp.fi/webhook-test/<uuid>`

!!! tip

    Why `-test`? Because n8n provides two webhook URLs: one for testing and one for production.

    We need to eventually add two Outgoing Webhooks: one for test, one for production.

!!! info

    Ok, so what is a trigger word? It is a word that, when typed as the first word in a message, will trigger the outgoing webhook. For example, if you type:

    > ask-test What is on the menu today?

    The trigger word is `ask-test`, so the outgoing webhook will include payload with the message text and other metadata. This allows n8n to know that it should process this message.

## Step 4: Test the Integration

So far, we should be able to trigger the n8n workflow by sending a message in the Mattermost channel. Try it out:

1. Go to n8n and click the `Listen for test event` button in the Webhook node.
2. In Mattermost, in your channel, type: `ask-test This is a test message`

![alt text](images/04-n8n-webhook-output.png)
/// caption
You should now see the message payload in n8n on the right side of the node. The right side is the output. You can press the Pin icon to make sure that the output stays the same. This will allow you to develop the pipeline without calling the webhook again and again.
///



## Step 5: Add AI Agent.

Add `AI Agent` node that is connected to the Webhook. Open the settings and change:

* Source for Prompts: `Define below`
* Prompt: `Expression` (see below)

```
You are a helpful assistant.

Answer ONLY using the information in the documents provided by the Minio S3 related tools. Try to infer what file you need based on the user query and the file names.

If the answer is not found, reply: "I could not find this information in the documents."

USER QUERY:
{{ $json.body.text }}
```

## Step 6: Add Output Parser

In the `AI Agent` Node, activate the `Require Specific Output Format`. It will guide you to add an output parser. Click the link and it will open the Add Node menu to the right. Choose `Structured Output Parser`. Choose the default Schema type as Generate From JSON Example, and add the following JSON as an example of the output you want from the LLM:

```json
{
  "answer": "This would contain the answer to the user query.",
  "source_file": "menu.txt)"
}
```

## Step 7: Add MinIO Tools

Add two Tools. Click the `+` icon in the AI Agent node, and add an **S3 Tool Node**.

Click the Set up Credential and fill the following content:

* S3 Endpoint: `http://minio:9000` (Internal!)
* Region: anything
* Access Key ID: your MinIO username (e.g. `fit-dassie`)
* Secret Access Key: your MinIO password (e.g. `Fit-Dassie-42`)
* Region: `us-east-1`
* Force Path Style: `true` (important for MinIO!)

In the Node itself, set the...

* Resource: File
* Operation: Get Many
* Bucket Name: `fit-dassie` (or your alias)

