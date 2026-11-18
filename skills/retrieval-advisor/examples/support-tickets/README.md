# Support copilot knowledge base

The support copilot suggests replies to support agents, based on how similar tickets were solved before.

The knowledge source is the archive of resolved support tickets: about 2 million tickets from the last six years, with around 3,000 new tickets added every day. Product behavior changed a lot over those years, so old solutions are often wrong for current versions. Each ticket has a creation date, a product version, and a resolution.

Ingestion splits each ticket into question and resolution, embeds them, and stores them with the ticket id, date, and product version. The retrieval step is in `retrieve.py`.
