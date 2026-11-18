# HR assistant knowledge base

The HR assistant answers employee questions about company policies (vacation, remote work, expenses, benefits).

The only knowledge source is the employee handbook: a single document of about 30 pages (around 15,000 words). HR updates it twice a year. All employees can read the whole handbook.

The assistant receives about 2,000 questions per month. The current pipeline (`ingest.py`) splits the handbook into chunks, embeds them, and stores them in a vector database. At question time, the four most similar chunks are added to the prompt.
