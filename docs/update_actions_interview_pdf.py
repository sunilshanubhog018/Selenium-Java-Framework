"""Rebuild Actions Class Interview Q&A PDF with accuracy fixes."""
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
    r"\Actions class (hover, drag-drop)\Actions_Class_InterviewQA.pdf"
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
styles.add(ParagraphStyle(name="TMain", fontName="Helvetica-Bold", fontSize=16,
                          leading=20, textColor=white, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="TSub", fontName="Helvetica", fontSize=9.5,
                          leading=12, textColor=HexColor("#dbeafe"), alignment=TA_CENTER))
styles.add(ParagraphStyle(name="DH1", fontName="Helvetica-Bold", fontSize=11.5,
                          leading=14, textColor=NAVY, spaceBefore=8, spaceAfter=4))
styles.add(ParagraphStyle(name="DH2", fontName="Helvetica-Bold", fontSize=10,
                          leading=12, textColor=TEAL, spaceBefore=6, spaceAfter=3))
styles.add(ParagraphStyle(name="DQ", fontName="Helvetica-Bold", fontSize=9,
                          leading=11.5, textColor=NAVY, spaceBefore=5, spaceAfter=1))
styles.add(ParagraphStyle(name="DA", fontName="Helvetica", fontSize=8.5,
                          leading=11, textColor=DARK, alignment=TA_JUSTIFY, spaceAfter=2))
styles.add(ParagraphStyle(name="DTip", fontName="Helvetica-Oblique", fontSize=8,
                          leading=10, textColor=GOLD, leftIndent=5, spaceBefore=1, spaceAfter=3))
styles.add(ParagraphStyle(name="DFix", fontName="Helvetica-Oblique", fontSize=7.8,
                          leading=10, textColor=GREEN, spaceAfter=4))
styles.add(ParagraphStyle(name="DBody", fontName="Helvetica", fontSize=8.8,
                          leading=11, textColor=DARK, spaceAfter=3))
styles.add(ParagraphStyle(name="CodeB", fontName="Courier", fontSize=6.9,
                          leading=9, textColor=DARK, backColor=LIGHT, spaceBefore=1, spaceAfter=2))
styles.add(ParagraphStyle(name="DCell", fontName="Helvetica", fontSize=7.5,
                          leading=9.5, textColor=DARK))
styles.add(ParagraphStyle(name="DHead", fontName="Helvetica-Bold", fontSize=7.5,
                          leading=9.5, textColor=white))
styles.add(ParagraphStyle(name="LvlBlue", fontName="Helvetica-Bold", fontSize=8,
                          textColor=HexColor("#1d4ed8"), spaceAfter=2))
styles.add(ParagraphStyle(name="LvlRed", fontName="Helvetica-Bold", fontSize=8,
                          textColor=RED, spaceAfter=2))
styles.add(ParagraphStyle(name="LvlGreen", fontName="Helvetica-Bold", fontSize=8,
                          textColor=GREEN, spaceAfter=2))


def P(t, s="DA"):
    return Paragraph(t, styles[s])


def code(t):
    return Preformatted(t.rstrip(), styles["CodeB"])


def tip(t):
    return P(f"<b>Interview Tip:</b> {t}", "DTip")


def hline():
    return HRFlowable(width="100%", thickness=0.45, color=SOFT, spaceBefore=2, spaceAfter=4)


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
        canvas.rect(0, A4[1] - 14, A4[0], 14, fill=1, stroke=0)
        canvas.setFillColor(white)
        canvas.setFont("Helvetica", 7)
        canvas.drawString(30, A4[1] - 10, "Actions Class Interview Q&A | Hover · Drag-Drop · Keyboard")
        canvas.drawRightString(A4[0] - 30, A4[1] - 10, "Week 2 · SDET")
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 7)
        canvas.drawCentredString(A4[0] / 2, 12, f"Page {page}")
    canvas.restoreState()


