# Framework Updates Needed

**Project:** Selenium Banking Framework (ParaBank)  
**Repo:** https://github.com/sunilshanubhog018/Selenium-Java-Framework  
**Local path:** `C:\workspaces\SeleniumAutomation\SeleniumBankingFramework`  
**Last re-check (GitHub `main`):** 30 July 2026  

---

## Re-check summary (what changed since first review)

| Item | First review | Now on GitHub | Status |
|------|--------------|---------------|--------|
| Rest Assured / API package | Missing | **Added** — `rest-assured` 5.5.0, Jackson, `com.parabank.api.*` (BaseApiTest, ApiSpecs, LoginApiTest, AccountApiTest) | **Improved** |
| `pom.xml` API deps | No | **Yes** | **Done** |
| `updateneeded.md` on GitHub | No | **Yes** (checklist file committed) | Note only |
| Remove `target/` from Git | Open | Still present (~37 paths) | **Still open** |
| Remove `test-output/` from Git | Open | Still present (~84 paths) | **Still open** |
| Remove `allure-results/` from Git | Open | Still present (**~5000+ paths**) | **Still open (worst)** |
| Rewrite README | Open | Still “Week 1 starting soon” / Technologies Planned | **Still open** |
| CI `continue-on-error: true` | Open | Still present on `mvn clean test` | **Still open** |
| `.gitignore` includes `allure-results/` | Partial | Still missing explicit `allure-results/` | **Still open** |
| Reduce `Thread.sleep` / `pause` | Open | EndToEndTest still heavy (~31 pause/sleep uses) | **Still open** |
| Logout / panel into page objects | Open | Still raw `By.linkText` in E2E/Login tests | **Still open** |
| Stronger transfer/bill asserts | Open | Not re-verified as tightened | **Still open** |
| Rename `Endtoenddatadriventest` | Open | Still that name in tree + `testng.xml` | **Still open** |
| API tests wired into `testng.xml` | N/A | **Not wired** — suite only lists UI tests | **New gap** |
| Smoke vs full suite split | Open | Still single full `testng.xml` for Surefire | **Still open** |
| SLF4J instead of System.out | Open | API tests still use `System.out.println` | **Still open** |
| Parallel suite enabled | Optional | Still commented only | **Still open (P2)** |
| Playwright | Later | Correctly not started | **OK (deferred)** |

### Bottom line of re-check

- **Reduced / improved:** API automation foundation (Rest Assured + package structure + deps).  
- **Not reduced:** P0 hygiene (artifacts, README, CI fail-on-error) — still the biggest portfolio blockers.  
- **New follow-up:** Wire API tests into TestNG/Maven so `mvn clean test` actually runs them.

---

## Status snapshot (current)

| Area | Status | Notes |
|------|--------|--------|
| POM + page objects | Good | Keep and extend |
| BaseTest / BasePage | Good | ThreadLocal, multi-browser |
| E2E + data-driven UI | Good | ParaBank flows exist |
| **API (Rest Assured)** | **Started** | Package + deps present; not in suite yet |
| CI (GitHub Actions) | Partial | Soft-fails; needs hardening |
| README | Outdated | Still says “Week 1 / planned” |
| Repo hygiene | Poor | `target/`, `test-output/`, huge `allure-results/` still committed |
| Playwright | Not needed yet | Phase 3 only |

---

## P0 — Critical (do first) — mostly still open

### 1. Remove generated / build folders from Git  ❌ OPEN

**Why:** Repo looks unprofessional; language bar skewed by Allure HTML/JSON noise.

**Still on GitHub `main` as of re-check:**

- `target/`
- `test-output/`
- `allure-results/` (thousands of files)

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

Then:

```bash
git commit -m "Remove build artifacts and generated reports from version control"
git push
```

**Note:** `.gitignore` already lists `target/` and `test-output/` but those folders are **still tracked** (added before ignore). Must `git rm --cached`. Add **`allure-results/`** explicitly — currently not listed.

---

### 2. Rewrite README.md (recruiter-facing)  ❌ OPEN

**Still on GitHub:** “Work in Progress - Week 1 starting soon!” and “Technologies (Planned)” including Java 11 (project uses 21).

**README must include:**

1. Title + one-line description (ParaBank UI + API automation)
2. **Actual** stack: Java 21, Selenium 4.x, TestNG, Maven, Rest Assured, POI, Allure, GitHub Actions
3. Features (POM, ThreadLocal, Excel DDT, E2E, CI, API tests)
4. Project structure
5. How to run: `mvn clean test`
6. CI behaviour
7. Suites (smoke / UI / API) once split

**Remove:** Week 1 WIP language.

---

### 3. Fix CI so failures actually fail the pipeline  ❌ OPEN

**File:** `.github/workflows/selenium-tests.yml`  

**Still present:**

```yaml
run: mvn clean test
continue-on-error: true
```

**Change:**

- Remove `continue-on-error: true`
- Prefer smoke on push/PR; full suite on `workflow_dispatch`
- Keep report upload with `if: always()`

---

## P1 — Stability & code quality — still open

### 4. Reduce / remove `Thread.sleep`  ❌ OPEN

**Re-check:** `EndToEndTest.java` still ~31 `pause` / sleep-style waits. Prefer `BasePage` explicit waits / URL-condition waits.

---

