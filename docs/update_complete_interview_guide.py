"""Rebuild Complete Interview Q&A Guide PDF with accuracy fixes."""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether, Preformatted, ListFlowable, ListItem
)

OUT = Path(r"C:\Users\sunil\OneDrive\Desktop\Java_selenium_material\CLAUDE AI NOTES\Complete_Interview_QA_Guide.pdf")

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
styles.add(ParagraphStyle(name="TMain", fontName="Helvetica-Bold", fontSize=16,
                          leading=20, textColor=white, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="TSub", fontName="Helvetica", fontSize=9,
                          leading=12, textColor=HexColor("#dbeafe"), alignment=TA_CENTER))
styles.add(ParagraphStyle(name="DH1", fontName="Helvetica-Bold", fontSize=11,
                          leading=13.5, textColor=NAVY, spaceBefore=8, spaceAfter=3))
styles.add(ParagraphStyle(name="DH2", fontName="Helvetica-Bold", fontSize=9.2,
                          leading=11.5, textColor=TEAL, spaceBefore=5, spaceAfter=2))
styles.add(ParagraphStyle(name="DQ", fontName="Helvetica-Bold", fontSize=8.3,
                          leading=10.5, textColor=NAVY, spaceBefore=3, spaceAfter=1))
styles.add(ParagraphStyle(name="DA", fontName="Helvetica", fontSize=7.8,
                          leading=9.9, textColor=DARK, alignment=TA_JUSTIFY, spaceAfter=1))
styles.add(ParagraphStyle(name="DTip", fontName="Helvetica-Oblique", fontSize=7.1,
                          leading=9, textColor=GOLD, leftIndent=3, spaceAfter=1))
styles.add(ParagraphStyle(name="DFix", fontName="Helvetica-Oblique", fontSize=7.0,
                          leading=8.9, textColor=GREEN, spaceAfter=2))
styles.add(ParagraphStyle(name="DBody", fontName="Helvetica", fontSize=8,
                          leading=10.2, textColor=DARK, spaceAfter=2))
styles.add(ParagraphStyle(name="CodeB", fontName="Courier", fontSize=6.1,
                          leading=7.8, textColor=DARK, backColor=LIGHT, spaceBefore=1, spaceAfter=1))
styles.add(ParagraphStyle(name="DCell", fontName="Helvetica", fontSize=6.8,
                          leading=8.5, textColor=DARK))
styles.add(ParagraphStyle(name="DHead", fontName="Helvetica-Bold", fontSize=6.8,
                          leading=8.5, textColor=white))
styles.add(ParagraphStyle(name="TOC", fontName="Helvetica", fontSize=8.5,
                          leading=12, textColor=DARK, leftIndent=8, spaceAfter=1))


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
        canvas.drawString(26, A4[1] - 8, "Complete Interview Q&A Guide | QA Automation Engineer")
        canvas.drawRightString(A4[0] - 26, A4[1] - 8, "Technical · Behavioral · Portfolio")
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 6.4)
        canvas.drawCentredString(A4[0] / 2, 10, f"Page {page}")
    canvas.restoreState()


