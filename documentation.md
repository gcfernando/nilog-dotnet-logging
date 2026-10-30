---
layout: default
title: "Nilog — Documentation and Guides"
description: "Typed ILogger extensions and Roslyn analyzers for structured logging in .NET."
permalink: /documentation/
---

# Nilog Documentation

Find typed ILogger call patterns, provider configuration, analyzer guidance and reproducible development commands.

<a id="explore-more"></a>
<a id="markdown-source-library"></a>
<a id="read-online"></a>

## 🧭 Choose a guide

| Task | Guide |
|---|---|
| Add Nilog to an existing ILogger application | [Quick start](REFERENCE.md#-quick-start) and [installation](REFERENCE.md#-install) |
| Choose typed logging or exception overloads | [Method selection](REFERENCE.md#-choosing-the-right-method) and [API reference](REFERENCE.md#-api-reference) |
| Configure levels, providers, cache or flush hooks | [Configuration](REFERENCE.md#-optional-advanced-configuration) |
| Enable the Roslyn analyzer package | [NILOG001–NILOG008 reference](REFERENCE.md#-static-analysis-niloganalyzers) |
| Integrate ASP.NET Core, workers or Functions | [Recipes](REFERENCE.md#-recipes) |
| Understand allocations and benchmark limits | [Architecture](REFERENCE.md#-how-it-works), [benchmarks](REFERENCE.md#-benchmarks) and [limitations](REFERENCE.md#-limitations) |
| Build and run repository tests | [Development and testing](REFERENCE.md#-build-test-benchmark) |
| Read the package-facing guide | [NuGet README](Nilog/README.nuget.md) |
| Report a vulnerability or check release history | [Security policy](SECURITY.md) and [changelog](CHANGELOG.md) |

## 🔗 Source references

[Core implementation](https://github.com/gcfernando/nilog-dotnet-logging/blob/main/Nilog/Nilog.Core/Nilogger.cs) · [High-arity source generator](https://github.com/gcfernando/nilog-dotnet-logging/blob/main/Nilog/Nilog.SourceGenerators/HighArityOverloadGenerator.cs) · [Pinned SDK](https://github.com/gcfernando/nilog-dotnet-logging/blob/main/global.json) · [CI workflow](https://github.com/gcfernando/nilog-dotnet-logging/blob/main/.github/workflows/ci.yml)

Nilog is a call-site layer over existing providers. Disabled typed-call allocation claims do not cover argument-expression evaluation or allocations performed by an enabled provider. Historical benchmark tables describe their stated harness and environment, not a guarantee for every application.

## 🌐 Published documentation

This index is also rendered by the repository's GitHub Pages site. Relative links above point to the authored repository documents; package READMEs target NuGet readers and may use absolute GitHub links.

[Repository](https://github.com/gcfernando/nilog-dotnet-logging) · [Project overview](README.md)
