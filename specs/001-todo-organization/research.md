# Research: Todo Application – Intermediate Level (Organization & Usability)

## Research Summary

This research document addresses the technical decisions required for implementing the intermediate level todo application features: task priorities, tags, search, filter, and sort functionality.

## Decision: Priority Representation and Ordering Logic

**Rationale**: Priorities need to be represented in a way that supports both user display and sorting operations. Using an enumeration with defined ordering ensures consistent behavior.

**Decision**: Implement priority as an enum with High > Medium > Low ordering for sorting operations. Store as string values "High", "Medium", "Low" with "Medium" as default.

**Alternatives considered**:
- Integer values (1, 2, 3) - rejected for less readability
- Single character codes (H, M, L) - rejected for less clarity

## Decision: Tag/Category Structure (Single vs Multiple Tags)

**Rationale**: Users need flexibility to categorize tasks with multiple contexts (e.g., a task could be both "work" and "urgent").

**Decision**: Implement tags as a list/array of strings allowing multiple tags per task. Validate for non-empty, trimmed strings to prevent invalid tags.

**Alternatives considered**:
- Single tag per task - rejected for limiting user flexibility
- Dictionary/object-based tags - rejected for unnecessary complexity

## Decision: Sorting and Filtering Strategies

**Rationale**: Sorting and filtering operations need to be efficient while affecting only the display layer without modifying underlying data.

**Decision**: Implement sorting and filtering as view-layer operations that return filtered/sorted views of the original data without modifying the source. Use Python's built-in sorted() and filter() functions with appropriate key functions.

**Alternatives considered**:
- Maintaining separate sorted lists - rejected for memory overhead
- In-place sorting - rejected for modifying original data structure

## Decision: Handling Optional Fields for Existing Tasks

**Rationale**: Existing Phase 1 tasks don't have priority or tags, so defaults must be provided for backward compatibility.

**Decision**: For existing tasks without priority, assign default "Medium" priority. For tags, initialize as empty list. This ensures all tasks have consistent data structure.

**Alternatives considered**:
- Null/None values - rejected for requiring additional null checks
- Separate handling for old vs new tasks - rejected for complexity

## Decision: CLI Usability for Added Features

**Rationale**: New features must be accessible through intuitive CLI commands that don't conflict with existing functionality.

**Decision**: Extend existing CLI commands with subcommands and flags:
- `add "task" --priority High --tags work,urgent`
- `list --filter-priority High --filter-tag work`
- `search "keyword" --sort priority`

**Alternatives considered**:
- Separate command namespaces - rejected for breaking existing CLI patterns
- Interactive mode - rejected for complexity and consistency with existing interface

## Research on Data Model Evolution

**Findings**: The existing task model needs extension to support new fields while maintaining backward compatibility. The approach will be to add optional fields with appropriate defaults that don't break existing functionality.

**Validation**: All new features can be implemented as additive changes without modifying existing task creation, viewing, updating, or deletion logic.

## Research on Search Implementation

**Findings**: Text-based search can be implemented using simple substring matching for both title and description fields. For better performance, search will be case-insensitive and match partial strings.

**Approach**: Implement search as a function that checks both title and description fields for the search term, returning matching tasks without modifying the original data.

## Research on Filter Implementation

**Findings**: Filtering can be implemented using Python's built-in filter() function or list comprehensions. Multiple filters can be applied sequentially for complex filtering requirements.

**Approach**: Create separate filter functions for each filter type (status, priority, tag) that can be combined as needed.