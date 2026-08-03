"""Rebuild TestNG Interview QA PDF with accuracy fixes."""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether, Preformatted
)

OUT = Path(
    r"C:\Users\sunil\OneDrive\Desktop\Java_selenium_material"
    r"\CLAUDE AI NOTES\Week 1 Java Fundamentals and Selenium Setup"
    r"\TetNG\TestNG_Interview_QA.pdf"
)

NAVY = HexColor("#0b3d5c")
TEAL = HexColor("#0f766e")
LIGHT = HexColor("#f0f9ff")
SOFT = HexColor("#e2e8f0")
DARK = HexColor("#1e293b")
MUTED = HexColor("#475569")
GOLD = HexColor("#b45309")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleMain", fontName="Helvetica-Bold", fontSize=18,
                          leading=22, textColor=white, alignment=TA_CENTER, spaceAfter=6))
styles.add(ParagraphStyle(name="SubMain", fontName="Helvetica", fontSize=10,
                          leading=13, textColor=HexColor("#dbeafe"), alignment=TA_CENTER))
styles.add(ParagraphStyle(name="DocH1", fontName="Helvetica-Bold", fontSize=12.5,
                          leading=16, textColor=NAVY, spaceBefore=10, spaceAfter=6))
styles.add(ParagraphStyle(name="DocH2", fontName="Helvetica-Bold", fontSize=10.5,
                          leading=13, textColor=TEAL, spaceBefore=8, spaceAfter=3))
styles.add(ParagraphStyle(name="DocQ", fontName="Helvetica-Bold", fontSize=9.5,
                          leading=12, textColor=NAVY, spaceBefore=7, spaceAfter=2))
styles.add(ParagraphStyle(name="DocA", fontName="Helvetica", fontSize=9,
                          leading=12, textColor=DARK, alignment=TA_JUSTIFY, spaceAfter=3))
styles.add(ParagraphStyle(name="DocTip", fontName="Helvetica-Oblique", fontSize=8.5,
                          leading=11, textColor=GOLD, leftIndent=8, spaceBefore=1, spaceAfter=4))
styles.add(ParagraphStyle(name="CodeBlock", fontName="Courier", fontSize=7.5,
                          leading=10, textColor=DARK, backColor=LIGHT,
                          leftIndent=4, rightIndent=4, spaceBefore=2, spaceAfter=4))
styles.add(ParagraphStyle(name="DocBody", fontName="Helvetica", fontSize=9,
                          leading=12, textColor=DARK, spaceAfter=4))
styles.add(ParagraphStyle(name="DocCell", fontName="Helvetica", fontSize=8,
                          leading=10, textColor=DARK))
styles.add(ParagraphStyle(name="DocHead", fontName="Helvetica-Bold", fontSize=8,
                          leading=10, textColor=white))
styles.add(ParagraphStyle(name="FixNote", fontName="Helvetica-Oblique", fontSize=8,
                          leading=10, textColor=MUTED, spaceAfter=6))


def P(t, s="DocA"):
    return Paragraph(t, styles[s])


def hline():
    return HRFlowable(width="100%", thickness=0.5, color=SOFT, spaceBefore=2, spaceAfter=6)


def code(text):
    # Escape for reportlab-ish plain text
    return Preformatted(text.rstrip(), styles["CodeBlock"])


def tip(t):
    return P(f"<b>Interview Tip:</b> {t}", "DocTip")


def qa(num, question, answer_parts):
    """answer_parts: list of flowables or strings (strings become A paragraphs)."""
    items = [P(f"Q{num}. {question}", "DocQ")]
    for part in answer_parts:
        if isinstance(part, str):
            items.append(P(part, "DocA"))
        else:
            items.append(part)
    return KeepTogether(items)


def footer(canvas, doc):
    canvas.saveState()
    page = canvas.getPageNumber()
    if page > 1:
        canvas.setFillColor(NAVY)
        canvas.rect(0, A4[1] - 16, A4[0], 16, fill=1, stroke=0)
        canvas.setFillColor(white)
        canvas.setFont("Helvetica", 7.5)
        canvas.drawString(36, A4[1] - 11, "TestNG Interview Questions | SDET 4+ Years")
        canvas.drawRightString(A4[0] - 36, A4[1] - 11, "Easy · Medium · Difficult")
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 7.5)
        canvas.drawCentredString(A4[0] / 2, 16, f"Page {page}")
    canvas.restoreState()


