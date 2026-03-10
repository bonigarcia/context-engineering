# Human-in-the-Loop (HITL) example

This example demonstrates a simple **Human-in-the-Loop (HITL)** workflow. It's a collaborative story-writing assistant where an AI generates parts of a story, and the user provides feedback, corrections, or approval at each step.

## Requirements

This project requires [Python](https://www.python.org/) 3.6+ and the libraries listed in `requirements.txt`.

## Steps for running this example

1.  Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows cmd: .venv\Scripts\activate # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Set environment variables:
   Ensure your OpenAI API key is set as an environment variable. You can do this by:
```
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
```
Alternatively, create a `.env` file in the source directory with the content `OPENAI_API_KEY="YOUR_OPENAI_API_KEY"`.

3. Run the script:
```bash
python human_in_the_loop.py
```

## Output

Here's an example of an interactive session:

```text
--- Collaborative Story Writing Assistant ---
You and the AI will write a story together.
Type 'quit' or 'exit' at any time to end the story.

To start, what should the story be about? A lone explorer discovers a forgotten temple in the jungle.

... The AI is thinking ...

--- AI's suggestion ---
Elara, a seasoned archaeo-botanist with a compass as her only true companion, hacked through the dense, emerald curtain of the Amazon. For weeks, the hum of insects and the distant roar of howler monkeys had been her lullaby. Her quest: the legendary Sunken Temple of Xylos, a myth whispered only in the most obscure indigenous legends. Then, through a sudden break in the canopy, a glint of weathered stone caught her eye – an impossibly geometric pattern amidst the chaos of nature.
-----------------------
What happens next? (Approve with Enter, or provide a different direction): The temple entrance is blocked by ancient, glowing vines.

... The AI is thinking ...

--- AI's suggestion ---
As Elara approached, the air grew heavy, thick with the scent of ozone and ancient earth. What she had first taken for moss on the temple's façade now pulsed with a soft, ethereal luminescence. Thick, fibrous vines, impossibly intertwined, writhed with an inner light, forming an impenetrable barrier across the temple's grand entrance. They seemed to breathe, contracting and expanding with a slow, deliberate rhythm, guarding secrets untold.
-----------------------
What happens next? (Approve with Enter, or provide a different direction): quit

--- Your Final Story ---
A lone explorer discovers a forgotten temple in the jungle.
Elara, a seasoned archaeo-botanist with a compass as her only true companion, hacked through the dense, emerald curtain of the Amazon. For weeks, the hum of insects and the distant roar of howler monkeys had been her lullaby. Her quest: the legendary Sunken Temple of Xylos, a myth whispered only in the most obscure indigenous legends. Then, through a sudden break in the canopy, a glint of weathered stone caught her eye – an impossibly geometric pattern amidst the chaos of nature.
[The temple entrance is blocked by ancient, glowing vines.]
As Elara approached, the air grew heavy, thick with the scent of ozone and ancient earth. What she had first taken for moss on the temple's façade now pulsed with a soft, ethereal luminescence. Thick, fibrous vines, impossibly intertwined, writhed with an inner light, forming an impenetrable barrier across the temple's grand entrance. They seemed to breathe, contracting and expanding with a slow, deliberate rhythm, guarding secrets untold.
```
