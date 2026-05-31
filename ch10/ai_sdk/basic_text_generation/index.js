import { generateText } from 'ai';
import { MockLanguageModelV3 } from 'ai/test';

const model = new MockLanguageModelV3({
  doGenerate: async () => ({
    content: [{ type: 'text', text: 'Hello from the AI SDK mock model.' }],
    finishReason: { unified: 'stop', raw: undefined },
    usage: {
      inputTokens: { total: 2, noCache: 2, cacheRead: undefined, cacheWrite: undefined },
      outputTokens: { total: 6, text: 6, reasoning: undefined },
    },
    warnings: [],
  }),
});

const { text } = await generateText({
  model,
  prompt: 'Say hello in one sentence.',
});

console.log(text);
