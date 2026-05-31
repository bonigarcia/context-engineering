import { generateText, Output } from 'ai';
import { MockLanguageModelV3 } from 'ai/test';
import { z } from 'zod';

const model = new MockLanguageModelV3({
  doGenerate: async () => ({
    content: [{ type: 'text', text: '{"recipe":{"name":"Toast","ingredients":[{"name":"Bread","amount":"2 slices"}],"steps":["Toast the bread","Serve warm"]}}' }],
    finishReason: { unified: 'stop', raw: undefined },
    usage: {
      inputTokens: { total: 4, noCache: 4, cacheRead: undefined, cacheWrite: undefined },
      outputTokens: { total: 12, text: 12, reasoning: undefined },
    },
    warnings: [],
  }),
});

const { output } = await generateText({
  model,
  output: Output.object({
    schema: z.object({
      recipe: z.object({
        name: z.string(),
        ingredients: z.array(
          z.object({
            name: z.string(),
            amount: z.string(),
          }),
        ),
        steps: z.array(z.string()),
      }),
    }),
  }),
  prompt: 'Generate a tiny recipe object.',
});

console.log(output);