def build():
    story = []

    # Cover
    cover = Table([
        [P("COMPLETE INTERVIEW Q&amp;A GUIDE", "TMain")],
        [P("QA Automation Engineer<br/>"
           "Technical · Behavioral · Framework Walkthroughs<br/><br/>"
           "Verified &amp; updated · Selenium 4 · TestNG · CI/CD · Framework Design<br/>"
           "Primary portfolio: ParaBank Selenium-Java Banking Framework",
           "TSub")],
    ], colWidths=[6.7 * inch])
    cover.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("TOPPADDING", (0, 0), (-1, -1), 22),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
    ]))
    story.append(Spacer(1, 40))
    story.append(cover)
    story.append(Spacer(1, 10))
    story.append(P(
        "This guide consolidates high-frequency interview topics. Answers are written so you can speak them "
        "in first person and tie them to your real GitHub framework.",
        "DBody"
    ))
    story.append(P(
        "Accuracy updates: Selenium 4 Duration API; ThreadLocal (not singleton driver); no public DB INIT by default; "
        "get vs navigate; waits mixing; PageFactory ≠ POM; CI reports/ci/run-N; honest portfolio claims.",
        "DFix"
    ))

    story.append(P("TABLE OF CONTENTS", "DH1"))
    story.append(hline())
    for line in [
        "1. Selenium with Java",
        "2. Playwright (comparison / interview awareness)",
        "3. API Automation (Rest Assured)",
        "4. CI/CD Integration (GitHub Actions / Jenkins)",
        "5. Performance Testing (JMeter / Gatling)",
        "6. Behavioral & Soft Skills (STAR)",
        "7. Framework Architecture (YOUR portfolio walkthrough)",
        "8. Tricky Scenario Questions",
        "Appendix: How to present your portfolio",
    ]:
        story.append(P(line, "TOC"))

    story.append(PageBreak())

    # ========== SECTION 1 SELENIUM ==========
    story.append(P("SECTION 1: SELENIUM WITH JAVA", "DH1"))
    story.append(hline())

    story.append(qa(1, "What is Selenium WebDriver and how does it work?", [
        "WebDriver automates real browsers via browser drivers using the <b>W3C WebDriver</b> protocol "
        "(evolution of JSON Wire). Commands like findElement are sent to the driver, which instructs the browser.",
        tip("Mention W3C standardization to show you know the evolution."),
    ]))
    story.append(qa(2, "close() vs quit()?", [
        "close() closes current window/tab. quit() ends the whole session and all windows. "
        "Prefer quit() in @AfterMethod teardown for isolation; always free resources.",
    ]))
    story.append(qa(3, "Types of waits? Preference?", [
        "Implicit (global find polling), Explicit WebDriverWait+ExpectedConditions, FluentWait "
        "(custom poll/ignore). Prefer explicit. Avoid Thread.sleep as strategy. "
        "WebDriverWait extends FluentWait. Use Duration.ofSeconds(...) (Selenium 4), not TimeUnit for new code.",
        tip("Never mix implicit+explicit casually — unpredictable total wait."),
    ]))
    story.append(qa(4, "findElement vs findElements?", [
        "findElement → one WebElement or NoSuchElementException. findElements → List, empty if none. "
        "Use empty-list check for presence without try/catch.",
    ]))
    story.append(qa(5, "Alerts?", [
        "Wait alertIsPresent → switchTo().alert() → getText/accept/dismiss/sendKeys(prompt). "
        "JS alerts ≠ HTML modals ≠ OS file dialogs.",
    ]))
    story.append(qa(6, "Frames?", [
        "switchTo().frame(index|name|WebElement); prefer WebElement. Exit: parentFrame or defaultContent. Nested: outer then inner.",
    ]))
    story.append(qa(7, "Multiple windows/tabs?", [
        "Store main handle → action → wait numberOfWindowsToBe → switch to other handle → work → close → switch main. "
        "Also Selenium 4 newWindow(WindowType.TAB/WINDOW).",
    ]))
    story.append(qa(8, "XPath vs CSS?", [
        "CSS: clean/fast for id/class/attributes, downward only. XPath: axes, text(), parent/sibling. "
        "Pick maintainability first; micro-benchmarks rarely matter at suite level.",
    ]))
    story.append(qa(9, "Drag and drop?", [
        "Actions.dragAndDrop / clickAndHold+move+release. HTML5 DnD often needs manual sequence or JS DataTransfer.",
    ]))
    story.append(qa(10, "StaleElementReferenceException?", [
        "DOM node replaced after locate. Re-find before act; FluentWait ignoring Stale; don’t cache WebElements across AJAX.",
    ]))
    story.append(qa(11, "File upload?", [
        "sendKeys(absolutePath) on input[type=file]. Don’t open OS dialog. Grid: LocalFileDetector on RemoteWebDriver.",
    ]))
    story.append(qa(12, "Screenshots?", [
        "TakesScreenshot FILE/BASE64/BYTES; element.getScreenshotAs in S4; attach on failure via ITestListener + Extent/Allure.",
    ]))
    story.append(qa(13, "POM?", [
        "Page classes hold locators+actions; tests assert. POM ≠ PageFactory (@FindBy needs initElements).",
    ]))
    story.append(qa(14, "Flaky tests?", [
        "Explicit waits, unique data, ThreadLocal isolation, one RetryAnalyzer retry, stable locators, root-cause not endless retry.",
    ]))
    story.append(qa(15, "TestNG integration?", [
        "@Test/groups/DataProvider/listeners; testng.xml suites; Surefire suiteXmlFiles; dependsOnMethods skips dependents.",
    ]))

    # SECTION 2 Playwright
    story.append(P("SECTION 2: PLAYWRIGHT (Interview awareness)", "DH1"))
    story.append(hline())
    story.append(P(
        "Even if your strongest portfolio is Selenium, interviewers compare tools. Answer honestly about depth.",
        "DBody"
    ))
    story.append(qa(16, "Playwright vs Selenium?", [
        "Playwright: auto-wait, multi-browser from one API, tracing, network interception, often faster setup. "
        "Selenium: wider language/tooling ecosystem, W3C standard, very common in enterprises. "
        "Choose based on team stack, not hype.",
    ]))
    story.append(qa(17, "Playwright auto-waiting?", [
        "Actions wait for actionability (visible, stable, enabled) reducing explicit waits. Still need waits for app-specific states.",
    ]))
    story.append(qa(18, "When keep Selenium?", [
        "Legacy suite, org standard, Grid/cloud investments, existing skills/hiring market.",
    ]))

    # SECTION 3 API
    story.append(P("SECTION 3: API AUTOMATION (Rest Assured)", "DH1"))
    story.append(hline())
    story.append(qa(19, "What is REST API testing?", [
        "Validate endpoints: status, headers, body schema, business data, auth, errors — without UI. Faster feedback for backend.",
    ]))
    story.append(qa(20, "Rest Assured basics?", [
        code("given()\n  .baseUri(base)\n  .header(\"Authorization\", token)\n"
             ".when()\n  .get(\"/accounts/{id}\", id)\n"
             ".then()\n  .statusCode(200)\n  .body(\"status\", equalTo(\"ACTIVE\"));"),
    ]))
    story.append(qa(21, "UI vs API automation?", [
        "API: speed, contract, data setup/teardown. UI: user journeys, rendering, JS issues. Best suites combine both.",
    ]))
    story.append(qa(22, "Auth in API tests?", [
        "Bearer tokens, basic auth, OAuth flows; never commit secrets — use env/CI secrets.",
    ]))
    story.append(qa(23, "Schema validation?", [
        "JSON Schema / Hamcrest matchers; assert types and required fields, not only happy path values.",
    ]))

    story.append(PageBreak())

    # SECTION 4 CI/CD
    story.append(P("SECTION 4: CI/CD INTEGRATION", "DH1"))
    story.append(hline())
    story.append(qa(24, "What is CI/CD and why for QA?", [
        "CI auto-builds/tests every push; CD delivers after gates. Catches regressions early; no “works on my machine only”.",
    ]))
    story.append(qa(25, "GitHub Actions for Selenium?", [
        "ubuntu-latest → setup-java → Chrome → mvn clean test with CI=true headless → upload artifacts → "
        "optional publish reports/ci/run-N. Fail job on test failure.",
    ]))
    story.append(qa(26, "Local pass, CI fail?", [
        "Headless, timing, browser version, absolute paths, Linux flags (--no-sandbox, --disable-dev-shm-usage), env data.",
    ]))
    story.append(qa(27, "Where are reports?", [
        "Local: test-output/, target/surefire-reports/. CI: Actions Artifacts + repo reports/ci/run-N after pull.",
    ]))
    story.append(qa(28, "Secrets in CI?", [
        "GitHub Secrets / env vars; never commit passwords/tokens; mask logs.",
    ]))

    # SECTION 5 Performance
    story.append(P("SECTION 5: PERFORMANCE TESTING", "DH1"))
    story.append(hline())
    story.append(qa(29, "What is performance testing?", [
        "Measure speed/stability under load: response time, throughput, error rate, resource use — not functional pass/fail alone.",
    ]))
    story.append(qa(30, "JMeter vs Gatling?", [
        "JMeter: GUI + plugins, widely known. Gatling: code-as-test (Scala/Java DSL), strong reporting. Pick team skill/stack.",
    ]))
    story.append(qa(31, "Selenium for load testing?", [
        "No — UI automation is heavy. Use protocol-level tools for load; Selenium for functional UX checks.",
    ]))
    story.append(qa(32, "Key metrics?", [
        "p95/p99 latency, RPS, error %, CPU/memory, saturation point. Define SLAs with stakeholders.",
    ]))

    # SECTION 6 Behavioral
    story.append(P("SECTION 6: BEHAVIORAL & SOFT SKILLS (STAR)", "DH1"))
    story.append(hline())
    story.append(P(
        "STAR = Situation · Task · Action · Result. Always end with a measurable or clear outcome.",
        "DBody"
    ))
    story.append(qa(33, "Tell me about yourself (automation focus)?", [
        "I am a QA automation engineer focused on Selenium/TestNG frameworks. I built a banking UI framework "
        "with POM, data-driven Excel tests, Extent reporting, and GitHub Actions CI. I care about maintainable "
        "tests, meaningful asserts, and stable pipelines — not just recording scripts.",
    ]))
    story.append(qa(34, "Conflict with a developer over a bug?", [
        "S: Dev said “works on my machine”. T: Prove/disprove. A: Repro steps, logs, screenshots, env versions, "
        "pair debug. R: Confirmed bug or adjusted test; relationship stayed professional.",
    ]))
    story.append(qa(35, "Missed a bug / production issue?", [
        "Own it, analyze gap (missing case, false green assert), add test + process fix (review checklist). No blame game.",
    ]))
    story.append(qa(36, "Tight deadline 100 tests / 2 hours?", [
        "Risk-based smoke first, parallelize, communicate residual risk, document untested areas, never claim unrun tests passed.",
    ]))
    story.append(qa(37, "Why automation / why this company?", [
        "Quality at speed; continuous feedback. Company research: product, stack, testing challenges you want to help solve.",
    ]))

    story.append(PageBreak())

    # SECTION 7 Framework
    story.append(P("SECTION 7: FRAMEWORK ARCHITECTURE (YOUR PORTFOLIO)", "DH1"))
    story.append(hline())
    story.append(P(
        "Speak about the ParaBank Selenium-Java framework on GitHub. Show code; don’t invent tools you didn’t build.",
        "DBody"
    ))

    story.append(qa(38, "Walk me through your framework (5–7 min script).", [
        "1) Context: ParaBank banking UI automation, Java 21, Selenium 4, TestNG, Maven. "
        "2) Layers: base (BaseTest ThreadLocal driver, BasePage waits), pages (POM), tests (asserts), "
        "utils (ConfigReader classpath, ExcelReader, UserFactory, ExtentManager), listeners (Extent+screenshot, Retry). "
        "3) Suites: smoke/account/transaction/data-driven/E2E via testng.xml. "
        "4) Data: Excel Execute flag + unique users. "
        "5) CI: GitHub Actions headless, artifacts, reports/ci/run-N. "
        "6) Results: ~50 pass / intentional skips for known demo auth-bypass. "
        "7) Close: happy to deep-dive any layer.",
    ]))
    story.append(qa(39, "How is test data handled?", [
        "config.properties for env; Excel for scenarios; UserFactory for unique runtime users; "
        "no hard dependency on shared static demo accounts under parallel.",
    ]))
    story.append(qa(40, "Parallel safety?", [
        "ThreadLocal&lt;WebDriver&gt;, getDriver(), quit+remove, unique data, no static mutable page state.",
    ]))
    story.append(qa(41, "Reporting?", [
        "Extent HTML + screenshots on fail; Surefire/TestNG HTML; Allure in CI; per-run folders not overwritten.",
    ]))
    story.append(qa(42, "Public demo limitations?", [
        "Auth bypass, throttling, shared DB. Document in KNOWN_ISSUES; SkipException for impossible negatives; "
        "don’t INIT public DB by default.",
    ]))
    story.append(qa(43, "Improvements if more time?", [
        "Deeper Log4j usage, visual regression, more negative/boundary cases, private test env, "
        "optional API data setup, smoke-only PR pipeline vs full nightly.",
        tip("Never say the framework is perfect — show growth mindset."),
    ]))

    # SECTION 8 Tricky
    story.append(P("SECTION 8: TRICKY / SCENARIO QUESTIONS", "DH1"))
    story.append(hline())
    story.append(qa(44, "100 tests, 2 hours to release?", [
        "Smoke critical paths; parallel; stakeholder risk talk; document untested; plan hotfix readiness. Never fake green.",
    ]))
    story.append(qa(45, "Passes local, fails CI?", [
        "Env/browser/headless/timing/paths/Linux flags/logs/screenshots. Reproduce headless locally.",
    ]))
    story.append(qa(46, "Automation finds bug, manual can’t repro?", [
        "Share exact data/env/build, screenshots, HAR/logs; pair with manual/dev; check race conditions and timing.",
    ]))
    story.append(qa(47, "What to automate vs manual?", [
        "Automate stable, frequent, data-driven, high-value regression. Manual for exploratory, UX, CAPTCHA/OTP UX, "
        "rapidly changing UI. ROI-driven 80/20.",
    ]))
    story.append(qa(48, "False green test?", [
        "Weak assert (URL only) + env accepting any login. Strengthen asserts (identity, account data); fix env or skip known defect honestly.",
    ]))
    story.append(qa(49, "Shared user under parallel messes balances?", [
        "Design flaw: unique users per thread; never share mutable financial data across parallel tests.",
    ]))
    story.append(qa(50, "Empty Extent report?", [
        "flush() not called; listener not registered; onTestStart never created node.",
    ]))

    story.append(PageBreak())

    # APPENDIX
    story.append(P("APPENDIX: PRESENT YOUR PORTFOLIO", "DH1"))
    story.append(hline())
    story.append(P("Before interview", "DH2"))
    story.append(P(
        "Open GitHub profile + repo; clone IDE ready; know how to run mvn clean test; "
        "have Extent/CI Actions tab ready; practice 5–7 min walkthrough timed.",
        "DBody"
    ))
    story.append(P("5–7 minute walkthrough order", "DH2"))
    for line in [
        "1. GitHub README + CI badge (30s)",
        "2. Folder structure: base → pages → tests → utils → listeners",
        "3. Open LoginPage + LoginTest (locators vs asserts)",
        "4. ConfigReader + Excel DataProvider + Execute flag",
        "5. BaseTest ThreadLocal setUp/tearDown",
        "6. testng.xml suites/groups/listeners",
        "7. GitHub Actions + reports/ci/run-N",
        "8. One real failure story (wait/outcome or auth-bypass)",
        "9. Invite deep-dive questions",
    ]:
        story.append(P(line, "TOC"))

    story.append(P("Emphasize", "DH2"))
    story.append(P(
        "Built/owned architecture · industry practices · CI-ready · maintainable · honest about demo-site limits.",
        "DBody"
    ))
    story.append(P("Avoid", "DH2"))
    story.append(P(
        "Theory only; “I followed a tutorial”; claiming tools you can’t demo; 20-minute monologue; messy TODOs.",
        "DBody"
    ))

    story.append(P("Final interview tips", "DH1"))
    story.append(hline())
    story.append(P(
        "Research company; map JD to your framework; STAR for behavioral; pause before answering; "
        "if unknown: “I haven’t used X yet; closest is Y; I’d learn by…”; ask smart questions about their stack/challenges.",
        "DBody"
    ))
    story.append(P(
        "Questions to ask them: automation stack? biggest quality risks? QA–dev collaboration? success in 6 months? growth path?",
        "DBody"
    ))
    story.append(Spacer(1, 8))
    story.append(hline())
    story.append(P(
        "<b>Remember:</b> Confidence comes from preparation. Your framework is proof of skill — show it, don’t only talk about it.",
        "DTip"
    ))
    story.append(P("END OF COMPLETE INTERVIEW Q&amp;A GUIDE — verified &amp; updated.", "DBody"))

    doc = SimpleDocTemplate(
        str(OUT), pagesize=A4,
        leftMargin=28, rightMargin=28, topMargin=24, bottomMargin=22,
        title="Complete Interview Q&A Guide",
        author="QA Automation Interview Prep",
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print("Updated:", OUT, "bytes=", OUT.stat().st_size)


if __name__ == "__main__":
    build()
