[Nilog documentation](../README.md)

<a id="-nilog--low-allocation-ilogger-extensions-for-net"></a>

# Nilog — Typed ILogger Extensions from NuGet

<a id="allocation-aware-high-performance-logging-for-microsoftextensionslogging"></a>

Allocation-aware, high-performance logging for `Microsoft.Extensions.Logging`

> **In this guide:** [Get started](#guide-install) · [Understand the details](#guide-features) · [Check the limits](#guide-limitations)

**Typed logging calls through your existing `ILogger` pipeline.**

[![NuGet](https://img.shields.io/badge/NuGet-v1.0.6-004880?logo=nuget&logoColor=white)](https://www.nuget.org/packages/Nilog)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/gcfernando/Nilog/blob/main/LICENSE)
[![.NET](https://img.shields.io/badge/.NET-8.0%20%7C%209.0%20%7C%2010.0-512BD4?logo=dotnet&logoColor=white)](https://dotnet.microsoft.com)
[![Disabled path](https://img.shields.io/badge/disabled%20call-0%20bytes%20%7C%20~2%20ns-2ea44f)](https://github.com/gcfernando/Nilog#-benchmarks)
[![16-arg typed](https://img.shields.io/badge/up%20to%2016--arg%20typed-0%20bytes%20disabled-brightgreen)](https://github.com/gcfernando/Nilog#-benchmarks)
[![Analyzer](https://img.shields.io/badge/Nilog.Analyzers-NILOG001--008%20%2B%20codefix-orange)](https://github.com/gcfernando/Nilog#-static-analysis-niloganalyzers)
[![AOT](https://img.shields.io/badge/Native%20AOT-analyzed-blueviolet)](https://github.com/gcfernando/Nilog)

> 📖 **Full docs, recipes, and architecture:** [github.com/gcfernando/Nilog](https://github.com/gcfernando/Nilog)

---

## ⚡ What Nilog is

Nilog is a set of **low-allocation, strongly typed extension methods on `ILogger`**. It is not a
new logging framework, provider, or transport — it uses the `Microsoft.Extensions.Logging`
(MEL) pipeline you already use, and enabled calls flow through the supplied `ILogger`
and provider(s) (Console, Serilog, NLog, OpenTelemetry, Seq, Application Insights, …). Swap
`LogInformation(...)` for `WriteInformation(...)` to avoid a call-site `params object[]`
when the call binds to a typed overload. Review the formatting and scope
contracts below when migrating.

Conventional templated `ILogger` extensions with value arguments can allocate a **`params object[]` at the call site** — even when
the level is switched off and the message is thrown straight in the bin. On a hot path that is
millions of pointless allocations and a busy garbage collector.

**Nilog uses readonly value-type state for typed arguments.** After warmup a disabled typed call allocates **nothing** inside Nilog and
returns in about **2 ns** (measured, v1.0.6). `LoggerMessage.Define`/`[LoggerMessage]` achieve the same disabled-path cost; Nilog needs no per-message declaration.

```csharp
using Nilog;

// Typed args: no Nilog argument array when disabled; argument expressions still run.
// Enabled allocations depend on arity, formatting and provider; see the benchmark limits.
logger.WriteInformation("User {UserId} ordered {Count} items", userId, count);

// Up to sixteen typed args avoid a call-site array; 9–16-value rendering builds an array.
logger.WriteInformation("User {UserId} bought {Sku} x{Qty} in {Region} via {Channel} ({Tier}) at {Ts} ref {Ref} batch {B}",
    userId, sku, qty, region, channel, tier, ts, refId, batch);
```

---

## ⚡ At a glance

| | |
|--|--|
| 🚀 **Zero-alloc disabled path** | Disabled typed calls avoid Nilog per-call allocations after warmup; exact-zero tests cover representative arities through 16. Conventional Microsoft extensions cost 17–43 ns and 56–272 B per filtered call (v1.0.6 measurement). |
| 🆕 **6–16 arg typed overloads (v1.0.4)** | Source-generated `Write*`/`Nilogger.Log` overloads now reach **sixteen** arguments — **0 bytes** disabled; ≈2.8 ns vs 42.6 ns for the conventional extension at 9 args (v1.0.6 measurement). |
| 🆕 **Typed multi-pair scopes (v1.0.4)** | `WriteScope<T1,T2>`, `WriteScope<T1,T2,T3>`, `WriteScope<T1,T2,T3,T4>` — no dictionary allocation, no array copy for the most common scope shapes. |
| 🆕 **Compact exception report (v1.0.4)** | `WriteErrorException(ex, moreDetailsEnabled: false)` has a **< 300 B** gate for a short fixture report (down from ≈ 992 B); single-line `[Title] Type: Message` summary. |
| 🔥 **Leaner than MEL extensions when enabled** | Less allocation than the conventional extensions at 1–6 args; equal at 9; not faster than `LoggerMessage.Define`/`[LoggerMessage]`. |
| 🆕 **Span-based rendering** | Plain 1–8-value templates can use a 256-character stack buffer, allocating the final string. Format/overflow fallbacks and 9–16-value rendering can allocate arrays. |
| 🆕 **`Nilog.Analyzers` — 8 rules + code fix** | `NILOG001`–`NILOG008`: interpolation (one-click fix), count mismatch, concatenated templates, duplicate, positional, exception-as-value, malformed, and non-PascalCase placeholders. |
| 🆕 **WriteError/WriteCritical typed no-exception** | `logger.WriteError("Error {Id}", id)` → **zero-array typed overload** (no `params` fallback). |
| 🔌 **Existing MEL providers** | Uses standard named-value and `{OriginalFormat}` conventions; export/formatting behavior depends on the provider. |
| 🧩 **Zero setup** | Just `using Nilog;` — no DI, no registration, no config. |
| 🧯 **Hardened formatting** | Typed paths can return raw text for too few values/invalid format and sanitize recoverable argument-formatting failures; surplus values remain in state but are ignored in text. Validation and provider exceptions still propagate. |
| 🧵 **Concurrency & AOT analysis** | Internal state uses concurrency controls and the library enables SDK compatibility analysis. Providers/callbacks must support their calling pattern; validate the complete host. |
| 🔒 **Bounded template cache** | `MaxTemplateCacheEntries` (default 10,000) stops caching new entries instead of growing unboundedly. |

---

## 📊 Benchmarks

The following are historical reported measurements, not results rerun for this documentation review. The external packed-package harness is not included in the checkout; repository benchmark suites measure local behavior and may produce different results.


> **Historical reported results.** Nilog's clear advantage is the **disabled path** (0 B, ~2–3 ns versus 17–43 ns / 56–272 B for
> conventional Microsoft extension methods) and **lower enabled-path allocation than conventional extensions at 1–6 typed
> args**. Compared with Microsoft's optimized `LoggerMessage.Define` / `[LoggerMessage]`, Nilog is **equal on the
> disabled path and not faster when enabled** (and allocates 3.6× more than the source generator at 9 args).
> Nilog's value is convenience — no per-message declaration — at near-optimized cost.

Measured for **v1.0.6** with BenchmarkDotNet 0.15.8 · .NET 10.0.12 · Intel Core Ultra 7 265H · Windows 11 · SDK 10.0.401,
3 launches × (5 warmup + 12 iterations), from an external harness that references the packed `Nilog 1.0.6` package.
Single-digit-nanosecond differences (< ~1 ns) are timer/loop-overhead artifacts, not real differences.

### Disabled path (level filtered off)

| Typed args | MEL extension   | `LoggerMessage.Define` | `[LoggerMessage]` | **Nilog**        |
| :---: | :---: | :---: | :---: | :---: |
| 1          | 17.2 ns / 56 B  | 0.6 ns / 0 B           | 0.1 ns / 0 B      | **2.0 ns / 0 B** |
| 3          | 22.7 ns / 104 B | 1.5 ns / 0 B           | 0.9 ns / 0 B      | **1.9 ns / 0 B** |
| 6          | 38.3 ns / 200 B | 2.1 ns / 0 B           | 1.7 ns / 0 B      | **2.0 ns / 0 B** |
| 9          | 42.6 ns / 272 B | n/a                    | 2.6 ns / 0 B      | **2.8 ns / 0 B** |

### Enabled path (message rendered)

| Typed args | MEL extension    | `LoggerMessage.Define` | `[LoggerMessage]`    | **Nilog**            |
| :---: | :---: | :---: | :---: | :---: |
| 1          | 53.0 ns / 88 B   | **22.6 ns / 32 B**     | **22.7 ns / 32 B**   | 29.4 ns / 56 B       |
| 3          | 106.1 ns / 152 B | **72.0 ns / 48 B**     | 77.3 ns / 48 B       | 81.1 ns / 104 B      |
| 6          | 240.6 ns / 280 B | 220.8 ns / 280 B       | 231.1 ns / 280 B     | **156.8 ns / 208 B** |
| 9          | 380.7 ns / 376 B | n/a                    | **211.2 ns / 104 B** | 360.0 ns / 376 B     |

* All-`object` call shapes can bind to `params`; mixed concrete/object values can still bind typed overloads. Caller-side boxing remains possible.
* A single scope: `BeginScope` 21.9 ns / 240 B vs `WriteScope("k", v)` 11.5 ns / 80 B (scope *creation* only).
* Parallel logging (50,000 calls, `MediumRun`): Microsoft 3.46 ms / 5.34 MB vs Nilog 3.54 ms / 3.82 MB — equal time, ~28% less allocation. These enabled-path figures describe the stated rendering sink; providers, formatting fallbacks and argument expressions can allocate differently.
* Real ASP.NET Core app (Kestrel, loopback): 1,696 B/request vs 1,833 B (−7.5%); throughput and latency not distinguishable from Microsoft in this run.

Do not extrapolate micro-benchmark ratios to application performance. Full methodology and limits:
[main README](https://github.com/gcfernando/Nilog#-benchmarks).

---


<a id="guide-limitations"></a>

## ⚠️ Limitations

Enabled text rendering uses the stack path only for plain 1–8-value templates fitting its
256-character buffer. The 9–16-value states allocate an argument array when rendered. Explicit
`object[]` calls use MEL formatting. Too few values/invalid format on the typed path can return
raw text; surplus values are ignored in text but retained in state. Providers and validation errors
can still throw. Numeric names are sequential holes: `{0} {0}` consumes two values, not argument
zero twice. No-argument messages bypass template parsing and do not acquire structured
`{OriginalFormat}` state from Nilog. Null scope values become `N/A`; null template values become `(null)`.

Built-in exception reports cap messages at 4,096 characters; verbose reports limit inner depth
to 3, visited nodes to 32, and body text to 32 KiB plus a truncation notice. Temporary allocation
can be larger. Compact titles/source have no separate cap, and a custom formatter bypasses these
output policies. The original exception, including its `Data`, still reaches the provider.

C# evaluates argument expressions before the logging method executes. Guard expensive payload construction explicitly when the level can be disabled. The log-state structs are ordinary readonly value types, not `ref struct` stack-only types; providers can box or allocate while processing them.


Nilog removes the call-site `object[]` allocation for common logging calls, but it does not make every logging scenario allocation-free. We list these honestly rather than overclaim.

| Scenario                                        | Allocation                                                                                                                                   |
| ---------- | ----------- |
| 0–**16** typed arguments, disabled path         | **0 bytes** (raised from 0–8 in v1.0.4)                                                                                                      |
| 0–**16** typed arguments, enabled path          | typed calls avoid a call-site argument array; rendering, fallback and provider processing can allocate                                                    |
| **17+** arguments                               | falls back to `params object[]`; argument evaluation and the params-array allocation happen before Nilog can check `IsEnabled`                                                   |
| Enabled logging                                 | may still allocate depending on the sink, formatter, and value types — Nilog cannot control what a downstream sink does                      |
| Dynamic / interpolated / concatenated templates | value-bearing dynamic templates may consume cache entries up to the dictionary limits; no-argument messages bypass that cache. NILOG001/003 check supported direct expressions.                             |
| `FlushAsync`                                    | **real flush** — awaits every callback registered via `Nilogger.RegisterFlush(...)`; a zero-allocation no-op only when nothing is registered |

> **Why some of these are by design, not bugs:** Nilog is a thin, allocation-aware layer over
> `ILogger`. It deliberately does **not** own the sink, the transport, or the async pipeline —
> that is what makes it a true drop-in that works with *any* `Microsoft.Extensions.Logging`
> provider and *any* hosting/cloud platform. Allocation past the call site (string rendering,
> sink I/O) belongs to the formatter and sink you already chose.

---

## 🗺️ Roadmap

Status of planned work. ✅ shipped · 🚧 in progress · 🔭 considering · ⛔ decided against.

| Item                                                 | Status            | Notes                                                                                                  |
| ------ | :------: | ------- |
| Typed overloads to **16 arguments**                  | ✅ **1.0.4**       | Source generator emits 6–16 typed overloads; disabled typed calls avoid Nilog per-call allocation after warmup. |
| Typed multi-pair scope overloads                     | ✅ **1.0.4**       | `WriteScope<T1,T2>`, `WriteScope<T1,T2,T3>`, `WriteScope<T1,T2,T3,T4>` — no dictionary allocation.     |
| Compact exception report                             | ✅ **1.0.4**       | A short `moreDetailsEnabled: false` fixture has a <300 B allocation gate; arbitrary reports can allocate more.                |
| Lift the typed-overload ceiling beyond 5 args        | ✅ **1.0.3**       | Source generator first emitted 6–8 arg zero-array overloads.                                           |
| More analyzer rules beyond `NILOG001`                | ✅ **1.0.3**       | Added `NILOG002`–`NILOG008` — 1 → 8 rules.                                                             |
| Ship `Nilog.Analyzers` as a standalone NuGet package | ✅ **1.0.3**       | Development-dependency package; adds no runtime dependency.                                            |
| Real `FlushAsync` for buffering sinks                | ✅ **1.0.3**       | `RegisterFlush`/`UnregisterFlush`; no-op only when nothing is registered.                              |
| Native AOT / trim analysis           | ✅ **1.0.3**       | `IsAotCompatible=true`; removed a real `Exception.TargetSite` trim hazard.                             |
| Code-fix provider for `NILOG001`                     | ✅ **1.0.3**       | One-click rewrite of `$"..."` into a literal template + appended args.                                 |
| Code fixes for `NILOG002` / `NILOG003`               | 🔭                 | Ambiguous to auto-rewrite safely; diagnostics ship without an auto-fix for now.                        |
| `ILogger`-free static sink adapters                  | ⛔ decided against | Would fork the API and undermine Nilog's "true drop-in `ILogger`" design.                              |

If you need something here sooner, open an issue at
[github.com/gcfernando/Nilog/issues](https://github.com/gcfernando/Nilog/issues).

---

<a id="guide-install"></a>

## 📦 Install

```bash
dotnet add package Nilog
```

```xml
<PackageReference Include="Nilog" Version="1.0.6" />
```

Targets **.NET 8.0, 9.0, and 10.0**. Dependencies: `Microsoft.Extensions.Logging.Abstractions`
and `Microsoft.Extensions.ObjectPool`. Native AOT / trimming friendly.

---

## 🚀 Quick start

```csharp
using Microsoft.Extensions.Logging;
using Nilog; // <- that's the whole setup

using ILoggerFactory factory = LoggerFactory.Create(b => b.AddConsole());
ILogger logger = factory.CreateLogger("App");

// Plain message uses an identity formatter; provider costs remain
logger.WriteInformation("Service started");

// Typed calls avoid a call-site array; enabled formatting can allocate
logger.WriteInformation("User {UserId} signed in from {Ip}", 42, "10.0.0.1");

// Up to sixteen args — 6–16 source-generated in v1.0.4, zero array, zero boxing on disabled path
logger.WriteInformation("User {UserId} bought {Sku} x{Qty} in {Region} via {Channel} ({Tier})",
    userId, sku, qty, region, channel, tier);

// Exception with typed context — avoids a call-site argument array
try { Risky(); }
catch (Exception ex)
{
    logger.WriteError("Checkout failed for cart {CartId}", ex, cartId);
}
```

> [!IMPORTANT]
> **No Nilog-specific configuration or DI registration is required for normal use.** There is
> no service to register, no logger factory to construct, and no config file to maintain — just
> `using Nilog;` and the existing `ILogger` you already have.

---

## ⚙️ Configuration

Nilog has **nothing to configure for normal use**. Log levels, categories, and providers remain
**standard `Microsoft.Extensions.Logging` configuration** and work exactly as they do today:

```csharp
builder.Logging
    .SetMinimumLevel(LogLevel.Information)
    .AddFilter("Microsoft", LogLevel.Warning)
    .AddConsole();
```

A few **optional**, process-wide static hooks exist on `Nilogger` for advanced scenarios —
`ExceptionFormatter` (custom exception rendering), `MaxTemplateCacheEntries` (template-cache
ceiling, default 10,000), and `RegisterFlush`/`UnregisterFlush`/`FlushAsync` (draining a custom
buffering sink). None of them are required; see the
[full configuration reference](https://github.com/gcfernando/Nilog#-optional-advanced-configuration)
for details.

---

## 🧩 Structured logging

A single Nilog call carries the same structured contract as the framework's own templated
logging through value-type state. Enabled rendering and provider processing can allocate:

```csharp
logger.WriteInformation("User {UserId} bought {Sku} x{Qty}", 42, "A-100", 3);
```

| What the sink receives   | Value                                                          |
| ------------------------ | ------- |
| Rendered message         | `User 42 bought A-100 x3`                                      |
| `UserId` / `Sku` / `Qty` | `42` / `"A-100"` / `3`                                         |
| `{OriginalFormat}`       | `User {UserId} bought {Sku} x{Qty}`                            |
| Exception (if any)       | attached via the `Exception`-overload, not as a template value |
| Scope                    | whatever `WriteScope(...)` wraps the call in                   |

Providers that consume MEL structured state can export these fields. Validate field mapping,
formatting and scope support with the actual provider configuration.

---

## 🔗 Provider compatibility

Nilog passes standard `Microsoft.Extensions.Logging` structured state and `{OriginalFormat}`
to the supplied `ILogger`. `LoggingEngineInteropTests` uses a real `LoggerFactory` and a custom
capture provider to check named values, text, exception forwarding and filtering. It does not
exercise real Serilog or OpenTelemetry exporters. The changelog records historical external
integration work, but those harnesses/results are not included here or rerun for this review.
Validate the consuming application with its specific provider, scopes and export configuration.
Nilog supplies no direct database, cloud transport or log-store integration.

---

## 🆚 Nilog vs the alternatives

| Call shape | Nilog behavior |
| --- | --- |
| Disabled typed 1–16 values | No Nilog per-call allocation after warmup; argument expressions still run. |
| Enabled typed 1–8 values | Plain output fitting 256 characters can use a stack buffer; final text, boxing, fallback and provider work can allocate. |
| Enabled typed 9–16 values | Text rendering creates an `object?[]` for `string.Format`. |
| 17+ values / params call shapes | The call-site array can allocate before the level check; MEL owns formatting. |
| Typed scopes, 2–4 pairs | Avoid dictionary/array construction, but value/state boxing, wrappers and provider allocations remain. |

Historical benchmarks above compare their stated call shapes. They do not establish a universal
cost or feature comparison across other libraries and their overloads.

---

## 🧭 Choosing the right method

| I want to…                             | Call                                                  | Allocates?              |
| ------------ | ------ | :----------: |
| Log a constant message                 | `logger.WriteInformation("Started")`                  | identity formatter; provider costs remain                |
| Log 1–16 structured values             | `logger.WriteInformation("User {Id}", id)`            | zero inside Nilog when disabled; enabled rendering/provider work can allocate        |
| Log 17+ structured values              | `logger.WriteInformation("{A} … {Q}", …)`             | one `object[]`          |
| Log an error **with** exception        | `logger.WriteError("Failed {Id}", ex, id)`            | zero inside Nilog when disabled; enabled rendering/provider work can allocate        |
| Log an error **without** exception     | `logger.WriteError("Bad request")`                    | identity formatter; provider costs remain                |
| Exception report — compact summary     | `logger.WriteErrorException(ex, "Title")`             | short fixture targets <300 B; report length/provider affect costs |
| Exception report — full verbose        | `logger.WriteErrorException(ex, "Title", moreDetailsEnabled: true)` | pooled builder, report string and other formatting costs      |
| Dynamic level at runtime               | `Nilogger.Log(logger, level, "…", a, b)`              | zero inside Nilog for disabled typed calls; enabled work can allocate |
| Attach 1-pair scope                    | `using (logger.WriteScope("Key", value)) { … }`       | state/value boxing, wrapper and provider costs (80 B in the historical null-scope-provider measurement)     |
| Attach 2–4 pair scope (typed, no dict) | `using (logger.WriteScope("K1", v1, "K2", v2)) { … }` | values/state boxing and provider costs; no dictionary/array construction       |
| Catch `$"..."` mistakes at build time  | add the `Nilog.Analyzers` package                     | n/a                     |

Allocation notes describe Nilog after warmup, not argument construction or arbitrary provider work.

> **Tip:** Keep templates to **≤ 16** named holes to stay on the zero-array typed path.

---

<a id="guide-features"></a>

## ✨ Features

### Six levels, typed for 0–16 args, params for 17+

```csharp
logger.WriteTrace("Polling queue, {Count} items", count);
logger.WriteDebug("Cache miss for key {Key}", key);
logger.WriteInformation("Order {OrderId} confirmed", orderId);
logger.WriteWarning("Retry {Attempt}/{Max} for {Job}", attempt, max, job);
logger.WriteError("Payment failed for {OrderId}", ex, orderId);
logger.WriteCritical("Database unreachable on {Host}", ex, host);

// Nine-arg typed — no Nilog per-call allocation when disabled after warmup
logger.WriteInformation("{A} {B} {C} {D} {E} {F} {G} {H} {I}", a, b, c, d, e, f, g, h, i);

// Up to sixteen args — no call-site array on the disabled path
logger.WriteInformation("User {UserId} bought {Sku} x{Qty} in {Region} via {Channel} ({Tier}) ref {Ref} at {Ts}",
    userId, sku, qty, region, channel, tier, refId, ts);
```

<a id="runtime-level-api--zero-alloc-for-016-typed-args"></a>

### Runtime-level API — disabled typed calls avoid Nilog allocations

```csharp
LogLevel level = config.Verbose ? LogLevel.Debug : LogLevel.Information;
Nilogger.Log(logger, level, "Processing {JobId}", jobId);                       // no Nilog allocation when disabled after warmup
Nilogger.Log(logger, level, "{A} {B} {C} {D} {E} {F} {G} {H} {I}", a, b, c, d, e, f, g, h, i); // still 0 B when disabled
```

### Bounded template cache

The shared dictionary defaults to 10,000 entries and 1,024-character templates. Zero entry limit
disables dictionary admission; negative entry limits and non-positive length limits are ignored.
Lowering the entry limit below its current count clears the dictionary; lowering the length limit
does not evict existing entries. `ClearTemplateCache()` does not clear per-thread last-template
slots: each thread can retain one formatter for a template up to 256 characters even when the
dictionary is disabled or cleared. Configure limits before concurrent logging; this is not an
instantaneous process-memory bound during concurrent configuration changes.


```csharp
// Prevent unbounded memory growth from interpolated templates
Nilogger.MaxTemplateCacheEntries = 10_000;  // default; new entries parsed but not cached beyond limit
```

### 🔍 Static analysis — catch the structured-logging footguns at compile time

Stable templates allow cache reuse and preserve named fields. Direct interpolation embeds values
into message text before the method executes:

```csharp
logger.WriteInformation($"User {id} signed in");  // values become message text, not named fields
logger.WriteInformation("{A} {B}", a);            // 2 holes, 1 arg: typed rendering returns raw text; state still contains the supplied value
logger.WriteInformation("User " + id + " in");    // dynamic concatenation embeds data into the message
```

`Nilog.Analyzers` is a separate, opt-in package (**not** referenced by `Nilog.Core`) that catches
supported direct call-site patterns using syntax and resolved method symbols:

```xml
<PackageReference Include="Nilog.Analyzers" Version="1.0.6" PrivateAssets="all" />
```

| Rule         | Severity | Catches                                                                        | Auto-fix |
| ------ | ---------- | --------- | :--------: |
| **NILOG001** | Warning  | An interpolated string (`$"..."`) used as the message template.                | ✅        |
| **NILOG002** | Warning  | A template whose `{Placeholder}` count ≠ the number of arguments supplied.     | —        |
| **NILOG003** | Warning  | A template built with string concatenation (`+`) or `string.Format(...)`.      | —        |
| **NILOG004** | Warning  | The same named `{Placeholder}` used twice (duplicate structured-property key). | —        |
| **NILOG005** | Info     | Positional `{0}` placeholders instead of named `{Name}` ones.                  | —        |
| **NILOG006** | Warning  | An `Exception` passed as a template value instead of the exception parameter.  | —        |
| **NILOG007** | Warning  | A malformed template — an unclosed `{` or an empty `{}` placeholder.           | —        |
| **NILOG008** | Info     | A placeholder beginning with a lowercase letter (`{userId}` → `{UserId}`).           | —        |

```csharp
logger.WriteInformation($"User {id} signed in");        // ❌ NILOG001 (+ one-click fix)
logger.WriteInformation("{A} {B}", a);                  // ❌ NILOG002 (2 placeholders, 1 arg)
logger.WriteInformation("User " + id + " in");          // ❌ NILOG003
logger.WriteInformation("{Id} retried {Id}", a, b);     // ❌ NILOG004 (duplicate {Id})
logger.WriteInformation("{0} {1}", a, b);               // 🔵 NILOG005 (prefer named)
logger.WriteInformation("Failed {Error}", ex);          // ❌ NILOG006 (use the exception parameter)
logger.WriteInformation("Unclosed {Brace");             // ❌ NILOG007 (malformed)
logger.WriteInformation("User {userId}", id);           // 🔵 NILOG008 (PascalCase)

logger.WriteInformation("User {UserId} signed in", id); // ✅ no diagnostic
```

Promote the correctness rules to build-breaking errors in CI (NILOG005/008 are Info-only style):

```xml
<WarningsAsErrors>$(WarningsAsErrors);NILOG001;NILOG002;NILOG003;NILOG004;NILOG006;NILOG007</WarningsAsErrors>
```

Or via `.editorconfig` for the whole repo: `dotnet_diagnostic.NILOG001.severity = error`.

It's syntax/semantics-based — it catches the mistake at the call site. Full details:
[Static analysis](https://github.com/gcfernando/Nilog#-static-analysis-niloganalyzers).

The analyzers do not perform data-flow analysis. NILOG001 checks direct interpolation with holes;
NILOG002 requires a constant template and skips named arguments and explicit params-array syntax;
NILOG006 uses static exception types and skips named arguments. NILOG008 checks a lowercase first
letter. Report helpers are not template-analysis entry points. The NILOG001 fix withholds other
named arguments, trailing arrays and multi-line raw strings. Review generated names and behavior:
null values change from empty interpolation text to `(null)`, formatting uses invariant culture,
and provider rendering may happen later. Arbitrary side-effect ordering is not proven safe.

### FlushAsync — real flush for buffering sinks

```csharp
// A batching/buffering sink registers how to drain itself…
Nilogger.RegisterFlush(ct => myBatchingSink.FlushAsync(ct));

// …and shutdown awaits every registered sink. With nothing registered this is a
// zero-allocation no-op (returns Task.CompletedTask synchronously).
await Nilogger.FlushAsync(cancellationToken);

// Retain the registered delegate if you need to UnregisterFlush it later.

// Typed multi-pair scopes — no dictionary allocation, no array copy (NEW in v1.0.4)
using (logger.WriteScope("OrderId", orderId, "CustomerId", customerId, "Currency", "GBP"))
{
    logger.WriteInformation("Order opened");   // all three KVPs in scope
}
```

Callbacks run sequentially from a registration snapshot; duplicates run twice and unregister
removes one match. Failures are aggregated while later callbacks are attempted. Caller cancellation
stops new callbacks and abandons waiting on an incomplete task, retaining earlier failures; it cannot
interrupt synchronous callback work or forcibly stop a task. Concurrent flush calls can overlap.
With no callbacks, even a canceled token returns the completed no-op task. Core logging does not
consult `AsyncSinkFilter`; custom sink code must use that hook explicitly.

---

## 🏭 Production readiness

| Concern               | Nilog answer                                                                                                                                                                        |
| --------- | ------------- |
| Thread safety         | Internal state uses concurrency controls; providers and callbacks own their thread safety                                                                                                                    |
| Trimming / Native AOT | `IsAotCompatible=true` enables SDK analysis; validate the complete consuming application and its providers when publishing. |
| Memory growth         | `MaxTemplateCacheEntries` stops caching at the limit instead of growing unboundedly                                                                                                 |
| Idle CPU cost         | No background timer — the UTC timestamp cache refreshes lazily, only when an exception is formatted                                                                                 |
| Process shutdown      | A final UTC refresh runs automatically on `ProcessExit`; `ShutdownUtcTimer()` for deterministic teardown                                                                            |
| Formatting robustness | Typed safeguards handle too few values/invalid format and recoverable argument-formatting failures; surplus values remain in state. Null template values render `(null)`.                                                                      |
| Sink compatibility    | Standard MEL conventions; repository interop uses a custom capture provider through `LoggerFactory`, not each named third-party sink                                                                                    |
| Supported frameworks  | .NET 8, 9, 10                                                                                                                                                                       |

---

## 📖 API at a glance

```csharp
// Extension methods on ILogger — Write* for all six levels (typed 0–16, params 17+)
void WriteInformation(this ILogger logger, string message, params object[] args);
void WriteInformation<T0>(this ILogger logger, string message, T0 arg0);
void WriteInformation<T0,T1>(this ILogger logger, string message, T0 arg0, T1 arg1);
void WriteInformation<T0,T1,T2>(this ILogger logger, string message, T0 arg0, T1 arg1, T2 arg2);
void WriteInformation<T0,T1,T2,T3>(this ILogger logger, string message, T0 arg0, T1 arg1, T2 arg2, T3 arg3);
void WriteInformation<T0,T1,T2,T3,T4>(this ILogger logger, string message, T0 arg0, T1 arg1, T2 arg2, T3 arg3, T4 arg4);
// …and 6–16-argument overloads source-generated by Nilog.SourceGenerators (extended to 16 in v1.0.4)
void WriteInformation<T0,…,T15>(this ILogger logger, string message, T0 arg0, …, T15 arg15);
// Identical shape for WriteTrace, WriteDebug, WriteWarning

// Error/Critical — without exception (typed, no call-site array; 1–16 args)
void WriteError<T0,…,T15>(this ILogger logger, string message, T0 arg0, …, T15 arg15);
// With exception
void WriteError<T0,…,T15>(this ILogger logger, string message, Exception exception, T0 arg0, …, T15 arg15);
// Identical shape for WriteCritical

// Exception reports
void WriteErrorException(this ILogger logger, Exception ex,
    string title = "System Error", bool moreDetailsEnabled = false);  // short allocation-gate fixture targets <300 B

// Scopes — typed multi-pair overloads NEW in v1.0.4 (no dictionary, no array)
IDisposable WriteScope(this ILogger logger, string key, object value);
IDisposable WriteScope<T1,T2>       (this ILogger logger, string key1, T1 val1, string key2, T2 val2);
IDisposable WriteScope<T1,T2,T3>    (this ILogger logger, string key1, T1 val1, string key2, T2 val2, string key3, T3 val3);
IDisposable WriteScope<T1,T2,T3,T4> (this ILogger logger, string key1, T1 val1, string key2, T2 val2, string key3, T3 val3, string key4, T4 val4);
IDisposable WriteScope(this ILogger logger, IDictionary<string, object>? context);
IDisposable WriteScope(this ILogger logger, IEnumerable<KeyValuePair<string, object>>? context);
// IReadOnlyDictionary uses the IEnumerable overload; pairs are shallow-copied.

// Static runtime-level API (no call-site array for typed values)
void Nilogger.Log<T0,…,T15>(ILogger logger, LogLevel level, string message, T0 a, …, T15 p);

// Global settings
static int MaxTemplateCacheEntries { get; set; }            // default 10,000
static int MaxCachedTemplateLength { get; set; }            // default 1,024 chars
static int TemplateCacheCount { get; }
static void ClearTemplateCache();                         // dictionary only; thread slots remain
static void ShutdownUtcTimer();

// Flush: real drain of registered buffering sinks (no-op when none registered)
static void RegisterFlush(Func<CancellationToken, Task> flush);
static bool UnregisterFlush(Func<CancellationToken, Task> flush);
static Task FlushAsync(CancellationToken cancellationToken = default);
```

---

## ❓ FAQ

**Is it really zero allocation?**
On the disabled path: yes — **0 bytes** for **0–16** typed args (extended to 16 in v1.0.4; covered by selected warmed fixtures, including `DisabledPath_NineTypedArgs_AllocatesZeroBytes`). On the enabled path
Nilog allocates rendered text when requested; 9–16-value rendering builds an `object?[]`. Historical measurements report less allocation than conventional
extensions at 1–6 args, equal at 9 args (376 B each), and more than `LoggerMessage.Define`/`[LoggerMessage]` at 1–3 args (v1.0.6 measurement).

**What about 9+ arguments?**
Typed overloads now reach **sixteen** (1–5 hand-written, 6–16 source-generated). A 9-arg disabled
call allocates **0 B** and runs in ~2.8 ns (v1.0.6 measurement; the conventional extension takes ~43 ns / 272 B). Only at **17+** args
does Nilog fall back to `params object[]` — the same as the framework. Prefer ≤ 16 named holes on
hot paths, or move extra context into a typed `WriteScope` (2–4 pairs) or dictionary scope.

**Does it work with my logging engine / sink / cloud platform?**
It uses the standard MEL contract. The repository's custom-provider interop tests support that
contract, while the consuming host must validate actual provider field mapping, scope support,
filtering, exceptions and publishing/runtime requirements. Nilog has no transport of its own.

**Is it AOT / trimming safe?**
`Nilog.Core` enables `<IsAotCompatible>true</IsAotCompatible>` and treats Release warnings as errors. Publish and test the complete consuming application with its actual providers to establish Native AOT/trimming compatibility.

**What does `Nilog.Analyzers` check?**
Eight rules: `NILOG001` (interpolated templates, with a
one-click code fix), `NILOG002` (placeholder/argument count mismatch), `NILOG003` (concatenated or
`string.Format` templates), `NILOG004` (duplicate named placeholder), `NILOG005` (positional
placeholders, Info), `NILOG006` (an exception passed as a template value), `NILOG007` (malformed
template), and `NILOG008` (lowercase initial letter, Info) — on supported
`Write*`/`Nilogger.Log` call shapes. It's a separate, opt-in package — not referenced by
`Nilog.Core` — so installing `Nilog` never pulls it in automatically.

---

## 📄 License

MIT © Gehan Fernando. Full docs at [github.com/gcfernando/Nilog](https://github.com/gcfernando/Nilog).

---

## Documentation links

[Read all Nilog guides online](https://gcfernando.github.io/nilog-dotnet-logging/documentation/) · [Project overview](https://gcfernando.github.io/nilog-dotnet-logging/) · [All developer projects](https://gcfernando.github.io/gcfernando/projects/)
