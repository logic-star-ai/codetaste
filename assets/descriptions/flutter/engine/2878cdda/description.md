# Refactor command buffer submission to use CommandQueue interface

## Summary

Introduce `CommandQueue` abstraction for submitting command buffers. Make `CommandBuffer::Submit()` private and require all submissions to go through `Context::GetCommandQueue()->Submit()`.

## Motivation

Vulkan backend benefits from batching command buffer submissions to the graphics queue. Previous automatic batching approach (#49870) introduced surprising/fragile thread-based behavior. Explicit batching via `CommandQueue` provides predictable, controlled submission ordering.

## Changes

**API Change:**
```cpp
// Old
buffer->Submit();

// New
context->GetCommandQueue()->Submit({buffer});
```

**Implementation:**
- Add `impeller::CommandQueue` interface with `Submit(vector<CommandBuffer>)` method
- Make `CommandBuffer::Submit()` private (only accessible via `CommandQueue`)
- Backend implementations:
  - **Metal/GLES**: Simple pass-through to private `Submit()` (potential for future optimization)
  - **Vulkan**: `CommandQueueVK` with batched submission logic
- `AiksContext`: Accumulate command buffers during frame render, submit batch in `FlushCommandBuffers()`
- `ContentContext`: Add `RecordCommandBuffer()` / `FlushCommandBuffers()` for buffer tracking

**Files:**
- New: `command_queue.{h,cc}`, `command_queue_vk.{h,cc}`
- Modified: All callsites updated to new submission pattern
- Updated: `ContextVK`, `ContextMTL`, `ContextGLES` with queue accessors

## Benefits

- Explicit control over submission batching
- No hidden thread behavior
- Ordering guarantees for command buffer execution
- Fixes flutter/flutter#141123