### 5. Move raw Selenium out of tests into page objects  ❌ OPEN

**Still:** logout / panel checks via raw `By` in tests. Add `logout()`, `getRightPanelText()`, success helpers on pages.

---

### 6. Strengthen assertions (bill pay / transfer)  ❌ OPEN

Avoid loose matches like only `"payment"` / `"successfully"`. Prefer exact success titles.

---

### 7. Wait strategy cleanup  ❌ OPEN

Prefer explicit waits; reduce long implicit wait (interview topic).

---

### 8. Naming consistency  ❌ OPEN

| Item | Still | Fix |
|------|--------|-----|
| `Endtoenddatadriventest.java` | Yes | → `EndToEndDataDrivenTest.java` + update `testng.xml` |

---

### 9. Config & credentials hygiene  ⚠️ PARTIAL

Demo ParaBank credentials in config is OK if documented. Prefer env overrides for CI. Do not commit real personal passwords.

---

## P2 — Portfolio upgrades

### 10. Rest Assured (API)  ✅ STARTED / ⚠️ INCOMPLETE

**Done on GitHub:**

- Dependencies: `rest-assured`, `json-schema-validator`, `jackson-databind`
- Packages:
  - `com.parabank.api.base.BaseApiTest`
  - `com.parabank.api.specs.ApiSpecs`
  - `com.parabank.api.tests.LoginApiTest`
  - `com.parabank.api.tests.AccountApiTest`
- Example: login API `GET /login/john/demo` with Hamcrest asserts

**Still needed:**

- [ ] Add API classes to `testng.xml` (or `testng-api.xml`) so Maven runs them  
- [ ] Document API base URL / how to run API-only  
- [ ] More tests (accounts, negative login) if stable  
- [ ] Replace `System.out` with logging  
- [ ] Mention UI + API on README  

**Suggested `testng.xml` addition (example):**

```xml
<test name="API Tests">
    <classes>
        <class name="com.parabank.api.tests.LoginApiTest"/>
        <class name="com.parabank.api.tests.AccountApiTest"/>
    </classes>
</test>
```

---

### 11. Parallel execution  ⏳ LATER

Enable only after sleeps reduced and tests independent.

---

### 12. Smoke vs regression suites  ❌ OPEN

| File | Purpose |
|------|---------|
| `testng-smoke.xml` | Login + Register (+ optional 1 API smoke) |
| `testng.xml` | Full UI + API |

CI → smoke; local/nightly → full.

---

### 13. Logging  ❌ OPEN

Use SLF4J; reduce `System.out.println` in UI and API tests.

---

### 14. Allure improvements  ⚠️ PARTIAL

Maven points results under `target/allure-results` (good). Root `allure-results/` must not be committed. Add `@Epic` / `@Feature` later.

---

### 15. Playwright  ⏳ DEFERRED (correct)

Do not start until P0 done + API suite wired.

---

## Suggested order (updated after re-check)

| Week | Focus | Done when |
|------|--------|-----------|
| **This week (P0)** | Untrack artifacts, gitignore `allure-results/`, README, CI fail-on-error | Clean GitHub page; CI red if tests fail |
| **Next** | Wire API into TestNG; smoke suite for CI | `mvn clean test` runs UI + API |
| **Then (P1)** | Waits, page methods, asserts, rename class | Stable smoke locally + CI |
| **Later (P2)** | More API cases, logging, Allure tags | Resume: UI + API + CI |

---

## Quick checklist (tick as you go)

### Done / improved
- [x] Rest Assured dependency in `pom.xml`
- [x] API base + specs + sample login/account API tests
- [x] Playwright correctly not started yet

### P0 still open
- [ ] Remove `target/`, `test-output/`, `allure-results/` from Git  
- [ ] Add `allure-results/` to `.gitignore`  
- [ ] Rewrite README (real stack + UI/API + how to run)  
- [ ] Remove CI `continue-on-error: true`  
- [ ] Optional: smoke suite for CI only  

### P1 still open
- [ ] Replace most `Thread.sleep` / `pause` with explicit waits  
- [ ] Move logout / panel checks into page objects  
- [ ] Tighten transfer/bill-pay assertions  
- [ ] Prefer explicit wait over long implicit wait  
- [ ] Rename `Endtoenddatadriventest` → `EndToEndDataDrivenTest`  
- [ ] Update `testng.xml` after renames  

### P2 / API completion
- [ ] **Wire API tests into TestNG / Surefire**  
- [ ] `testng-smoke.xml` + full suite split  
- [ ] SLF4J logging  
- [ ] Allure annotations  
- [ ] Parallel only after stability  
- [ ] Playwright only after polish  

---

## Resume line (update after P0 + API wired)

> Built a Java Selenium TestNG POM framework for ParaBank (register, login, transfer, bill pay, activity) with Excel data-driven UI tests, Rest Assured API tests, Allure reporting, and GitHub Actions CI (headless Chrome).

---

## Notes

- Re-check source: public GitHub `main` tree + raw files (README, workflow, pom, testng, API sources).  
- Local folder may differ until you `git pull` / push P0 fixes.  
- Keep this file as a living checklist; mark items `[x]` when verified on GitHub, not only local.  

**Next single best action:** run the `git rm --cached` cleanup + push, then rewrite README — biggest visual win for recruiters.
