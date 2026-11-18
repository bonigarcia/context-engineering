# Skill review checklist

Each rule has a short rationale and the book section where the idea is explained.

## Frontmatter

1. `name` is 1 to 64 characters of lowercase letters, digits, and single hyphens, and equals the directory name. Harnesses use the name for discovery and slash invocation, so a mismatch can hide the skill. (Chapter 2, The anatomy of a skill)
2. `description` is present and at most 1,024 characters. It is the only text the agent sees before loading the skill. (Chapter 2, The anatomy of a skill)
3. Optional fields such as `license` and `metadata` use the expected types. `metadata` holds string values only. (Chapter 2, The anatomy of a skill)

## Activation

4. The description says what the skill does and when to use it, with the words a user would actually type (file names, task verbs). A description such as "Helps with documents" gives the agent nothing to match. (Chapter 2, Best practices for designing agent skills)
5. The description says when not to use the skill, especially when a neighboring skill covers a similar task. Missing exclusions cause overactivation and wasted tokens. (Chapter 2, Best practices for designing agent skills)

## Procedure

6. Work that must be exact and repeatable (parsing, checksums, format conversion, counting, schema validation) is done by a script in `scripts/`, and `SKILL.md` says when and how to run it. Asking the model to compute such results by reasoning gives different answers on different runs. (Chapter 2, Best practices for designing agent skills)
7. Judgment work (summarizing, prioritizing, explaining) is left to the model with clear criteria, not forced into rigid templates that break on unusual inputs. (Chapter 2, Best practices for designing agent skills)
8. Instructions are stated as requirements, in order, with no optional-sounding wording for steps that matter. `SKILL.md` works as an operational contract. (Chapter 2, Best practices for designing agent skills)
9. Long reference material lives in separate files that `SKILL.md` points to and loads only when needed, so the skill body stays short. (Chapter 2, Agent skills)
10. Every file that `SKILL.md` mentions exists, and every script states its inputs, outputs, and exit codes.

## Output

11. The skill defines the output format exactly: sections, fields, and file names. Results that another step will consume have a machine-readable form such as JSON. (Chapter 2, Best practices for designing agent skills)
12. The skill says what to do when the input is missing, empty, or out of scope.

## Validation and maintenance

13. The skill comes with at least one representative example or test case that shows what correct behavior looks like. (Chapter 2, Best practices for designing agent skills)
14. The skill contains no secrets, credentials, or machine-specific paths, since skills are shared and versioned like code. (Chapter 2, Best practices for designing agent skills)
