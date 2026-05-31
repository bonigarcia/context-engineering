# Sub-agent Delegation

This example shows a parent DeepAgents agent delegating work to two isolated subagents: one for research and one for writing. The parent keeps the main context clean while the subagents stay focused on their own tasks.

## Requirements

* [Python](https://www.python.org/) 3.10+
* An [OpenAI API key](https://platform.openai.com/api-keys) set as an environment variable (`OPENAI_API_KEY`)

## Steps for running this example in the shell

1. Install dependencies:
```bash
python -m venv .venv

# macOS/Linux:
source .venv/bin/activate

# Windows Command Prompt:
.venv\Scripts\activate.bat

# Windows PowerShell:
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

2. Export your API key as an environment variable:
```bash
export OPENAI_API_KEY="sk-..." # Windows cmd: set OPENAI_API_KEY="sk-..." # Windows PowerShell: $env:OPENAI_API_KEY="sk-..."
```

3. Run the script:
```bash
python subagent_delegation.py
```

## Output

```
{'messages': [HumanMessage(content="Research the example's delegation pattern and give me a short brief.", additional_kwargs={}, response_metadata={}), AIMessage(content=[{'arguments': '{"description":"Identify and summarize the delegation pattern shown in the developer examples/instructions of this session. Focus on: when the coordinator should use subagents, how tasks should be split, when to parallelize, when not to delegate, and how results should be reconciled. Return a concise bullet list plus a 1-paragraph brief suitable for the user. Do not modify files.","subagent_type":"research-agent"}', 'call_id': 'call_nGi5evwZn2d6VbcSiJJI9BhV', 'name': 'task', 'type': 'function_call', 'id': 'fc_0129c8236bf31b20006a1c9cedae0081a0860fa9e1076f149b', 'status': 'completed'}], additional_kwargs={}, response_metadata={'id': 'resp_0129c8236bf31b20006a1c9ced2b3c81a0bfdf913ab63c71dc', 'created_at': 1780260077.0, 'metadata': {}, 'model': 'gpt-5.4-2026-03-05', 'object': 'response', 'service_tier': 'default', 'status': 'completed', 'model_provider': 'openai', 'model_name': 'gpt-5.4-2026-03-05'}, id='resp_0129c8236bf31b20006a1c9ced2b3c81a0bfdf913ab63c71dc', tool_calls=[{'name': 'task', 'args': {'description': 'Identify and summarize the delegation pattern shown in the developer examples/instructions of this session. Focus on: when the coordinator should use subagents, how tasks should be split, when to parallelize, when not to delegate, and how results should be reconciled. Return a concise bullet list plus a 1-paragraph brief suitable for the user. Do not modify files.', 'subagent_type': 'research-agent'}, 'id': 'call_nGi5evwZn2d6VbcSiJJI9BhV', 'type': 'tool_call'}], invalid_tool_calls=[], usage_metadata={'input_tokens': 5385, 'output_tokens': 97, 'total_tokens': 5482, 'input_token_details': {'cache_read': 0}, 'output_token_details': {'reasoning': 0}}), ToolMessage(content='- Use subagents for complex, multi-step, or high-context work where parts can be investigated independently; keep simple or very short tasks with the coordinator.\n- Split work into clear, self-contained subproblems with crisp scopes, explicit deliverables, and minimal overlap so each subagent can work without needing the others’ intermediate context.\n- Parallelize only independent branches that can run safely at the same time; if tasks depend on each other’s outputs, sequence them instead.\n- Don’t delegate trivial tasks, tightly coupled reasoning that benefits from one continuous line of thought, or work where coordination overhead would exceed any gain.\n- Have the coordinator retain the global plan, assign bounded tasks, and avoid sending unnecessary raw context; subagents should return only useful findings, not large dumps.\n- Reconcile by comparing subagent outputs, resolving inconsistencies, merging overlapping findings, and producing one coherent final answer in the requested format.\n- Track progress explicitly for larger efforts: start with an in-progress step, update status as work completes, revise tasks when new information appears, and ensure at least one active step remains until done.\n- Use parallel tool execution only for genuinely parallel operations; don’t run planning/tracking steps like todo updates in parallel.\n\nBrief: The delegation pattern here is “centralized coordination, distributed execution.” The coordinator should keep ownership of planning, sequencing, and final synthesis, while using subagents only when the work is substantial and divisible into mostly independent parts. Tasks should be scoped narrowly, parallelized only when independent, and not delegated when the job is simple or heavily interdependent. Results from subagents should come back as concise findings rather than raw source material, then be reconciled by the coordinator into a single consistent response.', name='task', id='98dff6a7-1878-4581-a8a1-6e0d7a66411e', tool_call_id='call_nGi5evwZn2d6VbcSiJJI9BhV'), AIMessage(content=[{'type': 'text', 'text': 'Delegation pattern brief:\n\n- Central coordinator, distributed execution.\n- Delegate only complex, multi-step, or context-heavy work.\n- Split work into self-contained tasks with clear outputs.\n- Parallelize only independent branches; sequence dependent ones.\n- Don’t delegate trivial or tightly coupled tasks.\n- Keep the main thread focused on planning, coordination, and synthesis.\n- Ask subagents for concise findings, not raw dumps.\n- Reconcile outputs by merging, checking consistency, and producing one final answer.\n\nShort brief:  \nThe example’s pattern is a coordinator-subagent model. The coordinator owns the overall plan and final response, while subagents handle isolated, well-scoped research or execution tasks. Delegation is useful when work is substantial and separable; it is not worth using for simple tasks or reasoning that needs one continuous context. Independent tasks should run in parallel for speed, then the coordinator should combine the results into a single coherent brief.', 'annotations': [], 'id': 'msg_0129c8236bf31b20006a1c9cf8cfc081a0bf482f91aed617c7', 'phase': 'final_answer'}], additional_kwargs={}, response_metadata={'id': 'resp_0129c8236bf31b20006a1c9cf8667081a08161d146025dfa3b', 'created_at': 1780260088.0, 'metadata': {}, 'model': 'gpt-5.4-2026-03-05', 'object': 'response', 'service_tier': 'default', 'status': 'completed', 'model_provider': 'openai', 'model_name': 'gpt-5.4-2026-03-05'}, id='resp_0129c8236bf31b20006a1c9cf8667081a08161d146025dfa3b', tool_calls=[], invalid_tool_calls=[], usage_metadata={'input_tokens': 5838, 'output_tokens': 192, 'total_tokens': 6030, 'input_token_details': {'cache_read': 5376}, 'output_token_details': {'reasoning': 0}})], 'files': {}}
```
