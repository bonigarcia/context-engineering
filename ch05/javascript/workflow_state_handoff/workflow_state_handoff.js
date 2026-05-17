import OpenAI from "openai";
import fs from "node:fs/promises";
import path from "node:path";
import readline from "node:readline/promises";
import { stdin as input, stdout as output } from "node:process";

const client = new OpenAI();
const model = process.env.MODEL || "gpt-5";
const stateFile = path.resolve(process.env.STATE_FILE || ".workflow_state_handoff.json");

function newState() {
  return {
    objective: "",
    status: "idle",
    currentStep: 0,
    plan: [],
    blockers: [],
    plannerNotes: "",
    executorNotes: "",
    turnCount: 0,
    handoffLog: [],
  };
}

async function loadState() {
  try {
    const raw = await fs.readFile(stateFile, "utf8");
    const data = JSON.parse(raw);
    return {
      objective: String(data.objective ?? ""),
      status: String(data.status ?? "idle"),
      currentStep: Number(data.currentStep ?? 0),
      plan: Array.isArray(data.plan) ? data.plan.map(String).filter(Boolean) : [],
      blockers: Array.isArray(data.blockers) ? data.blockers.map(String).filter(Boolean) : [],
      plannerNotes: String(data.plannerNotes ?? ""),
      executorNotes: String(data.executorNotes ?? ""),
      turnCount: Number(data.turnCount ?? 0),
      handoffLog: Array.isArray(data.handoffLog) ? data.handoffLog.map(String).filter(Boolean) : [],
    };
  } catch {
    return newState();
  }
}

async function saveState(state) {
  await fs.writeFile(stateFile, `${JSON.stringify(state, null, 2)}\n`, "utf8");
}

function ensureList(value) {
  if (Array.isArray(value)) return value.map(String).map((v) => v.trim()).filter(Boolean);
  if (typeof value === "string" && value.trim()) return [value.trim()];
  return [];
}

function renderState(state) {
  return [
    `- objective: ${state.objective || "(unset)"}`,
    `- status: ${state.status}`,
    `- current_step: ${state.currentStep}`,
    `- plan: ${state.plan.length ? JSON.stringify(state.plan) : "(none)"}`,
    `- blockers: ${state.blockers.length ? JSON.stringify(state.blockers) : "(none)"}`,
    `- planner_notes: ${state.plannerNotes || "(none)"}`,
    `- executor_notes: ${state.executorNotes || "(none)"}`,
    `- turn_count: ${state.turnCount}`,
    `- handoff_log: ${state.handoffLog.length ? JSON.stringify(state.handoffLog.slice(-4)) : "(none)"}`,
  ].join("\n");
}

function buildPlannerPrompt(state, userRequest) {
  return `Shared workflow state:\n${renderState(state)}\n\nUser request:\n${userRequest}\n\nReturn JSON with these keys:\n- objective: concise statement of the current goal\n- plan: ordered list of 3 to 5 short steps\n- handoff_note: short note for the executor agent\n- risks: list of likely blockers or assumptions`;
}

function buildExecutorPrompt(state) {
  return `You are the executor agent in a two-agent workflow.\n\nRead the shared workflow state carefully and continue from the current plan.\n\nShared workflow state:\n${renderState(state)}\n\nReturn JSON with these keys:\n- status: one of idle, planned, in_progress, blocked, or complete\n- completed_step: short description of the step just completed\n- blockers: list of unresolved blockers\n- next_step: short description of the next step to take`;
}

async function requestJson(instructions, prompt) {
  const response = await client.responses.create({
    model,
    instructions,
    input: prompt,
  });

  const raw = (response.output_text || "{}").trim();
  try {
    return JSON.parse(raw);
  } catch {
    return { raw };
  }
}

function applyPlannerResult(state, payload) {
  const objective = String(payload.objective ?? "").trim();
  if (objective) state.objective = objective;

  const plan = ensureList(payload.plan);
  if (plan.length) {
    state.plan = plan;
    state.currentStep = 0;
  }

  const handoffNote = String(payload.handoff_note ?? "").trim();
  if (handoffNote) state.plannerNotes = handoffNote;

  const risks = ensureList(payload.risks);
  if (risks.length) state.blockers = risks;

  state.status = "planned";
}

function applyExecutorResult(state, payload) {
  state.status = String(payload.status ?? "in_progress").trim() || "in_progress";

  const completedStep = String(payload.completed_step ?? "").trim();
  if (completedStep) {
    state.executorNotes = completedStep;
    state.handoffLog.push(`executor: ${completedStep}`);
  }

  const blockers = ensureList(payload.blockers);
  if (blockers.length) {
    state.blockers = [...new Set([...state.blockers, ...blockers])];
  }

  if (state.plan.length && state.currentStep < state.plan.length) {
    state.currentStep += 1;
  }

  const nextStep = String(payload.next_step ?? "").trim();
  if (nextStep) state.handoffLog.push(`next: ${nextStep}`);
}

async function main() {
  if (!process.env.OPENAI_API_KEY) {
    console.error("OPENAI_API_KEY is not set. Put it in your environment or a .env file.");
    process.exitCode = 2;
    return;
  }

  const rl = readline.createInterface({ input, output });
  let state = await loadState();

  console.log(`[Workflow state demo] model=${model} state_file=${stateFile}`);
  console.log("Type /help for commands.\n");

  while (true) {
    const userText = (await rl.question("you> ")).trim();
    if (!userText) continue;

    if (userText.startsWith("/")) {
      const cmd = userText.toLowerCase().trim();
      if (cmd === "/help") {
        console.log("Commands:\n  /help    show commands\n  /state   show the shared workflow state\n  /reset   clear the workflow state file\n  /exit    quit\n");
      } else if (cmd === "/state") {
        console.log("Shared workflow state\n" + renderState(state) + "\n");
      } else if (cmd === "/reset") {
        state = newState();
        await saveState(state);
        console.log("Cleared workflow state.\n");
      } else if (cmd === "/exit") {
        console.log("Goodbye.");
        break;
      } else {
        console.log("Unknown command. Type /help.\n");
      }
      continue;
    }

    state.turnCount += 1;
    if (!state.objective.trim()) {
      state.objective = userText.trim();
    }

    const plannerPayload = await requestJson(
      "You are the planning agent. Produce concise, structured workflow state.",
      buildPlannerPrompt(state, userText),
    );
    applyPlannerResult(state, plannerPayload);

    const executorPayload = await requestJson(
      "You are the execution agent. Advance the shared workflow state.",
      buildExecutorPrompt(state),
    );
    applyExecutorResult(state, executorPayload);

    await saveState(state);

    console.log("Planner output");
    console.log(JSON.stringify(plannerPayload, null, 2));
    console.log("Executor output");
    console.log(JSON.stringify(executorPayload, null, 2));
    console.log("Shared state");
    console.log(renderState(state) + "\n");
  }

  rl.close();
}

await main();
