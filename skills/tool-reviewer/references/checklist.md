# Tool review checklist

Each rule has a short rationale and the book section where the idea is explained.

## Names and descriptions

1. Tool names are specific verbs plus objects (`search_orders`, `create_refund`). Generic names such as `get_data` or `process` give the model nothing to choose by. (Chapter 4, Tool definitions as contracts)
2. Each description says what the tool does, when to use it, when not to use it, and what it returns. The description is the model's only documentation. (Chapter 4, Tool definitions as contracts)
3. Descriptions mention important side effects and costs, for example that a call sends an email or takes several seconds. (Chapter 4, Strengths, limits, and failure modes)

## Parameters

4. Every parameter has a type and a description. Formats are explicit: dates as ISO 8601 (`format: date`), money as integer cents or a decimal string with currency, identifiers with their pattern. (Chapter 4, Tool definitions as contracts)
5. Closed sets of values use `enum`. Required parameters are listed in `required`, and optional ones have documented defaults. (Chapter 4, Tool definitions as contracts)
6. Parameter names are consistent across tools: the same concept has the same name everywhere (`customer_id`, not `customer_id` in one tool and `client` in another). (Chapter 4, Tool definitions as contracts)

## The tool set

7. Tools do not overlap. Two tools with the same purpose and different parameter names make the model pick at random. Merge them or separate their purposes clearly. (Chapter 4, Strengths, limits, and failure modes)
8. The set is as small as the task allows. Every definition costs tokens on every call, and large sets lower selection accuracy. Load rarely used tools on demand. (Chapter 4, Strengths, limits, and failure modes)

## Outputs and errors

9. Outputs return only what the model needs, in a compact structured form, with pagination or limits for lists. Large raw outputs fill the context window. (Chapter 4, MCP servers)
10. Errors are returned as messages the model can act on ("order 123 not found, check the id"), not as stack traces or empty results. (Chapter 4, MCP in production environments)

## MCP servers

11. An MCP server exposes tools with the same quality rules, and uses resources or prompts for content that is read rather than executed. (Chapter 4, MCP servers)
12. An MCP server validates its inputs and enforces its own limits, since any client can call it. (Chapter 4, MCP in production environments)
