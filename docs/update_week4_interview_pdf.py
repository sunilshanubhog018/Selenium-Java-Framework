"""Rebuild Week4 Framework Enhancement + DDT Interview PDF."""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether, Preformatted
)

OUT = Path(
    r"C:\Users\sunil\OneDrive\Desktop\Java_selenium_material"
    r"\CLAUDE AI NOTES\Week4_Framework Enhancement + Data-Driven Testing"
    r"\Week4_Framework_Enhancement_InterviewQA.pdf"
)

NAVY = HexColor("#0b3d5c")
TEAL = HexColor("#0f766e")
RED = HexColor("#9f1239")
GREEN = HexColor("#166534")
LIGHT = HexColor("#f0f9ff")
SOFT = HexColor("#e2e8f0")
DARK = HexColor("#1e293b")
MUTED = HexColor("#475569")
GOLD = HexColor("#b45309")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TMain", fontName="Helvetica-Bold", fontSize=13.5,
                          leading=17, textColor=white, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="TSub", fontName="Helvetica", fontSize=8.6,
                          leading=11.2, textColor=HexColor("#dbeafe"), alignment=TA_CENTER))
styles.add(ParagraphStyle(name="DH1", fontName="Helvetica-Bold", fontSize=10.3,
                          leading=12.5, textColor=NAVY, spaceBefore=6, spaceAfter=2))
styles.add(ParagraphStyle(name="DH2", fontName="Helvetica-Bold", fontSize=8.8,
                          leading=11, textColor=TEAL, spaceBefore=4, spaceAfter=2))
styles.add(ParagraphStyle(name="DQ", fontName="Helvetica-Bold", fontSize=8.1,
                          leading=10.3, textColor=NAVY, spaceBefore=3, spaceAfter=1))
styles.add(ParagraphStyle(name="DA", fontName="Helvetica", fontSize=7.7,
                          leading=9.9, textColor=DARK, alignment=TA_JUSTIFY, spaceAfter=1))
styles.add(ParagraphStyle(name="DTip", fontName="Helvetica-Oblique", fontSize=7.0,
                          leading=8.9, textColor=GOLD, leftIndent=3, spaceAfter=1))
styles.add(ParagraphStyle(name="DFix", fontName="Helvetica-Oblique", fontSize=6.9,
                          leading=8.8, textColor=GREEN, spaceAfter=2))
styles.add(ParagraphStyle(name="DBody", fontName="Helvetica", fontSize=7.8,
                          leading=10, textColor=DARK, spaceAfter=2))
styles.add(ParagraphStyle(name="CodeB", fontName="Courier", fontSize=6.0,
                          leading=7.8, textColor=DARK, backColor=LIGHT, spaceBefore=1, spaceAfter=1))
styles.add(ParagraphStyle(name="DCell", fontName="Helvetica", fontSize=6.6,
                          leading=8.4, textColor=DARK))
styles.add(ParagraphStyle(name="DHead", fontName="Helvetica-Bold", fontSize=6.6,
                          leading=8.4, textColor=white))
styles.add(ParagraphStyle(name="LvlB", fontName="Helvetica-Bold", fontSize=7.1,
                          textColor=HexColor("#1d4ed8"), spaceAfter=1))
styles.add(ParagraphStyle(name="LvlR", fontName="Helvetica-Bold", fontSize=7.1,
                          textColor=RED, spaceAfter=1))


def P(t, s="DA"):
    return Paragraph(t, styles[s])


def code(t):
    return Preformatted(t.rstrip(), styles["CodeB"])


def tip(t):
    return P(f"<b>Tip:</b> {t}", "DTip")


def hline():
    return HRFlowable(width="100%", thickness=0.35, color=SOFT, spaceBefore=1, spaceAfter=2)


def qa(n, q, parts):
    items = [P(f"Q{n}. {q}", "DQ")]
    for p in parts:
        items.append(P(p, "DA") if isinstance(p, str) else p)
    return KeepTogether(items)


