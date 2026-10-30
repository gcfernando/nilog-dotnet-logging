# Nilog

Typed structured logging extensions for `Microsoft.Extensions.Logging`, with optional Roslyn analyzers for C# projects.

## Overview

Nilog adds `WriteTrace`, `WriteDebug`, `WriteInformation`, `WriteWarning`, `WriteError` and `WriteCritical` to your existing `ILogger`. The library targets .NET 8, 9 and 10. Your application keeps its existing logging providers, filtering and destinations.

Typed overloads support up to 16 arguments and avoid a call-site argument array. Seventeen or more arguments use `params object[]`. Enabled rendering, value boxing, argument evaluation and providers can still allocate. Historical benchmark results and their limits are documented in the [full reference](https://github.com/gcfernando/nilog-dotnet-logging/blob/main/REFERENCE.md#guide-benchmarks).

## Install

From your application directory:

```powershell
dotnet add package Nilog
```

The optional analyzer is available as a [source project](https://github.com/gcfernando/nilog-dotnet-logging/blob/main/Nilog/Nilog.Analyzers/Nilog.Analyzers.csproj). A public `Nilog.Analyzers` package was unavailable from NuGet when checked on 2026-10-30. The [Functions integration example](https://github.com/gcfernando/nilog-dotnet-logging/blob/main/Nilog/Nilog.Function/Nilog.Function.csproj) references the project with `OutputItemType="Analyzer"` and `ReferenceOutputAssembly="false"` to keep it a build-time dependency.

## Quick start

Use a logger supplied by your existing application:

```csharp
using Microsoft.Extensions.Logging;
using Nilog;

static void RecordOrder(ILogger logger, int orderId, decimal total)
{
    logger.WriteInformation("Order {OrderId} total {Total:N2}", orderId, total);
}
```

Call the method with your application's `ILogger`. A standalone console app must configure a logging provider separately. Nilog needs no registration, initialization or configuration file.

## Usage and configuration

Keep templates constant and pass values separately. `WriteScope` adds scope properties; `Nilogger.Log` accepts a runtime-selected level. Normal logging levels, categories and sinks remain Microsoft.Extensions.Logging settings.

Guard expensive argument computation with `IsEnabled` where appropriate, because C# evaluates arguments before calling Nilog. Compiler version and statically object-typed arguments can affect overload binding. Use the [exception and overload reference](https://github.com/gcfernando/nilog-dotnet-logging/blob/main/REFERENCE.md) for exception calls and advanced hooks.

`Nilog.Analyzers` checks supported call shapes for NILOG001–NILOG008: interpolation, argument-count mismatch, concatenation, duplicate/positional names, misplaced exceptions, malformed templates and name style. Its interpolation fix does not provide general data-flow analysis.

## Limitations

- Disabled warmed typed-call allocation results do not establish zero allocation for a whole logging pipeline.
- Providers control formatting, transport, retention and sink allocation.
- `FlushAsync` awaits callbacks registered for buffering sinks; register your sink explicitly.
- Exception text limits are not a redaction boundary; the original exception reaches the provider.
- Library AOT analysis does not establish compatibility of your complete application and providers.

See the [security policy](https://github.com/gcfernando/nilog-dotnet-logging/blob/main/SECURITY.md) for component responsibilities and safe logging practices.

## Documentation and development

The [repository README](https://github.com/gcfernando/nilog-dotnet-logging/blob/main/README.md) provides source build and test commands using the SDK pinned in `global.json`. The [full reference](https://github.com/gcfernando/nilog-dotnet-logging/blob/main/REFERENCE.md) preserves recipes, API tables, configuration hooks and detailed measurements. See the [changelog](https://github.com/gcfernando/nilog-dotnet-logging/blob/main/CHANGELOG.md) for version history.

## Support and license

Report [issues](https://github.com/gcfernando/nilog-dotnet-logging/issues) with target framework, compiler, provider and a minimal call shape. Follow the [contribution guide](https://github.com/gcfernando/nilog-dotnet-logging/blob/main/CONTRIBUTING.md) for changes. MIT, copyright Gehan Fernando; see the [license](https://github.com/gcfernando/nilog-dotnet-logging/blob/main/LICENSE).