def build():
    story = []

    # Cover
    cover = Table([[P("TestNG Interview Questions &amp; Answers", "TitleMain")],
                   [P("For SDET / Automation Engineer – 4+ Years Experience<br/>"
                      "Banking &amp; Financial Domain Focus<br/><br/>"
                      "Easy (15) | Medium (15) | Difficult / Real-World (10)", "SubMain")]],
                  colWidths=[6.6 * inch])
    cover.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("TOPPADDING", (0, 0), (-1, -1), 28),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 22),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 16),
    ]))
    story.append(Spacer(1, 50))
    story.append(cover)
    story.append(Spacer(1, 16))
    story.append(P(
        "Verified study guide. Content aligns with real TestNG usage in Selenium frameworks "
        "(POM, listeners, retry, DataProvider, parallel, CI with Maven Surefire).",
        "DocBody"
    ))
    story.append(P(
        "Corrections applied vs older draft: Maven Surefire suite property name, report output "
        "paths (IDE vs Maven), Excel numeric cells, RetryAnalyzer vs listeners, @BeforeClass failure notes.",
        "FixNote"
    ))
    story.append(PageBreak())

    # SECTION A
    story.append(P("SECTION A – Easy (Fundamentals)", "DocH1"))
    story.append(hline())
    story.append(P("Answer these confidently and quickly. Interviewers use them as warm-ups.", "DocBody"))

    story.append(qa(1, "What is TestNG and why do we use it over JUnit?", [
        "TestNG (Test Next Generation) is a Java testing framework inspired by JUnit with richer features for automation. "
        "We prefer it for @BeforeSuite/@AfterSuite, groups, parallel execution, @DataProvider, dependsOnMethods/groups, "
        "flexible testng.xml control, and built-in HTML reporting. JUnit 5 has improved, but TestNG is still widely used "
        "in Selenium enterprise frameworks for suite XML + parallel + data-driven patterns.",
    ]))

    story.append(qa(2, "What are the different TestNG annotations? List them in execution order.", [
        "Typical order when all are present:",
        code("@BeforeSuite → @BeforeTest → @BeforeClass → @BeforeMethod\n"
             "    → @Test →\n"
             "@AfterMethod → @AfterClass → @AfterTest → @AfterSuite"),
        "Suite = once for entire suite. Test = once per &lt;test&gt; in testng.xml. Class = once per class. "
        "Method = before/after each @Test.",
        tip("Draw this lifecycle on a whiteboard — interviewers like visual answers."),
    ]))

    story.append(qa(3, "What is the difference between @BeforeMethod and @BeforeClass?", [
        "<b>@BeforeClass:</b> Runs once before the first @Test in the class. Good for one-time class setup "
        "(e.g., register a shared test user).",
        "<b>@BeforeMethod:</b> Runs before every @Test. Good for fresh browser session, navigate to URL, reset UI state.",
        "Many solid Selenium frameworks launch the browser in @BeforeMethod (not @BeforeClass) for better isolation.",
    ]))

    story.append(qa(4, "What is the default priority of a @Test method?", [
        "Default priority is <b>0</b>. Lower priority numbers run first. If two methods share the same priority, "
        "TestNG typically runs them in alphabetical order of method names (unless other ordering rules apply).",
    ]))

    story.append(qa(5, "How do you skip a test in TestNG?", [
        "1) <b>enabled=false</b> on @Test — excluded from the run entirely.",
        "2) <b>throw new SkipException(\"reason\")</b> — conditional skip at runtime (e.g., environment limitation).",
        "Skipped tests appear as SKIP in reports (not FAIL).",
    ]))

    story.append(qa(6, "What is the difference between Hard Assert and Soft Assert?", [
        "<b>Hard Assert (Assert):</b> Stops the test method at the first failure.",
        "<b>Soft Assert (SoftAssert):</b> Continues; call softAssert.assertAll() to report all failures together. "
        "Ideal for multi-field form validation.",
        tip("Always mention: forgetting assertAll() silently swallows soft failures."),
    ]))

    story.append(qa(7, "What is dependsOnMethods in TestNG?", [
        "Creates a dependency: if the parent method fails/skips, dependents are <b>SKIPPED</b> (not executed as FAIL). "
        "Example: checkBalance dependsOnMethods=\"loginTest\".",
    ]))

    story.append(qa(8, "What is testng.xml and why is it used?", [
        "Central suite config: which classes/methods run, order, parallel mode, groups include/exclude, parameters, "
        "and listeners — without changing Java code. Maven Surefire usually points to this file.",
    ]))

    story.append(qa(9, "How do you run tests in parallel using TestNG?", [
        code('<suite name="Suite" parallel="methods" thread-count="3">'),
        "parallel values: methods | tests | classes | instances. Always pair with ThreadLocal&lt;WebDriver&gt; "
        "so threads do not share one browser session.",
    ]))

    story.append(qa(10, "What is @DataProvider in TestNG?", [
        "Supplies multiple data sets to one @Test. Provider returns Object[][] (or Iterator&lt;Object[]&gt;). "
        "Test method runs once per row.",
        code('@DataProvider(name = "loginData")\n'
             'public Object[][] getData() {\n'
             '  return new Object[][] { {"u1","p1"}, {"u2","p2"} };\n'
             '}\n'
             '@Test(dataProvider = "loginData")\n'
             'public void loginTest(String user, String pass) { }'),
    ]))

    story.append(PageBreak())

    story.append(qa(11, "What are groups in TestNG?", [
        "Tag tests: @Test(groups={\"smoke\",\"regression\"}). In testng.xml use &lt;groups&gt;&lt;run&gt;&lt;include/&gt; "
        "to run only selected categories (smoke on PR, full regression nightly).",
    ]))

    story.append(qa(12, "What is the difference between @BeforeTest and @BeforeSuite?", [
        "<b>@BeforeSuite:</b> once before the entire suite (all &lt;test&gt; tags).",
        "<b>@BeforeTest:</b> once before each &lt;test&gt; tag in testng.xml. Three &lt;test&gt; blocks ⇒ runs three times.",
    ]))

    story.append(qa(13, "How do you set test execution order in TestNG?", [
        "1) priority on @Test  2) dependsOnMethods / dependsOnGroups  3) testng.xml method order with preserve-order. "
        "Prefer priority/groups for maintainability over hard-coded name dependencies where possible.",
    ]))

    story.append(qa(14, "What reports does TestNG generate by default?", [
        "When run from IDE / TestNG runner: usually under <b>test-output/</b> — index.html and emailable-report.html.",
        "When run via <b>Maven Surefire</b>: mainly under <b>target/surefire-reports/</b> (index.html, emailable-report.html, "
        "TEST-*.xml, testng-results.xml).",
        "Know both paths — interviewers often ask why they don’t see test-output after mvn test.",
    ]))

    story.append(qa(15, "What is timeOut in @Test?", [
        "@Test(timeOut = 5000) fails the test if it exceeds 5000 ms. Useful for hung UI waits or accidental infinite loops.",
    ]))

    # SECTION B
    story.append(P("SECTION B – Medium (Implementation)", "DocH1"))
    story.append(hline())

    story.append(qa(16, "How do you implement Retry Logic for failed tests in TestNG?", [
        "Implement IRetryAnalyzer and attach via @Test(retryAnalyzer=...) or globally with IAnnotationTransformer.",
        code("public class RetryAnalyzer implements IRetryAnalyzer {\n"
             "  private int count = 0;\n"
             "  private static final int MAX = 1;\n"
             "  public boolean retry(ITestResult result) {\n"
             "    if (count < MAX) { count++; return true; }\n"
             "    return false;\n"
             "  }\n"
             "}"),
        tip("Retry absorbs infra flake (network). Overuse hides real product bugs — say that out loud."),
    ]))

    story.append(qa(17, "What are TestNG Listeners? Name the commonly used ones.", [
        "Listeners hook into the TestNG lifecycle for custom behavior:",
        "• <b>ITestListener</b> — onTestStart/Success/Failure/Skipped (screenshots, Extent logs)",
        "• <b>ISuiteListener</b> — suite start/finish",
        "• <b>IReporter</b> — custom end-of-suite reports",
        "• <b>IAnnotationTransformer</b> — change annotations at runtime (e.g., attach retry to all tests)",
        "Note: <b>IRetryAnalyzer</b> is a retry hook, often registered via transformer — not the same as ITestListener.",
        "Register in testng.xml &lt;listeners&gt; or with @Listeners.",
    ]))

    story.append(qa(18, "How do you pass parameters to tests from testng.xml?", [
        "1) &lt;parameter name=\"browser\" value=\"chrome\"/&gt; + @Parameters({\"browser\"}) on @BeforeMethod/@Test.",
        "2) @DataProvider for multi-row test data (Excel/DB).",
        "Rule of thumb: Parameters for environment config; DataProvider for business test data.",
    ]))

    story.append(qa(19, "How do you run specific groups from testng.xml?", [
        code('<test name="Smoke">\n'
             '  <groups><run>\n'
             '    <include name="smoke"/>\n'
             '    <exclude name="broken"/>\n'
             '  </run></groups>\n'
             '  <classes>...</classes>\n'
             '</test>'),
        "Only included groups execute (subject to exclude).",
    ]))

    story.append(qa(20, "dependsOnMethods vs dependsOnGroups?", [
        "dependsOnMethods: tight coupling to method names (rename breaks it).",
        "dependsOnGroups: looser coupling — run after an entire group passes. Better for larger suites.",
    ]))

    story.append(PageBreak())

    story.append(qa(21, "How do you take a screenshot on test failure in TestNG?", [
        "Implement ITestListener.onTestFailure, get WebDriver from the test instance (e.g., BaseTest.getDriver()), "
        "use TakesScreenshot, save PNG, attach to Extent/Allure.",
        tip("In banking projects, include test name + timestamp (and txn id if available) in the file name for audit trails."),
    ]))

    story.append(qa(22, "How do you read test data from Excel using @DataProvider?", [
        "Use Apache POI (XSSFWorkbook) inside a @DataProvider. Prefer a shared ExcelReader utility.",
        "Handle cell types carefully — numeric cells throw if you only call getStringCellValue(). "
        "Convert NUMBER/BOOLEAN/BLANK to String (DataFormatter or cell-type switch).",
        "Also load from classpath in CI, not only FileInputStream of a hard-coded path.",
    ]))

    story.append(qa(23, "How do you configure TestNG with Maven Surefire Plugin?", [
        code("<plugin>\n"
             "  <groupId>org.apache.maven.plugins</groupId>\n"
             "  <artifactId>maven-surefire-plugin</artifactId>\n"
             "  <version>3.2.5</version>\n"
             "  <configuration>\n"
             "    <suiteXmlFiles>\n"
             "      <suiteXmlFile>testng.xml</suiteXmlFile>\n"
             "    </suiteXmlFiles>\n"
             "  </configuration>\n"
             "</plugin>"),
        "Override at runtime with: "
        "<font face='Courier'>mvn test -Dsurefire.suiteXmlFiles=testng-smoke.xml</font>",
        "Note: property name is <b>surefire.suiteXmlFiles</b> (not suiteXmlFile).",
    ]))

    story.append(qa(24, "What is IAnnotationTransformer and when do you use it?", [
        "Modifies annotations at runtime. Classic use: apply RetryAnalyzer to every @Test without annotating each method. "
        "Also used to enable/disable tests dynamically by environment.",
    ]))

    story.append(qa(25, "How do you handle multiple browser testing with TestNG?", [
        "Multiple &lt;test&gt; blocks with browser parameters, parallel=\"tests\", ThreadLocal&lt;WebDriver&gt; in BaseTest, "
        "switch on @Parameters browser in @BeforeMethod.",
    ]))

    story.append(qa(26, "Difference between @Factory and @DataProvider?", [
        "@DataProvider: same test method, multiple data rows, typically one class instance.",
        "@Factory: creates multiple class instances (e.g., one per browser/config); all @Test methods run per instance.",
    ]))

    story.append(qa(27, "How do you implement custom reporting with TestNG?", [
        "IReporter and/or Extent/Allure via ITestListener: init onStart, log per test, screenshot on failure, flush onFinish. "
        "Banking reports often add environment, build id, and transaction references for compliance.",
    ]))

    story.append(qa(28, "What is invocationCount and threadPoolSize?", [
        "@Test(invocationCount=10, threadPoolSize=3) runs the method 10 times with up to 3 threads — quick concurrency check. "
        "For real performance testing use JMeter/Gatling; this is not a load-test replacement.",
    ]))

    story.append(qa(29, "How do you handle test data setup and cleanup?", [
        "@BeforeSuite global data/env, @BeforeClass shared user/accounts, @BeforeMethod reset state, "
        "@AfterMethod logout/close browser, @AfterClass delete test data, @AfterSuite teardown. "
        "Isolation prevents cascading failures in banking flows.",
    ]))

    story.append(qa(30, "What happens if @BeforeClass fails?", [
        "All @Test methods in that class are <b>SKIPPED</b>. Configuration failure is reported on the @BeforeClass method. "
        "@BeforeMethod for those tests will not run. Cleanup (@AfterClass) may still run depending on failure type/config — "
        "always design teardown to be null-safe (driver may never have started).",
    ]))

    story.append(PageBreak())

    # SECTION C
    story.append(P("SECTION C – Difficult / Real-World Scenarios", "DocH1"))
    story.append(hline())
    story.append(P("Scenario questions for senior SDET / banking automation interviews.", "DocBody"))

    story.append(qa(31, "Design a TestNG framework for a banking app with 500+ tests?", [
        "POM + BaseTest/BasePage; modules under tests (login, accounts, transfers); resources for data &amp; suites; "
        "smoke vs regression vs module XMLs; Excel/DB DataProviders; Extent/Allure + screenshots; "
        "ThreadLocal drivers for parallel; CI (Jenkins/GitHub Actions) running mvn test and publishing artifacts.",
        tip("Whiteboard layers. Mention audit-friendly reports (txn id, timestamps, environment)."),
    ]))

    story.append(qa(32, "500 tests take 8 hours — how reduce with TestNG?", [
        "1) parallel methods/classes with safe thread-count  2) smoke vs nightly pipelines  "
        "3) dependsOnGroups to skip blocked modules  4) limited smart retry  "
        "5) cut redundant data via equivalence classes. Often 8h → a few hours with parallel + suite split.",
    ]))

    story.append(qa(33, "Passes locally, fails in CI — how debug?", [
        "1) Compare Surefire/TestNG reports local vs CI  2) failure screenshots  "
        "3) browser/headless/resolution/URL/env  4) timing &amp; explicit waits  "
        "5) ThreadLocal/shared state if parallel  6) environment-specific test data/DB.",
    ]))

    story.append(qa(34, "How do you handle flaky tests in banking automation?", [
        "Identify (retry-pass metrics) → quarantine group out of main CI gate → root-cause "
        "(waits, sessions, data) → fix &amp; re-stabilize → restore to regression. "
        "Flakes in fund transfer hide real defects — treat flaky rate as framework health KPI.",
    ]))

    story.append(qa(35, "Cross-browser testing with TestNG?", [
        "BaseTest with ThreadLocal&lt;WebDriver&gt;, @Parameters browser, switch chrome/firefox/edge, "
        "quit + driver.remove() in @AfterMethod to avoid leaks. ThreadLocal is mandatory for parallel browsers.",
        tip("Saying ThreadLocal + remove() is a senior differentiator."),
    ]))

    story.append(qa(36, "Integrate TestNG with Extent Reports + screenshots?", [
        "Listener creates ExtentReports/SparkReporter onStart, ExtentTest per method onTestStart, "
        "fail + screen capture onTestFailure, flush onFinish. Use ThreadLocal&lt;ExtentTest&gt; if parallel.",
    ]))

    story.append(qa(37, "Database verification after banking UI transfer?", [
        "UI action then DB assert (status, amount, debit/credit accounts) with SoftAssert + assertAll. "
        "dependsOnMethods so DB check runs only if transfer test passed. Use prepared statements / parameters "
        "for queries; clean test data in @AfterClass.",
    ]))

    story.append(qa(38, "DataProvider 100 rows; fails at row 45 — debug &amp; re-run?", [
        "Reports show parameters for the failed iteration. Use testng-failed.xml to re-run failures "
        "(failed invocations). Log current row keys inside the test. Prefer continuing with SoftAssert when you want "
        "all row failures in one pass.",
        code("# Re-run failed suite (Maven Surefire):\n"
             "mvn test -Dsurefire.suiteXmlFiles=target/surefire-reports/testng-failed.xml\n"
             "# IDE runs may place testng-failed.xml under test-output/"),
    ]))

    story.append(qa(39, "Multiple environments (Dev/QA/Staging/Prod) with TestNG?", [
        "Env property files + @Parameters env or -Denv=qa; load in @BeforeSuite into ConfigReader. "
        "CI job parameter selects env. Never hard-code prod credentials in repo.",
    ]))

    story.append(qa(40, "Thread safety with parallel tests &amp; shared resources?", [
        "ThreadLocal WebDriver and ThreadLocal DB connections; unique data per thread "
        "(thread id + timestamp); no mutable static test state; synchronize only shared report writers if needed.",
        tip("Thread safety is a must-ask at higher SDET bands — practice a 3-thread whiteboard diagram."),
    ]))

    story.append(PageBreak())

    # Revision table
    story.append(P("Quick Revision – One-Liners", "DocH1"))
    story.append(hline())

    rows = [
        ["#", "Question", "Key Answer"],
        ["1", "TestNG over JUnit?", "Groups, parallel, DataProvider, dependencies, XML"],
        ["2", "Annotation order?", "Suite → Test → Class → Method → @Test → reverse"],
        ["3", "@BeforeMethod vs Class?", "Per test vs once per class"],
        ["4", "Default priority?", "0 (alpha if same)"],
        ["5", "Skip a test?", "enabled=false or SkipException"],
        ["6", "Hard vs Soft Assert?", "Stop vs continue; need assertAll()"],
        ["7", "dependsOnMethods?", "Dependent SKIPPED if parent fails"],
        ["8", "testng.xml?", "Central suite control"],
        ["9", "Parallel modes?", "methods, tests, classes, instances"],
        ["10", "@DataProvider?", "Object[][] / Iterator; one run per row"],
        ["11", "Retry?", "IRetryAnalyzer (+ transformer for global)"],
        ["12", "Screenshot on fail?", "ITestListener.onTestFailure"],
        ["13", "Factory vs DataProvider?", "Many class instances vs many data sets"],
        ["14", "Thread safety?", "ThreadLocal&lt;WebDriver&gt; + unique data"],
        ["15", "testng-failed.xml?", "Re-run failures; Surefire path under target/"],
        ["16", "Maven suite prop?", "surefire.suiteXmlFiles"],
        ["17", "Maven reports folder?", "target/surefire-reports (not only test-output)"],
    ]
    data = []
    for i, r in enumerate(rows):
        style = styles["DocHead"] if i == 0 else styles["DocCell"]
        data.append([Paragraph(c, style) for c in r])
    t = Table(data, colWidths=[0.35 * inch, 1.7 * inch, 4.5 * inch], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT]),
        ("GRID", (0, 0), (-1, -1), 0.35, SOFT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))
    story.append(P(
        "Practice: answer Easy section in under 10 minutes without notes, then one Medium + one Difficult scenario aloud.",
        "DocTip"
    ))

    doc = SimpleDocTemplate(
        str(OUT), pagesize=A4,
        leftMargin=36, rightMargin=36, topMargin=32, bottomMargin=32,
        title="TestNG Interview Questions & Answers",
        author="SDET Interview Prep",
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print("Updated:", OUT, "bytes=", OUT.stat().st_size)


if __name__ == "__main__":
    build()
