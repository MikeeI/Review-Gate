# Implementation Plan: PRs 1-5 Quick Wins

### Problem Statement

The codebase contains multiple quick-win opportunities including unused imports, invalid
dependencies, bare exception handling, JavaScript warnings, and inconsistent naming references that
reduce code quality and maintainability.

### Solution Overview

Implement 5 focused PRs with minimal code changes to eliminate code smell, fix dependency issues,
improve error handling, clean up linting warnings, and complete the project naming transition from
"Review Gate" to "Cursor Enhancer".

### Technical Architecture

- **Components**: Python source files, requirements.txt, JavaScript extension files, configuration
  constants
- **Dependencies**: ruff (Python linting), eslint (JavaScript linting), existing codebase utilities
- **Integration Points**: Existing logging utilities, file operation helpers, configuration
  constants

### Implementation Phases

#### Phase 1: Remove Unused Imports Across Python Codebase

##### Phase 1.1: Automated Import Cleanup

- [ ] Step 1.1.1: Run ruff import cleanup in
      `/root/projects/project-cursor-enhancer/cursor_enhancer_mcp.py`
- [ ] Step 1.1.2: Run ruff import cleanup in
      `/root/projects/project-cursor-enhancer/src/managers/response_manager.py`
- [ ] Step 1.1.3: Run ruff import cleanup in
      `/root/projects/project-cursor-enhancer/src/managers/trigger_manager.py`
- [ ] Step 1.1.4: Run ruff import cleanup in
      `/root/projects/project-cursor-enhancer/src/protocol/mcp_handler.py`
- [ ] Step 1.1.5: Run ruff import cleanup in
      `/root/projects/project-cursor-enhancer/src/utils/logging_utils.py`

##### Phase 1.2: Verification

- [ ] Step 1.2.1: Verify all Python files still import correctly with
      `python -c "import cursor_enhancer_mcp"`
- [ ] Step 1.2.2: Run full linting check with `python -m ruff check .` to confirm no new issues

#### Phase 2: Fix Invalid Python Dependency

##### Phase 2.1: Remove Built-in Module from Requirements

- [ ] Step 2.1.1: Remove `asyncio` line from
      `/root/projects/project-cursor-enhancer/requirements_simple.txt`

##### Phase 2.2: Verification

- [ ] Step 2.2.1: Test dependency installation with `pip install -r requirements_simple.txt` in
      clean environment
- [ ] Step 2.2.2: Verify no asyncio installation warnings or errors

#### Phase 3: Fix Bare Exception Handling Anti-Pattern

##### Phase 3.1: Update Response Manager Exception Handling

- [ ] Step 3.1.1: Replace bare except clause on line 128 in
      `/root/projects/project-cursor-enhancer/src/managers/response_manager.py`
    ```python
    except Exception as e:
        self.logger.warning(f"Failed to cleanup acknowledgement file: {e}")
    ```

##### Phase 3.2: Update Additional Exception Handlers

- [ ] Step 3.2.1: Review and update any additional bare except clauses found during ruff scan
- [ ] Step 3.2.2: Add proper logging context to exception handlers

##### Phase 3.3: Verification

- [ ] Step 3.3.1: Run `python -m ruff check src/managers/response_manager.py` to confirm no bare
      except warnings
- [ ] Step 3.3.2: Test exception handling by simulating file cleanup failures

#### Phase 4: Clean Up JavaScript Unused Variables

##### Phase 4.1: Automated JavaScript Cleanup

- [ ] Step 4.1.1: Run eslint auto-fix on
      `/root/projects/project-cursor-enhancer/cursor-extension/extension.js`
- [ ] Step 4.1.2: Run eslint auto-fix on
      `/root/projects/project-cursor-enhancer/cursor-extension/extension_original.js`
- [ ] Step 4.1.3: Run eslint auto-fix on
      `/root/projects/project-cursor-enhancer/cursor-extension/src/managers/file-watcher.js`
