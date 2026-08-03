"""Rebuild Week3 Framework Design + POM Interview PDF (aligned to current framework)."""
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
    r"\CLAUDE AI NOTES\week3_Framework Design - Page Object Model"
    r"\Week3_Framework_Design_InterviewQA.pdf"
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
styles.add(ParagraphStyle(name="TMain", fontName="Helvetica-Bold", fontSize=14,
                          leading=17, textColor=white, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="TSub", fontName="Helvetica", fontSize=8.8,
                          leading=11.5, textColor=HexColor("#dbeafe"), alignment=TA_CENTER))
styles.add(ParagraphStyle(name="DH1", fontName="Helvetica-Bold", fontSize=10.5,
                          leading=13, textColor=NAVY, spaceBefore=6, spaceAfter=3))
styles.add(ParagraphStyle(name="DH2", fontName="Helvetica-Bold", fontSize=9,
                          leading=11, textColor=TEAL, spaceBefore=4, spaceAfter=2))
styles.add(ParagraphStyle(name="DQ", fontName="Helvetica-Bold", fontSize=8.3,
                          leading=10.5, textColor=NAVY, spaceBefore=3, spaceAfter=1))
styles.add(ParagraphStyle(name="DA", fontName="Helvetica", fontSize=7.9,
                          leading=10.1, textColor=DARK, alignment=TA_JUSTIFY, spaceAfter=1))
styles.add(ParagraphStyle(name="DTip", fontName="Helvetica-Oblique", fontSize=7.2,
                          leading=9.1, textColor=GOLD, leftIndent=3, spaceAfter=2))
styles.add(ParagraphStyle(name="DFix", fontName="Helvetica-Oblique", fontSize=7.1,
                          leading=9, textColor=GREEN, spaceAfter=2))
styles.add(ParagraphStyle(name="DBody", fontName="Helvetica", fontSize=8,
                          leading=10.2, textColor=DARK, spaceAfter=2))
styles.add(ParagraphStyle(name="CodeB", fontName="Courier", fontSize=6.2,
                          leading=8, textColor=DARK, backColor=LIGHT, spaceBefore=1, spaceAfter=1))
styles.add(ParagraphStyle(name="DCell", fontName="Helvetica", fontSize=6.8,
                          leading=8.6, textColor=DARK))
styles.add(ParagraphStyle(name="DHead", fontName="Helvetica-Bold", fontSize=6.8,
                          leading=8.6, textColor=white))
styles.add(ParagraphStyle(name="LvlB", fontName="Helvetica-Bold", fontSize=7.3,
                          textColor=HexColor("#1d4ed8"), spaceAfter=1))
