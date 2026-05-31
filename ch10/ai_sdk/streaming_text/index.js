import { simulateReadableStream, streamText } from 'ai';
import { MockLanguageModelV3 } from 'ai/test';

const model = new MockLanguageModelV3({
  doStream: async () => ({
    stream: simulateReadableStream({
      chunks: [
        { type: 'stream-start', warnings: [] },
        { type: 'text-start', id: 'text-1' },
        { type: 'text-delta', id: 'text-1', delta: 'Hello' },
        { type: 'text-delta', id: 'text-1', delta: ', ' },
        { type: 'text-delta', id: 'text-1', delta: 'world!' },
        { type: 'text-end', id: 'text-1' },
        {
          type: 'finish',
          finishReason: { unified: 'stop', raw: undefined },
          usage: {
            inputTokens: { total: 2, noCache: 2, cacheRead: undefined, cacheWrite: undefined },
            outputTokens: { total: 3, text: 3, reasoning: undefined },
          },
        },
      ],
    }),
  }),
});

const result = streamText({
  model,
  prompt: 'Say hello in one short sentence.',
});

for await (const part of result.textStream) {
  process.stdout.write(part);
}

process.stdout.write('\n');
