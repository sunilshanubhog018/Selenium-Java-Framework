"""Rebuild Tables & Dynamic Elements Interview PDF with accuracy polish."""
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
    r"\Tables, dynamic elements\Tables_DynamicElements_InterviewQA.pdf"
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
styles.add(ParagraphStyle(name="TMain", fontName="Helvetica-Bold", fontSize=14.5,
                          leading=18, textColor=white, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="TSub", fontName="Helvetica", fontSize=9,
                          leading=12, textColor=HexColor("#dbeafe"), alignment=TA_CENTER))
styles.add(ParagraphStyle(name="DH1", fontName="Helvetica-Bold", fontSize=11,
                          leading=13, textColor=NAVY, spaceBefore=7, spaceAfter=3))
styles.add(ParagraphStyle(name="DH2", fontName="Helvetica-Bold", fontSize=9.3,
                          leading=11.5, textColor=TEAL, spaceBefore=5, spaceAfter=2))
styles.add(ParagraphStyle(name="DQ", fontName="Helvetica-Bold", fontSize=8.5,
                          leading=10.8, textColor=NAVY, spaceBefore=4, spaceAfter=1))
styles.add(ParagraphStyle(name="DA", fontName="Helvetica", fontSize=8.0,
                          leading=10.3, textColor=DARK, alignment=TA_JUSTIFY, spaceAfter=2))
styles.add(ParagraphStyle(name="DTip", fontName="Helvetica-Oblique", fontSize=7.4,
                          leading=9.4, textColor=GOLD, leftIndent=4, spaceAfter=2))
styles.add(ParagraphStyle(name="DFix", fontName="Helvetica-Oblique", fontSize=7.3,
                          leading=9.3, textColor=GREEN, spaceAfter=3))
styles.add(ParagraphStyle(name="DBody", fontName="Helvetica", fontSize=8.3,
                          leading=10.4, textColor=DARK, spaceAfter=3))
styles.add(ParagraphStyle(name="CodeB", fontName="Courier", fontSize=6.4,
                          leading=8.3, textColor=DARK, backColor=LIGHT, spaceBefore=1, spaceAfter=2))
styles.add(ParagraphStyle(name="DCell", fontName="Helvetica", fontSize=7.0,
                          leading=8.8, textColor=DARK))
styles.add(ParagraphStyle(name="DHead", fontName="Helvetica-Bold", fontSize=7.0,
                          leading=8.8, textColor=white))
styles.add(ParagraphStyle(name="LvlB", fontName="Helvetica-Bold", fontSize=7.5,
                          textColor=HexColor("#1d4ed8"), spaceAfter=2))
styles.add(ParagraphStyle(name="LvlR", fontName="Helvetica-Bold", fontSize=7.5,
                          textColor=RED, spaceAfter=2))
styles.add(ParagraphStyle(name="LvlG", fontName="Helvetica-Bold", fontSize=7.5,
                          textColor=GREEN, spaceAfter=2))


def P(t, s="DA"):
    return Paragraph(t, styles[s])


def code(t):
    return Preformatted(t.rstrip(), styles["CodeB"])


def tip(t):
    return P(f"<b>Tip:</b> {t}", "DTip")


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
        canvas.setFont("Helvetica", 6.7)
        canvas.drawString(28, A4[1] - 9, "Tables & Dynamic Elements | Interview Q&A")
        canvas.drawRightString(A4[0] - 28, A4[1] - 9, "Week 2 · SDET")
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 6.7)
        canvas.drawCentredString(A4[0] / 2, 11, f"Page {page}")
    canvas.restoreState()


