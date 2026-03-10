# Human-in-the-Loop (HITL) with n8n

This example demonstrates a **Human-in-the-Loop (HITL)** workflow using n8n. It models a content approval process where an AI generates a draft response to a customer review, but a human must approve or reject it before any action is taken. This workflow provides a practical illustration of the HITL pattern discussed in Chapter 6.

## Requirements

*   An active [n8n](https://n8n.io/) instance (cloud or local).
*   An OpenAI account and API key.

## Steps for running this example

1. Open n8n:
- You can either sign up for a free account on n8n.cloud (https://n8n.cloud) or install it on your own computer.
- The easiest way to run n8n locally is by using Docker:
```bash
docker run -it --rm -p 5678:5678 n8nio/n8n
```
Once the container is running, open your web browser and navigate to `http://localhost:5678`.

2. Import the workflow:
- Create a new, blank workflow.
- In the top-right menu, click the three dots (`...`) and select `Import from file`.
- Select the `human-in-the-loop-workflow.n8n.json` file from this directory.

3. Configure credentials:
- In the n8n workflow, find the *AI Draft Response* node.
- Select the node and configure your OpenAI credentials.

4. Activate and run:
- Save and activate the workflow.
- Click *Test workflow* to start a manual execution.

5. Provide human input:
- The workflow will pause at the *Wait for Human* step.
- Go to the *Send for Approval* node's execution log in the n8n UI. You will see the output, which includes a URL for `webhook.site`.
- Open this `webhook.site` URL in your browser. This page acts as your "inbox."
- Click either the "Approve" or "Reject" link on that page. This action sends a request back to the n8n workflow and resumes its execution.

## Output

After you click "Approve" or "Reject," you can observe the final outcome in the n8n execution log. The *If Approved* node will direct the flow to one of two final *NoOp* nodes:
- *Send to Customer*: If you approved the draft.
- *Escalate*: If you rejected the draft.