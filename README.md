# ParaBank Banking Test Automation Framework

![CI](https://github.com/sunilshanubhog018/Selenium-Java-Framework/actions/workflows/selenium-tests.yml/badge.svg)

End-to-end test automation framework for [ParaBank](https://parabank.parasoft.com) banking application
covering UI automation, data-driven testing, and API automation.

## Tech Stack

| Tool | Version |
|------|---------|
| Java | 21 |
| Selenium WebDriver | 4.27 |
| TestNG | 7.10 |
| Maven | 3.x |
| Rest Assured | 5.5 (in progress) |
| Apache POI | 5.2 |
| Allure Reports | 2.28 |
| Extent Reports | 5.1 |
| GitHub Actions | CI/CD |

## Features

- Page Object Model (POM) — all locators and actions in page classes, zero raw Selenium in tests
- ThreadLocal WebDriver — safe for parallel execution
- Multi-browser support — Chrome, Firefox, Edge (configured via `config.properties`)
- Headless mode — auto-enabled on CI
- Data-driven testing — Excel-driven login and E2E tests using Apache POI
- End-to-end flows — register, login, transfer funds, bill pay, activity verification
- API automation — Rest Assured foundation with request/response specs (in progress)
- Allure Reports — generated on every CI run
- Extent Reports — HTML report with screenshots on failure
- GitHub Actions CI — runs on every push to main

## Project Structure

```
src/test/java/
├── base/
│   ├── BaseTest.java        # ThreadLocal driver, browser setup, teardown
│   └── BasePage.java        # Common Selenium actions (click, type, wait)
├── pages/
│   ├── LoginPage.java
│   ├── RegisterPage.java
│   ├── AccountsOverviewPage.java
│   ├── TransferFundsPage.java
│   ├── BillPayPage.java
│   └── ActivityPage.java
├── tests/
│   ├── LoginTest.java
│   ├── RegisterTest.java
│   ├── AccountsOverviewTest.java
│   ├── TransferFundsTest.java
│   ├── BillPayTest.java
│   ├── DataDrivenLoginTest.java
│   ├── EndToEndTest.java
│   └── EndToEndDataDrivenTest.java
├── com/parabank/api/
│   ├── base/BaseApiTest.java
│   ├── specs/ApiSpecs.java
│   └── tests/
│       ├── LoginApiTest.java
│       └── AccountApiTest.java
├── listeners/
│   └── TestListener.java    # Extent report + screenshot on failure
└── utils/
    ├── ConfigReader.java
    ├── ExcelReader.java
    ├── ExtentManager.java
    └── Utils.java

src/test/resources/
├── config.properties
└── testdata/
    ├── LoginTestData.xlsx
    └── E2ETestData.xlsx
```

## How to Run

**Run all tests:**
```bash
mvn clean test
```

**Run specific suite:**
```bash
mvn clean test -Dsurefire.suiteXmlFiles=testng.xml
```

**Run headless:**
```bash
mvn clean test -Dheadless=true
```

**Generate Allure report:**
```bash
mvn allure:report
```

## Configuration

All settings in `src/test/resources/config.properties`:

```properties
browser=chrome          # chrome / firefox / edge
headless=true           # true for CI, false for local
implicit.wait=10
explicit.wait=15
page.load.timeout=30
```

## Test Suites

| Suite | Tests Included |
|-------|---------------|
| Smoke Tests | RegisterTest, LoginTest |
| Account Tests | AccountsOverviewTest |
| Transaction Tests | TransferFundsTest, BillPayTest |
| Data Driven Tests | DataDrivenLoginTest |
| E2E Tests | EndToEndTest |
| E2E Data Driven | EndToEndDataDrivenTest |

## CI/CD

GitHub Actions runs on every push to `main`:
- Sets up JDK 21 + headless Chrome
- Runs full test suite via `mvn clean test`
- Generates and uploads Allure report as artifact
- Uploads TestNG surefire reports as artifact

## Author

Sunil — QA Automation Engineer
