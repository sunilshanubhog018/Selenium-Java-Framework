"""Rebuild Dropdowns/Checkboxes/Radio Interview PDF with accuracy fixes."""
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
    r"\Dropdowns, checkboxes, radio buttons"
    r"\Dropdowns, checkboxes, radio buttons_Interview_QA_Tests.pdf"
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
                          leading=14, textColor=NAVY, spaceBefore=8, spaceAfter=4))
styles.add(ParagraphStyle(name="DH2", fontName="Helvetica-Bold", fontSize=9.5,
                          leading=12, textColor=TEAL, spaceBefore=6, spaceAfter=2))
styles.add(ParagraphStyle(name="DQ", fontName="Helvetica-Bold", fontSize=8.8,
                          leading=11, textColor=NAVY, spaceBefore=5, spaceAfter=1))
styles.add(ParagraphStyle(name="DA", fontName="Helvetica", fontSize=8.3,
                          leading=10.6, textColor=DARK, alignment=TA_JUSTIFY, spaceAfter=2))
styles.add(ParagraphStyle(name="DTip", fontName="Helvetica-Oblique", fontSize=7.7,
                          leading=9.8, textColor=GOLD, leftIndent=4, spaceAfter=2))
styles.add(ParagraphStyle(name="DFix", fontName="Helvetica-Oblique", fontSize=7.6,
                          leading=9.6, textColor=GREEN, spaceAfter=3))
styles.add(ParagraphStyle(name="DBody", fontName="Helvetica", fontSize=8.6,
                          leading=11, textColor=DARK, spaceAfter=3))
styles.add(ParagraphStyle(name="CodeB", fontName="Courier", fontSize=6.7,
                          leading=8.7, textColor=DARK, backColor=LIGHT, spaceBefore=1, spaceAfter=2))
styles.add(ParagraphStyle(name="DCell", fontName="Helvetica", fontSize=7.3,
                          leading=9.2, textColor=DARK))
styles.add(ParagraphStyle(name="DHead", fontName="Helvetica-Bold", fontSize=7.3,
                          leading=9.2, textColor=white))


def P(t, s="DA"):
    return Paragraph(t, styles[s])


def code(t):
    return Preformatted(t.rstrip(), styles["CodeB"])


def tip(t):
    return P(f"<b>Interview Tip:</b> {t}", "DTip")


def hline():
    return HRFlowable(width="100%", thickness=0.4, color=SOFT, spaceBefore=2, spaceAfter=4)


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
        canvas.setFont("Helvetica", 7)
        canvas.drawString(28, A4[1] - 9, "Dropdowns · Checkboxes · Radios | Interview Q&A")
        canvas.drawRightString(A4[0] - 28, A4[1] - 9, "Week 2 · SDET")
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 7)
        canvas.drawCentredString(A4[0] / 2, 11, f"Page {page}")
    canvas.restoreState()


