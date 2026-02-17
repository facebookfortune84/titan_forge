# Plan to Fix Routing and Schema Mismatches

This document outlines the plan to refactor the TitanForge codebase to resolve routing inconsistencies, schema mismatches, and code redundancy.

## 1. Backend Refactoring

The backend will be refactored to have a single source of truth for all API routes and schemas.

### 1.1. Consolidate Routing

- **Centralize routing in `api/v1`**: All API endpoints will be moved from `main.py` to the appropriate router files in the `titanforge_backend/app/api/v1/` directory.
- **Remove redundant routers**: The functionality of `landing.py` and `landing_page.py` will be merged into a single `landing_router.py`. The `/agents` endpoint in `admin.py` will be removed in favor of the `agents.py` router.
- **Standardize route prefixes**: All routers will be included in `main.py` with the `/api/v1` prefix to ensure consistent API versioning. The `auth` router will have the prefix `/api/v1/auth`.
- **Remove `main.py` endpoint duplication**: All endpoints currently duplicated between `main.py` and the `api/v1` routers will be removed from `main.py`.

### 1.2. Align Schemas

- **Create a single source of truth for schemas**: The `titanforge_backend/app/schemas.py` file will be the single source of truth for all Pydantic models.
- **Sync with frontend types**: All Pydantic models in `schemas.py` will be updated to match the TypeScript types in `frontend/src/types/index.ts`. This includes field names, data types, and optional properties.
- **Address specific mismatches**:
    - `User` schema will be aligned with the frontend `User` type.
    - `Task` schema will be aligned to use `description` instead of `goal`.
    - `Product` schema will be updated to use `price` (and converted from cents to dollars in the API response) and `is_active`.
    - All other schemas will be reviewed and updated as needed.

## 2. Frontend Refactoring

The frontend will be updated to align with the refactored backend.

### 2.1. Update `api.ts`

- **Update API calls**: All API calls in `frontend/src/services/api.ts` will be updated to match the new backend routes. This includes URLs, request bodies, and response handling.
- **Remove FIX comments**: All `// FIX` comments in `api.ts` will be addressed and removed.

### 2.2. Update `types/index.ts`

- **Sync with backend schemas**: The TypeScript types in `frontend/src/types/index.ts` will be updated to perfectly match the Pydantic models in `titanforge_backend/app/schemas.py`.

## 3. Code Cleanup

- **Remove unused files**: After the refactoring, I will scan the entire repository for unused files and propose their deletion. This will include the redundant router files and any other files that are no longer needed.
- **Remove hardcoded paths**: I will replace hardcoded paths like `AGENT_NEW_RECRUITS_DIR` with a more configurable solution.

## 4. Testing

- **Create new integration tests**: I will write new integration tests to verify that the frontend and backend are correctly aligned. These tests will cover all major API endpoints and will test for correct request/response formats and data consistency.

## 5. New Features, UI/UX, and SEO

This is a large and separate task. After the codebase is cleaned up and stable, I will present a separate, detailed plan for this phase. This will allow us to focus on fixing the immediate issues first.

## Approval

Please review this plan. Once you approve, I will begin the implementation.
