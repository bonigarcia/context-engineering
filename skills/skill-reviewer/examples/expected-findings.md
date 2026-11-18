# Expected findings for examples/pdf_helper

A correct review of `examples/pdf_helper` reports at least these problems:

- The `name` field is invalid: it has uppercase letters and a space, and it does not match the directory name `pdf_helper` (which itself contains an underscore). The validation script reports both errors, so `frontmatter_valid` is `false`.
- The description does not say when to use the skill or when not to use it. "Helps with documents" matches almost any request.
- Step 2 asks the model to compute a SHA-256 checksum by reasoning. A checksum must come from a script, since the model cannot compute it reliably.
- The skill defines no output format for the summary and the extracted entities.

The review may also mention the vague closing line "Be helpful and thorough" and the lack of instructions for non-PDF input. It must not report missing scripts or references as broken links, since `SKILL.md` does not mention any.
