"""Generate Framework Interview Guide PDF."""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)

OUT = Path(__file__).resolve().parent / "Framework-Interview-Guide.pdf"

NAVY = HexColor("#0f2744")
TEAL = HexColor("#0d9488")
LIGHT = HexColor("#f1f5f9")
SOFT = HexColor("#e2e8f0")
DARK = HexColor("#1e293b")
MUTED = HexColor("#475569")
ACCENT = HexColor("#0369a1")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="CoverTitle", fontName="Helvetica-Bold", fontSize=22, leading=28,
    textColor=white, alignment=TA_CENTER, spaceAfter=12
))
styles.add(ParagraphStyle(
    name="CoverSub", fontName="Helvetica", fontSize=11, leading=15,
    textColor=HexColor("#cbd5e1"), alignment=TA_CENTER, spaceAfter=6
))
styles.add(ParagraphStyle(
    name="H1Doc", fontName="Helvetica-Bold", fontSize=14, leading=18,
    textColor=NAVY, spaceBefore=14, spaceAfter=8
))
styles.add(ParagraphStyle(
    name="H2Doc", fontName="Helvetica-Bold", fontSize=11.5, leading=15,
    textColor=TEAL, spaceBefore=10, spaceAfter=5
))
styles.add(ParagraphStyle(
    name="H3Doc", fontName="Helvetica-Bold", fontSize=10.5, leading=13,
    textColor=ACCENT, spaceBefore=8, spaceAfter=4
))
styles.add(ParagraphStyle(
    name="BodyDoc", fontName="Helvetica", fontSize=9.5, leading=13,
    textColor=DARK, alignment=TA_JUSTIFY, spaceAfter=6
))
styles.add(ParagraphStyle(
    name="BulletDoc", fontName="Helvetica", fontSize=9.5, leading=12.5,
    textColor=DARK, leftIndent=12, spaceAfter=2
))
styles.add(ParagraphStyle(
    name="QuoteDoc", fontName="Helvetica-Oblique", fontSize=9.5, leading=13,
    textColor=MUTED, leftIndent=10, rightIndent=10, spaceBefore=4, spaceAfter=8
))
styles.add(ParagraphStyle(
    name="CodeDoc", fontName="Courier", fontSize=8, leading=11,
    textColor=DARK, backColor=LIGHT, leftIndent=6, rightIndent=6,
    spaceBefore=4, spaceAfter=6
))
styles.add(ParagraphStyle(
    name="TableCell", fontName="Helvetica", fontSize=8.5, leading=11, textColor=DARK
))
styles.add(ParagraphStyle(
    name="TableHead", fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=white
))
styles.add(ParagraphStyle(
    name="InterviewQ", fontName="Helvetica-Bold", fontSize=9.5, leading=12,
    textColor=NAVY, spaceBefore=6, spaceAfter=2
))
styles.add(ParagraphStyle(
    name="InterviewA", fontName="Helvetica", fontSize=9.5, leading=12.5,
    textColor=DARK, leftIndent=8, spaceAfter=6
))


def p(text, style="BodyDoc"):
    return Paragraph(text, styles[style])


def bullet(items):
    return [Paragraph(f"• {it}", styles["BulletDoc"]) for it in items]


def hline():
    return HRFlowable(width="100%", thickness=0.6, color=SOFT, spaceBefore=4, spaceAfter=8)


