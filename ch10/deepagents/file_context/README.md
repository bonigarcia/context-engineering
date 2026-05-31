# File context

This folder describes the file-read side of the DeepAgents pattern.

- Read a few selected repo/docs files
- Turn each read into a short note
- Keep only the most recent notes in a bounded buffer
- Pass only the reduced summary forward

The point is not to preserve every byte of source text. It is to preserve the useful shape of the context while keeping the task long-horizon and manageable.

## Run

```bash
pip install -r ../requirements.txt
python file_context.py
```
