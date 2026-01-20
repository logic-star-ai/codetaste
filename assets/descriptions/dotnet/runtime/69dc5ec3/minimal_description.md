# Move `IsDebuggerPresent` to minipal, convert debugger methods to QCall

Consolidate native debugger detection across CoreCLR, Mono, and NativeAOT into a shared `minipal` component and convert managed debugger APIs to use QCalls.