def build():
    story = []

    cover = Table([
        [P("Tables &amp; Dynamic Elements", "TMain")],
        [P("Interview Q&amp;A + 5 Practice Tests<br/>"
           "Selenium 4 | Java | TestNG | SDET Prep<br/><br/>"
           "PART 1 Fundamentals (Q1–Q15) · PART 2 Senior (Q16–Q35) · PART 3 Practice",
           "TSub")],
    ], colWidths=[6.7 * inch])
    cover.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("TOPPADDING", (0, 0), (-1, -1), 20),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
    ]))
    story.append(Spacer(1, 28))
    story.append(cover)
    story.append(Spacer(1, 8))
    story.append(P(
        "Verified. Original content was already strong; small accuracy polish applied for interviews "
        "(index bases, waits, stale elements, virtualized tables, BigDecimal totals).",
        "DBody"
    ))
    story.append(P(
        "Polish: XPath 1-based vs Java 0-based; scope findElements to row; presence vs visibility; "
        "stale re-find; pagination + stalenessOf; money as BigDecimal.",
        "DFix"
    ))
    story.append(PageBreak())

    # PART 1
    story.append(P("PART 1 — FUNDAMENTALS", "DH1"))
    story.append(P("Blue | All levels", "LvlB"))
    story.append(hline())

    story.append(P("HTML Tables", "DH2"))
    story.append(qa(1, "Key HTML table tags?", [
        "<b>table</b> container; <b>thead</b>/<b>tbody</b>/<b>tfoot</b> sections; <b>tr</b> row; "
        "<b>th</b> header cell; <b>td</b> data cell. Navigate with XPath like "
        "//table[@id='t1']//tbody/tr/td…",
    ]))
    story.append(qa(2, "Read a specific cell?", [
        code('// XPath indexes are 1-based\n'
             'By.xpath("//table[@id=\'table1\']//tbody/tr[2]/td[3]")'),
        "Critical bug source: XPath <b>tr[1]/td[1]</b> = first row/col, but "
        "List&lt;WebElement&gt; uses <b>get(0)</b> for first cell.",
    ]))
    story.append(qa(3, "Iterate all rows and columns?", [
        "1) rows = table tbody tr  2) for each row: cells = row.findElements(By.tagName(\"td\"))  "
        "Call findElements on the <b>row</b>, not driver, so you only get that row’s cells.",
    ]))
    story.append(qa(4, "findElements on driver vs parent element?", [
        "driver.findElements → entire DOM. parent.findElements → subtree only. "
        "For tables always scope to table/row to avoid grabbing every td on the page.",
    ]))
    story.append(qa(5, "Find row by value and act (edit/delete)?", [
        "Loop rows, match cells.get(col).getText(), then row.findElement(By.xpath(\".//a[text()='edit']\")). "
        "Or pure XPath: //tbody/tr[td[1][normalize-space()='Bach']]//a[contains(.,'edit')]. "
        "Prefer normalize-space() for whitespace-safe matching.",
    ]))
    story.append(qa(6, "Why is the dot in .//a critical?", [
        ".//a searches under the current context node (the row). //a from a context still often "
        "searches from document root depending on usage — with WebElement.findElement, use "
        "<b>.//</b> (relative) so you don’t click another row’s link.",
        tip("Always use relative XPath (.//…) when searching inside a row WebElement."),
    ]))
    story.append(qa(7, "Count rows and columns?", [
        "Rows: tbody/tr size. Columns: first data row’s td size, or thead th size. "
        "Don’t mix header rows into data row counts. Watch for rowspan/colspan — simple counts can lie.",
    ]))

    story.append(P("Dynamic elements", "DH2"))
    story.append(qa(8, "What are dynamic elements?", [
        "Properties/DOM change at runtime: AJAX appear/disappear, generated ids, enable/disable, "
        "lazy tables, modals. Banking UIs are full of these (balances, txn tables, spinners).",
    ]))
    story.append(qa(9, "Key ExpectedConditions?", [
        "visibilityOfElementLocated, presenceOfElementLocated, invisibilityOfElementLocated, "
        "elementToBeClickable, stalenessOf, textToBePresentInElement, numberOfElementsToBeMoreThan.",
    ]))
    story.append(qa(10, "presence vs visibility?", [
        "presence = in DOM (may be hidden). visibility = in DOM and displayed (size &gt; 0). "
        "Interact/read text → visibility (or clickable). getText() on invisible often empty.",
    ]))
    story.append(qa(11, "StaleElementReferenceException?", [
        "You hold a WebElement whose DOM node was replaced/removed (refresh, AJAX redraw, SPA re-render). "
        "Fix: re-find before use; wait stalenessOf(old) then locate again; FluentWait ignoring Stale…",
    ]))
    story.append(qa(12, "Dynamic IDs?", [
        "contains(@id,'…'), starts-with, stable parent+child, text(), CSS [id*='partial']. "
        "Never hard-code full random ids.",
    ]))
    story.append(qa(13, "Wait for spinner then content?", [
        "invisibilityOf(spinner) then visibilityOf(results). Two-step pattern is standard for banking loaders.",
    ]))
    story.append(qa(14, "Implicit vs explicit for dynamic UI?", [
        "Implicit: global presence polling only. Explicit: targeted conditions. Prefer explicit; "
        "keep implicit 0/small to avoid hard-to-reason combined waits.",
    ]))
    story.append(qa(15, "AJAX-loaded content pattern?", [
        "Trigger action → wait correct condition → interact. No Thread.sleep as primary sync.",
    ]))

    story.append(PageBreak())

    # PART 2
    story.append(P("PART 2 — SENIOR / FRAMEWORK", "DH1"))
    story.append(P("Red | 4+ years · utilities · stale · pagination · banking", "LvlR"))
    story.append(hline())

    story.append(qa(16, "TableHelper in framework?", [
        "getCellValue, getRowCount, getColumnValues, findRowByCellValue, clickActionInRow — "
        "centralize XPath/index rules. Document if row/col args are 0-based (Java) or 1-based (XPath).",
    ]))
    story.append(qa(17, "Dynamic waits in POM?", [
        "Waits inside page methods or WaitHelper; tests stay business-language only.",
    ]))
    story.append(qa(18, "findRowByCellValue sketch?", [
        code("List<WebElement> rows = table.findElements(By.cssSelector(\"tbody tr\"));\n"
             "for (WebElement row : rows) {\n"
             "  List<WebElement> cells = row.findElements(By.tagName(\"td\"));\n"
             "  if (cells.get(colIndex).getText().trim().equals(value))\n"
             "    return row;\n"
             "}\n"
             "return null;"),
    ]))
    story.append(qa(19, "Paginated tables?", [
        "Search page → if not found and Next enabled → click Next → wait table refresh "
        "(stalenessOf old row + new rows visible) → search again; maxPages guard.",
    ]))
    story.append(qa(20, "Flaky StaleElement in CI?", [
        "Headless timing, AJAX between find and click. Log step, screenshot, re-find before action, "
        "FluentWait ignoring Stale, don’t keep row refs across refresh.",
    ]))
    story.append(qa(21, "Robust stale handling layers?", [
        "1) Prevent (re-find) 2) FluentWait ignore Stale 3) retryOnStale wrapper. Most bugs fixed by (1).",
    ]))
    story.append(qa(22, "Auto-refreshing live table?", [
        "Minimize find→act gap; read whole row into Strings quickly; assert on snapshot; "
        "optional JS pause refresh if app allows.",
    ]))
    story.append(qa(23, "Verify column sorted after header click?", [
        "Wait re-render → collect column texts → copy+sort → assert equals (or reverse for DESC). "
        "Parse numbers/dates before compare.",
    ]))
    story.append(qa(24, "Thread-safe table helpers?", [
        "ThreadLocal driver; helpers take WebDriver; no static WebElement state; never share elements across threads.",
    ]))
    story.append(qa(25, "Parallel tests fight shared data?", [
        "Unique test data per thread (API setup), cleanup, search by unique ref no — not shared names.",
    ]))
    story.append(qa(26, "Banking tables you automated?", [
        "Txn history, statements, beneficiaries, EMI schedule, transfer confirmation — same helper patterns.",
    ]))
    story.append(qa(27, "presence vs visibility bug story?", [
        "Table in DOM with display:none → presence returned early → empty text. Fix: visibilityOf…",
    ]))
    story.append(qa(28, "AJAX typeahead after 3 chars?", [
        "sendKeys → wait options container → wait option text → click. Don’t assert instantly after type.",
    ]))
    story.append(qa(29, "Confirmation table inside modal?", [
        "Wait modal visible → scope finds to modal → read cells → close → wait modal gone. Return DTO from POM.",
    ]))
    story.append(qa(30, "Statement total vs sum of rows?", [
        "Sum amount column with <b>BigDecimal</b> (not double). Compare to footer total. Paginate and accumulate if needed.",
        tip("Saying BigDecimal for money is a senior banking signal."),
    ]))
    story.append(qa(31, "Flaky dynamic table rows STAR?", [
        "Wait container visible + row count stabilizes (T == T+500ms) before iterating.",
    ]))
    story.append(qa(32, "Junior used Thread.sleep before table?", [
        "Replace with visibility/row-count wait; point to WaitHelper; ban sleep in reviews.",
    ]))
    story.append(qa(33, "Mentor mental models?", [
        "Tables = nested loops + parent scope. Dynamics = wait until condition. Debug checklist: table id, index base, wait, re-find.",
    ]))

    story.append(P("Rapid fire", "DH2"))
    rf = [
        ["34", "driver.findElement(td) for one cell?",
         "Gets first td on page — wrong. Scope to table/row."],
        ["35", "visibility wait never true?",
         "TimeoutException after timeout; assert with clear message."],
        ["36", "Virtualized grid (AG Grid)?",
         "Only visible rows in DOM — scroll/virtualization-aware strategy, not simple tbody loop."],
    ]
    data = [[Paragraph(x, styles["DHead"]) for x in ["#", "Q", "A"]]]
    for r in rf:
        data.append([Paragraph(x, styles["DCell"]) for x in r])
    t = Table(data, colWidths=[0.35 * inch, 1.9 * inch, 4.3 * inch], repeatRows=1)
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

    story.append(PageBreak())

    # PART 3
    story.append(P("PART 3 — PRACTICE TESTS", "DH1"))
    story.append(P("Green | the-internet.herokuapp.com | no Thread.sleep", "LvlG"))
    story.append(hline())

    story.append(P("Test 1 — Read cell by XPath index", "DH2"))
    story.append(code(
        "driver.get(\"https://the-internet.herokuapp.com/tables\");\n"
        "WebElement cell = driver.findElement(\n"
        "  By.xpath(\"//table[@id='table1']//tbody/tr[1]/td[3]\"));\n"
        "Assert.assertTrue(cell.getText().contains(\"@\"));"
    ))

    story.append(P("Test 2 — Iterate rows with scoped findElements", "DH2"))
    story.append(code(
        "List<WebElement> rows = driver.findElements(\n"
        "  By.xpath(\"//table[@id='table1']//tbody/tr\"));\n"
        "Assert.assertEquals(rows.size(), 4);\n"
        "for (WebElement row : rows) {\n"
        "  List<WebElement> cells = row.findElements(By.tagName(\"td\")); // scoped!\n"
        "  System.out.println(cells.get(0).getText() + \" | \" + cells.get(2).getText());\n"
        "}"
    ))

    story.append(P("Test 3 — Find row by last name + relative .//a", "DH2"))
    story.append(code(
        "String target = \"Bach\";\n"
        "boolean found = false;\n"
        "for (WebElement row : driver.findElements(\n"
        "    By.xpath(\"//table[@id='table1']//tbody/tr\"))) {\n"
        "  if (target.equals(row.findElements(By.tagName(\"td\")).get(0).getText())) {\n"
        "    found = true;\n"
        "    row.findElement(By.xpath(\".//a[contains(.,'edit')]\")).click();\n"
        "    break;\n"
        "  }\n"
        "}\n"
        "Assert.assertTrue(found);"
    ))

    story.append(P("Test 4 — Dynamic loading 1 &amp; 2", "DH2"))
    story.append(code(
        "WebDriverWait w = new WebDriverWait(driver, Duration.ofSeconds(10));\n"
        "SoftAssert sa = new SoftAssert();\n"
        "driver.get(\"https://the-internet.herokuapp.com/dynamic_loading/1\");\n"
        "driver.findElement(By.xpath(\"//button[text()='Start']\")).click();\n"
        "sa.assertEquals(w.until(ExpectedConditions.visibilityOfElementLocated(\n"
        "  By.id(\"finish\"))).getText().trim(), \"Hello World!\");\n"
        "driver.get(\"https://the-internet.herokuapp.com/dynamic_loading/2\");\n"
        "driver.findElement(By.xpath(\"//button[text()='Start']\")).click();\n"
        "sa.assertEquals(w.until(ExpectedConditions.visibilityOfElementLocated(\n"
        "  By.id(\"finish\"))).getText().trim(), \"Hello World!\");\n"
        "sa.assertAll();"
    ))
    story.append(P(
        "/1 = hidden then shown; /2 = not in DOM then added. Both need visibility wait before assert.",
        "DTip"
    ))

    story.append(P("Test 5 — Dynamic controls remove/add/enable", "DH2"))
    story.append(code(
        "driver.get(\"https://the-internet.herokuapp.com/dynamic_controls\");\n"
        "WebDriverWait w = new WebDriverWait(driver, Duration.ofSeconds(10));\n"
        "driver.findElement(By.xpath(\"//button[text()='Remove']\")).click();\n"
        "w.until(ExpectedConditions.invisibilityOfElementLocated(\n"
        "  By.cssSelector(\"#checkbox-example input[type='checkbox']\")));\n"
        "Assert.assertEquals(driver.findElement(By.id(\"message\")).getText(), \"It's gone!\");\n"
        "driver.findElement(By.xpath(\"//button[text()='Add']\")).click();\n"
        "w.until(ExpectedConditions.visibilityOfElementLocated(\n"
        "  By.cssSelector(\"#checkbox-example input[type='checkbox']\")));\n"
        "WebElement input = driver.findElement(By.cssSelector(\"#input-example input\"));\n"
        "Assert.assertFalse(input.isEnabled());\n"
        "driver.findElement(By.xpath(\"//button[text()='Enable']\")).click();\n"
        "w.until(ExpectedConditions.elementToBeClickable(\n"
        "  By.cssSelector(\"#input-example input\")));\n"
        "input = driver.findElement(By.cssSelector(\"#input-example input\")); // re-find\n"
        "input.sendKeys(\"Banking Test Data\");\n"
        "Assert.assertEquals(input.getAttribute(\"value\"), \"Banking Test Data\");"
    ))

    story.append(Spacer(1, 6))
    story.append(hline())
    story.append(P(
        "End of Tables &amp; Dynamic Elements Interview Q&amp;A — verified for Selenium 4.",
        "DBody"
    ))

    doc = SimpleDocTemplate(
        str(OUT), pagesize=A4,
        leftMargin=30, rightMargin=30, topMargin=26, bottomMargin=24,
        title="Tables Dynamic Elements Interview Q&A",
        author="SDET Week 2",
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print("Updated:", OUT, "bytes=", OUT.stat().st_size)


if __name__ == "__main__":
    build()
