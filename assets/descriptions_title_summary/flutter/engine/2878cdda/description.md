# Refactor command buffer submission to use CommandQueue interface

Introduce `CommandQueue` abstraction for submitting command buffers. Make `CommandBuffer::Submit()` private and require all submissions to go through `Context::GetCommandQueue()->Submit()`.