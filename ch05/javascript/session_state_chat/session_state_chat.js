import OpenAI from "openai";
import readline from "node:readline/promises";
import { stdin as input, stdout as output } from "node:process";

const client = new OpenAI();
const model = process.env.MODEL || "gpt-5";

function newState() {
  return {
    goal: "",
    stage: "collecting_context",
    topic: "",
    constraints: [],
    openQuestions: [],
    turnCount: 0,
    lastUserMessage: "",
    lastAssistantMessage: "",
  };
}

function extractTopic(text) {
  const match = text.match(/[A-Za-z][A-Za-z0-9_-]+/);
  return match ? match[0].toLowerCase() : "";
}

function looksLikeNewGoal(text) {
  const lower = text.toLowerCase();
  return ["instead", "switch to", "change to", "new task", "new goal", "actually"].some((token) => lower.includes(token));
}

function updateState(state, userText, assistantText) {
  state.turnCount += 1;
  state.lastUserMessage = userText;
  state.lastAssistantMessage = assistantText;

  if (!state.goal.trim() || looksLikeNewGoal(userText)) {
    state.goal = userText.trim();
    state.topic = extractTopic(userText);
    state.constraints = [];
    state.openQuestions = [];
  }

  const lower = userText.toLowerCase();
  if (["plan", "outline", "roadmap"].some((token) => lower.includes(token))) {
    state.stage = "planning";
  } else if (["review", "check", "verify"].some((token) => lower.includes(token))) {
    state.stage = "reviewing";
  } else if (["done", "finished", "complete"].some((token) => lower.includes(token))) {
    state.stage = "done";
  } else {
    state.stage = "working";
  }

  if (!state.topic.trim()) {
    state.topic = extractTopic(userText);
  }

  const constraintMatch = userText.match(/(?:must|should|needs to|do not|don't)\s+([^.;!?]+)/i);
  if (constraintMatch) {
    const constraint = constraintMatch[0].trim();
    if (!state.constraints.includes(constraint)) {
      state.constraints = [...state.constraints, constraint].slice(-5);
    }
  }

  if (userText.includes("?")) {
    const question = userText.trim().replace(/\?$/, "");
    if (question && !state.openQuestions.includes(question)) {
      state.openQuestions = [...state.openQuestions, question].slice(-5);
    }
  }
}

function renderState(state) {
  return [
    `- goal: ${state.goal || "(unset)"}`,
    `- stage: ${state.stage}`,
    `- topic: ${state.topic || "(unset)"}`,
    `- turn_count: ${state.turnCount}`,
    `- constraints: ${state.constraints.length ? state.constraints.join(", ") : "(none)"}`,
    `- open_questions: ${state.openQuestions.length ? state.openQuestions.join(", ") : "(none)"}`,
    `- last_user_message: ${state.lastUserMessage || "(unset)"}`,
    `- last_assistant_message: ${state.lastAssistantMessage || "(unset)"}`,
  ].join("\n");
}

function buildSystemPrompt(state) {
  return `You are a helpful assistant in a stateful demo.

The current session state is:
${renderState(state)}

Use the state as the current snapshot of the task. Keep answers concise and grounded in the
information already present in the session. If the user changes goals or constraints, adapt to the
new state instead of assuming older context is still correct.`;
}

async function main() {
  if (!process.env.OPENAI_API_KEY) {
    console.error("OPENAI_API_KEY is not set. Put it in your environment or a .env file.");
    process.exitCode = 2;
    return;
  }

  const rl = readline.createInterface({ input, output });
  const state = newState();
  const transcript = [];

  console.log(`[Session state demo] model=${model}`);
  console.log("Type /help for commands.\n");

  while (true) {
    const userText = (await rl.question("you> ")).trim();
    if (!userText) continue;

    if (userText.startsWith("/")) {
      const cmd = userText.toLowerCase().trim();
      if (cmd === "/help") {
        console.log("Commands:\n  /help    show commands\n  /state   show the current session state\n  /reset   clear the session state\n  /exit    quit\n");
      } else if (cmd === "/state") {
        console.log("Current session state\n" + renderState(state) + "\n");
      } else if (cmd === "/reset") {
        Object.assign(state, newState());
        transcript.length = 0;
        console.log("Cleared session state.\n");
      } else if (cmd === "/exit") {
        console.log("Goodbye.");
        break;
      } else {
        console.log("Unknown command. Type /help.\n");
      }
      continue;
    }

    transcript.push({ role: "user", content: userText });
    const response = await client.responses.create({
      model,
      instructions: buildSystemPrompt(state),
      input: transcript,
    });

    const assistantText = (response.output_text || "").trim();
    transcript.push({ role: "assistant", content: assistantText });
    updateState(state, userText, assistantText);
    console.log(`${assistantText}\n`);
  }

  rl.close();
}

await main();