def build():
    story = []

    cover = Table([
        [P("Actions Class (Hover, Drag-Drop)", "TMain")],
        [P("Interview Questions &amp; Answers<br/>"
           "Week 2 | Selenium Java Automation | SDET Study Plan<br/><br/>"
           "PART 1 Fundamentals &nbsp;·&nbsp; PART 2 Senior/Framework &nbsp;·&nbsp; PART 3 Practice Tests",
           "TSub")],
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
        "Verified for Selenium 4. Content kept from your original guide; accuracy fixes applied "
        "where interview answers could mislead.",
        "DBody"
    ))
    story.append(P(
        "Fixes: perform()/chain reuse wording; HTML5 DnD practice test (no double-swap); "
        "Ctrl vs Command; custom context menus; pause API; headless hover caveats.",
        "DFix"
    ))
    story.append(PageBreak())

    # ========== PART 1 ==========
    story.append(P("PART 1 — FUNDAMENTALS", "DH1"))
    story.append(P("Blue Level | All experience levels", "LvlBlue"))
    story.append(hline())

    story.append(P("Basics &amp; Core Concepts", "DH2"))
    story.append(qa(1, "What is the Actions class? When use it instead of WebElement methods?", [
        "Actions (org.openqa.selenium.interactions.Actions) builds complex user gestures: hover, "
        "double-click, right-click, drag-and-drop, key chords, scroll. WebElement click()/sendKeys() "
        "cover simple interactions; composite mouse/keyboard sequences need Actions (or JS fallback).",
    ]))
    story.append(qa(2, "How do you create an Actions object?", [
        code("Actions actions = new Actions(driver);  // driver is required"),
    ]))
    story.append(qa(3, "Explain the Builder Pattern / method chaining in Actions.", [
        "Each Actions method returns the same builder so you can chain. Actions are queued until "
        "you execute with perform().",
        code('actions.moveToElement(el).click().sendKeys("text").perform();'),
    ]))
    story.append(qa(4, "Difference between build() and perform()?", [
        "<b>perform()</b> builds (if needed) and runs the sequence — use this almost always. "
        "In Selenium 4, perform() is enough; you do not have to call build() first.",
        "<b>build()</b> returns an Action (singular) without running it — useful only if you want to "
        "store/reuse a compiled sequence and call action.perform() later.",
        "Actions (plural) = builder; Action (singular) = built sequence interface.",
    ]))
    story.append(qa(5, "What if you forget .perform()?", [
        "No exception. The chain is never sent to the browser — silent no-op. #1 beginner mistake.",
    ]))

    story.append(P("Mouse Actions", "DH2"))
    story.append(qa(6, "How do you perform hover (mouseover)?", [
        code("actions.moveToElement(element).perform();"),
        "Moves pointer to element center; triggers CSS :hover / JS mouseover. Common for mega-menus.",
    ]))
    story.append(qa(7, "Multi-level nested hover menus?", [
        "Hover parent → explicit wait for child visible → hover child → wait → click leaf. "
        "Without waits, submenus are not in DOM yet → NoSuchElementException / flaky failures.",
    ]))
    story.append(qa(8, "moveToElement(element, xOffset, yOffset)?", [
        "Moves relative to element origin/center offset in pixels. Use for sliders, canvas, partial hit-areas.",
    ]))
    story.append(qa(9, "Double-click?", [
        code("actions.doubleClick(element).perform();"),
        "Example: enter edit mode on a table cell / remarks field.",
    ]))
    story.append(qa(10, "Right-click (context click)?", [
        code("actions.contextClick(element).perform();"),
        "Then interact with custom menu items via normal findElement/click (not always native OS menu).",
    ]))
    story.append(qa(11, "clickAndHold() and release()?", [
        "clickAndHold presses mouse button down; release releases it. Manual DnD: "
        "clickAndHold(src) → moveToElement(tgt) → release().perform().",
    ]))

    story.append(P("Drag and Drop", "DH2"))
    story.append(qa(12, "Three approaches for drag-and-drop?", [
        "1) dragAndDrop(source, target)  2) dragAndDropBy(source, x, y)  "
        "3) Manual clickAndHold → moveToElement → release (often most reliable of the three).",
    ]))
    story.append(qa(13, "Why does dragAndDrop() fail on modern apps?", [
        "Many UIs use HTML5 DnD events (dragstart, dragover, drop, dragend). Selenium’s high-level "
        "dragAndDrop does not always fire them. Use manual sequence or JS DataTransfer simulation.",
        tip("the-internet.herokuapp.com/drag_and_drop is a classic HTML5 case where Actions often fails."),
    ]))
    story.append(qa(14, "When use dragAndDropBy()?", [
        "No target element — e.g. slider thumb by N pixels: dragAndDropBy(handle, 100, 0).",
    ]))

    story.append(P("Keyboard Actions", "DH2"))
    story.append(qa(15, "Simulate Ctrl+A (Select All)?", [
        code("actions.keyDown(Keys.CONTROL).sendKeys(\"a\").keyUp(Keys.CONTROL).perform();"),
        "Always pair keyDown with keyUp. On macOS use Keys.COMMAND (or Keys.META) instead of CONTROL "
        "for real user-equivalent shortcuts.",
    ]))
    story.append(qa(16, "Forget keyUp() after keyDown()?", [
        "Modifier may stay “stuck” for later interactions in that session → hard-to-debug Ctrl+click side effects. "
        "Always keyUp in the same chain (or try/finally style cleanup if you split steps).",
    ]))
    story.append(qa(17, "Actions.sendKeys() vs WebElement.sendKeys()?", [
        "WebElement.sendKeys types into that element. Actions.sendKeys without element goes to active "
        "element; Actions.sendKeys(element, keys) focuses then types and can chain with other gestures.",
    ]))
    story.append(qa(18, "Tab through form fields?", [
        code('actions.sendKeys(Keys.TAB).sendKeys("value1")\n'
             '       .sendKeys(Keys.TAB).sendKeys("value2").perform();'),
        "Useful for accessibility / tab-order checks.",
    ]))

    story.append(PageBreak())

    # ========== PART 2 ==========
    story.append(P("PART 2 — SENIOR / FRAMEWORK LEVEL", "DH1"))
    story.append(P("Red Level | 4+ years | Framework · Edge cases · Banking · Behavioral", "LvlRed"))
    story.append(hline())

    story.append(P("Framework Design", "DH2"))
    story.append(qa(19, "Reusable Actions utility in a framework?", [
        "Wrap patterns: hoverAndClick(parent, childBy) with waits; safeDragAndDrop (manual + JS fallback); "
        "doubleClickAndType; shortcut(modifier, key). Construct with WebDriver from ThreadLocal. "
        "Keep raw Actions out of test classes.",
    ]))
    story.append(qa(20, "Flaky hover in CI headless Chrome?", [
        "1) Explicit wait after hover  2) pause(Duration) for CSS transitions (Selenium 4)  "
        "3) Ensure real viewport size in headless  4) JS MouseEvent('mouseover', {bubbles:true}) fallback  "
        "5) Prefer redesign to click-accessible menus when product allows.",
    ]))
    story.append(qa(21, "Actions + parallel execution?", [
        "Actions is bound to one WebDriver. Safe if each thread has its own driver (ThreadLocal). "
        "Create Actions per method/page — never share one Actions instance across threads.",
    ]))
    story.append(qa(22, "All DnD approaches fail — escalation?", [
        "Manual sequence → intermediate moves + pause → JS HTML5 DataTransfer events → framework-specific "
        "event hooks → Robot (last resort, not headless-friendly).",
    ]))

    story.append(P("Edge Cases", "DH2"))
    story.append(qa(23, "Tooltip verification with Actions?", [
        "moveToElement → wait visible → assert text. Tooltips may be title attribute, portal div, or animated "
        "component. Banking: also assert masking of account numbers.",
    ]))
    story.append(qa(24, "MoveTargetOutOfBoundsException?", [
        "Target outside viewport. Scroll first: actions.scrollToElement(el).perform() (Selenium 4) or "
        "JS scrollIntoView, then move/hover.",
    ]))
    story.append(qa(25, "Slider / EMI calculator accurately?", [
        "Compute offset from track width × percent; dragAndDropBy or clickAndHold+moveByOffset; assert displayed value. "
        "Also try Keys.ARROW_RIGHT for step precision. Test min/max/step boundaries.",
    ]))
    story.append(qa(26, "Context menu option disabled?", [
        "After contextClick, check isEnabled(), aria-disabled, disabled class/CSS. Note: custom HTML menus "
        "may ignore isEnabled() — prefer aria/class checks. Banking example: Delete disabled for settled txn.",
    ]))

    story.append(P("Banking Domain", "DH2"))
    story.append(qa(27, "Fund transfer with hover menus + tab + OTP?", [
        "Hover Payments → wait → Fund Transfer; TAB through fields; proceed; OTP handler. "
        "Helpers: NavigationHelper, FormHelper, OTPHandler. Retry only hover/nav flakiness, not business asserts.",
    ]))
    story.append(qa(28, "Drag-drop reorder dashboard widgets?", [
        "Capture order → manual DnD → assert new order → refresh persistence check → edge cases "
        "(same position, first-to-last, invalid zone). CI: small pause after clickAndHold.",
    ]))

    story.append(P("Behavioral", "DH2"))
    story.append(qa(29, "Flaky test caused by Actions (STAR)?", [
        "Situation: hover nav flaky in CI only. Task: stabilize. Action: waits + ActionUtils retry + JS mouseover "
        "fallback + larger headless window. Result: reliability ~70% → ~99%.",
    ]))
    story.append(qa(30, "Actions vs JavascriptExecutor decision?", [
        "Default = Actions (real user-ish events). JS when Actions cannot trigger framework/HTML5 handlers "
        "or unsupported gestures. Document JS workarounds as tech debt.",
    ]))

    story.append(P("Rapid Fire", "DH2"))
    rf = [
        ["31", "Package?", "org.openqa.selenium.interactions.Actions"],
        ["32", "Actions vs Action?", "Builder class vs built Action interface"],
        ["33", "Default move target?", "Element center"],
        ["34", "After perform()?", "That sequence is done; start a new chain for next gestures "
         "(same Actions object can be reused for a new sequence)"],
        ["35", "Multiple perform()?", "Yes — separate sequences each ending with perform() "
         "(not one infinite chain without perform)"],
        ["36", "Selenium 4 scroll?", "actions.scrollToElement(el).perform()"],
        ["37", "Pause in chain?", "actions.pause(Duration.ofMillis(500)) — Selenium 4+"],
        ["38", "Headless hover fallback?", "JS dispatchEvent MouseEvent mouseover"],
        ["39", "RemoteWebDriver?", "Yes — W3C WebDriver actions endpoint"],
        ["40", "release without hold?", "Typically no-op / no useful effect"],
    ]
    data = [[Paragraph(c, styles["DHead"]) for c in ["#", "Q", "A"]]]
    for r in rf:
        data.append([Paragraph(c, styles["DCell"]) for c in r])
    t = Table(data, colWidths=[0.35 * inch, 1.5 * inch, 4.7 * inch], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT]),
        ("GRID", (0, 0), (-1, -1), 0.3, SOFT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(t)

    story.append(PageBreak())

    # ========== PART 3 ==========
    story.append(P("PART 3 — PRACTICE TESTS", "DH1"))
    story.append(P("Green Level | 5 scenarios | the-internet.herokuapp.com", "LvlGreen"))
    story.append(hline())

    story.append(P("Test 1: Hover and click profile (hovers)", "DH2"))
    story.append(code(
        "driver.get(\"https://the-internet.herokuapp.com/hovers\");\n"
        "WebElement figure = driver.findElements(By.cssSelector(\".figure\")).get(0);\n"
        "new Actions(driver).moveToElement(figure).perform();\n"
        "WebElement caption = new WebDriverWait(driver, Duration.ofSeconds(5)).until(\n"
        "  ExpectedConditions.visibilityOf(figure.findElement(By.cssSelector(\".figcaption\"))));\n"
        "Assert.assertTrue(caption.findElement(By.tagName(\"h5\")).getText().toLowerCase().contains(\"user\"));\n"
        "caption.findElement(By.tagName(\"a\")).click();\n"
        "Assert.assertTrue(driver.getCurrentUrl().contains(\"/users/\"));"
    ))
    story.append(P("Prefer findElements(\".figure\").get(0) over brittle nth-child selectors.", "DTip"))

    story.append(P("Test 2: Drag and drop (HTML5) — fixed fallback pattern", "DH2"))
    story.append(P(
        "Important fix: do <b>not</b> always run Actions then JS — that can double-swap columns. "
        "Try Actions first; only if assert fails, run JS HTML5 simulation once.",
        "DFix"
    ))
    story.append(code(
        "WebElement a = driver.findElement(By.id(\"column-a\"));\n"
        "WebElement b = driver.findElement(By.id(\"column-b\"));\n"
        "Assert.assertEquals(a.getText().trim(), \"A\");\n"
        "new Actions(driver).clickAndHold(a).moveToElement(b).release().perform();\n"
        "a = driver.findElement(By.id(\"column-a\"));\n"
        "if (!\"B\".equals(a.getText().trim())) {\n"
        "  // HTML5 fallback (run ONCE)\n"
        "  String js = \"var s=arguments[0],t=arguments[1],dt=new DataTransfer();\"\n"
        "    + \"s.dispatchEvent(new DragEvent('dragstart',{dataTransfer:dt}));\"\n"
        "    + \"t.dispatchEvent(new DragEvent('drop',{dataTransfer:dt}));\"\n"
        "    + \"s.dispatchEvent(new DragEvent('dragend',{dataTransfer:dt}));\";\n"
        "  ((JavascriptExecutor)driver).executeScript(js, a, b);\n"
        "  a = driver.findElement(By.id(\"column-a\"));\n"
        "}\n"
        "Assert.assertEquals(a.getText().trim(), \"B\");"
    ))

    story.append(P("Test 3: Context click → alert", "DH2"))
    story.append(code(
        "driver.get(\"https://the-internet.herokuapp.com/context_menu\");\n"
        "new Actions(driver).contextClick(driver.findElement(By.id(\"hot-spot\"))).perform();\n"
        "Alert alert = new WebDriverWait(driver, Duration.ofSeconds(5))\n"
        "  .until(ExpectedConditions.alertIsPresent());\n"
        "Assert.assertEquals(alert.getText(), \"You selected a context menu\");\n"
        "alert.accept();"
    ))

    story.append(P("Test 4: Slider (offset + keys)", "DH2"))
    story.append(code(
        "WebElement slider = driver.findElement(By.cssSelector(\"input[type='range']\"));\n"
        "WebElement output = driver.findElement(By.id(\"range\"));\n"
        "Assert.assertEquals(output.getText(), \"0\");\n"
        "new Actions(driver).clickAndHold(slider).moveByOffset(40, 0).release().perform();\n"
        "Assert.assertNotEquals(output.getText(), \"0\");\n"
        "slider.click();\n"
        "for (int i = 0; i < 10; i++) slider.sendKeys(Keys.ARROW_RIGHT);\n"
        "Assert.assertEquals(output.getText(), \"5\");"
    ))
    story.append(P("Pixel offsets vary by screen/DPI — prefer assert “changed” or keyboard steps for stability.", "DTip"))

    story.append(P("Test 5a: Keyboard detection (key_presses)", "DH2"))
    story.append(code(
        "driver.get(\"https://the-internet.herokuapp.com/key_presses\");\n"
        "WebElement input = driver.findElement(By.id(\"target\"));\n"
        "WebElement result = driver.findElement(By.id(\"result\"));\n"
        "Actions a = new Actions(driver);\n"
        "a.click(input).sendKeys(\"Hello\").perform();\n"
        "Assert.assertTrue(result.getText().contains(\"You entered\"));\n"
        "a.keyDown(Keys.CONTROL).sendKeys(\"a\").keyUp(Keys.CONTROL).perform();\n"
        "a.sendKeys(Keys.ENTER).perform();\n"
        "Assert.assertTrue(result.getText().contains(\"ENTER\"));"
    ))

    story.append(P("Test 5b: Double-click Add Element", "DH2"))
    story.append(code(
        "driver.get(\"https://the-internet.herokuapp.com/add_remove_elements/\");\n"
        "WebElement add = driver.findElement(By.xpath(\"//button[text()='Add Element']\"));\n"
        "new Actions(driver).doubleClick(add).perform();\n"
        "int n = driver.findElements(By.cssSelector(\".added-manually\")).size();\n"
        "// Some browsers fire 2 clicks; if flaky, assert n >= 1 or use two single clicks for product tests\n"
        "Assert.assertTrue(n >= 1);"
    ))
    story.append(P(
        "Note: double-click on a normal button is browser-dependent for “two submits”. "
        "Good for learning Actions API; for business tests prefer explicit two clicks if that’s the requirement.",
        "DTip"
    ))

    story.append(Spacer(1, 8))
    story.append(hline())
    story.append(P(
        "End of Actions Class Interview Q&amp;A — Week 2, SDET Study Plan (verified &amp; corrected).",
        "DBody"
    ))

    doc = SimpleDocTemplate(
        str(OUT), pagesize=A4,
        leftMargin=32, rightMargin=32, topMargin=28, bottomMargin=26,
        title="Actions Class Interview Q&A",
        author="SDET Study Plan Week 2",
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print("Updated:", OUT, "bytes=", OUT.stat().st_size)


if __name__ == "__main__":
    build()
