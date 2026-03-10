# Sequential multi-agent workflow with n8n

This example demonstrates the **sequential multi-agent pattern** using n8n, a graph-based workflow automation tool. The workflow orchestrates a simple content creation process involving three specialized agents connected in a sequence:
1. Generate idea agent: Creates a blog post title based on an initial topic.
2. Write post agent: Writes a full blog post based on the generated title.
3. Summarize post agent: Summarizes the blog post into a short tweet.

This demonstrates how orchestration tools can manage state (the content being created) as it flows from one agent to the next.

## Steps for running this example

1. Open n8n:
- You can either sign up for a free account on n8n.cloud (https://n8n.cloud) or install it on your own computer.
- The easiest way to run n8n locally is by using Docker:
```bash
docker run -it --rm -p 5678:5678 n8nio/n8n
```
Once the container is running, open your web browser and navigate to `http://localhost:5678`.

2. Import workflow:
- Create a new, blank workflow.
- In the top-right menu, click the three dots (`...`) and select `Import from file`.
- Select the `blog-post-workflow.n8n.json` file from this directory.

3. Configure credentials:
- The workflow uses the "OpenAI Chat Model" node. You will need to configure it with your own OpenAI API credentials.
- Click on each of the OpenAI nodes (`Generate Idea`, `Write Post`, `Summarize Post`).
- In the `Credentials` section for each node, either select an existing OpenAI account or create a new one by providing your API key.

4. Run the workflow:
- The workflow starts with a `Start` node. You can manually trigger it.
- To provide an initial topic, you can pass input JSON to the Start node, for example:
```json
{
   "topic": "The future of AI in software development"
}
```
- Click `Execute Workflow` to run the sequence. You can inspect the output of each node to see the state flow from idea to finished summary.