"""Rebuild Selenium Waits Interview Q&A PDF with accuracy polish."""
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
    r"\CLAUDE AI NOTES\Week 2 Selenium Core Concepts"
    r"\Waits (Implicit, Explicit, Fluent"
    r"\Week2_Selenium_Waits_Interview_QA.pdf"
)

NAVY = HexColor("#0b3d5c")
TEAL = HexColor("#0f766e")
GREEN = HexColor("#166534")
LIGHT = HexColor("#f0f9ff")
SOFT = HexColor("#e2e8f0")
DARK = HexColor("#1e293b")
MUTED = HexColor("#475569")
GOLD = HexColor("#b45309")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TMain", fontName="Helvetica-Bold", fontSize=15,
                          leading=19, textColor=white, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="TSub", fontName="Helvetica", fontSize=9,
                          leading=12, textColor=HexColor("#dbeafe"), alignment=TA_CENTER))
styles.add(ParagraphStyle(name="DH1", fontName="Helvetica-Bold", fontSize=11,
                          leading=13, textColor=NAVY, spaceBefore=7, spaceAfter=3))
styles.add(ParagraphStyle(name="DH2", fontName="Helvetica-Bold", fontSize=9.3,
                          leading=11.5, textColor=TEAL, spaceBefore=5, spaceAfter=2))
styles.add(ParagraphStyle(name="DQ", fontName="Helvetica-Bold", fontSize=8.6,
                          leading=11, textColor=NAVY, spaceBefore=4, spaceAfter=1))
styles.add(ParagraphStyle(name="DA", fontName="Helvetica", fontSize=8.2,
                          leading=10.4, textColor=DARK, alignment=TA_JUSTIFY, spaceAfter=2))
styles.add(ParagraphStyle(name="DTip", fontName="Helvetica-Oblique", fontSize=7.5,
                          leading=9.5, textColor=GOLD, leftIndent=4, spaceAfter=2))
styles.add(ParagraphStyle(name="DFix", fontName="Helvetica-Oblique", fontSize=7.4,
                          leading=9.4, textColor=GREEN, spaceAfter=3))
styles.add(ParagraphStyle(name="DBody", fontName="Helvetica", fontSize=8.4,
                          leading=10.5, textColor=DARK, spaceAfter=3))
styles.add(ParagraphStyle(name="CodeB", fontName="Courier", fontSize=6.6,
                          leading=8.5, textColor=DARK, backColor=LIGHT, spaceBefore=1, spaceAfter=2))
styles.add(ParagraphStyle(name="DCell", fontName="Helvetica", fontSize=7.1,
                          leading=9, textColor=DARK))
styles.add(ParagraphStyle(name="DHead", fontName="Helvetica-Bold", fontSize=7.1,
                          leading=9, textColor=white))


def P(t, s="DA"):
    return Paragraph(t, styles[s])


def code(t):
    return Preformatted(t.rstrip(), styles["CodeB"])


def tip(t):
    return P(f"<b>Interview Tip:</b> {t}", "DTip")


def hline():
    return HRFlowable(width="100%", thickness=0.4, color=SOFT, spaceBefore=1, spaceAfter=3)


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
        canvas.rect(0, A4[1] - 13, A4[0], 13, fill=1, stroke=0)
        canvas.setFillColor(white)
        canvas.setFont("Helvetica", 6.8)
        canvas.drawString(28, A4[1] - 9, "Selenium Waits | Interview Q&A")
        canvas.drawRightString(A4[0] - 28, A4[1] - 9, "Week 2 · SDET")
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 6.8)
        canvas.drawCentredString(A4[0] / 2, 11, f"Page {page}")
    canvas.restoreState()