- [ ] Step 4.1.4: Run eslint auto-fix on
      `/root/projects/project-cursor-enhancer/cursor-extension/src/managers/popup-manager.js`

##### Phase 4.2: Manual Parameter Fixes

- [ ] Step 4.2.1: Prefix unused but required parameters with underscore in popup-manager.js
- [ ] Step 4.2.2: Remove truly unused variables that eslint cannot auto-fix

##### Phase 4.3: Verification

- [ ] Step 4.3.1: Run `npm run lint` in cursor-extension directory to confirm zero warnings
- [ ] Step 4.3.2: Test extension functionality to ensure no breaking changes

#### Phase 5: Update Remaining Review Gate References

##### Phase 5.1: Update File Path References

- [ ] Step 5.1.1: Update line 87 in
      `/root/projects/project-cursor-enhancer/src/managers/trigger_manager.py` to use
      "cursor_enhancer.log"
- [ ] Step 5.1.2: Update line 111 in
      `/root/projects/project-cursor-enhancer/src/managers/response_manager.py` to use
      "cursor*enhancer_ack*" prefix

##### Phase 5.2: Update System References

- [ ] Step 5.2.1: Update line 27 in
      `/root/projects/project-cursor-enhancer/src/managers/trigger_manager.py` from "review-gate-v2"
      to "cursor-enhancer"
- [ ] Step 5.2.2: Update line 118 in
      `/root/projects/project-cursor-enhancer/src/managers/trigger_manager.py` from "review-gate-v2"
      to "cursor-enhancer"

##### Phase 5.3: Update Constants for Consistency

- [ ] Step 5.3.1: Review `/root/projects/project-cursor-enhancer/src/config/constants.py` for any
      remaining review gate references
- [ ] Step 5.3.2: Update FilePatterns class to ensure all prefixes use "cursor_enhancer"
      consistently

##### Phase 5.4: Verification

- [ ] Step 5.4.1: Search entire codebase for remaining "review_gate" or "review-gate" references
- [ ] Step 5.4.2: Test MCP server startup to ensure log files are created with correct names

### Technical Details

- **Files to Create**: None - all modifications to existing files
- **Files to Modify**:
    - `/root/projects/project-cursor-enhancer/cursor_enhancer_mcp.py` - remove unused imports
    - `/root/projects/project-cursor-enhancer/requirements_simple.txt` - remove asyncio
    - `/root/projects/project-cursor-enhancer/src/managers/response_manager.py` - fix exception
      handling, update references
    - `/root/projects/project-cursor-enhancer/src/managers/trigger_manager.py` - update log file
      references
    - `/root/projects/project-cursor-enhancer/cursor-extension/src/managers/*.js` - fix unused
      variables
- **Key Functions/Classes**: ResponseManager.wait_for_extension_acknowledgement,
  TriggerManager.trigger_cursor_popup_immediately

### Validation Strategy

- **Unit Tests**: Run existing linting tools (ruff, eslint) to verify code quality improvements
- **Integration Tests**:
    - `python cursor_enhancer_mcp.py` - verify MCP server starts without import errors
    - `npm run lint:all` - verify all linting passes
    - Test popup functionality to ensure no breaking changes
- **Success Criteria**:
    - Zero unused import warnings from ruff
    - Zero unused variable warnings from eslint
    - Clean dependency installation
    - Consistent "cursor_enhancer" naming throughout codebase
    - Proper exception handling with logging context

### Risk Mitigation

- **Known Challenges**:
    - Automatic import removal might remove imports used in dynamic/conditional code
    - Mitigation: Test import functionality after each cleanup
- **Decision Points**:
    - Whether to prefix unused parameters with underscore vs removing entirely
    - Criteria: Keep parameters required for API compatibility, remove truly unused ones
    - Whether to update all "review-gate" references or maintain some for backwards compatibility
    - Criteria: Update all references for complete migration consistency
