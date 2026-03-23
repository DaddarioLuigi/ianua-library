---
name: e2e-testing-capybara
description: >-
  Create and run end-to-end tests using Playwright for React/Next.js and Flask APIs.
  Use when writing browser automation, end-to-end UI flows, and integration checks.
---

# E2E Testing with Playwright

Full browser automation using Playwright (Chromium/WebKit/Firefox).

## Setup Requirements

Install dependencies:
```bash
pnpm add -D @playwright/test
npx playwright install
```

Create `playwright.config.ts` with:
- `baseURL` for local app
- retries on CI
- trace/screenshot/video on failure
- parallelization tuned for CI resources

Create a global setup that:
- starts Flask API and Next.js app (or assumes they are running)
- runs DB seed/migrations for E2E dataset
```

## Test Structure

E2E tests live in `tests/e2e/`. One file per user journey or feature.

```ts
import { test, expect } from "@playwright/test";

test("user can log in and view dashboard", async ({ page }) => {
  await page.goto("/login");
  await page.getByLabel("Email").fill("doctor@example.com");
  await page.getByLabel("Password").fill("password");
  await page.getByRole("button", { name: "Sign in" }).click();
  await expect(page.getByRole("heading", { name: "Dashboard" })).toBeVisible();
});
```

## Conventions

### Setup Pattern (Arrange → Act → Assert)
```ts
test("creates an item", async ({ page }) => {
  // Arrange
  await page.goto("/items/new");
  // Act
  await page.getByLabel("Name").fill("My item");
  await page.getByRole("button", { name: "Create" }).click();
  // Assert
  await expect(page.getByText("Item created")).toBeVisible();
});
```

## Running E2E Tests

```bash
pnpm playwright test
pnpm playwright test tests/e2e/auth.spec.ts
pnpm playwright test --headed
pnpm playwright test --debug
```

## Common Scenarios to Test

For each major feature, create system specs covering:
1. **Happy path**: main user journey from start to finish
2. **Validation errors**: form submission with invalid data
3. **Authorization**: unauthenticated and unauthorized access
4. **Async/UI updates**: loading states, optimistic updates, race conditions