styles.add(ParagraphStyle(name="LvlR", fontName="Helvetica-Bold", fontSize=7.3,
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
        canvas.setFont("Helvetica", 6.5)
        canvas.drawString(26, A4[1] - 8, "Week 3: Framework Design + POM | Interview Q&A")
        canvas.drawRightString(A4[0] - 26, A4[1] - 8, "SDET Prep")
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 6.5)
        canvas.drawCentredString(A4[0] / 2, 10, f"Page {page}")
    canvas.restoreState()


def build():
    story = []

    cover = Table([
        [P("Week 3: Framework Design + Page Object Model", "TMain")],
        [P("POM · BasePage · BaseTest · ConfigReader · ExcelReader · Listeners · CI<br/>"
           "Aligned to ParaBank Selenium-Java Banking Framework<br/><br/>"
           "PART 1 Fundamentals &nbsp;·&nbsp; PART 2 Senior &nbsp;·&nbsp; PART 3 Practice MCQs + Answer Key",
           "TSub")],
    ], colWidths=[6.7 * inch])
    cover.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("TOPPADDING", (0, 0), (-1, -1), 18),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(Spacer(1, 24))
    story.append(cover)
    story.append(Spacer(1, 8))
    story.append(P(
        "Verified against your current framework (ThreadLocal driver, classpath ConfigReader, "
        "UserFactory, RetryListener, reports/ci/run-N, no public DB INIT by default).",
        "DBody"
    ))
    story.append(P(
        "Updates: POM vs PageFactory wording; ConfigReader classpath load; DB INIT opt-in only; "
        "auth-bypass SkipException; parallel ThreadLocal; meaningful assertions.",
        "DFix"
    ))
    story.append(PageBreak())

    # PART 1
    story.append(P("PART 1 — FUNDAMENTALS (Blue)", "DH1"))
    story.append(P("Concept clarity — asked at all levels", "LvlB"))
    story.append(hline())

    story.append(qa(1, "What is Page Object Model (POM)?", [
        "Design pattern: each page/screen → Java class with locators + actions. Tests call methods "
        "(login, transferFunds), not raw Selenium. Reduces duplication and localizes UI change impact.",
        code("public class LoginPage extends BasePage {\n"
             "  private final By username = By.name(\"username\");\n"
             "  private final By password = By.name(\"password\");\n"
             "  private final By loginBtn = By.cssSelector(\"input[value='Log In']\");\n"
             "  public void login(String u, String p) {\n"
             "    type(username, u); type(password, p); click(loginBtn);\n"
             "  }\n"
             "}"),
        tip("POM ≠ PageFactory. PageFactory (@FindBy + initElements) is optional Selenium helper."),
    ]))

    story.append(qa(2, "BasePage vs BaseTest?", [
        "<b>BasePage</b>: parent of page objects — click/type/getText/waits/select.  "
        "<b>BaseTest</b>: parent of tests — browser lifecycle (@BeforeMethod/@AfterMethod), ThreadLocal driver.",
        "LoginPage extends BasePage; LoginTest extends BaseTest.",
    ]))

    story.append(qa(3, "Why private final By locators (not WebElement fields)?", [
        "private: encapsulation. final: constant locator definition. By: stores the address, finds at use-time "
        "→ fewer stale references than caching WebElement at construction.",
        code("// Good\nprivate final By username = By.name(\"username\");\n"
             "// Risky at field init time\n// private WebElement username = driver.findElement(...);"),
    ]))

    story.append(qa(4, "What is ConfigReader and why?", [
        "Loads key=value from config.properties once; code uses ConfigReader.get(\"base.url\"). "
        "Change URL/browser/timeouts in one file.",
        "In our framework it loads from <b>classpath</b> via getResourceAsStream (works in IDE, Maven, CI):",
        code("static {\n"
             "  try (InputStream in = ConfigReader.class.getClassLoader()\n"
             "      .getResourceAsStream(\"config.properties\")) {\n"
             "    properties = new Properties(); properties.load(in);\n"
             "  }\n"
             "}"),
    ]))

    story.append(qa(5, "Static block in ConfigReader?", [
        "Runs once when class first loads. Properties stay in memory for get() calls — efficient, no re-read per test.",
    ]))

    story.append(qa(6, "ExcelReader + data-driven testing?", [
        "Apache POI reads .xlsx. @DataProvider returns Object[][] / filtered rows; one @Test runs per data set. "
        "Business can add rows without Java changes. Our Execute=Yes column filters which rows run.",
    ]))

    story.append(qa(7, "TestNG Listener / ITestListener?", [
        "Hooks into lifecycle: onTestStart/Success/Failure/Skipped. Used for Extent logging + screenshots on failure. "
        "Register in testng.xml &lt;listeners&gt; or @Listeners.",
    ]))

    story.append(qa(8, "Why @BeforeMethod / @AfterMethod in BaseTest?", [
        "Fresh browser per test → isolation (no leftover session/cookies). tearDown quits driver and "
        "ThreadLocal.remove() to prevent leaks.",
    ]))

    story.append(qa(9, "Implicit vs explicit wait?", [
        "Implicit: global presence polling. Explicit: condition-specific (clickable/visible/url). "
        "Prefer explicit in BasePage; avoid relying on both mixed together.",
    ]))

    story.append(qa(10, "@DataProvider?", [
        "Method returning Object[][] (or Iterator). TestNG invokes @Test once per row with those params.",
    ]))

    story.append(qa(11, "Method chaining in page objects?", [
        "Action methods return this → fluent calls: enterUsername(u).enterPassword(p).clickLogin().",
    ]))

    story.append(qa(12, "Why no assertions in Page Objects?", [
        "Pages perform actions / return state. Assertions live in tests so the same login() works for "
        "positive and negative cases.",
    ]))

    story.append(PageBreak())

    # PART 2
    story.append(P("PART 2 — SENIOR / FRAMEWORK LEVEL (Red)", "DH1"))
    story.append(P("4+ years — architecture, flaky env, parallel, real stories", "LvlR"))
    story.append(hline())

    story.append(qa("S1", "Design a POM banking framework from scratch?", [
        "Layers: base/ (BasePage, BaseTest) · pages/ · tests/ · utils/ (Config, Excel, UserFactory, Extent) · "
        "listeners/ (TestListener, RetryListener) · resources/ (config, testdata) · testng.xml · CI workflow · "
        "reports/ci/run-N/. One page per feature (Login, Accounts, Transfer, BillPay).",
    ]))

    story.append(qa("S2", "Flaky shared public test environment?", [
        "1) Unique users (timestamp prefix) via UserFactory  2) RetryAnalyzer once for infra flake  "
        "3) Env-specific config  4) Health awareness / KNOWN_ISSUES  "
        "5) <b>Do NOT wipe public shared DB by default</b> — INIT only on private instances "
        "(-Dparabank.init.db=true). Public INIT harms everyone else.",
        tip("Senior answer: isolate data, don’t nuke shared demos in CI."),
    ]))

    story.append(qa("S3", "Excel DataProvider with Execute filter?", [
        code("for (Map<String,String> row : ExcelReader.readExcel(path, \"Sheet1\")) {\n"
             "  if (\"Yes\".equalsIgnoreCase(row.get(\"Execute\"))) {\n"
             "    filtered.add(new Object[]{ row.get(\"Username\"), row.get(\"Password\"), ...});\n"
             "  }\n"
             "}"),
    ]))

    story.append(qa("S4", "Screenshot listener — get driver?", [
        code("WebDriver d = ((BaseTest) result.getInstance()).getDriver();\n"
             "File src = ((TakesScreenshot) d).getScreenshotAs(OutputType.FILE);\n"
             "// save testName_timestamp.png; attach to Extent"),
        "Cast fails if test class does not extend BaseTest.",
    ]))

    story.append(qa("S5", "Two @BeforeMethod — BaseTest + LoginTest order?", [
        "Parent first: BaseTest.setUp() → LoginTest.navigateToLoginPage() → @Test → tearDown(). "
        "Browser generic setup vs page-specific navigation.",
    ]))

    story.append(qa("S6", "Parallel execution?", [
        code("private static final ThreadLocal<WebDriver> driver = new ThreadLocal<>();\n"
             "@BeforeMethod public void setUp() { driver.set(new ChromeDriver(opts)); }\n"
             "public static WebDriver getDriver() { return driver.get(); }\n"
             "@AfterMethod public void tearDown() {\n"
             "  if (getDriver()!=null) { getDriver().quit(); driver.remove(); }\n"
             "}"),
        "testng.xml parallel=methods + unique data/users + unique download dirs.",
    ]))

    story.append(qa("S7", "Test passed but feature broken (false green)?", [
        "Example: invalid login still landed on overview (demo auth bypass). Assertion only checked "
        "URL contains overview. Fix: assert identity (welcome name/accounts) or SkipException for known "
        "env defect with documentation — not silent pass.",
    ]))

    story.append(qa("S8", "Unstable ParaBank handling (current approach)?", [
        "Unique users; registration retries (UserFactory); outcome waits for transfer/billpay; "
        "negative login skips when auth-bypass active (KNOWN_ISSUES); CI headless; reports per run. "
        "Real banks: dedicated QA + fresh data snapshot.",
    ]))

    story.append(P("Rapid fire", "DH2"))
    rf = [
        ["POM is?", "UI separation design pattern (not PageFactory itself)"],
        ["Locators live?", "Page classes only"],
        ["Assertions live?", "Test classes only"],
        ["super(driver)?", "BasePage ctor sets driver + wait"],
        ["ConfigReader?", "Classpath properties externalization"],
        ["Apache POI?", "Read/write Excel"],
        ["readExcel vs AsArray?", "List&lt;Map&gt; vs Object[][] for DataProvider"],
        ["Register listener?", "&lt;listeners&gt;&lt;listener class-name=.../&gt; in testng.xml"],
        ["ThreadLocal why?", "One driver per thread in parallel"],
        ["CI headless?", "config headless OR env CI=true"],
    ]
    data = [[Paragraph(h, styles["DHead"]) for h in ["Q", "A"]]]
    for a, b in rf:
        data.append([Paragraph(a, styles["DCell"]), Paragraph(b, styles["DCell"])])
    t = Table(data, colWidths=[1.8 * inch, 4.7 * inch], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT]),
        ("GRID", (0, 0), (-1, -1), 0.3, SOFT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))
    story.append(t)

    story.append(PageBreak())

    # PART 3 MCQs condensed with answers
    story.append(P("PART 3 — PRACTICE MCQs (with answers)", "DH1"))
    story.append(hline())

    story.append(P("Test 1 — POM Basics", "DH2"))
    mcq1 = [
        ("1. POM stands for?", "B) Page Object Model"),
        ("2. Locators belong in?", "C) Page Object class"),
        ("3. readExcelAsArray return type?", "C) Object[][]"),
        ("4. super(driver) does?", "B) Calls BasePage constructor"),
        ("5. Before every @Test?", "C) @BeforeMethod"),
        ("6. Assert.assertTrue belongs in?", "C) Test class methods"),
        ("7. ConfigReader.get(\"base.url\")?", "C) URL from config.properties"),
        ("8. Correct locator field?", "B) private final By btn = By.id(\"btn\");"),
        ("9. onTestFailure typically?", "C) Captures screenshot"),
        ("10. POI class for .xlsx?", "B) XSSFWorkbook"),
    ]
    for q, a in mcq1:
        story.append(P(f"{q} → <b>{a}</b>", "DA"))

    story.append(P("Test 2 — Framework structure", "DH2"))
    mcq2 = [
        ("1. BasePage package?", "C) base"),
        ("2. Excel Execute column?", "B) Controls whether row runs"),
        ("3. ConfigReader method?", "B) get(key)"),
        ("4. @DataProvider does?", "B) Feeds params to @Test"),
        ("5. Unique username?", "C) prefix + currentTimeMillis()"),
        ("6. static block runs?", "B) Once when class first loads"),
        ("7. Skip listener method?", "C) onTestSkipped()"),
        ("8. Driver for parallel?", "ThreadLocal (not plain static)"),
        ("9. navigateToLoginPage?", "C) Opens URL + creates LoginPage"),
        ("10. Array method for DP?", "C) readExcelAsArray()"),
    ]
    for q, a in mcq2:
        story.append(P(f"{q} → <b>{a}</b>", "DA"))

    story.append(P("Test 3 — Page objects & waits", "DH2"))
    mcq3 = [
        ("1. Field-level findElement risk?", "C) Stale/timing — prefer By + find at use"),
        ("2. elementToBeClickable why?", "B) Visible ≠ clickable"),
        ("3. getText().trim() returns?", "B) Visible text without edge spaces"),
        ("4. After Transfer wait for?", "C) Success/error message (outcome)"),
        ("5. Native dropdown?", "B) new Select(...).selectByVisibleText"),
        ("6. try/catch in isDisplayed?", "B) Return false if missing"),
        ("7. After register auto-login?", "B) Logout then login page"),
        ("8. Method chaining?", "B) Methods return this"),
        ("9. No assert in login()?", "B) Reuse for valid + invalid"),
        ("10. getCellType handles?", "B) STRING/NUMERIC/BOOLEAN/…"),
    ]
    for q, a in mcq3:
        story.append(P(f"{q} → <b>{a}</b>", "DA"))

    story.append(PageBreak())

    story.append(P("Test 4 — Advanced framework", "DH2"))
    mcq4 = [
        ("1. ThreadLocal why?", "B) Own driver copy per thread"),
        ("2. @BeforeMethod order?", "B) BaseTest setUp → child navigate → test → tearDown"),
        ("3. Headless DB init browser?", "B) Temp browser need not be visible (if INIT enabled)"),
        ("4. Execute filter?", "B) Selective run without deleting Excel rows"),
        ("5. Unique user?", "B) currentTimeMillis suffix"),
        ("6. Cast to BaseTest?", "A) getDriver() lives on BaseTest"),
        ("7. dependsOnMethods parent fails?", "B) Dependent is skipped"),
        ("8. headless local false + CI=true?", "D) headless if config OR CI env"),
        ("9. .trim() on properties?", "B) Avoid whitespace key/value bugs"),
        ("10. Parallel methods in XML?", "parallel=\"methods\" thread-count=\"N\""),
    ]
    for q, a in mcq4:
        story.append(P(f"{q} → <b>{a}</b>", "DA"))

    story.append(P("Test 5 — Banking scenarios (hard)", "DH2"))
    mcq5 = [
        ("1. Invalid login → Accounts Overview?", "B) Demo env auth bypass / accepts bad creds"),
        ("2. Many registrations → internal error?", "B) Shared demo instability/throttling"),
        ("3. Transfer $100 balance same?", "C) Single-account transfer nets zero total"),
        ("4. Add LoanRequestPage order?", "B) Inspect → page extends BasePage → test extends BaseTest"),
        ("5. Parallel downloads clash?", "C) Thread-specific download directories"),
        ("6. False green login URL-only?", "B) Env accepts any credentials"),
        ("7. Numeric Excel 123 not 123.0?", "C) floor check → long cast"),
        ("8. Parallel 5 threads 40min suite?", "C) ~8–12 min (overhead/deps)"),
        ("9. ClassCastException getDriver?", "B) Test class doesn’t extend BaseTest"),
        ("10. Multi-env suite?", "C) env-specific properties + -Denv=qa"),
    ]
    for q, a in mcq5:
        story.append(P(f"{q} → <b>{a}</b>", "DA"))

    story.append(Spacer(1, 6))
    story.append(hline())
    story.append(P(
        "End of Week 3 Framework Design + POM Interview Q&amp;A — aligned to current ParaBank framework.",
        "DBody"
    ))

    doc = SimpleDocTemplate(
        str(OUT), pagesize=A4,
        leftMargin=28, rightMargin=28, topMargin=24, bottomMargin=22,
        title="Week3 Framework Design POM Interview Q&A",
        author="SDET Week 3",
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print("Updated:", OUT, "bytes=", OUT.stat().st_size)


if __name__ == "__main__":
    build()
