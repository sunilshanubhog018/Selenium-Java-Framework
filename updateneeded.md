# Framework Updates Needed

**Project:** Selenium Banking Framework (ParaBank)  
**Repo reference:** https://github.com/sunilshanubhog018/Selenium-Java-Framework  
**Local path:** `C:\workspaces\SeleniumAutomation\SeleniumBankingFramework`  
**Purpose:** Checklist of improvements before using this as a strong SDET portfolio project.  
**Priority order:** Do P0 first, then P1, then P2.

---

## Status snapshot (current)

| Area | Status | Notes |
|------|--------|--------|
| POM + page objects | Good | Keep and extend |
| BaseTest / BasePage | Good | ThreadLocal, multi-browser |
| E2E + data-driven | Good | ParaBank flows exist |
| CI (GitHub Actions) | Partial | Soft-fails; needs hardening |
| README | Outdated | Still says “Week 1 / planned” |
| Repo hygiene | Poor | `target/`, `test-output/`, `allure-results/` committed |
| Rest Assured / API | Missing | Next skill after polish |
| Playwright | Not needed yet | Phase 3 only |

---

## P0 — Critical (do first)

### 1. Remove generated / build folders from Git

**Why:** Repo looks unprofessional; GitHub language bar shows ~56% HTML because of Allure/report files. Reviewers see noise, not code.

**Folders to stop tracking:**

- `target/`
- `test-output/`
- `allure-results/`
- Any `screenshots/` or `logs/` if present

**Commands (from project root):**

```bash
git rm -r --cached target test-output allure-results
```

**Update `.gitignore` to include at least:**

```gitignore
# Build
target/
out/
build/

# Test outputs
test-output/
allure-results/
allure-report/
screenshots/
logs/
*.log

# IDE
.idea/
*.iml
.vscode/
.settings/
.classpath
.project

# OS
.DS_Store
Thumbs.db

# Secrets
*.env
credentials.txt
```

Then commit:

```bash
git commit -m "Remove build artifacts and generated reports from version control"
```

---

### 2. Rewrite README.md (recruiter-facing)

**Why:** Current README still says “Week 1 starting soon” and “Technologies (Planned)” while the framework already has POM, CI, E2E, Allure.

**README must include:**

1. **Title + one-line description**  
   ParaBank banking automation with Selenium + Java + TestNG + POM
2. **Tech stack (actual, not planned)**  
   Java 21, Selenium 4.x, TestNG, Maven, WebDriverManager, Apache POI, Allure, Extent, GitHub Actions
3. **Features**  
   - Page Object Model  
   - Explicit waits in BasePage  
   - ThreadLocal driver (parallel-ready)  
   - Data-driven Excel tests  
   - E2E banking flows (register, login, transfer, bill pay, activity)  
   - CI headless Chrome  
   - Allure + TestNG reports
4. **Project structure** (short tree)
5. **How to run locally**

   ```bash
   mvn clean test
   ```

6. **How CI works** (push/PR on `main` → GitHub Actions)
7. **Test suites** (smoke / E2E / data-driven from `testng.xml`)
8. **Optional:** screenshot of Allure or CI badge

**Remove:** “Work in Progress - Week 1 starting soon!”  
**Replace learning timeline** with “Completed” vs “Next” if you keep a roadmap.

---

### 3. Fix CI so failures actually fail the pipeline

**File:** `.github/workflows/selenium-tests.yml`

**Problem:**

```yaml
run: mvn clean test
continue-on-error: true   # BAD for portfolio — always looks green
```

**Change:**

- Remove `continue-on-error: true` on the test step  
- Prefer a **smoke suite** on every push (faster, more reliable), full suite on schedule or manual dispatch  
- Keep report upload with `if: always()` so reports upload even when tests fail  

**Suggested approach:**

| Trigger | Suite |
|---------|--------|
| push / PR | Smoke only (`RegisterTest`, `LoginTest`) |
| workflow_dispatch / nightly | Full `testng.xml` |

Optional: set `headless=true` via env / config in CI (already partially handled in `BaseTest` via `CI` env).

---

## P1 — Stability & code quality

### 4. Reduce / remove `Thread.sleep`

**Why:** Interviewers flag fixed sleeps; flaky on CI.

**Where:** `EndToEndTest` and other tests use `pause()` / `Thread.sleep`.

**Change:**

- Prefer existing `BasePage` waits (`click`, `type`, `isDisplayed`, `waitForElementToDisappear`)  
- Add targeted waits for specific conditions (URL contains `overview`, element visible)  
- Keep sleep only as last resort with a short comment if ParaBank is truly slow  

---

### 5. Move raw Selenium out of tests into page objects

**Examples of leakage today:**

- `getDriver().findElement(By.linkText("Log Out")).click()` inside tests  
- Direct `By.id("rightPanel")` assertions in E2E tests  

**Change:**

- Add methods on a shared page (e.g. `HomePage` / `AccountsOverviewPage`):  
  - `logout()`  
  - `getRightPanelText()`  
  - `isTransferComplete()`  
  - `isBillPayComplete()`  
- Tests should only call page methods + Assert  

---

### 6. Strengthen assertions (especially bill pay / transfer)

**Problem:** Assertions like `pageText.contains("payment")` or `"successfully"` are too loose (false positives).

**Change:**

- Assert specific known success strings, e.g.:  
  - `"Transfer Complete"`  
  - `"Bill Payment Complete"`  
- Optionally assert amount/payee on confirmation page  
- Avoid matching generic words alone  

---

