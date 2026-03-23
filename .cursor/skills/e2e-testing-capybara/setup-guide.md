# E2E Testing Setup Guide (Playwright)

Complete setup guide for Playwright with a Flask API + Next.js frontend.

## 1. Install Dependencies

```bash
pnpm add -D @playwright/test
npx playwright install --with-deps
```

## 2. Base Configuration

Create `playwright.config.ts` with:
- `testDir: "./tests/e2e"`
- `use.baseURL` (e.g. `http://localhost:3000`)
- `trace: "on-first-retry"`, `screenshot: "only-on-failure"`, `video: "retain-on-failure"`
- CI retries (`retries: process.env.CI ? 2 : 0`)

## 3. Start Services for E2E

Ensure both services are available:
- Flask API (e.g. `http://localhost:5000`)
- Next.js app (e.g. `http://localhost:3000`)

Use Playwright `webServer` entries or a dedicated script that starts both.

## 4. Folder Structure

```bash
mkdir -p tests/e2e
```

Suggested layout:
- `tests/e2e/auth.spec.ts`
- `tests/e2e/patients.spec.ts`
- `tests/e2e/helpers/`

## 5. First Test

```ts
import { test, expect } from "@playwright/test";

test("sign in success", async ({ page }) => {
  await page.goto("/login");
  await page.getByLabel("Email").fill("doctor@example.com");
  await page.getByLabel("Password").fill("password");
  await page.getByRole("button", { name: "Sign in" }).click();
  await expect(page.getByRole("heading", { name: "Dashboard" })).toBeVisible();
});
```

## 6. Run Locally

```bash
pnpm playwright test
pnpm playwright test tests/e2e/auth.spec.ts
pnpm playwright test --headed
pnpm playwright test --debug
```

## 7. CI Configuration

In GitHub Actions:
- install Node + dependencies
- run `npx playwright install --with-deps`
- start test services
- run `pnpm playwright test`
- upload `playwright-report/` on failure

## Troubleshooting

### Browser dependencies missing (Linux CI)
Run:
```bash
npx playwright install --with-deps
```

### Flaky async UI assertions
- Prefer role/text locators over CSS-only selectors
- Wait for meaningful UI states (`toBeVisible`, `toHaveURL`)
- Avoid fixed sleeps unless strictly necessary

### API-authenticated flows
- Seed deterministic test users/tokens
- Reset test data between runs