def footer(canvas, doc):
    canvas.saveState()
    page = canvas.getPageNumber()
    if page > 1:
        canvas.setFillColor(NAVY)
        canvas.rect(0, A4[1] - 12, A4[0], 12, fill=1, stroke=0)
        canvas.setFillColor(white)
        canvas.setFont("Helvetica", 6.4)
        canvas.drawString(26, A4[1] - 8, "Week 4: Framework Enhancement + DDT | Interview Q&A")
        canvas.drawRightString(A4[0] - 26, A4[1] - 8, "SDET Prep")
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 6.4)
        canvas.drawCentredString(A4[0] / 2, 10, f"Page {page}")
    canvas.restoreState()


def build():
    story = []

    cover = Table([
        [P("Week 4: Framework Enhancement + Data-Driven Testing", "TMain")],
        [P("Parallel · ThreadLocal · Extent · Log4j · CI/CD · Excel DDT · E2E<br/>"
           "Aligned to ParaBank Selenium-Java Banking Framework<br/><br/>"
           "PART 1 Fundamentals · PART 2 Senior · PART 3 MCQs + Answer Key",
           "TSub")],
    ], colWidths=[6.7 * inch])
    cover.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("TOPPADDING", (0, 0), (-1, -1), 16),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(Spacer(1, 22))
    story.append(cover)
    story.append(Spacer(1, 7))
    story.append(P(
        "Verified against current framework: ThreadLocal driver, Extent singleton, RetryAnalyzer, "
        "CI headless, reports/ci/run-N, no public DB INIT by default, Excel Execute filter.",
        "DBody"
    ))
    story.append(P(
        "Updates: DB INIT opt-in; RetryAnalyzer vs surefire rerun; pause/sleep not preferred; "
        "CI reports path; unique users under parallel; MCQ answer fixes where needed.",
        "DFix"
    ))
    story.append(PageBreak())

    # PART 1
    story.append(P("PART 1 — FUNDAMENTALS (Blue)", "DH1"))
    story.append(P("Parallel · Reports · CI · DDT basics", "LvlB"))
    story.append(hline())

    story.append(qa(1, "What is TestNG parallel execution and why needed?", [
        "Runs multiple tests on different threads at once to cut suite time. "
        "Example: 50 sequential tests ~40 min → ~10–15 min with thread-count=3–4 (plus overhead).",
        code('<suite name="Banking" parallel="methods" thread-count="3">'),
        tip("Parallel without ThreadLocal WebDriver causes random cross-test failures."),
    ]))

    story.append(qa(2, "What is ThreadLocal and why for WebDriver?", [
        "Each thread gets its own isolated copy of a variable. One shared static WebDriver is unsafe in parallel.",
        code("private static final ThreadLocal<WebDriver> driver = new ThreadLocal<>();\n"
             "public static WebDriver getDriver() { return driver.get(); }\n"
             "// set() in @BeforeMethod; quit()+remove() in @AfterMethod"),
    ]))

    story.append(qa(3, "What is Extent Reports?", [
        "HTML reporting library: pass/fail/skip, logs, screenshots, system info, timeline. "
        "ExtentSparkReporter writes a shareable HTML dashboard for stakeholders.",
    ]))

    story.append(qa(4, "Singleton in ExtentManager?", [
        "One ExtentReports instance for the whole suite so all tests write into one report. "
        "For parallel safety use double-checked locking + volatile (or synchronized create).",
        code("public static ExtentReports getInstance() {\n"
             "  if (extent == null) {\n"
             "    synchronized (ExtentManager.class) {\n"
             "      if (extent == null) extent = createInstance();\n"
             "    }\n"
             "  }\n"
             "  return extent;\n"
             "}"),
    ]))

    story.append(qa(5, "What is CI/CD? What tool?", [
        "CI: auto build/test on every push. CD: auto deliver/deploy after quality gates. "
        "We use <b>GitHub Actions</b>: checkout → JDK 21 → Chrome → mvn clean test (CI=true headless) → "
        "Allure/artifacts → publish reports/ci/run-N/.",
    ]))

    story.append(qa(6, "Headless browser — when?", [
        "Chrome without GUI — required on CI runners (no display), often faster. Detect CI env:",
        code("boolean headless = Boolean.parseBoolean(ConfigReader.get(\"headless\"))\n"
             "    || Boolean.parseBoolean(System.getenv(\"CI\"));\n"
             "if (headless) options.addArguments(\"--headless=new\");"),
    ]))

    story.append(qa(7, "Data-driven testing implementation?", [
        "Separate data from logic: Excel (Apache POI) + TestNG @DataProvider. Same @Test runs once per row.",
        code("@Test(dataProvider = \"loginData\")\n"
             "public void testLogin(String user, String pass, String expected) { ... }"),
    ]))

    story.append(qa(8, "What is the Execute column?", [
        "Run flag: Yes → include in DataProvider; No → skip without deleting the row. "
        "Useful for known env defects or WIP cases.",
    ]))

    story.append(qa(9, "@BeforeSuite usage (current framework)?", [
        "Runs once before the suite. Optional ParaBank admin INIT exists but is <b>OFF by default</b> "
        "because public INIT wipes the shared demo DB. Enable only on private instances: "
        "-Dparabank.init.db=true or PARABANK_INIT_DB=true.",
        tip("Senior answer: never casually reset a shared public environment in CI."),
    ]))

    story.append(qa(10, "driver.remove() importance?", [
        "After quit(), remove ThreadLocal entry to avoid leaking closed sessions → memory growth in long parallel runs.",
    ]))

    story.append(qa(11, "Chrome args for Linux CI?", [
        "--headless=new, --no-sandbox, --disable-dev-shm-usage, --window-size=1920,1080, "
        "--disable-gpu, optional --disable-extensions. Stability flags matter more on Linux CI than on local Windows.",
    ]))

    story.append(qa(12, "extent.flush() when?", [
        "Writes in-memory report to disk. Call in ITestListener.onFinish after all tests. Without flush, HTML is empty/incomplete.",
    ]))

    story.append(qa(13, "Log4j in the framework?", [
        "Logging facade for console + file (log4j2.xml). Prefer structured logs over System.out for CI diagnosis. "
        "Keep root level WARN/INFO to avoid noisy driver logs.",
    ]))

    story.append(PageBreak())

    # PART 2
    story.append(P("PART 2 — SENIOR / FRAMEWORK LEVEL (Red)", "DH1"))
    story.append(P("Speed, reports, unstable env, CI stories", "LvlR"))
    story.append(hline())

    story.append(qa("S1", "50 tests in 40 min → ~10 min?", [
        "ThreadLocal driver + parallel methods (thread-count 3–5) + unique users per thread + "
        "explicit waits (no sleeps) + headless CI. Expect ~8–15 min depending on deps/overhead — not pure math.",
    ]))

    story.append(qa("S2", "Extent + TestNG integration?", [
        "ExtentManager singleton; TestListener: onTestStart createTest → ThreadLocal&lt;ExtentTest&gt;; "
        "success/fail/skip log; fail attaches screenshot; onFinish flush. "
        "Report shared, nodes per-thread via ThreadLocal.",
    ]))

    story.append(qa("S3", "Unstable public ParaBank strategies?", [
        "Unique users (UserFactory); registration retries; outcome waits; SkipException for known auth-bypass "
        "negatives; KNOWN_ISSUES.md; optional private DB INIT only. Prefer isolated QA in real banks.",
    ]))

    story.append(qa("S4", "CI/CD end-to-end?", [
        "Push main → Actions → Ubuntu → Java/Chrome → mvn clean test → allure:report → upload artifacts → "
        "commit reports/ci/run-&lt;N&gt;/ → developer git pull. Failures fail the job (exit 1).",
    ]))

    story.append(qa("S5", "parallel methods vs classes?", [
        "methods: max parallelism, each @Test own thread (needs isolation). "
        "classes: one thread per class, methods sequential inside class (better if class shares state).",
    ]))

    story.append(qa("S6", "Failure screenshot to report?", [
        "onTestFailure → BaseTest.getDriver() → TakesScreenshot FILE → absolute path under test-output/screenshots → "
        "MediaEntityBuilder attach to ExtentTest. Unique names (method + timestamp + thread).",
    ]))

    story.append(qa("S7", "CI Chrome crash first startup story?", [
        "Linux shm/GPU/port issues → flags --disable-dev-shm-usage, --disable-gpu, --no-sandbox, headless=new. "
        "Optional one retry (IRetryAnalyzer or surefire rerun). Lesson: always validate headless Linux before trusting CI.",
    ]))

    story.append(qa("S8", "Maintainable scalable suite?", [
        "POM separation; ConfigReader; dynamic data; listeners for cross-cuts; groups/suites for smoke vs full; "
        "adding tests doesn’t change architecture.",
    ]))

    story.append(qa("S9", "Retry: RetryAnalyzer vs surefire rerunFailingTestsCount?", [
        "IRetryAnalyzer (via RetryListener) retries inside TestNG for flaky UI. "
        "surefire rerunFailingTestsCount re-runs failed tests at Maven level. "
        "Our framework primarily uses <b>RetryAnalyzer (max 1)</b> — don’t over-retry business failures.",
    ]))

    story.append(P("Rapid fire", "DH2"))
    rf = [
        ["parallel=methods?", "Each @Test on its own thread"],
        ["ThreadLocal driver?", "Isolated browser per thread"],
        ["extent.flush()?", "Write HTML report to disk"],
        ["driver.remove()?", "Avoid ThreadLocal memory leak"],
        ["CI=true?", "Auto headless without config edit"],
        ["RetryAnalyzer?", "TestNG-level flaky retry (e.g. once)"],
        ["Local Extent path?", "test-output/ExtentReport.html"],
        ["CI report path?", "reports/ci/run-N/ after publish"],
        ["Execute=No?", "Row excluded from DataProvider"],
        ["Public DB INIT?", "Off by default — shared demo risk"],
    ]
    data = [[Paragraph(h, styles["DHead"]) for h in ["Q", "A"]]]
    for a, b in rf:
        data.append([Paragraph(a, styles["DCell"]), Paragraph(b, styles["DCell"])])
    t = Table(data, colWidths=[1.7 * inch, 4.8 * inch], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT]),
        ("GRID", (0, 0), (-1, -1), 0.25, SOFT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))
    story.append(t)

    story.append(PageBreak())

    # PART 3 MCQs with answers
    story.append(P("PART 3 — PRACTICE MCQs (answers included)", "DH1"))
    story.append(hline())

    story.append(P("Test 1 — Parallel basics", "DH2"))
    for q, a in [
        ("1. testng.xml parallel attribute?", "B) parallel=\"methods\""),
        ("2. ThreadLocal ensures?", "B) Each thread own driver"),
        ("3. driver.remove() called in?", "C) @AfterMethod"),
        ("4. No display on Linux CI?", "C) --headless=new"),
        ("5. ExtentReports pattern?", "C) Singleton"),
        ("6. extent.flush() in?", "D) onFinish()"),
        ("7. parallel=\"classes\"?", "B) Each class own thread"),
        ("8. GitHub Actions env?", "B) CI=true"),
        ("9. Once before all tests?", "C) @BeforeSuite"),
        ("10. thread-count=3?", "B) Up to 3 concurrent tests"),
    ]:
        story.append(P(f"{q} → <b>{a}</b>", "DA"))

    story.append(P("Test 2 — Extent & listeners", "DH2"))
    for q, a in [
        ("1. Fail callback?", "C) onTestFailure()"),
        ("2. Attach screenshot?", "B) MediaEntityBuilder.createScreenCaptureFromPath()"),
        ("3. ThreadLocal ExtentTest?", "B) Own node per parallel thread"),
        ("4. Create test node?", "B) extent.createTest()"),
        ("5. Status.PASS from?", "C) ExtentReports"),
        ("6. Spark output?", "C) HTML"),
        ("7. Register listener?", "C) testng.xml listeners"),
        ("8. Absolute path base?", "B) System.getProperty(\"user.dir\")"),
        ("9. No flush?", "B) Report empty/incomplete"),
        ("10. Theme.DARK?", "B) Dark HTML theme"),
    ]:
        story.append(P(f"{q} → <b>{a}</b>", "DA"))

    story.append(P("Test 3 — CI/CD & DDT", "DH2"))
    for q, a in [
        ("1. mvn clean test?", "C) Clean + compile + run tests"),
        ("2. getenv(\"CI\")?", "B) Auto headless on Actions"),
        ("3. XSSFWorkbook?", "C) .xlsx Excel 2007+"),
        ("4. Link DataProvider?", "B) @Test(dataProvider=...)"),
        ("5. Execute=No?", "C) Not added to DP — never runs"),
        ("6. Surefire rerun count?", "B) Retry failed tests once at Maven level"),
        ("7. timestamp username?", "B) Unique users / less DB conflict"),
        ("8. Workflow trigger?", "B) Push to main"),
        ("9. gitignore test-output?", "C) Generated — noisy commits"),
        ("10. Numeric cell 123?", "B) Whole number string without .0"),
    ]:
        story.append(P(f"{q} → <b>{a}</b>", "DA"))

    story.append(PageBreak())

    story.append(P("Test 4 — Framework integration", "DH2"))
    for q, a in [
        ("1. @BeforeSuite fails?", "B) Dependent tests often skipped/config fail"),
        ("2. try/catch on optional INIT?", "B) Non-fatal if INIT disabled/partial"),
        ("3. 3 parallel threads drivers?", "C) 3 (one per thread)"),
        ("4. CONFIG_USERNAME?", "B) Resolve from config.properties"),
        ("5. @Listeners on BaseTest?", "B) Works for individual class runs too"),
        ("6. Absolute screenshot path?", "B) Report finds images when opened elsewhere"),
        ("7. acc_timestamp unique?", "B) No clash across threads/runs"),
        ("8. First getInstance creates?", "B) createInstance + SparkReporter path"),
        ("9. pause() instead of waits?", "Avoid — use explicit waits; pause is not preferred"),
        ("10. static block runs?", "B) Once when class first loaded"),
    ]:
        story.append(P(f"{q} → <b>{a}</b>", "DA"))

    story.append(P(
        "Note on T4-Q9: Prefer explicit waits / outcome waits over pause/sleep in E2E — more reliable in CI.",
        "DTip"
    ))

    story.append(P("Test 5 — Banking hard scenarios", "DH2"))
    for q, a in [
        ("1. First Chrome crash on CI then pass?", "B) Linux stability flags (+ optional retry)"),
        ("2. Balance locator timeout many accounts?", "B) DOM/table structure differs for heavy users"),
        ("3. Registration shows signup page not Welcome?", "B) Registration failed / env unhealthy"),
        ("4. Local error msg ≠ CI internal error?", "B) Shared demo instability under load"),
        ("5. Parallel same config user wrong balance?", "B) Shared account — use unique users"),
        ("6. Empty Extent 0 tests?", "B) flush() not called"),
        ("7. New user + config user both fail overview?", "B) Site showing error page / env down"),
        ("8. CI 13m → under 5m?", "B) More threads + remove sleeps + split smoke PR vs full nightly"),
        ("9. extentTest.get() NPE?", "B) onTestStart didn’t set ThreadLocal node"),
        ("10. Stale config user long-term?", "Prefer unique users each run; private env snapshot — not public INIT as default"),
    ]:
        story.append(P(f"{q} → <b>{a}</b>", "DA"))

    story.append(Spacer(1, 6))
    story.append(hline())
    story.append(P(
        "End of Week 4 Framework Enhancement + DDT Interview Q&amp;A — aligned to current framework.",
        "DBody"
    ))

    doc = SimpleDocTemplate(
        str(OUT), pagesize=A4,
        leftMargin=28, rightMargin=28, topMargin=24, bottomMargin=22,
        title="Week4 Framework Enhancement Interview Q&A",
        author="SDET Week 4",
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print("Updated:", OUT, "bytes=", OUT.stat().st_size)


if __name__ == "__main__":
    build()