def make_table(headers, rows, col_widths):
    head = [Paragraph(h, styles["TableHead"]) for h in headers]
    data = [head]
    for r in rows:
        data.append([Paragraph(str(c), styles["TableCell"]) for c in r])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("BACKGROUND", (0, 1), (-1, -1), white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT]),
        ("GRID", (0, 0), (-1, -1), 0.4, SOFT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def add_page_number(canvas, doc):
    canvas.saveState()
    page = canvas.getPageNumber()
    if page == 1:
        canvas.restoreState()
        return
    canvas.setFillColor(NAVY)
    canvas.rect(0, A4[1] - 18, A4[0], 18, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(40, A4[1] - 12, "ParaBank Selenium Framework — Interview Guide")
    canvas.drawRightString(A4[0] - 40, A4[1] - 12, "E2E Architecture Walkthrough")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(
        A4[0] / 2, 18,
        f"Page {page}  |  For interview explanation  |  Practice aloud 5–7 minutes"
    )
    canvas.restoreState()


def build():
    story = []

    # Cover
    cover = Table([[
        Paragraph("ParaBank Banking<br/>Test Automation Framework", styles["CoverTitle"]),
    ]], colWidths=[6.5 * inch])
    cover.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("TOPPADDING", (0, 0), (-1, -1), 40),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 20),
        ("LEFTPADDING", (0, 0), (-1, -1), 20),
        ("RIGHTPADDING", (0, 0), (-1, -1), 20),
    ]))
    story.append(Spacer(1, 70))
    story.append(cover)

    sub = Table([[
        Paragraph(
            "End-to-End Architecture &amp; Interview Explanation Guide<br/>"
            "How to explain this framework like a 3–4 years experienced Automation Engineer",
            styles["CoverSub"]
        )
    ]], colWidths=[6.5 * inch])
    sub.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), HexColor("#1e3a5f")),
        ("TOPPADDING", (0, 0), (-1, -1), 16),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
    ]))
    story.append(sub)
    story.append(Spacer(1, 28))
    story.append(p("<b>Application under test:</b> ParaBank (Parasoft demo banking app)"))
    story.append(p(
        "<b>Stack:</b> Java 21 · Selenium 4 · TestNG · Maven · Apache POI · "
        "Extent · Allure · GitHub Actions"
    ))
    story.append(p(
        "<b>Design:</b> Page Object Model · ThreadLocal WebDriver · "
        "Data-driven tests · CI/CD reporting"
    ))
    story.append(Spacer(1, 16))
    story.append(p(
        "<i>Use this as your speaking script. Start with the 60-second pitch, "
        "then walk the execution flow, then deep-dive into patterns when asked.</i>",
        "QuoteDoc"
    ))
    story.append(PageBreak())

    # 1
    story.append(p("1. The 60-Second Interview Pitch", "H1Doc"))
    story.append(hline())
    story.append(p(
        "When the interviewer says <b>“Tell me about your framework”</b>, start here:"
    ))
    story.append(p(
        "“I built / worked on a hybrid Selenium TestNG framework for the ParaBank banking "
        "application using Java and Maven. It follows the <b>Page Object Model</b> so locators "
        "and UI actions live in page classes, and tests stay readable business scenarios. "
        "We use <b>ThreadLocal WebDriver</b> for parallel-safe sessions, <b>config-driven</b> "
        "browser and environment settings, and <b>Excel data-driven</b> tests via Apache POI. "
        "Cross-cutting concerns like screenshots, Extent reporting, and retry are handled "
        "through <b>TestNG listeners</b>. The suite covers smoke, regression, transfer/bill-pay "
        "transactions, and end-to-end journeys. On every push to main, <b>GitHub Actions</b> "
        "runs headless Chrome, publishes Extent/TestNG/Allure artifacts, and stores per-run "
        "reports under <b>reports/ci/run-N</b>. I can walk you through how a single test flows "
        "from Maven → TestNG → BaseTest → Page Object → assertion → report.”",
        "QuoteDoc"
    ))
    story.append(p(
        "<b>Why this sounds senior:</b> You name architecture (POM), isolation (ThreadLocal), "
        "externalization (config/Excel), cross-cutting (listeners), scope (smoke/regression/E2E), "
        "and delivery (CI + reports) — not just “I wrote Selenium scripts.”"
    ))

    # 2
    story.append(p("2. Tech Stack (What &amp; Why)", "H1Doc"))
    story.append(hline())
    story.append(make_table(
        ["Tool", "Role in this framework", "Interview one-liner"],
        [
            ["Java 21", "Language", "Industry standard for enterprise automation"],
            ["Maven", "Build &amp; dependency mgmt", "Surefire runs TestNG suite from pom.xml"],
            ["Selenium 4", "Browser automation", "WebDriver + explicit waits + CI ChromeOptions"],
            ["TestNG", "Test runner", "Suites, groups, DataProviders, listeners, retry"],
            ["WebDriverManager", "Driver binaries", "Matches chromedriver to browser version"],
            ["Apache POI", "Excel I/O", "Data-driven login &amp; E2E scenarios"],
            ["Extent Reports", "HTML dashboard", "Pass/fail + screenshots via TestListener"],
            ["Allure", "Rich test report", "Generated in CI with mvn allure:report"],
            ["Log4j2", "Logging", "Console + logs/test.log"],
            ["GitHub Actions", "CI/CD", "Headless Chrome on ubuntu + report publish"],
        ],
        [1.1 * inch, 2.2 * inch, 3.2 * inch]
    ))

    # 3
    story.append(p("3. Project Structure (Layers)", "H1Doc"))
    story.append(hline())
    story.append(p(
        "Explain the framework as <b>layers</b> with clear separation of concerns:"
    ))
    story.append(make_table(
        ["Layer / Package", "Responsibility", "Key classes"],
        [
            ["base", "Lifecycle &amp; shared UI helpers", "BaseTest, BasePage"],
            ["pages", "Locators + user actions (POM)", "LoginPage, RegisterPage, TransferFundsPage…"],
            ["tests", "Assertions &amp; business scenarios only", "LoginTest, EndToEndTest…"],
            ["listeners", "Reporting, retry, hooks", "TestListener, RetryListener, RetryAnalyzer"],
            ["utils", "Reusable infrastructure", "ConfigReader, ExcelReader, ExtentManager, UserFactory"],
            ["resources", "External config &amp; data", "config.properties, LoginTestData.xlsx"],
            ["testng.xml", "Suite orchestration", "Smoke / Account / Transaction / E2E order"],
            [".github/workflows", "CI pipeline", "selenium-tests.yml"],
            ["reports/ci/run-N", "Per-run CI report archive", "Extent + TestNG HTML (never overwrite)"],
        ],
        [1.3 * inch, 2.4 * inch, 2.8 * inch]
    ))
    story.append(p(
        "<b>Golden rule:</b> Test classes never hold raw By locators. Page classes never assert "
        "business outcome. Utils never open browsers. That keeps the framework maintainable."
    ))

    story.append(PageBreak())

    # 4
    story.append(p("4. How Execution Starts (Entry Point)", "H1Doc"))
    story.append(hline())
    story.append(p("4.1 Local command", "H2Doc"))
    story.append(p("<font face='Courier'>mvn clean test</font>", "CodeDoc"))
    story.extend(bullet([
        "<b>Maven</b> reads <b>pom.xml</b> — compiles sources, resolves dependencies.",
        "<b>maven-surefire-plugin</b> is configured with <b>testng.xml</b> as the suite file.",
        "Surefire launches the JVM and hands control to <b>TestNG</b>.",
        "TestNG loads listeners from testng.xml: <b>TestListener</b> + <b>RetryListener</b>.",
        "Then TestNG executes &lt;test&gt; blocks in order: Smoke → Account → Transaction → Data Driven → E2E.",
    ]))
    story.append(p("4.2 CI entry point", "H2Doc"))
    story.extend(bullet([
        "Push to <b>main</b> triggers <b>GitHub Actions</b> workflow <b>selenium-tests.yml</b>.",
        "Job on <b>ubuntu-latest</b>: JDK 21 + Chrome, <b>CI=true</b> (forces headless).",
        "Same <b>mvn clean test</b>, then <b>mvn allure:report</b>.",
        "Uploads artifacts and commits reports to <b>reports/ci/run-&lt;number&gt;/</b> (each run separate).",
    ]))
    story.append(p(
        "Interview line: “The single source of truth for what runs is testng.xml; "
        "Maven and CI are just runners around it.”",
        "QuoteDoc"
    ))

    # 5
    story.append(p("5. Test Lifecycle — Start to End of One Method", "H1Doc"))
    story.append(hline())
    story.append(p("This is the most important flow to memorize. Explain it as a timeline:"))
    story.append(p("Phase A — Suite start", "H3Doc"))
    story.extend(bullet([
        "<b>@BeforeSuite</b> in BaseTest (optional DB init — OFF by default on public ParaBank).",
        "TestListener <b>onStart</b>: creates screenshot folders, logs suite name.",
    ]))
    story.append(p("Phase B — Before each test method", "H3Doc"))
    story.extend(bullet([
        "<b>@BeforeMethod setUp()</b> in BaseTest: read browser/headless from ConfigReader (+ env CI).",
        "WebDriverManager + ChromeOptions (no-sandbox, disable-dev-shm, headless=new on CI).",
        "Driver in <b>ThreadLocal&lt;WebDriver&gt;</b> — parallel-safe.",
        "Timeouts from config.properties; child @BeforeMethod navigates and builds page objects.",
    ]))
    story.append(p("Phase C — Test body", "H3Doc"))
    story.extend(bullet([
        "Test calls page methods: loginPage.login(user, pass).",
        "BasePage click/type/getText use <b>explicit waits</b>.",
        "Assertions with TestNG Assert / SoftAssert on URL, messages, balances.",
    ]))
    story.append(p("Phase D — After method", "H3Doc"))
    story.extend(bullet([
        "On failure: screenshot + Extent log; optional one retry via RetryAnalyzer.",
        "<b>@AfterMethod tearDown()</b>: quit driver, clear ThreadLocal.",
    ]))
    story.append(p("Phase E — Suite finish", "H3Doc"))
    story.extend(bullet([
        "TestListener flushes Extent → test-output/ExtentReport.html.",
        "Surefire writes target/surefire-reports/.",
        "CI generates Allure and publishes reports/ci/run-N/.",
    ]))
    story.append(p("5.1 One-line flow diagram", "H2Doc"))
    story.append(p(
        "Maven → Surefire → TestNG (testng.xml + listeners) → BaseTest.setUp (ThreadLocal driver) → "
        "Test @BeforeMethod → Page Object actions → Assertions → Listener (pass/fail/screenshot) → "
        "BaseTest.tearDown → Extent flush → CI artifacts / reports/ci/run-N",
        "CodeDoc"
    ))

    story.append(PageBreak())

    # 6
    story.append(p("6. Core Components — Deep Dive", "H1Doc"))
    story.append(hline())
    story.append(p("6.1 BaseTest", "H2Doc"))
    story.extend(bullet([
        "Browser factory for chrome/firefox/edge; ThreadLocal isolation.",
        "Headless when config headless=true OR env CI=true.",
        "DB Initialize opt-in only — never wipe shared public demo in CI.",
    ]))
    story.append(p("6.2 BasePage", "H2Doc"))
    story.extend(bullet([
        "Shared click, type, getText, selects, waitForUrl, logout.",
        "Explicit waits; fix locator once in page class when UI changes.",
    ]))
    story.append(p("6.3 Page Objects (quality examples)", "H2Doc"))
    story.extend(bullet([
        "LoginPage: waitForLoginOutcome; errors scoped to #rightPanel.",
        "TransferFundsPage: ensureAccountsSelected (AJAX dropdowns); wait for title change after Transfer.",
        "BillPayPage: selectFirstFromAccount for dynamic account IDs.",
        "These “wait for outcome, not element already present” fixes are strong flaky-test stories.",
    ]))
    story.append(p("6.4 ConfigReader / UserFactory / ExcelReader", "H2Doc"))
    story.extend(bullet([
        "ConfigReader: classpath config.properties (base.url, browser, waits, headless).",
        "UserFactory: unique user registration with retries; Welcome OR overview = success.",
        "ExcelReader: POI + classpath fallback; DataProviders for login/E2E Excel rows.",
    ]))
    story.append(p("6.5 Listeners &amp; reporting", "H2Doc"))
    story.extend(bullet([
        "RetryListener auto-applies RetryAnalyzer (1 retry; no retry on SkipException).",
        "TestListener: Extent nodes, failure screenshots, flush on suite end.",
        "ExtentManager: double-checked locking Singleton → one HTML report per suite.",
    ]))

    # 7
    story.append(p("7. What We Automate (Suite Map)", "H1Doc"))
    story.append(hline())
    story.append(make_table(
        ["Suite block", "Classes", "What it proves"],
        [
            ["Smoke", "RegisterTest, LoginTest", "App up; core auth/register"],
            ["Account", "AccountsOverviewTest", "Overview, balances, nav, logout"],
            ["Transaction", "TransferFundsTest, BillPayTest", "Money movement + validation"],
            ["Data Driven", "DataDrivenLoginTest", "Excel credential scenarios"],
            ["E2E", "EndToEndTest", "Multi-step banking journeys"],
            ["E2E Data Driven", "EndToEndDataDrivenTest", "Parameterized full flows"],
        ],
        [1.3 * inch, 2.2 * inch, 3.0 * inch]
    ))
    story.append(p(
        "Groups: smoke, regression, login, e2e, datadriven — enable selective pipeline runs later."
    ))
    story.append(p(
        "Healthy CI result: <b>53 executed · 50 passed · 0 failed · 3 skipped</b>. "
        "Three intentional skips = negative login while public ParaBank auth-bypass is active "
        "(documented in KNOWN_ISSUES.md)."
    ))

    # 8
    story.append(p("8. Walkthrough — Valid Login Test", "H1Doc"))
    story.append(hline())
    story.extend(bullet([
        "TestNG runs LoginTest.testValidLogin (smoke + regression).",
        "BaseTest opens headless Chrome into ThreadLocal.",
        "Navigate to base URL; create LoginPage.",
        "Register unique user → logout → login → wait for overview URL.",
        "Assert URL contains overview; Extent PASS; tearDown quits browser.",
    ]))
    story.append(p(
        "Shows setup isolation (unique user), page abstractions, and assertion intent.",
        "QuoteDoc"
    ))

    story.append(PageBreak())

    # 9
    story.append(p("9. CI/CD Pipeline", "H1Doc"))
    story.append(hline())
    story.extend(bullet([
        "Trigger: push/PR to main, or manual full/smoke dispatch.",
        "checkout → JDK 21 → Chrome → mvn clean test → allure:report → artifacts.",
        "Publish: reports/ci/run-N/ + INDEX.md + LATEST.txt (never overwrites older runs).",
        "Developer: git pull → open reports/ci/run-N/ExtentReport.html.",
        "CI report timestamps: UTC (GitHub runner default).",
    ]))

    # 10
    story.append(p("10. Design Patterns &amp; Best Practices", "H1Doc"))
    story.append(hline())
    story.append(make_table(
        ["Practice", "How we apply it", "Why it matters"],
        [
            ["Page Object Model", "pages/* only", "UI change = one file update"],
            ["Fluent methods", "return this", "Readable test DSL"],
            ["ThreadLocal driver", "BaseTest", "Parallel-ready isolation"],
            ["External config", "config.properties", "Env portability"],
            ["Data-driven", "Excel + DataProvider", "Scale without code churn"],
            ["Factory helper", "UserFactory", "DRY registration + retry"],
            ["Listeners", "TestListener", "Reporting not mixed into tests"],
            ["Retry analyzer", "1 automatic retry", "Absorb transient flake"],
            ["Explicit waits", "BasePage", "Less flaky than Thread.sleep"],
            ["SoftAssert", "multi-field checks", "See all failures in one run"],
            ["Groups / suites", "testng.xml", "Smoke vs full regression"],
            ["CI as product", "Actions + reports/ci", "Feedback on every commit"],
        ],
        [1.4 * inch, 2.2 * inch, 2.9 * inch]
    ))

    # 11
    story.append(p("11. Real Challenges We Solved", "H1Doc"))
    story.append(hline())
    story.append(p("Challenge 1 — Flaky transfer/bill pay success", "H3Doc"))
    story.append(p(
        "Root cause: waited for h1.title that already existed on the form. "
        "Fix: wait for title change / result panel. Strong debugging story."
    ))
    story.append(p("Challenge 2 — Registration success detection", "H3Doc"))
    story.append(p(
        "ParaBank may stay on register.htm with Welcome. UserFactory accepts Welcome OR overview."
    ))
    story.append(p("Challenge 3 — Public demo auth bypass", "H3Doc"))
    story.append(p(
        "Invalid credentials 302 to overview. Negative tests SkipException + KNOWN_ISSUES — "
        "honest automation, not infinite red CI."
    ))
    story.append(p("Challenge 4 — Shared DB Initialize", "H3Doc"))
    story.append(p(
        "Admin INIT wipes public data. Disabled by default; only private instances."
    ))

    # 12
    story.append(p("12. How a Run Ends (Deliverables)", "H1Doc"))
    story.append(hline())
    story.extend(bullet([
        "Console TestNG summary (run / fail / skip).",
        "Extent: test-output/ExtentReport.html or reports/ci/run-N/ExtentReport.html.",
        "TestNG: target/surefire-reports/index.html + emailable-report.html.",
        "Screenshots under screenshots/ on failure.",
        "Allure after mvn allure:report; CI artifacts ~30 days retention.",
    ]))

    story.append(PageBreak())

    # 13
    story.append(p("13. Likely Interview Q&amp;A", "H1Doc"))
    story.append(hline())
    qa = [
        ("Why POM?",
         "Separates UI structure from test intent. Locators change often; tests should not."),
        ("Why ThreadLocal?",
         "Each thread needs its own WebDriver. Static driver races in parallel. Future-proof design."),
        ("Implicit vs explicit wait?",
         "Modest implicit for basic finds; BasePage uses explicit waits for clickable/visible/url — more deterministic."),
        ("How do you handle flaky tests?",
         "Fix waits, unique data, one infra retry, document environment limits, don’t wipe shared demo DB."),
        ("How is data-driven testing done?",
         "POI reads Excel; DataProvider supplies rows; Execute flag; tokens map to runtime users."),
        ("What runs in CI?",
         "Full testng.xml headless on Chrome; smoke is manual-only; per-run reports published."),
        ("Where are reports?",
         "Local: test-output &amp; surefire-reports. CI: Artifacts + reports/ci/run-N after git pull."),
        ("How would you scale?",
         "Careful parallel + isolated users, Grid/cloud, split smoke vs nightly, APIs when backend is stable."),
    ]
    for q, a in qa:
        story.append(p(f"Q: {q}", "InterviewQ"))
        story.append(p(f"A: {a}", "InterviewA"))

    # 14
    story.append(p("14. One-Page Speaking Order (Memorize)", "H1Doc"))
    story.append(hline())
    story.append(p("Use this sequence in a 5–7 minute framework explanation:"))
    story.extend(bullet([
        "<b>1. Context:</b> Automating ParaBank banking UI with Java/Selenium/TestNG/Maven.",
        "<b>2. Architecture:</b> POM + BaseTest/BasePage + utils + listeners.",
        "<b>3. Entry:</b> mvn clean test → Surefire → testng.xml.",
        "<b>4. Lifecycle:</b> setUp ThreadLocal → page actions → asserts → tearDown → Extent.",
        "<b>5. Data:</b> config.properties + Excel DataProviders + UserFactory.",
        "<b>6. Quality:</b> explicit waits, SoftAssert, retry, groups.",
        "<b>7. CI:</b> GitHub Actions headless, artifacts, reports/ci/run-N.",
        "<b>8. Results:</b> ~50 pass / 3 intentional skips / 0 fail on healthy run.",
        "<b>9. Lessons:</b> wait-for-outcome bugs, public demo limits, shared DB caution.",
        "<b>10. Close:</b> “Happy to deep-dive into any layer — pages, listeners, or CI.”",
    ]))

    story.append(p("15. Commands You’ll Be Asked", "H1Doc"))
    story.append(hline())
    story.append(p("Full suite:  <font face='Courier'>mvn clean test</font>"))
    story.append(p(
        "Smoke only:  <font face='Courier'>mvn clean test "
        "-Dsurefire.suiteXmlFiles=testng-smoke.xml</font>"
    ))
    story.append(p(
        "Allure:      <font face='Courier'>mvn allure:report</font> → "
        "target/site/allure-report/index.html"
    ))
    story.append(p(
        "After CI:    <font face='Courier'>git pull</font> → "
        "reports/ci/run-N/ExtentReport.html"
    ))

    story.append(Spacer(1, 14))
    story.append(hline())
    story.append(p(
        "<b>Closing confidence line:</b> “This framework is not a script dump — it’s a layered "
        "automation product with clear ownership of browser lifecycle, pages, data, reporting, "
        "and CI. I can maintain it, extend scenarios, and debug pipeline failures end-to-end.”",
        "QuoteDoc"
    ))
    story.append(p(
        "— End of guide. Practice aloud once with a timer (5–7 minutes). Good luck!"
    ))

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=36,
        bottomMargin=36,
        title="ParaBank Selenium Framework — Interview Guide",
        author="Selenium Banking Framework",
    )
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
