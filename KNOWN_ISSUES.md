# Known Issues

Known limitations and intermittent failures in this framework. These are not bugs in the automation code — they are constraints of the [ParaBank](https://parabank.parasoft.com) public demo environment.

---

## 1. ParaBank Site Instability

**Affected Tests:** All tests  
**Symptom:** `TimeoutException` or connection errors  
**Cause:** ParaBank is a public demo site with no SLA. It occasionally goes down, responds slowly, or returns unexpected pages.  
**Mitigation:** `RetryAnalyzer` retries each failed test once automatically.

---

## 2. Registration Throttling

**Affected Tests:** `RegisterTest`, `AccountsOverviewTest`, `TransferFundsTest`, `BillPayTest`, `EndToEndTest`  
**Symptom:** Registration succeeds but welcome message doesn't appear, or registration silently fails  
**Cause:** ParaBank throttles rapid user registrations. Tests that register a fresh user in `@BeforeMethod` can hit this limit when the full suite runs back-to-back.  
**Mitigation:** `EndToEndTest` falls back to `config.properties` credentials if registration fails.

---

## 3. Single Account — Transfer Tests

**Affected Tests:** `TransferFundsTest`, `EndToEndTest.testFundTransferFlow`  
**Symptom:** Transfer completes but balance doesn't change  
**Cause:** New users only get 1 account. Transfers go from that account to the same account, so the net balance stays the same. This is expected behaviour for a single-account user.  
**Mitigation:** `testTransferAndVerifyBalance` asserts balance remains equal — this is intentional.

---

## 4. API Customer ID

**Affected Tests:** `AccountApiTest`  
**Symptom:** `AccountApiTest` returns empty list or 404  
**Cause:** `api.customer.id=12212` is a hardcoded demo customer on ParaBank. If the demo site is reset, this customer's data may be wiped.  
**Mitigation:** Update `api.customer.id` in `config.properties` with a valid customer ID after logging in via the API.

---

## 5. Allure Report Requires Separate Command

**Symptom:** `target/site/allure-report/` is empty after `mvn clean test`  
**Cause:** Allure report generation is a separate Maven goal.  
**Fix:** Run `mvn allure:report` after `mvn clean test`, then open `target/site/allure-report/index.html`.

---

## CI Status

If the CI badge shows failing, check the [Actions tab](https://github.com/sunilshanubhog018/Selenium-Java-Framework/actions) — it is likely a ParaBank site issue rather than a code defect.
