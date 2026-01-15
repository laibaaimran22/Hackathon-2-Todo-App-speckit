---
id: "005"
title: "Fix Cohere Model Deprecation Error"
stage: "red"
date: "2026-01-13"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "Phase-3"
branch: "main"
user: "laiba"
command: "fix"
labels: ["bug-fix", "api", "cohere", "model", "deprecation"]
links:
  spec: "specs/Phase-3/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "Phase-3/frontend/src/lib/cohere-client.ts"
tests: []
---

## User Prompt
"NotFoundError Status code: 404 Body: { \"id\": \"922a5e46-b4c1-4d3f-a9c6-72f8fffad928\", \"message\": \"model 'command-r-plus' was removed on September 15, 2025. See https://docs.cohere.com/docs/models for a list of models you can use instead.\" }"

## Response
Fixed the Cohere API error by updating the deprecated 'command-r-plus' model to the supported 'command-r' model in the cohere-client.ts file. The model was changed on line 141 from "command-r-plus" to "command-r" to resolve the 404 error indicating the model had been removed.

## Outcome
The Cohere API integration now uses a supported model and should no longer throw the deprecation error when making chat requests with tool calling functionality.

## Evaluation
The fix addresses the immediate error by using a supported model. The 'command-r' model is a capable alternative that supports tool calling functionality needed for the AI-powered todo chatbot.