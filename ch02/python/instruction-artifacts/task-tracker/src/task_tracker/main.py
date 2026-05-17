import sys


def create_task(title: str) -> str:
    """Creates a new task with the given title."""
    # Note: In a real app, this would save to a database or file.
    # For this exercise, we just return a success message.
    return f"Task '{title}' created successfully."


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: task-tracker <task_title>")
        sys.exit(1)

    title = " ".join(sys.argv[1:])
    result = create_task(title)
    print(result)

if __name__ == "__main__":
    main()