def build():
    story = []

    cover = Table([
        [P("Selenium Waits", "TMain")],
        [P("Interview Questions &amp; Answers<br/>"
           "Implicit · Explicit · Fluent · ExpectedConditions<br/>"
           "Week 2 — Selenium Core Concepts | QA Automation Study Plan", "TSub")],
    ], colWidths=[6.7 * inch])
    cover.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("TOPPADDING", (0, 0), (-1, -1), 22),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
    ]))
    story.append(Spacer(1, 36))
    story.append(cover)
    story.append(Spacer(1, 10))
    story.append(P(
        "Verified for Selenium 4 (Duration API). Original structure kept; a few absolute statements "
        "softened so you don’t fail a picky interviewer.",
        "DBody"
    ))
    story.append(P(
        "Polish: WebDriverWait extends FluentWait; mix implicit+explicit = unpredictable (not fixed formula); "
        "implicit returns early if found; Thread.sleep anti-pattern; banking Fluent examples.",
        "DFix"
    ))
    story.append(PageBreak())

    story.append(P("Basic / Conceptual", "DH1"))
    story.append(hline())

    story.append(qa(1, "What are Selenium waits and why needed?", [
        "Mechanisms that pause until a condition is true or timeout. Modern apps load via AJAX/JS — "
        "without waits you get NoSuchElementException / ElementNotInteractableException and flaky tests.",
        tip("Lead with: asynchronous UI + flaky tests without synchronization."),
    ]))

    story.append(qa(2, "Three types of waits?", [
        "1) <b>Implicit</b> — global timeout for findElement/findElements polling.  "
        "2) <b>Explicit (WebDriverWait + ExpectedConditions)</b> — condition on a specific element/state.  "
        "3) <b>FluentWait</b> — configurable timeout, polling, ignored exceptions, custom conditions.",
        "Also know: <b>Thread.sleep</b> is a hard wait (not a Selenium wait) — avoid as primary strategy. "
        "Related driver timeouts: pageLoadTimeout, scriptTimeout.",
        tip("Be ready to code any of the three on a whiteboard."),
    ]))

    story.append(qa(3, "What is Implicit Wait? Limitations?", [
        code("driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10));"),
        "When finding elements, WebDriver polls until found or timeout. If found quickly, it returns immediately "
        "(it does <b>not</b> always sleep the full 10s).",
        "Limitations: global only; only helps “element present in DOM”; slows “element should NOT exist” checks "
        "(waits until timeout); mixes poorly with explicit waits → hard-to-predict total wait behaviour.",
        tip("Saying “never mix with explicit” is a common interview answer — phrase it as best practice."),
    ]))

    story.append(qa(4, "What is Explicit Wait? Why better?", [
        code("WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));\n"
             "wait.until(ExpectedConditions.elementToBeClickable(By.id(\"btn\")));"),
        "Condition-based, per use-case, many ExpectedConditions, returns as soon as condition is met. "
        "Recommended default for modern frameworks.",
        "Note: <b>WebDriverWait extends FluentWait</b> with sensible defaults (often 500ms polling).",
    ]))

    story.append(qa(5, "What is Fluent Wait? When over plain WebDriverWait?", [
        "Use FluentWait API when you need custom polling interval, ignored exceptions, or a custom lambda "
        "condition not covered cleanly by ExpectedConditions.",
        code("Wait<WebDriver> wait = new FluentWait<>(driver)\n"
             "  .withTimeout(Duration.ofSeconds(60))\n"
             "  .pollingEvery(Duration.ofSeconds(2))\n"
             "  .ignoring(NoSuchElementException.class)\n"
             "  .ignoring(StaleElementReferenceException.class);\n"
             "WebElement el = wait.until(d -> d.findElement(By.id(\"result\")));"),
        tip("Examples: OTP field, slow statement generation, intermittent loaders."),
    ]))

    story.append(P("Intermediate", "DH1"))
    story.append(hline())

    story.append(qa(6, "Why avoid mixing Implicit and Explicit waits?", [
        "Combined behaviour is version/driver dependent and hard to reason about — tests can wait longer "
        "than expected or become flaky/hard to debug.",
        "Rule of thumb in frameworks: prefer <b>explicit waits only</b>; set implicit to <b>0</b> (or a tiny value). "
        "Don’t quote a fixed “10 + 5 = 15s” formula as absolute fact.",
        tip("Common trap question — nuanced answer beats oversimplification."),
    ]))

    story.append(qa(7, "visibilityOfElementLocated vs presenceOfElementLocated?", [
        "<b>presence</b> — in DOM (may be hidden). <b>visibility</b> — in DOM and displayed (size &gt; 0). "
        "Interact / getText → prefer visibility or elementToBeClickable.",
    ]))

    story.append(qa(8, "the-internet dynamic_loading /1 vs /2?", [
        "/1: #finish already in DOM but display:none → revealed after Start.  "
        "/2: #finish not in DOM → created after Start.  "
        "visibilityOfElementLocated works for both before reading text.",
        tip("Shows you understand CSS hide vs DOM inject."),
    ]))

    story.append(qa(9, "FluentWait lambda return rules?", [
        "For Function&lt;WebDriver, T&gt;: return non-null T → success; return null → keep polling. "
        "For Boolean conditions: true = success, false = continue. "
        "TimeoutException if still not met at timeout.",
        code("wait.until(d -> {\n"
             "  WebElement el = d.findElement(By.id(\"finish\"));\n"
             "  return el.isDisplayed() ? el : null;\n"
             "});"),
    ]))

    story.append(qa(10, "Wait for loading spinner to disappear?", [
        code("wait.until(ExpectedConditions.invisibilityOfElementLocated(By.id(\"loading\")));\n"
             "wait.until(ExpectedConditions.visibilityOfElementLocated(By.id(\"result\")));"),
        "Spinner-first then content-second is a professional pattern.",
    ]))

    story.append(P("Scenario-based", "DH1"))
    story.append(hline())

    story.append(qa(11, "TimeoutException but element is on screen — checklist?", [
        "1) Implicit+explicit mix  2) Wrong locator  3) Overlay/spinner  4) Wrong condition "
        "(presence vs visibility)  5) iframe/window context  6) Temporarily raise timeout to confirm timing.",
    ]))

    story.append(qa(12, "Element appears only sometimes / very slow?", [
        "FluentWait long timeout, slower poll, ignore NoSuchElement/Stale; optional custom message "
        "withMessage(\"OTP field not ready\").",
    ]))

    story.append(qa(13, "Why is Thread.sleep() bad?", [
        "Always waits full time; still fails if longer; multiplies suite time; hides real sync bugs; "
        "CI machines differ. Prefer explicit/fluent waits.",
    ]))

    story.append(qa(14, "Banking examples for Fluent Wait?", [
        "OTP field after SMS, transfer confirmation, statement PDF ready link, KYC status change, "
        "balance refresh after payment — unpredictable server latency.",
    ]))

    story.append(qa(15, "pageLoadTimeout vs waits?", [
        "pageLoadTimeout limits how long get()/navigation may take for document load. "
        "It does not wait for AJAX widgets after load — that’s still explicit wait territory.",
    ]))

    story.append(PageBreak())

    story.append(P("Quick revision cheatsheet", "DH1"))
    story.append(hline())
    rows = [
        ["Wait", "Scope", "Condition", "Polling", "Ignore exc.", "Use when"],
        ["Implicit", "Driver global", "Element present", "Driver poll", "No", "Legacy/simple only"],
        ["WebDriverWait", "Per call", "ExpectedConditions", "~500ms default", "Limited", "Default choice"],
        ["FluentWait", "Per call", "Custom lambda", "You set", "Yes", "Slow/custom/stale-prone"],
        ["Thread.sleep", "Thread", "None", "N/A", "N/A", "Avoid as strategy"],
    ]
    data = []
    for i, r in enumerate(rows):
        st = styles["DHead"] if i == 0 else styles["DCell"]
        data.append([Paragraph(c, st) for c in r])
    t = Table(data, colWidths=[1.05*inch, 0.85*inch, 1.25*inch, 0.95*inch, 0.85*inch, 1.15*inch], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT]),
        ("GRID", (0, 0), (-1, -1), 0.3, SOFT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(t)

    story.append(Spacer(1, 8))
    story.append(P("Practice — Explicit Wait (dynamic_loading/1)", "DH1"))
    story.append(hline())
    story.append(P(
        "Element exists from start but display:none. Start → spinner → Hello World!",
        "DBody"
    ))
    story.append(code(
        "WebDriver driver = new ChromeDriver();\n"
        "WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(15));\n"
        "driver.get(\"https://the-internet.herokuapp.com/dynamic_loading/1\");\n"
        "wait.until(ExpectedConditions.elementToBeClickable(\n"
        "    By.cssSelector(\"#start button\"))).click();\n"
        "wait.until(ExpectedConditions.invisibilityOfElementLocated(By.id(\"loading\")));\n"
        "WebElement result = wait.until(\n"
        "    ExpectedConditions.visibilityOfElementLocated(By.id(\"finish\")));\n"
        "Assert.assertEquals(result.getText().trim(), \"Hello World!\");\n"
        "driver.quit();"
    ))

    story.append(P("Practice — Fluent Wait (custom poll + lambda)", "DH1"))
    story.append(hline())
    story.append(code(
        "Wait<WebDriver> fluent = new FluentWait<>(driver)\n"
        "  .withTimeout(Duration.ofSeconds(20))\n"
        "  .pollingEvery(Duration.ofSeconds(1))\n"
        "  .ignoring(NoSuchElementException.class);\n"
        "driver.get(\"https://the-internet.herokuapp.com/dynamic_loading/1\");\n"
        "fluent.until(d -> d.findElement(By.cssSelector(\"#start button\"))).click();\n"
        "WebElement result = fluent.until(d -> {\n"
        "  WebElement el = d.findElement(By.id(\"finish\"));\n"
        "  return el.isDisplayed() ? el : null;  // null = keep polling\n"
        "});\n"
        "Assert.assertEquals(result.getText().trim(), \"Hello World!\");"
    ))

    story.append(Spacer(1, 6))
    story.append(P("Key differences", "DH2"))
    diff = [
        ["Aspect", "WebDriverWait (Explicit)", "FluentWait"],
        ["Condition", "ExpectedConditions helpers", "Custom lambda / Function"],
        ["Polling", "Default ~500ms", "You choose"],
        ["Ignore exceptions", "Limited defaults", "ignoring(...)"],
        ["Stop rule", "Built into EC", "non-null / true"],
        ["Best for", "Standard UI waits", "Slow / custom / stale-prone"],
    ]
    data = []
    for i, r in enumerate(diff):
        st = styles["DHead"] if i == 0 else styles["DCell"]
        data.append([Paragraph(c, st) for c in r])
    t2 = Table(data, colWidths=[1.2*inch, 2.5*inch, 2.5*inch], repeatRows=1)
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT]),
        ("GRID", (0, 0), (-1, -1), 0.3, SOFT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(t2)

    story.append(Spacer(1, 8))
    story.append(hline())
    story.append(P(
        "End of Selenium Waits Interview Q&amp;A — verified for Selenium 4 (Duration API).",
        "DBody"
    ))

    doc = SimpleDocTemplate(
        str(OUT), pagesize=A4,
        leftMargin=30, rightMargin=30, topMargin=26, bottomMargin=24,
        title="Selenium Waits Interview Q&A",
        author="SDET Week 2",
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print("Updated:", OUT, "bytes=", OUT.stat().st_size)


if __name__ == "__main__":
    build()
