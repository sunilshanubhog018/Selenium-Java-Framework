"""Rebuild Alerts/Frames/Windows Interview Q&A PDF with accuracy fixes."""
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
    r"\Alerts, frames, multiple windows\Alerts_Frames_Windows_InterviewQA.pdf"
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
styles.add(ParagraphStyle(name="TMain", fontName="Helvetica-Bold", fontSize=15,
                          leading=19, textColor=white, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="TSub", fontName="Helvetica", fontSize=9,
                          leading=12, textColor=HexColor("#dbeafe"), alignment=TA_CENTER))
styles.add(ParagraphStyle(name="DH1", fontName="Helvetica-Bold", fontSize=11,
                          leading=14, textColor=NAVY, spaceBefore=7, spaceAfter=3))
styles.add(ParagraphStyle(name="DH2", fontName="Helvetica-Bold", fontSize=9.5,
                          leading=12, textColor=TEAL, spaceBefore=5, spaceAfter=2))
styles.add(ParagraphStyle(name="DQ", fontName="Helvetica-Bold", fontSize=8.7,
                          leading=11, textColor=NAVY, spaceBefore=4, spaceAfter=1))
styles.add(ParagraphStyle(name="DA", fontName="Helvetica", fontSize=8.2,
                          leading=10.5, textColor=DARK, alignment=TA_JUSTIFY, spaceAfter=2))
styles.add(ParagraphStyle(name="DTip", fontName="Helvetica-Oblique", fontSize=7.6,
                          leading=9.5, textColor=GOLD, leftIndent=4, spaceAfter=2))
styles.add(ParagraphStyle(name="DFix", fontName="Helvetica-Oblique", fontSize=7.5,
                          leading=9.5, textColor=GREEN, spaceAfter=3))
styles.add(ParagraphStyle(name="DBody", fontName="Helvetica", fontSize=8.5,
                          leading=10.5, textColor=DARK, spaceAfter=3))
styles.add(ParagraphStyle(name="CodeB", fontName="Courier", fontSize=6.6,
                          leading=8.6, textColor=DARK, backColor=LIGHT, spaceBefore=1, spaceAfter=2))
styles.add(ParagraphStyle(name="DCell", fontName="Helvetica", fontSize=7.2,
                          leading=9, textColor=DARK))
styles.add(ParagraphStyle(name="DHead", fontName="Helvetica-Bold", fontSize=7.2,
                          leading=9, textColor=white))
styles.add(ParagraphStyle(name="LvlB", fontName="Helvetica-Bold", fontSize=7.8,
                          textColor=HexColor("#1d4ed8"), spaceAfter=2))
styles.add(ParagraphStyle(name="LvlR", fontName="Helvetica-Bold", fontSize=7.8,
                          textColor=RED, spaceAfter=2))
