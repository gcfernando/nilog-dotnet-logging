# Nilog

Typed structured logging extensions for `Microsoft.Extensions.Logging`, with optional Roslyn analyzers for C# projects.

[![NuGet package](https://img.shields.io/nuget/v/Nilog?color=2563eb)](https://www.nuget.org/packages/Nilog)
[![Continuous integration](https://github.com/gcfernando/nilog-dotnet-logging/actions/workflows/ci.yml/badge.svg)](https://github.com/gcfernando/nilog-dotnet-logging/actions/workflows/ci.yml)

## Overview

Nilog adds `WriteInformation`, `WriteWarning`, `WriteError` and related methods to your existing `ILogger`. Use it when you want typed message-template calls without declaring a separate logging method for each message. Your application still chooses its logging providers, levels and destinations.

- Typed overloads for up to 16 arguments; additional arguments use `params object[]`.
- Named structured properties, scopes, exception reports and flush callback hooks.
- Optional `Nilog.Analyzers` diagnostics NILOG001–NILOG008 and an interpolation code fix.
- Library targets for .NET 8, 9 and 10, with a build-time generator for higher-arity overloads.

Typed overloads avoid a call-site argument array. Enabled rendering, argument computation and provider processing can still allocate. The [measurement methodology and limitations](REFERENCE.md#guide-benchmarks) explain the recorded results; they are historical measurements rather than universal performance guarantees.

<a id="guide-quick-start"></a>

## Quick start

From an existing .NET application's directory:

```powershell
dotnet add package Nilog
```

Use the `ILogger` already supplied by your application:

```csharp
using Microsoft.Extensions.Logging;
using Nilog;

static void RecordOrder(ILogger logger, int orderId, decimal total)
{
    logger.WriteInformation("Order {OrderId} total {Total:N2}", orderId, total);
}
```

The example defines a method; call it with your application's logger. In a new console app, configure an `ILogger` provider separately, as shown in the [runnable demo](Nilog/Nilog.Demo/Program.cs). Nilog requires no service registration or configuration file.

## Requirements and installation

Use a project targeting .NET 8, 9 or 10 and a compatible `Microsoft.Extensions.Logging` provider.

The optional analyzer is available as a [source project](Nilog/Nilog.Analyzers/Nilog.Analyzers.csproj). A public `Nilog.Analyzers` package was unavailable from NuGet when checked on 2026-10-30. Follow the [Functions project's analyzer integration](Nilog/Nilog.Function/Nilog.Function.csproj) to reference it with `OutputItemType="Analyzer"` and `ReferenceOutputAssembly="false"`; adjust the project path for your application.

Read [NuGet package guidance](Nilog/README.nuget.md) or browse [published releases](https://github.com/gcfernando/nilog-dotnet-logging/releases) for package, DLL and demo downloads. Source development uses the exact SDK in [global.json](global.json); this is distinct from a package consumer's runtime requirements.

<a id="guide-choosing-the-right-method"></a>

## Usage

Keep message templates constant and pass values separately:

```csharp
logger.WriteWarning("Queue {QueueName} contains {Count} messages", "orders", 120);

using (logger.WriteScope("OrderId", 42))
{
    logger.WriteInformation("Processing order");
}
```

Use `WriteTrace`, `WriteDebug`, `WriteInformation`, `WriteWarning`, `WriteError` or `WriteCritical` for a fixed level. Use `Nilogger.Log` for a level determined at runtime. Check the [API and exception overload reference](REFERENCE.md) when passing exceptions or values statically typed as `object`; compiler and call shape affect overload selection.

<a id="guide-static-analysis-niloganalyzers"></a>

The optional source analyzers check supported call shapes for interpolation, template/value mismatches, concatenation, duplicate or positional names, misplaced exceptions, malformed templates and naming style. They do not perform general data-flow analysis.

## Configuration

Keep using your application's normal logging configuration for categories, levels, providers and sinks. Advanced Nilog cache, exception-report and flush hooks are documented in the [full reference](REFERENCE.md). Guard expensive argument computation with `logger.IsEnabled(...)` when necessary: C# evaluates arguments before calling Nilog.

## Development and testing

Install the SDK pinned by [global.json](global.json), plus the .NET runtimes for each target you intend to test. From the repository root:

```powershell
dotnet restore Nilog/Nilog.sln --locked-mode
dotnet build Nilog/Nilog.Core/Nilog.Core.csproj -c Release --no-restore
dotnet test Nilog/Nilog.Tests/Nilog.Tests.csproj -c Release --no-restore
dotnet test Nilog/Nilog.Analyzers.Tests/Nilog.Analyzers.Tests.csproj -c Release --no-restore
dotnet run --project Nilog/Nilog.Demo -c Release -f net10.0
```

Run benchmarks separately with `dotnet run --project Nilog/Nilog.Benchmark -c Release -f net10.0 -- --filter "*HighArityExtendedBenchmarks*"`. Reproduce workloads and report environment and provider behavior before interpreting timings. Keep SDK updates and dependency lock regeneration together.

The root [CI workflow](https://github.com/gcfernando/nilog-dotnet-logging/actions/workflows/ci.yml) runs core and analyzer tests. The existing [release workflow](https://github.com/gcfernando/nilog-dotnet-logging/actions/workflows/release.yml) gates core package publication on core tests; it does not publish the analyzer package or rerun analyzer tests. The nested historical workflow is outside GitHub's root workflow discovery.

## Troubleshooting and limitations

- Use constant named templates instead of interpolation or concatenation to retain structured properties.
- Seventeen or more arguments use the params path; all-object arguments and compiler versions can affect overload binding.
- Enabled logging, scope value boxing, formatting, providers and expensive arguments can allocate.
- `FlushAsync` calls registered callbacks; register your buffering sink's flush operation explicitly.
- Exception reports are not a redaction boundary. The original exception reaches the provider; applications must remove secrets and personal data.
- Library AOT compatibility analysis does not establish compatibility of a complete host. Publish and test your application with its actual providers.

See [detailed limits, cache behavior and measurement qualifications](REFERENCE.md) and the [security policy](SECURITY.md).

## Contributing and support

Read [CONTRIBUTING.md](CONTRIBUTING.md). For [issues](https://github.com/gcfernando/nilog-dotnet-logging/issues), include target framework, compiler version, provider and a minimal call shape. Follow the [security policy](SECURITY.md) for private vulnerability reports.

[Documentation index](documentation.md) · [Full reference](REFERENCE.md) · [Changelog](CHANGELOG.md) · [Repository standards](REPOSITORY_STANDARDS.md)

## License

MIT, copyright Gehan Fernando. See [LICENSE](LICENSE).

## Detailed reference

<a id="-nilog--low-allocation-structured-logging-extensions-for-net"></a>
<a id="high-performance-c-structured-logging-extensions-for-microsoftextensionslogging"></a>
<a id="in-plain-words"></a>
<a id="-install"></a>
<a id="️-optional-advanced-configuration"></a>
<a id="-optional-advanced-configuration"></a>
<a id="-before---after"></a>
<a id="-how-it-works"></a>
<a id="-build-test-benchmark"></a>
<a id="️-build-test-benchmark"></a>
<a id="guide-benchmarks"></a>
<a id="-limitations"></a>
<a id="️-limitations"></a>
<a id="-roadmap"></a>
<a id="-license"></a>

The [full reference](REFERENCE.md) preserves the detailed API guide, historical measurements or screenshots, and examples previously included here.
