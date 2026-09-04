# Observability with Spring AI and Ollama

This example shows **Observability** — using Micrometer to monitor AI
context flow. Spring AI auto-instruments ChatClient calls with Micrometer
observations (token counts, latency). A custom metric tracks vector store
retrievals.

## Requirements

* Java 21+, Maven 3.9+, Ollama with `llama3.2:3b`, `nomic-embed-text`

## Steps

```
ollama serve
ollama pull llama3.2:3b
ollama pull nomic-embed-text
mvn spring-boot:run
```

## Output

The app prints custom and auto-instrumented metrics after answering:

```
User: How do I reset my password?
Model: To reset your password, please follow these steps:

1. Go to the self-service portal and click on "Forgot Password" or "Reset Password".
2. Enter your username or email address and follow the prompts to reset your password.
3. Once you've reset your password, log back in to the portal with your new password.

That's it! You should now be able to access the portal without any issues.
---
Custom metric 'context.retrievals': 1
--- Available Micrometer metrics:
  jvm.buffer.memory.used = 1712249.0
  jvm.threads.states = 0.0
  jvm.memory.committed = 1.179648E7
  process.uptime = 23.931
  application.started.time = 8.8
  jvm.memory.used = 5575040.0
  jvm.threads.states = 22.0
  spring.ai.advisor = 1.0
  disk.total = 5.35910412288E11
  http.client.requests = 1.0
  gen_ai.client.token.usage = 80.0
  gen_ai.client.token.usage = 165.0
  jvm.memory.used = 3.9185184E7
  jvm.buffer.count = 0.0
  logback.events = 0.0
  jvm.memory.committed = 5.24288E7
  http.client.requests.active = 0.0
  gen_ai.client.operation = 4.0
  executor.queue.remaining = 2.147483647E9
  jvm.buffer.total.capacity = 1712248.0
  jvm.memory.committed = 2.097152E7
  executor.pool.size = 0.0
  jvm.memory.max = -1.0
  disk.free = 5.1675303936E10
  system.cpu.usage = 1.0
  jvm.threads.live = 26.0
  jvm.classes.unloaded = 0.0
  jvm.memory.committed = 5898240.0
  gen_ai.client.operation = 1.0
  jvm.classes.loaded = 9500.0
  jvm.threads.peak = 26.0
  process.cpu.time = 1.53125E10
  gen_ai.client.token.usage = 46.0
  jvm.gc.overhead = 0.0
  logback.events = 0.0
  gen_ai.client.token.usage = 46.0
  logback.events = 0.0
  jvm.gc.memory.promoted = 0.0
  gen_ai.client.operation.active = 0.0
  jvm.memory.max = 1.073741824E9
  jvm.threads.started = 28.0
  jvm.threads.states = 2.0
  spring.ai.advisor.active = 0.0
  jvm.buffer.count = 0.0
  executor.completed = 0.0
  jvm.memory.used = 1.4680064E7
  http.client.requests = 4.0
  jvm.memory.max = 5.0331648E7
  executor.pool.max = 2.147483647E9
  jvm.gc.memory.allocated = 0.0
  logback.events = 1.0
  jvm.memory.usage.after.gc = 0.0
  jvm.memory.used = 1651560.0
  jvm.buffer.total.capacity = 0.0
  jvm.gc.max.data.size = 4.139778048E9
  jvm.buffer.memory.used = 0.0
  http.client.requests.active = 0.0
  jvm.memory.max = 4.139778048E9
  system.cpu.count = 16.0
  gen_ai.client.operation.active = 0.0
  jvm.info = 1.0
  gen_ai.client.token.usage = 85.0
  executor.pool.core = 8.0
  process.start.time = 1.788520649429E9
  jvm.buffer.count = 12.0
  jvm.buffer.memory.used = 0.0
  jvm.classes.loaded.count = 9501.0
  jvm.memory.used = 8475136.0
  jvm.threads.daemon = 25.0
  jvm.compilation.time = 3046.0
  spring.ai.chat.client = 1.0
  jvm.threads.states = 0.0
  jvm.buffer.total.capacity = 0.0
  jvm.memory.committed = 2097152.0
  spring.ai.advisor = 1.0
  jvm.threads.states = 2.0
  jvm.memory.used = 3.8468576E7
  jvm.memory.committed = 3.9911424E7
  executor.active = 0.0
  jvm.memory.max = -1.0
  jvm.memory.max = -1.0
  spring.ai.chat.client.active = 0.0
  jvm.threads.states = 0.0
  gen_ai.client.token.usage = 0.0
  context.retrievals = 1.0
  spring.ai.advisor.active = 0.0
  jvm.gc.live.data.size = 0.0
  executor.queued = 0.0
  logback.events = 0.0
  process.cpu.usage = 0.05895295879981855
---
```