styles.add(ParagraphStyle(name="LvlG", fontName="Helvetica-Bold", fontSize=7.8,
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
        canvas.setFont("Helvetica", 6.8)
        canvas.drawString(28, A4[1] - 9, "Alerts · Frames · Windows | Interview Q&A")
        canvas.drawRightString(A4[0] - 28, A4[1] - 9, "Week 2 · SDET")
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 6.8)
        canvas.drawCentredString(A4[0] / 2, 11, f"Page {page}")
    canvas.restoreState()


def build():
    story = []

    cover = Table([
        [P("Alerts, Frames &amp; Multiple Windows", "TMain")],
        [P("Interview Q&amp;A + Practice Tests<br/>"
           "Selenium 4 | Java | TestNG | SDET Prep<br/><br/>"
           "PART 1 Fundamentals (Q1–Q20) &nbsp;·&nbsp; "
           "PART 2 Senior/Framework (Q21–Q50) &nbsp;·&nbsp; "
           "PART 3 Practice Tests", "TSub")],
    ], colWidths=[6.7 * inch])
    cover.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("TOPPADDING", (0, 0), (-1, -1), 20),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
    ]))
    story.append(Spacer(1, 30))
    story.append(cover)
    story.append(Spacer(1, 8))
    story.append(P(
        "Verified interview guide. Core ideas from your original doc kept; technical wording tightened "
        "for Selenium 4 accuracy.",
        "DBody"
    ))
    story.append(P(
        "Fixes: JS alert vs HTML modal vs OS dialog vs HTTP auth; UnhandledPromptBehaviour API; "
        "window handle typing; newWindow(); TinyMCE notes; practice-test robustness.",
        "DFix"
    ))
    story.append(PageBreak())

    # ========== PART 1 ==========
    story.append(P("PART 1 — FUNDAMENTALS", "DH1"))
    story.append(P("Blue | Asked at all levels — answer cleanly and fast", "LvlB"))
    story.append(hline())

    story.append(P("Alerts", "DH2"))
    story.append(qa(1, "What are JavaScript alerts? How many types?", [
        "Native browser dialogs from JS. Three types: (1) <b>alert()</b> — OK only  "
        "(2) <b>confirm()</b> — OK/Cancel  (3) <b>prompt()</b> — text field + OK/Cancel. "
        "Handle via <font face='Courier'>driver.switchTo().alert()</font> returning Alert.",
        tip("Not the same as HTML modals, OS file dialogs, or HTTP Basic auth popups."),
    ]))
    story.append(qa(2, "How do you handle alerts?", [
        "Wait → switch → act:",
        code("WebDriverWait w = new WebDriverWait(driver, Duration.ofSeconds(10));\n"
             "Alert a = w.until(ExpectedConditions.alertIsPresent());\n"
             "String msg = a.getText();\n"
             "a.accept();   // OK\n"
             "// a.dismiss(); // Cancel (confirm/prompt)\n"
             "// a.sendKeys(\"text\"); // prompt only"),
        "After accept/dismiss, focus returns to the page that opened the alert.",
    ]))
    story.append(qa(3, "accept() vs dismiss()?", [
        "accept() = OK. dismiss() = Cancel on confirm/prompt. On simple alert both usually close it; "
        "prefer accept() for simple alerts. On prompt, dismiss discards typed text.",
    ]))
    story.append(qa(4, "NoAlertPresentException?", [
        "Thrown if switchTo().alert() when no alert exists (often race: alert not ready). "
        "Fix: ExpectedConditions.alertIsPresent() before interacting.",
    ]))
    story.append(qa(5, "Can Selenium handle OS file upload/download dialogs?", [
        "Not as JS alerts. Upload: sendKeys absolute path to input[type=file] when present. "
        "OS dialogs: Robot/AutoIT (limited, not headless-friendly). Download: browser prefs / CDP.",
    ]))
    story.append(qa(6, "JS alert vs custom modal?", [
        "JS alert: native; cannot Inspect/findElement; must use switchTo().alert(). "
        "Custom modal (Bootstrap/SweetAlert): normal HTML in DOM → findElement/click. "
        "Rule: if you can Inspect Element on it, treat as DOM modal.",
    ]))

    story.append(P("Frames", "DH2"))
    story.append(qa(7, "What is an iframe? Why special handling?", [
        "iframe embeds another document with its own DOM. WebDriver works in one document context "
        "at a time (main or a frame). Switch with switchTo().frame(...) before interacting inside.",
    ]))
    story.append(qa(8, "Three ways to switch to a frame?", [
        "1) frame(index)  2) frame(nameOrId)  3) frame(WebElement) — preferred when id/name dynamic.",
        code("driver.switchTo().frame(driver.findElement(By.cssSelector(\"iframe[title='x']\")));"),
    ]))
    story.append(qa(9, "defaultContent() vs parentFrame()?", [
        "defaultContent() → top-level page (always). parentFrame() → one level up. "
        "Nested Main→A→B: from B, parentFrame→A; defaultContent→Main.",
    ]))
    story.append(qa(10, "Nested frames?", [
        "Switch outer then inner (cannot jump straight to deep child by name if not in that document). "
        "Exit with parentFrame stepwise or defaultContent once.",
    ]))
    story.append(qa(11, "Forget to switch back from a frame?", [
        "findElement searches only inside current frame → NoSuchElementException for main-page elements. "
        "Always defaultContent() (or parentFrame) when done — ideally in finally inside POM methods.",
    ]))
    story.append(qa(12, "frameToBeAvailableAndSwitchToIt()?", [
        "ExpectedCondition: waits until frame is available AND switches into it. Accepts name, index, or By.",
        code("wait.until(ExpectedConditions.frameToBeAvailableAndSwitchToIt(\"mce_0_ifr\"));"),
    ]))

    story.append(P("Windows", "DH2"))
    story.append(qa(13, "What is a window handle?", [
        "Opaque unique String id per open window/tab. getWindowHandle() = current; "
        "getWindowHandles() = Set&lt;String&gt; of all handles for that driver session.",
    ]))
    story.append(qa(14, "Switch to a new window after click?", [
        code("String main = driver.getWindowHandle();\n"
             "link.click();\n"
             "new WebDriverWait(driver, Duration.ofSeconds(10))\n"
             "  .until(ExpectedConditions.numberOfWindowsToBe(2));\n"
             "for (String h : driver.getWindowHandles()) {\n"
             "  if (!h.equals(main)) { driver.switchTo().window(h); break; }\n"
             "}"),
        tip("numberOfWindowsToBe only means the window exists — also wait for title/url/element before asserting content."),
    ]))
    story.append(qa(15, "close() vs quit()?", [
        "close() = current window only (session may continue). quit() = all windows + end session. "
        "After close() on a child, you must switchTo().window(parent) or risk NoSuchWindowException.",
    ]))
    story.append(qa(16, "newWindow() in Selenium 4?", [
        code("driver.switchTo().newWindow(WindowType.TAB);\n"
             "driver.switchTo().newWindow(WindowType.WINDOW);"),
        "Opens empty tab/window AND switches to it — cleaner than window.open + handle hunt.",
    ]))
    story.append(qa(17, "Why Set for getWindowHandles()?", [
        "Handles are unique. Set has no guaranteed order — don’t use “last index” blindly. "
        "Store parent handle before open, then pick the handle not equal to parent.",
    ]))
    story.append(qa(18, "NoSuchWindowException?", [
        "Switching to a closed/invalid handle. Common after close() without switching back.",
    ]))
    story.append(qa(19, "Switch by title?", [
        "No direct API. Loop handles, switchTo each, compare getTitle()/getCurrentUrl(), break on match.",
    ]))
    story.append(qa(20, "Common thread across alerts, frames, windows?", [
        "All are context switches via driver.switchTo(): alert() / frame() / window(). "
        "Matching waits: alertIsPresent, frameToBeAvailableAndSwitchToIt, numberOfWindowsToBe. "
        "Driver is always in exactly one context at a time.",
    ]))

    story.append(PageBreak())

    # ========== PART 2 ==========
    story.append(P("PART 2 — SENIOR / FRAMEWORK LEVEL", "DH1"))
    story.append(P("Red | 4+ years — design, debugging, parallel, banking stories", "LvlR"))
    story.append(hline())

    story.append(P("Framework patterns", "DH2"))
    story.append(qa(21, "How did you handle alerts in your framework?", [
        "AlertHelper with accept/dismiss/getText/sendKeys/isPresent/acceptIfPresent. "
        "Internal WebDriverWait(alertIsPresent). Tests never call raw switchTo().alert().",
    ]))
    story.append(qa(22, "Sketch of AlertHelper?", [
        code("public static void acceptAlert(WebDriver d) {\n"
             "  new WebDriverWait(d, Duration.ofSeconds(10))\n"
             "    .until(ExpectedConditions.alertIsPresent()).accept();\n"
             "}\n"
             "public static boolean isAlertPresent(WebDriver d, int sec) {\n"
             "  try {\n"
             "    new WebDriverWait(d, Duration.ofSeconds(sec))\n"
             "      .until(ExpectedConditions.alertIsPresent());\n"
             "    return true;\n"
             "  } catch (TimeoutException e) { return false; }\n"
             "}"),
        "Prefer short wait for isPresent over bare switchTo (less flaky than try/catch only).",
    ]))
    story.append(qa(23, "Frames in POM?", [
        "A) Frame-aware page methods switch in/out internally. "
        "B) switchToPaymentFrame() returns a dedicated PaymentGatewayPage. Tests stay business-readable.",
    ]))
    story.append(qa(24, "WindowHelper methods?", [
        "switchToNewWindow, switchToByTitle, closeAndReturn(main), closeAllExcept(main) — all with waits; "
        "driver passed in (no static WebDriver).",
    ]))
    story.append(qa(25, "Hide switching from tests?", [
        "Encapsulation: fundTransferPage.enterOtp(\"123456\") does frame switch + type + defaultContent. "
        "Tests should not look like Selenium tutorials.",
    ]))

    story.append(P("Edge cases", "DH2"))
    story.append(qa(26, "Unexpected alerts mid-test?", [
        "1) options.setUnhandledPromptBehaviour(UnexpectedAlertBehaviour.DISMISS_AND_NOTIFY) "
        "(Selenium 4 ChromeOptions)  2) @BeforeMethod/@AfterMethod acceptIfPresent cleanup  "
        "3) Listener safety net. Banking: session-timeout alerts are classic.",
    ]))
    story.append(qa(27, "Flaky alert in CI only?", [
        "Headless differences, speed, unexpected cookie/session alerts, UnhandledAlertException on next command. "
        "Screenshots + alertIsPresent before critical steps + longer CI timeout.",
    ]))
    story.append(qa(28, "Alert may or may not appear?", [
        "acceptIfPresent with short timeout (2–3s); continue on TimeoutException. "
        "Common for amount-threshold confirmation dialogs.",
    ]))
    story.append(qa(29, "UnhandledPromptBehaviour options?", [
        "ACCEPT, DISMISS, ACCEPT_AND_NOTIFY, DISMISS_AND_NOTIFY, IGNORE. "
        "NOTIFY variants auto-handle then surface UnhandledAlertException for awareness.",
        code("ChromeOptions o = new ChromeOptions();\n"
             "o.setUnhandledPromptBehaviour(\n"
             "  UnexpectedAlertBehaviour.DISMISS_AND_NOTIFY);"),
    ]))
    story.append(qa(30, "Dynamic frame / element ids?", [
        "Stable css/xpath (title/src/class), relative locators, switch by WebElement not index. "
        "Inside frame wait for a known content element after switch.",
    ]))

    story.append(P("Parallel / Thread safety", "DH2"))
    story.append(qa(31, "Thread-safe window switching?", [
        "ThreadLocal&lt;WebDriver&gt; per thread; never static shared handles. Helpers take WebDriver param; no static mutable state.",
    ]))
    story.append(qa(32, "Parallel tests interfere on windows?", [
        "Usually shared static driver. One thread’s close() kills another’s window. Fix ThreadLocal isolation. "
        "Also avoid assuming global window count if drivers are mis-shared.",
    ]))
    story.append(qa(33, "Frames + parallel?", [
        "Frame context is per-driver. ThreadLocal drivers keep switches isolated automatically.",
    ]))

    story.append(P("Banking / combined flows", "DH2"))
    story.append(qa(34, "Payment iframe + validation story?", [
        "Wait frameToBeAvailableAndSwitchToIt; fill fields; defaultContent before main-page Confirm. "
        "Use finally for defaultContent so failures don’t leave context stuck.",
    ]))
    story.append(qa(35, "Forgot defaultContent after OTP frame?", [
        "Next main-page click → NoSuchElementException. Fix: POM method ends with defaultContent in finally.",
    ]))
    story.append(qa(36, "Session timeout alerts in long suites?", [
        "Cleanup in before/after method; keep-alive ping if allowed; DISMISS_AND_NOTIFY safety net; "
        "shorter tests / re-login strategy.",
    ]))
    story.append(qa(37, "Pay Now → new window → iframe card form?", [
        "Save main handle → click → wait 2 windows → switch child → frameToBeAvailableAndSwitchToIt → "
        "fill → defaultContent → submit → wait windows=1 → switch main → assert success.",
    ]))
    story.append(qa(38, "OTP as alert vs modal vs new tab by env?", [
        "OTPHandler interface + Alert/Modal/Window implementations; factory from config env. "
        "Test calls enterOtp(code) only.",
    ]))

    story.append(P("Advanced", "DH2"))
    story.append(qa(39, "TinyMCE / CKEditor?", [
        "Usually iframe + contenteditable body. clear() often fails. Reliable: switch frame + JS set/get text "
        "(or sendKeys on body after click). Always defaultContent after.",
    ]))
    story.append(qa(40, "ElementClickInterceptedException in editors?", [
        "Overlaying nodes intercept clicks. Prefer JS set content / JS click; scroll into view; Actions move+click as secondary.",
    ]))
    story.append(qa(41, "Screenshot inside iframe?", [
        "After switchTo frame, element or viewport screenshot captures frame content context. "
        "defaultContent before main-page shots.",
    ]))
    story.append(qa(42, "switchTo().frame vs JS window.frames?", [
        "Selenium changes WebDriver document context (works across origins at protocol level). "
        "JS window.frames is same-origin limited. Prefer Selenium frame() for automation.",
    ]))
    story.append(qa(43, "Async iframe src load?", [
        "frameToBeAvailableAndSwitchToIt then wait for an inner element. For dynamic inject: wait presence of iframe by src/title first.",
    ]))

    story.append(P("Behavioral", "DH2"))
    story.append(qa(44, "Flaky window handling (STAR)?", [
        "Wait numberOfWindowsToBe(2) AND titleContains/urlContains after switch — existence ≠ content ready.",
    ]))
    story.append(qa(45, "Mentor juniors on context bugs?", [
        "Flashlight model: one context. Checklist: title, url, window count, defaultContent, then re-find.",
    ]))
    story.append(qa(46, "PR uses Thread.sleep before alert?", [
        "Replace with alertIsPresent wait; point to AlertHelper; ban sleep in review checklist.",
    ]))
    story.append(qa(47, "Design framework for alerts/frames/windows?", [
        "Helpers + POM encapsulation + waits from config + logging every switch + AfterMethod cleanup "
        "(alert, defaultContent, extra windows) + ThreadLocal driver.",
    ]))

    story.append(P("Rapid fire", "DH2"))
    rf = [
        ["48", "Two frames at once?", "No — one context; switch A → work → default → B"],
        ["49", "Window + nested frames sequence?",
         "main handle → click → wait 2 wins → child window → outer frame → inner frame → work → "
         "defaultContent → close → main window"],
        ["50", "Selenium 4 improvements?",
         "newWindow(TAB/WINDOW); better W3C consistency; CDP extras. Alert/frame APIs largely same."],
    ]
    data = [[Paragraph(x, styles["DHead"]) for x in ["#", "Q", "A"]]]
    for r in rf:
        data.append([Paragraph(x, styles["DCell"]) for x in r])
    t = Table(data, colWidths=[0.35 * inch, 1.6 * inch, 4.6 * inch], repeatRows=1)
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

    # ========== PART 3 ==========
    story.append(P("PART 3 — PRACTICE TESTS", "DH1"))
    story.append(P("Green | the-internet.herokuapp.com | waits only (no Thread.sleep)", "LvlG"))
    story.append(hline())

    story.append(P("Test 1 — Simple alert accept", "DH2"))
    story.append(code(
        "driver.get(\"https://the-internet.herokuapp.com/javascript_alerts\");\n"
        "driver.findElement(By.xpath(\"//button[text()='Click for JS Alert']\")).click();\n"
        "Alert a = new WebDriverWait(driver, Duration.ofSeconds(10))\n"
        "  .until(ExpectedConditions.alertIsPresent());\n"
        "Assert.assertEquals(a.getText(), \"I am a JS Alert\");\n"
        "a.accept();\n"
        "Assert.assertEquals(driver.findElement(By.id(\"result\")).getText(),\n"
        "  \"You successfully clicked an alert\");"
    ))

    story.append(P("Test 2 — Confirm dismiss (Cancel)", "DH2"))
    story.append(code(
        "driver.findElement(By.xpath(\"//button[text()='Click for JS Confirm']\")).click();\n"
        "Alert a = new WebDriverWait(driver, Duration.ofSeconds(10))\n"
        "  .until(ExpectedConditions.alertIsPresent());\n"
        "Assert.assertEquals(a.getText(), \"I am a JS Confirm\");\n"
        "a.dismiss();\n"
        "Assert.assertEquals(driver.findElement(By.id(\"result\")).getText(),\n"
        "  \"You clicked: Cancel\");"
    ))

    story.append(P("Test 3 — Prompt sendKeys + accept", "DH2"))
    story.append(code(
        "driver.findElement(By.xpath(\"//button[text()='Click for JS Prompt']\")).click();\n"
        "Alert a = new WebDriverWait(driver, Duration.ofSeconds(10))\n"
        "  .until(ExpectedConditions.alertIsPresent());\n"
        "Assert.assertEquals(a.getText(), \"I am a JS prompt\");\n"
        "a.sendKeys(\"Selenium Automation\");\n"
        "a.accept();\n"
        "Assert.assertEquals(driver.findElement(By.id(\"result\")).getText(),\n"
        "  \"You entered: Selenium Automation\");"
    ))
    story.append(P("Some Chrome versions need clear of default prompt value; if flaky, sendKeys after a short retry.", "DTip"))

    story.append(P("Test 4 — iframe TinyMCE via JS", "DH2"))
    story.append(code(
        "driver.get(\"https://the-internet.herokuapp.com/iframe\");\n"
        "new WebDriverWait(driver, Duration.ofSeconds(10))\n"
        "  .until(ExpectedConditions.frameToBeAvailableAndSwitchToIt(\"mce_0_ifr\"));\n"
        "JavascriptExecutor js = (JavascriptExecutor) driver;\n"
        "js.executeScript(\"document.getElementById('tinymce').innerText = 'Hello Selenium iframe';\");\n"
        "String text = (String) js.executeScript(\n"
        "  \"return document.getElementById('tinymce').innerText\");\n"
        "Assert.assertTrue(text.contains(\"Hello Selenium\"));\n"
        "driver.switchTo().defaultContent();\n"
        "Assert.assertTrue(driver.findElement(By.tagName(\"h3\")).getText().contains(\"iFrame\"));"
    ))

    story.append(P("Test 5 — Multiple windows", "DH2"))
    story.append(code(
        "driver.get(\"https://the-internet.herokuapp.com/windows\");\n"
        "String main = driver.getWindowHandle();\n"
        "driver.findElement(By.linkText(\"Click Here\")).click();\n"
        "new WebDriverWait(driver, Duration.ofSeconds(10))\n"
        "  .until(ExpectedConditions.numberOfWindowsToBe(2));\n"
        "for (String h : driver.getWindowHandles()) {\n"
        "  if (!h.equals(main)) { driver.switchTo().window(h); break; }\n"
        "}\n"
        "new WebDriverWait(driver, Duration.ofSeconds(10))\n"
        "  .until(ExpectedConditions.titleIs(\"New Window\"));\n"
        "Assert.assertEquals(driver.findElement(By.tagName(\"h3\")).getText(), \"New Window\");\n"
        "driver.close();\n"
        "driver.switchTo().window(main);\n"
        "Assert.assertEquals(driver.getTitle(), \"The Internet\");"
    ))

    story.append(Spacer(1, 6))
    story.append(hline())
    story.append(P(
        "End of Alerts / Frames / Windows Interview Q&amp;A — verified for Selenium 4 interviews.",
        "DBody"
    ))

    doc = SimpleDocTemplate(
        str(OUT), pagesize=A4,
        leftMargin=30, rightMargin=30, topMargin=26, bottomMargin=24,
        title="Alerts Frames Windows Interview Q&A",
        author="SDET Week 2",
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print("Updated:", OUT, "bytes=", OUT.stat().st_size)


if __name__ == "__main__":
    build()
