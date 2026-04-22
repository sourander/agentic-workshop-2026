---
icon: lucide/workflow
---

# Phase 3: First AI Agent

## Goal

The goal of this Phase is to create a simple AI Agent workflow in n8n. The workflow will be triggered manually, but it will utilize an OpenAI model to generate a response.

## Step 1: Create the workflow

![alt text](images/03-n8n-overview-view.png)
/// caption
In the front page of n8n, you can see the Overview view, which shows all your workflows. Click the "New Workflow" button to create a new workflow.
///

## Step X: Create the OpenAI credential

!!! warning

    This is work in progress. More steps and details will be added here.

When n8n asks for an OpenAI credential, create a new one with these values:

- Base URL: `http://openai-proxy/v1`
- Token: any placeholder value

The token value does not need to be real. The workshop environment routes OpenAI requests through an internal proxy, and that proxy adds the shared workshop API token before forwarding the request.