**LED Matrix Roadmap And Planning Guide**

Use this document as the primary context for future planning sessions on the LED Matrix project. It is both the long-range roadmap for completing the project and the working guide for agents that refine one roadmap step into an implementation-ready plan. Any future planning agent should treat this file as the source of truth unless the user explicitly overrides a decision.

**Project Background**

This repository controls a 64x32 RGB LED matrix connected to a Raspberry Pi 3B. It now has a FastAPI backend that manages display lifecycle plus standalone Python display scripts that render on the matrix.

The project is currently operated by SSHing into the Raspberry Pi and launching a display in tmux. Code deployment is done with rsync from VS Code tasks. There is a second "prod" rsync target, but the project is expected to converge on a single Raspberry Pi target unless future requirements change.

The goal is to make the project coherent, reliable, and maintainable without turning it into a large platform.

**Current Repository Context**

- [main.py](main.py) is the current FastAPI entrypoint.
- [backend/app/main.py](backend/app/main.py) contains the backend app factory and lifespan wiring.
- [backend/app/api/displays.py](backend/app/api/displays.py) and [backend/app/services/manager.py](backend/app/services/manager.py) are the core display-control surfaces.
- [displays/active/meetings.py](displays/active/meetings.py), [displays/active/weather.py](displays/active/weather.py), [displays/active/sports_display.py](displays/active/sports_display.py), and [displays/active/text_scroll.py](displays/active/text_scroll.py) are the main display implementations.
- [displays/active/news.py](displays/active/news.py) is incomplete and should not be assumed to be MVP-ready.
- [pyproject.toml](pyproject.toml) and [uv.lock](uv.lock) are the dependency sources.
- [.vscode/tasks.json](.vscode/tasks.json) contains the current rsync workflow.
- [rgb-matrix.sh](rgb-matrix.sh) is part of the Raspberry Pi hardware/bootstrap story.
- [README.md](README.md) will need a substantial rewrite once the architecture is updated.

**Working Assumptions And Target Architecture**

Unless the user says otherwise, planning should assume all of the following:

- The long-term target is one Raspberry Pi hosting both backend and frontend.
- The web interface becomes the primary way displays are controlled.
- Exactly one display is active at a time.
- The control plane starts automatically on boot and restores the last selected display.
- A FastAPI backend owns display lifecycle and state.
- A React frontend is the primary operator interface.
- A DisplayManager and explicit display registry replace raw script discovery and ad hoc process spawning.
- Configuration and secrets on the Raspberry Pi can live in manually managed env or secret files.
- The first React and FastAPI version should prioritize parity plus reliability.
- The Raspberry Pi runs the control plane through systemd.
- Deployments should be consistent, rsync-based, and not require routine SSH usage for normal operation.
- Separate dev and prod Raspberry Pi targets are out of scope for now.
- The React app should normally be built locally and deployed as static assets to the Pi.
- The UI may eventually be reachable from outside the local network, one shared login for trusted people is acceptable, and remote access should prefer a protected path such as Tailscale rather than direct public exposure.

**Roadmap**

The roadmap below is intentionally broken into manageable steps that should be small enough to plan and implement over one or a few agent sessions at a time. A future planning agent should usually refine one roadmap step, or one coherent subset of a step, not the entire roadmap at once.

1. Audit and prepare the migration surface.
   Document which display scripts are active, experimental, broken, or test-only. Remove ambiguity about what belongs in the MVP and what should be deferred. Confirm which files and assets are still needed.

2. Modernize Python project structure and dependency management.
   Maintain the pyproject + lockfile workflow under uv. Keep pure Python dependencies separated from Raspberry Pi specific system and hardware dependencies.

3. Add centralized configuration and runtime state handling.
   Introduce configuration for matrix settings, resource paths, default behavior, credential paths, and persisted state. Stop hard-coding values like coordinates, font paths, and matrix options inside display scripts.

4. Establish a clean backend package layout.
   Create a coherent backend structure for API routes, display management, runtime services, configuration, and persistence. Treat the current Flask code as migration reference only.

5. Design and implement the display runtime model.
   Create a DisplayManager and explicit display registry. Define how displays are started, stopped, monitored, and identified. Ensure only one display is active at a time and switching behavior is deterministic.

6. Refactor the MVP displays behind the shared runtime contract.
   Port the kept displays so they can run under the manager with consistent startup, shutdown, logging, and configuration injection. Remove or isolate test-only code from the production display surface.

