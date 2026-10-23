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
| Add Nilog to an existing ILogger application | [Quick start](README.md#-quick-start) and [installation](README.md#-install) |
| Choose typed logging or exception overloads | [Method selection](README.md#-choosing-the-right-method) and [API reference](README.md#-api-reference) |
| Configure levels, providers, cache or flush hooks | [Configuration](README.md#-optional-advanced-configuration) |
| Enable the Roslyn analyzer package | [NILOG001–NILOG008 reference](README.md#-static-analysis-niloganalyzers) |
| Integrate ASP.NET Core, workers or Functions | [Recipes](README.md#-recipes) |
| Understand allocations and benchmark limits | [Architecture](README.md#-how-it-works), [benchmarks](README.md#-benchmarks) and [limitations](README.md#-limitations) |
| Build and run repository tests | [Development and testing](README.md#-build-test-benchmark) |
| Read the package-facing guide | [NuGet README](Nilog/README.nuget.md) |
| Report a vulnerability or check release history | [Security policy](SECURITY.md) and [changelog](CHANGELOG.md) |

## 🔗 Source references

[Core implementation](Nilog/Nilog.Core/Nilogger.cs) · [High-arity source generator](Nilog/Nilog.SourceGenerators/HighArityOverloadGenerator.cs) · [Pinned SDK](global.json) · [CI workflow](.github/workflows/ci.yml)

Nilog is a call-site layer over existing providers. Disabled typed-call allocation claims do not cover argument-expression evaluation or allocations performed by an enabled provider. Historical benchmark tables describe their stated harness and environment, not a guarantee for every application.

## 🌐 Published documentation

This index is also rendered by the repository's GitHub Pages site. Relative links above point to the authored repository documents; package READMEs target NuGet readers and may use absolute GitHub links.

[Repository](https://github.com/gcfernando/nilog) · [Project overview](README.md)
