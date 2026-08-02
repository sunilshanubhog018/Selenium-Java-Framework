# Known Issues

Known limitations and intermittent failures in this framework. Many are constraints of the public [ParaBank](https://parabank.parasoft.com) demo environment (no SLA, shared database, occasional outages).

---

## 1. ParaBank Site Instability

**Affected Tests:** All tests  
**Symptom:** `TimeoutException` or connection errors  
**Cause:** ParaBank is a public demo site with no SLA. It occasionally goes down, responds slowly, or returns unexpected pages.  
**Mitigation:** `RetryAnalyzer` retries each failed test once automatically.

---

## 2. Auth Bypass on Invalid Login (active)

**Affected Tests:** `LoginTest.testInvalidLogin`, `testInvalidUsername`, `testInvalidPassword`, negative Excel rows in `DataDrivenLoginTest`  
**Symptom:** Submitting random username/password redirects to `overview.htm` as **John Smith** instead of showing an error. Confirmed via HTTP `POST /login.htm` → `302` to overview.  
**Cause:** Public ParaBank demo currently accepts arbitrary non-empty credentials (demo-site defect / misconfiguration). Empty-field validation still works.  
**Mitigation:** Negative login tests detect overview redirect and **skip** with a clear message instead of failing the suite. Re-enable hard assertions when the demo site restores proper auth.

---

## 3. Shared Database — Do Not INIT in CI

**Affected Tests:** Registration, login-with-fresh-user, E2E  
**Symptom:** Registered users disappear mid-suite; mass skips from failed `@BeforeClass` / `@BeforeMethod` login.  
**Cause:** `admin.htm` **Initialize** wipes the **shared** public database for every other user and CI job.  
**Mitigation:** DB init is **off by default**. Opt in only against a private ParaBank instance: `-Dparabank.init.db=true` or `PARABANK_INIT_DB=true`.

---

## 4. Registration Throttling

**Affected Tests:** `RegisterTest`, classes that register in `@BeforeClass`  
**Symptom:** Registration succeeds but welcome/overview does not appear, or registration fails silently  
**Cause:** ParaBank throttles rapid user registrations.  
**Mitigation:** `UserFactory.registerUniqueUser` retries registration up to 3 times with backoff.

---

## 5. Single Account — Transfer Tests

**Affected Tests:** `TransferFundsTest`, `EndToEndTest.testFundTransferFlow`  
**Symptom:** Transfer completes but total balance does not change  
**Cause:** New users only get 1 account. Transfers go from that account to the same account.  
**Mitigation:** `testTransferAndVerifyBalance` asserts balance remains equal — intentional.

---

## 6. RetryAnalyzer “Skipped” Counts

**Symptom:** TestNG / Surefire report shows skipped tests equal to first-attempt failures that were retried.  
**Cause:** TestNG marks a failed attempt as **SKIP** when `IRetryAnalyzer` schedules a retry.  
**Mitigation:** Expected framework behaviour. Final pass/fail is what matters for the suite result.

---

## 7. CI `smoke-tests` Job

**Symptom:** On every push, Actions shows `smoke-tests` as skipped.  
**Cause:** Smoke job runs only on **workflow_dispatch** with suite=`smoke` (manual run). Push/PR runs the full `run-tests` job.  
**Mitigation:** Not a failure. Use **Actions → Run workflow → smoke** for a quick suite.

---

## 8. Allure Report Requires Separate Command

**Symptom:** `target/site/allure-report/` is empty after `mvn clean test` alone  
**Cause:** Allure report generation is a separate Maven goal.  
**Fix:** Run `mvn allure:report` after tests (CI already does this), then open `target/site/allure-report/index.html`.

---

## CI Status

If the CI badge shows failing, open the [Actions tab](https://github.com/sunilshanubhog018/Selenium-Java-Framework/actions) and download the TestNG / Extent artifacts. Prefer investigating registration timeouts and site errors over assuming pure code defects when ParaBank is unstable.