7. Replace Flask with a FastAPI control plane.
   Implement endpoints for health, authentication, display listing, active status, start, stop, and state restoration. The backend should become the single control interface for the UI and for service startup behavior.

8. Build the React MVP.
   Implement a frontend that can list displays, show the current active display, start and stop displays, surface backend errors, and behave correctly across page refreshes and backend restarts.

9. Add lightweight authentication and safe access patterns.
   Implement the shared-login model in a way that is simple but not careless. Keep the plan aligned with private-network access first, and only add public exposure patterns if the user explicitly chooses them.

10. Set up Raspberry Pi service management and boot behavior.
    Create the systemd-based startup flow for the backend and the last-selected display restoration behavior. Define the one-time Raspberry Pi setup steps clearly enough that the user can execute them manually.

11. Simplify deployment and operational workflow.
    Replace the current ambiguous sync and deploy story with a clearer workflow that covers frontend build output, file sync, service restart, logs, and smoke testing.

12. Finish documentation, cleanup, and maintenance guardrails.
    Rewrite [README.md](README.md), remove obsolete Flask-era artifacts, add minimal automated quality checks, and document how to add or modify displays in the new architecture.

**How To Refine A Roadmap Step**

Refine one roadmap step, or one coherent subset of a step, at a time. The refined result is complete only when an implementation agent could start work immediately without another planning pass for basic structure, dependencies, or sequencing.

When refining a step, the planning agent should:

1. Read this entire document first.
2. Identify the exact roadmap step or subset being refined.
3. Gather current repository context relevant to that step.
4. Check whether any assumptions here have been superseded by codebase changes or new user instructions.
5. Produce an implementation-ready plan.
6. Review that plan for gaps, contradictions, bad sequencing, or oversized scope.
7. Revise it until it is ready for handoff.

Every refined step must include:

- Objective
- Why the step matters and what it unlocks
- In-scope and out-of-scope work
- Exact files, modules, and subsystems likely to be affected
- Dependencies on earlier or parallel roadmap steps
- Proposed sequence of work
- Risks, open questions, and edge cases
- Validation and acceptance criteria
- A handoff section that tells the implementation agent what to do first

Every refined step must also separate work into these two buckets with no ambiguity:

- Local work the agent can do: repository analysis, code edits, tests that can run locally, documentation, configuration templates, deployment scripts, frontend builds, backend refactors, and service file generation.
- Raspberry Pi work the user must do manually: physical setup, OS package installation when not already automated, hardware library installation or validation, secret placement on the device, enabling services, rebooting, and real hardware verification unless the repo already provides a safe automated path.

A refined step is not ready if the scope is too large for an implementation session, the work order is unclear, the local versus Raspberry Pi boundary is blurred, validation is vague, or unresolved unknowns are hidden instead of called out.

Before finalizing a refined step, verify that it is aligned with the assumptions above, manageable for an implementation agent, concrete about affected files and subsystems, explicit about local versus Raspberry Pi work, and free of unnecessary infrastructure. It should not quietly depend on manual SSH or tmux usage as part of the desired end state.

The exact output format can vary, but it should cover the same content as these headings: Objective, Why This Step Matters, In Scope, Out Of Scope, Affected Files And Components, Local Work For The Agent, Raspberry Pi Work For The User, Proposed Sequence, Risks And Open Questions, Validation, and Handoff To Implementation Agent.

**Verification Expectations Across The Full Roadmap**

The completed project should be validated at multiple levels:

1. Local backend verification for API behavior, configuration loading, state persistence, and display management logic.
2. Local frontend verification for display control flows, state refresh, and visible error handling.
3. Raspberry Pi verification for matrix behavior, service startup, reboot restore, and real hardware display switching.
4. Deployment verification for sync, restart, and smoke-test flow.
5. Access verification for the chosen authentication and remote-access model.

**Deliberate Non-Goals For The First Completion Pass**

Do not default to adding the following unless the user explicitly expands scope:

- Multi-device fleet management
- Advanced scheduling and playlists
- Complex observability stacks
- Full CI or CD pipelines
- Containerization as the default runtime model
- Public-internet exposure without a specific requirement

**Default Planning Bias**

Prefer solutions that are:

- Simple to understand
- Stable on a Raspberry Pi
- Friendly to one-person maintenance
- Easy to deploy repeatedly
- Easy to debug when hardware or network conditions are imperfect

Avoid solutions that add heavy infrastructure without clearly reducing operational pain.
