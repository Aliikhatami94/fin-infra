# fin-api Development Plan

## Overview
This document tracks the development plan for the fin-api project (examples/fin-infra-template), including architectural decisions and implementation tasks.

## API Versioning Strategy

### Version 0 (Initial Release)
- **Status**: In Development
- **Description**: The first version of the API will be version 0 (v0)
- **Rationale**: Starting with version 0 allows us to iterate on the API design before committing to a stable v1 release
- **Endpoint Structure**: All endpoints will be prefixed with `/v0/` or accessible without version prefix during development

## Entry Point Architecture

### Primary Entry Points
The application uses a layered approach to entry points, prioritizing developer experience and deployment flexibility:

1. **`run.sh`** (Primary Development Entry Point)
   - Located at: `examples/run.sh`
   - Purpose: Development server with hot-reload
   - Features:
     - Automatic environment variable loading from `.env`
     - Configurable host and port
     - Uvicorn with reload enabled
     - Clear startup logging with useful URLs
   - Usage: `./run.sh` or `make run`

2. **`Makefile`** (Primary Automation Interface)
   - Located at: `examples/Makefile`
   - Purpose: Standardized command interface for all operations
   - Key Commands:
     - `make setup` - Complete project initialization
     - `make run` - Start development server (calls `run.sh`)
     - `make install` - Install dependencies
     - `make test` - Run tests
     - `make clean` - Clean cache files
   - Usage: `make <command>`

3. **`main.py`** (Application Definition)
   - Located at: `examples/src/fin_infra_template/main.py`
   - Purpose: FastAPI application definition and configuration
   - Note: This is NOT the entry point for running the server
   - Role: Defines the `app` object that `run.sh` and other tools reference

### Architecture Decision
- ✅ Use `run.sh` for running the development server
- ✅ Use `Makefile` for all automation and commands
- ❌ Do NOT use `python main.py` as the entry point
- ✅ `main.py` remains as the application definition only

## Implementation Tasks

### Phase 1: Core Setup
- [x] Create `run.sh` script for development server
- [x] Create `Makefile` with automation commands
- [x] Define `main.py` as application definition
- [x] Setup environment variable loading
- [x] Configure uvicorn with proper settings

### Phase 2: Documentation
- [ ] Update README.md to emphasize `run.sh` and `Makefile` usage
- [ ] Add clear examples of entry point usage
- [ ] Document the version 0 API strategy
- [ ] Create migration guide for any projects using old entry points

### Phase 3: Testing & Validation
- [ ] Test `run.sh` on different environments
- [ ] Validate all Makefile commands work correctly
- [ ] Ensure documentation is clear and accurate
- [ ] Test with fresh clone of repository

## Notes
- The examples directory already has both `run.sh` and `Makefile` implemented
- Current implementation follows best practices for Python web applications
- Entry point structure is designed for both development and production deployment flexibility
