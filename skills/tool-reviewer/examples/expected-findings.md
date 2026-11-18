# Expected findings for examples/tools.json

A correct review reports at least these problems:

- `get_data` has a generic name, a description that says nothing, and an undocumented `query` parameter. The model cannot know when to call it.
- `search_orders` and `find_orders` overlap: both list a customer's orders, with different parameter names (`customer_id` and `status` against `client` and `state`). Keep one, with consistent names.
- `create_refund` takes `date` as a free string with no format. Use ISO 8601 (`format: date`) and say which date it is.

The review may also note that `amount` has no currency or unit, that `status` and `state` should be enums, and that `create_refund` does not mention its side effect. It must not report problems with `get_customer`, which follows the checklist.
