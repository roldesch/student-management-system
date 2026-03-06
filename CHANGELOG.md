Changelog

All notable changes to the Student Management System (SMS) are documented in this file.

The format follows Keep a Changelog principles, and the project adheres to Semantic Versioning.

[1.0.0] — Initial Governed Release

This release establishes the first stable version of SMS, including a governed CLI contract, a stable architectural boundary, and a comprehensive automated test suite.

Added
Core System

Domain model for students, teachers, and courses

Enrollment management between students and courses

Teacher assignment to courses

Grade assignment and removal

Repository-based persistence abstraction

In-memory repository implementation

SQLite persistence backend

Command-Line Interface

Production-ready SMS CLI

Deterministic command execution

Scriptable command design

Stable CLI command structure

Explicit version exposure via:

sms --version
CLI Contract

CLI v1 stability contract

Deterministic exit code semantics

Stable command hierarchy and argument behavior

Automation-safe CLI design

Architecture

Clean Architecture with explicit layer boundaries

Domain-Driven Design with a rich domain model

Immutable Response Models enforcing application boundaries

DTO-based application input contracts

Repository interfaces defined in the domain layer

Backend-agnostic persistence architecture

Testing

Layered test suite covering:

domain behavior

application orchestration

infrastructure persistence

integration workflows

CLI subprocess behavior

repository contract enforcement

Architectural Notes

The following architectural decisions are considered stable starting with v1.0.0:

Repository-driven architecture is the canonical persistence model

Application-level validation taxonomy is frozen

Domain entities never cross the application boundary

Application services act only as use-case orchestrators

CLI acts exclusively as a presentation adapter

These constraints define the architectural baseline against which future changes will be evaluated.

Compatibility

Version 1.0.0 establishes the first stable compatibility contract for the system:

CLI commands and exit codes are stable within the 1.x series

Architectural boundaries defined by the ADR set are considered binding

Future changes must preserve domain isolation and application boundaries