def build():
    story = []

    cover = Table([
        [P("Dropdowns · Checkboxes · Radio Buttons", "TMain")],
        [P("Interview Q&amp;A + Practice Tests<br/>"
           "Native Select · Multi-select · Custom dropdowns · Forms<br/>"
           "Week 2 — Day 2 | SDET Prep | Selenium 4 + TestNG", "TSub")],
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
        "Verified guide. Original structure kept; answers tightened for Selenium 4 interviews "
        "and DemoQA practice-site realities.",
        "DBody"
    ))
    story.append(P(
        "Fixes: Select only for &lt;select&gt;; multi-select deselect rules; hidden inputs on modern UIs; "
        "custom dropdown 2-step + waits; DemoQA checkbox/radio click targets.",
        "DFix"
    ))
    story.append(PageBreak())

    # ========== Q&A ==========
    story.append(P("PART 1 — Interview Questions &amp; Answers", "DH1"))
    story.append(hline())

    story.append(qa(1, "What is the Select class and when do you use it?", [
        "org.openqa.selenium.support.ui.Select wraps native HTML <b>&lt;select&gt;</b> elements. "
        "Methods: selectByVisibleText / selectByValue / selectByIndex, getOptions, getFirstSelectedOption, "
        "isMultiple, deselect* (multi only).",
        "If the tag is not select (div/ul/li Bootstrap/React), Select throws "
        "<b>UnexpectedTagNameException</b> — use open-then-click for custom dropdowns.",
    ]))

    story.append(qa(2, "Three ways to select a native option?", [
        code('Select s = new Select(driver.findElement(By.id("country")));\n'
             's.selectByVisibleText("India"); // user-visible text\n'
             's.selectByValue("in");          // option value attribute\n'
             's.selectByIndex(0);             // 0-based index'),
        tip("Prefer visible text or value over index — indexes break when options reorder."),
    ]))

    story.append(qa(3, "How do you handle a multi-select dropdown?", [
        "Confirm with isMultiple() == true. Call selectBy* multiple times to add options. "
        "Read with getAllSelectedOptions(). Deselect with deselectByValue/Index/VisibleText or deselectAll().",
        "On a <b>single-select</b> dropdown, a new selectBy* replaces the previous choice. "
        "Calling deselect* on single-select throws <b>UnsupportedOperationException</b> "
        "(it does not silently ignore).",
    ]))

    story.append(qa(4, "Why check isSelected() before clicking a checkbox?", [
        "click() toggles. Clicking an already-checked box unchecks it. Guard for determinism:",
        code("if (!checkbox.isSelected()) {\n  checkbox.click();\n}\nAssert.assertTrue(checkbox.isSelected());"),
        "Many UIs hide the real &lt;input&gt; and style a span/label — click the visible label, "
        "but call isSelected() on the actual input element.",
    ]))

    story.append(qa(5, "isSelected() vs isEnabled() vs isDisplayed()?", [
        "<b>isSelected</b> — checked/ticked (checkbox/radio/option).  "
        "<b>isEnabled</b> — not disabled.  "
        "<b>isDisplayed</b> — visible (not display:none / detached from layout).",
        "Independent states: can be displayed+enabled but not selected.",
    ]))

    story.append(qa(6, "Radio buttons vs checkboxes in Selenium?", [
        "Radios: one selection per name group; selecting another auto-deselects previous — no deselect click. "
        "Checkboxes: independent, multi-select. Both use click + isSelected, but group behaviour differs.",
    ]))

    story.append(qa(7, "Select a radio from a group?", [
        code('List<WebElement> radios = driver.findElements(By.name("gender"));\n'
             'for (WebElement r : radios) {\n'
             '  if ("female".equalsIgnoreCase(r.getAttribute("value"))) {\n'
             '    // if input is covered, click associated label instead\n'
             '    r.click();\n'
             '    break;\n'
             '  }\n'
             '}'),
        "Or CSS: input[name='gender'][value='female'] (click label if input not interactable).",
    ]))

    story.append(qa(8, "Select class on Bootstrap/React dropdown?", [
        "UnexpectedTagNameException. Custom pattern: (1) click toggle (2) wait options visible "
        "(3) click option by text/value. Do not force Select.",
    ]))

    story.append(qa(9, "Dropdown opens on hover, not click?", [
        code("new Actions(driver).moveToElement(menu).perform();\n"
             "wait.until(ExpectedConditions.elementToBeClickable(option)).click();"),
    ]))

    story.append(qa(10, "Options load with delay?", [
        "After opening, use explicit wait: visibilityOfAllElementsLocatedBy / elementToBeClickable on option. "
        "Never Thread.sleep as the primary sync strategy.",
    ]))

    story.append(qa(11, "Currently selected value?", [
        "Native: select.getFirstSelectedOption().getText() (or getAttribute(\"value\")). "
        "Multi: getAllSelectedOptions(). Custom: often the toggle’s visible text or a .single-value node.",
    ]))

    story.append(qa(12, "Verify all available options?", [
        code("List<WebElement> opts = select.getOptions();\n"
             "List<String> texts = opts.stream().map(WebElement::getText).toList();\n"
             "Assert.assertTrue(texts.contains(\"India\"));"),
    ]))

    story.append(qa(13, "Can you deselect a radio button?", [
        "Standard HTML radios: no — re-click does not clear. Select another radio in the group. "
        "If UI allows “none selected”, it may be a custom control, not a pure radio.",
    ]))

    story.append(qa(14, "By.name vs By.id for radios?", [
        "Shared name = group (findElements). Unique id per option (findElement). "
        "Iterate by name/value when selection is data-driven.",
    ]))

    story.append(qa(15, "Native vs custom dropdown — how identify?", [
        "DevTools Inspect: &lt;select&gt;/&lt;option&gt; → Select class. "
        "div/button/ul/li/React-Select → 2-step custom handling. Always inspect before coding.",
    ]))

    # Senior extras (common follow-ups)
    story.append(P("Common follow-ups (senior)", "DH2"))
    story.append(qa(16, "getFirstSelectedOption when nothing selected?", [
        "May throw NoSuchElementException on some empty selects. Guard with getAllSelectedOptions().isEmpty() "
        "or try/catch depending on browser/DOM.",
    ]))
    story.append(qa(17, "Partial / searchable custom dropdown (typeahead)?", [
        "Click field → sendKeys filter text → wait filtered options → click matching option. "
        "Clear previous value if re-selecting.",
    ]))
    story.append(qa(18, "Disabled option / disabled select?", [
        "isEnabled() on select or option. Assert cannot select disabled options; use getAttribute(\"disabled\").",
    ]))

    story.append(PageBreak())

    # ========== PRACTICE ==========
    story.append(P("PART 2 — Practice Tests (DemoQA)", "DH1"))
    story.append(hline())
    story.append(P(
        "Site: https://demoqa.com — no local app needed. Prefer WebDriverManager + explicit waits. "
        "DemoQA ads/footers often intercept clicks — scroll into view or close banners if flaky.",
        "DBody"
    ))

    story.append(P("Test 1: Native Select — three methods", "DH2"))
    story.append(code(
        "// https://demoqa.com/select-menu  →  #oldSelectMenu\n"
        "Select select = new Select(driver.findElement(By.id(\"oldSelectMenu\")));\n"
        "select.selectByVisibleText(\"Yellow\");\n"
        "Assert.assertEquals(select.getFirstSelectedOption().getText(), \"Yellow\");\n"
        "select.selectByValue(\"3\"); // Green\n"
        "Assert.assertEquals(select.getFirstSelectedOption().getText(), \"Green\");\n"
        "select.selectByIndex(1); // Blue\n"
        "Assert.assertEquals(select.getFirstSelectedOption().getText(), \"Blue\");"
    ))

    story.append(P("Test 2: Multi-select select + deselect", "DH2"))
    story.append(code(
        "Select ms = new Select(driver.findElement(By.id(\"cars\")));\n"
        "Assert.assertTrue(ms.isMultiple());\n"
        "ms.selectByValue(\"volvo\");\n"
        "ms.selectByValue(\"saab\");\n"
        "ms.selectByValue(\"audi\");\n"
        "Assert.assertEquals(ms.getAllSelectedOptions().size(), 3);\n"
        "ms.deselectByValue(\"saab\");\n"
        "Assert.assertEquals(ms.getAllSelectedOptions().size(), 2);\n"
        "ms.deselectAll();\n"
        "Assert.assertEquals(ms.getAllSelectedOptions().size(), 0);"
    ))

    story.append(P("Test 3: Checkboxes (DemoQA tree) — click visible control", "DH2"))
    story.append(P(
        "Fix: DemoQA hides real inputs. Click the visible checkbox span/label, not the hidden input, "
        "if you get ElementNotInteractable / click intercepted.",
        "DFix"
    ))
    story.append(code(
        "driver.get(\"https://demoqa.com/checkbox\");\n"
        "WebElement homeBox = driver.findElement(\n"
        "  By.xpath(\"//label[@for='tree-node-home']//span[@class='rct-checkbox']\"));\n"
        "((JavascriptExecutor)driver).executeScript(\"arguments[0].scrollIntoView(true);\", homeBox);\n"
        "homeBox.click();\n"
        "WebElement result = new WebDriverWait(driver, Duration.ofSeconds(5))\n"
        "  .until(ExpectedConditions.visibilityOfElementLocated(By.id(\"result\")));\n"
        "Assert.assertTrue(result.getText().toLowerCase().contains(\"home\"));\n"
        "// State check on real input:\n"
        "WebElement input = driver.findElement(By.id(\"tree-node-home\"));\n"
        "Assert.assertTrue(input.isSelected());"
    ))

    story.append(P("Test 4: Radio group behaviour", "DH2"))
    story.append(code(
        "driver.get(\"https://demoqa.com/radio-button\");\n"
        "// Inputs are often CSS-hidden → click labels\n"
        "driver.findElement(By.xpath(\"//label[@for='yesRadio']\")).click();\n"
        "Assert.assertTrue(driver.findElement(By.id(\"yesRadio\")).isSelected());\n"
        "driver.findElement(By.xpath(\"//label[@for='impressiveRadio']\")).click();\n"
        "Assert.assertFalse(driver.findElement(By.id(\"yesRadio\")).isSelected());\n"
        "Assert.assertTrue(driver.findElement(By.id(\"impressiveRadio\")).isSelected());\n"
        "Assert.assertTrue(driver.findElement(By.cssSelector(\".mt-3\")).getText()\n"
        "  .contains(\"Impressive\"));\n"
        "// Note: 'No' radio is disabled on DemoQA — good extra assert for isEnabled()==false"
    ))

    story.append(P("Test 5: Custom React dropdown (2-step + wait)", "DH2"))
    story.append(code(
        "driver.get(\"https://demoqa.com/select-menu\");\n"
        "WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));\n"
        "WebElement dd = wait.until(ExpectedConditions.elementToBeClickable(\n"
        "  By.id(\"withOptGroup\")));\n"
        "dd.click();\n"
        "WebElement option = wait.until(ExpectedConditions.elementToBeClickable(\n"
        "  By.xpath(\"//div[contains(@class,'option') and normalize-space()='Group 1, option 2']\")));\n"
        "option.click();\n"
        "String selected = wait.until(ExpectedConditions.visibilityOfElementLocated(\n"
        "  By.cssSelector(\"#withOptGroup .css-1uccc91-singleValue, "
        "#withOptGroup [class*='singleValue']\"))).getText();\n"
        "// class hashes change — prefer contains(@class,'singleValue') / role-based locators\n"
        "Assert.assertEquals(selected, \"Group 1, option 2\");"
    ))
    story.append(P(
        "React-Select class names (css-xxxxx) change often — prefer text, role=option, or partial class contains.",
        "DTip"
    ))

    story.append(Spacer(1, 6))
    story.append(P("Quick revision", "DH1"))
    story.append(hline())
    rows = [
        ["Topic", "Key point"],
        ["Select class", "Only &lt;select&gt;; else UnexpectedTagNameException"],
        ["3 select methods", "visibleText / value / index"],
        ["Multi-select", "isMultiple + deselect*; deselect fails on single"],
        ["Checkbox", "Guard with isSelected; click visible control if input hidden"],
        ["Radio", "One per name group; cannot unselect by re-click"],
        ["Custom DD", "Click open → wait → click option"],
        ["States", "selected / enabled / displayed are independent"],
    ]
    data = []
    for i, r in enumerate(rows):
        st = styles["DHead"] if i == 0 else styles["DCell"]
        data.append([Paragraph(c, st) for c in r])
    t = Table(data, colWidths=[1.5 * inch, 5.0 * inch], repeatRows=1)
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
    story.append(Spacer(1, 8))
    story.append(P(
        "End of Dropdowns / Checkboxes / Radios Interview Q&amp;A — verified for Selenium 4.",
        "DBody"
    ))

    doc = SimpleDocTemplate(
        str(OUT), pagesize=A4,
        leftMargin=30, rightMargin=30, topMargin=26, bottomMargin=24,
        title="Dropdowns Checkboxes Radios Interview Q&A",
        author="SDET Week 2",
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print("Updated:", OUT, "bytes=", OUT.stat().st_size)


if __name__ == "__main__":
    build()