### 7. Wait strategy cleanup

**Current:** Implicit wait + explicit wait both enabled in `BaseTest` / `BasePage`.

**Recommended:**

- Prefer **explicit waits only**  
- Set implicit wait to `0` or a very small value  
- Document why in a short code comment (good interview talking point)

---

### 8. Naming & package consistency

| Item | Issue | Suggested fix |
|------|--------|----------------|
| `Endtoenddatadriventest.java` | Inconsistent naming | `EndToEndDataDrivenTest.java` |
| Class names vs file names | Match Java conventions | PascalCase always |
| Package layout | All under `src/test/java` | OK for now; optional later split `main` vs `test` if you grow library code |

Update `testng.xml` class names after renames.

---

### 9. Config & credentials hygiene

**File:** `src/test/resources/config.properties`

**Changes:**

- Do not use real personal passwords  
- Prefer demo credentials only for public ParaBank  
- Support override via system properties / env for CI:

  ```text
  browser, headless, base.url, test.username, test.password
  ```

- Document in README that credentials are for public demo app only  
- Ensure sensitive files stay out of git (already partially in `.gitignore`)

**Note:** `ConfigReader` loads from `src/test/resources/config.properties` — keep that path; ensure CI working directory is project root when running Maven.

---

## P2 — Portfolio upgrades (after P0 + P1)

### 10. Add Rest Assured (API automation) — high priority for jobs

**Why:** Market expects UI + API for SDET (4–8 YOE). Playwright can wait.

**Ideas:**

- New package: `api/` with Rest Assured client  
- 3–5 API tests (public API or ParaBank-related if available)  
- Same TestNG suite group: `api`  
- Mention in README: “UI (Selenium) + API (Rest Assured)”

---

### 11. Parallel execution (optional polish)

**Current:** ThreadLocal is ready; `testng.xml` comments mention parallel but suite may not enable it.

**Change (when stable):**

```xml
<suite name="ParaBank Banking Test Suite" parallel="methods" thread-count="2">
```

Start with `thread-count="2"` only after sleeps are gone and tests are independent.

---

### 12. Smoke vs regression suites

**Split suites:**

| File | Content |
|------|---------|
| `testng-smoke.xml` | Login + Register only |
| `testng.xml` | Full suite |

Wire smoke into CI; full suite local / nightly.

---

### 13. Logging instead of `System.out.println`

**Change:**

- Use SLF4J (already on classpath via `slf4j-simple`)  
- Replace noisy console prints with `log.info` / `log.debug`  
- Keep step logs for Allure via annotations if useful  

---

### 14. Allure usage improvements

- Ensure results go only under `target/allure-results` (not committed root `allure-results/`)  
- Add `@Epic` / `@Feature` / `@Story` / `@Severity` on key tests  
- Document: `mvn allure:serve` or `mvn allure:report`  

---

### 15. Playwright (later only — Phase 3)

**Do not start until:**

- [ ] Repo cleaned  
- [ ] README updated  
- [ ] CI fails on real test failure  
- [ ] Sleeps reduced  
- [ ] Rest Assured basics added  

Then optionally add a small Playwright module or separate mini-repo. Primary stack for interviews remains **Java + Selenium + Rest Assured + CI**.

---

## Suggested implementation order (2–3 weeks)

| Week | Focus | Done when |
|------|--------|-----------|
| **Week 1** | P0: gitignore cleanup, remove artifacts, README, CI fail-on-error | Clean GitHub page; green only if tests pass |
| **Week 2** | P1: waits, page methods for logout/panel, stronger asserts, rename classes | Stable local `mvn clean test` smoke |
| **Week 3** | P2: Rest Assured API package + smoke suite split | Resume line: UI + API + CI |

---

## Resume / interview talking points (after updates)

Use something like:

> Built a Java Selenium TestNG POM framework for ParaBank covering registration, login, fund transfer, bill pay, and account activity. Includes Excel data-driven tests, Allure reporting, and GitHub Actions CI with headless Chrome. Currently extending with Rest Assured API tests.

---

## Quick checklist (tick as you go)

### P0
- [ ] Remove `target/`, `test-output/`, `allure-results/` from Git  
- [ ] Update `.gitignore`  
- [ ] Rewrite README (stack, run steps, structure, features)  
- [ ] Remove CI `continue-on-error: true`  
- [ ] Optional: smoke suite for CI only  

### P1
- [ ] Replace most `Thread.sleep` with explicit waits  
- [ ] Move logout / panel checks into page objects  
- [ ] Tighten transfer/bill-pay assertions  
- [ ] Prefer explicit wait over long implicit wait  
- [ ] Rename `Endtoenddatadriventest` → `EndToEndDataDrivenTest`  
- [ ] Update `testng.xml` after renames  
- [ ] Review credentials in config  

### P2
- [ ] Rest Assured API tests  
- [ ] `testng-smoke.xml` + full suite split  
- [ ] SLF4J logging  
- [ ] Allure annotations  
- [ ] Parallel only after stability  
- [ ] Playwright only after API + polish  

---

## Out of scope for now

- Full rewrite of framework  
- Switching primary language to TypeScript  
- Dropping Selenium for Playwright as main stack  
- Committing more Allure history / large binaries  

---

## Notes

- ParaBank is a public demo app: registration can be flaky; your fallback-to-config-user pattern is fine — document it in README.  
- Keep this file as a living checklist; strike items or move to a `CHANGELOG.md` when done.  
- After P0+P1, re-push to GitHub and re-check the language breakdown (should be mostly Java).
