"""Rebuild WebDriver Interview Questions PDF with accuracy fixes."""
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
    r"\CLAUDE AI NOTES\Week 1 Java Fundamentals and Selenium Setup"
    r"\webdriver commands\WebDriver_Interview_Questions.pdf"
)

NAVY = HexColor("#0b3d5c")
TEAL = HexColor("#0f766e")
LIGHT = HexColor("#f0f9ff")
SOFT = HexColor("#e2e8f0")
DARK = HexColor("#1e293b")
MUTED = HexColor("#475569")
GOLD = HexColor("#b45309")
GREEN = HexColor("#166534")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TMain", fontName="Helvetica-Bold", fontSize=18,
                          leading=22, textColor=white, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="TSub", fontName="Helvetica", fontSize=10,
                          leading=13, textColor=HexColor("#dbeafe"), alignment=TA_CENTER))
styles.add(ParagraphStyle(name="DH1", fontName="Helvetica-Bold", fontSize=12,
                          leading=15, textColor=NAVY, spaceBefore=8, spaceAfter=5))
styles.add(ParagraphStyle(name="DQ", fontName="Helvetica-Bold", fontSize=9.2,
                          leading=12, textColor=NAVY, spaceBefore=6, spaceAfter=2))
styles.add(ParagraphStyle(name="DA", fontName="Helvetica", fontSize=8.8,
                          leading=11.5, textColor=DARK, alignment=TA_JUSTIFY, spaceAfter=2))
styles.add(ParagraphStyle(name="DTip", fontName="Helvetica-Oblique", fontSize=8.2,
                          leading=10.5, textColor=GOLD, leftIndent=6, spaceBefore=1, spaceAfter=3))
styles.add(ParagraphStyle(name="DFix", fontName="Helvetica-Oblique", fontSize=8,
                          leading=10, textColor=GREEN, leftIndent=4, spaceAfter=4))
styles.add(ParagraphStyle(name="DBody", fontName="Helvetica", fontSize=9,
                          leading=11.5, textColor=DARK, spaceAfter=4))
styles.add(ParagraphStyle(name="CodeB", fontName="Courier", fontSize=7.2,
                          leading=9.5, textColor=DARK, backColor=LIGHT,
                          leftIndent=3, spaceBefore=1, spaceAfter=3))
styles.add(ParagraphStyle(name="DCell", fontName="Helvetica", fontSize=7.8,
                          leading=10, textColor=DARK))
styles.add(ParagraphStyle(name="DHead", fontName="Helvetica-Bold", fontSize=7.8,
                          leading=10, textColor=white))
styles.add(ParagraphStyle(name="Tag", fontName="Helvetica-Bold", fontSize=7.5,
                          leading=9, textColor=TEAL, spaceAfter=1))


def P(t, s="DA"):
    return Paragraph(t, styles[s])


def code(t):
    return Preformatted(t.rstrip(), styles["CodeB"])


def tip(t):
    return P(f"<b>Interview Tip:</b> {t}", "DTip")


def hline():
    return HRFlowable(width="100%", thickness=0.5, color=SOFT, spaceBefore=2, spaceAfter=5)


def qa(n, q, level, parts):
    items = [P(f"Q{n}. {q}", "DQ"), P(f"[{level}]", "Tag")]
    for p in parts:
        items.append(P(p, "DA") if isinstance(p, str) else p)
    return KeepTogether(items)


def footer(canvas, doc):
    canvas.saveState()
    page = canvas.getPageNumber()
    if page > 1:
        canvas.setFillColor(NAVY)
        canvas.rect(0, A4[1] - 15, A4[0], 15, fill=1, stroke=0)
        canvas.setFillColor(white)
        canvas.setFont("Helvetica", 7.5)
        canvas.drawString(32, A4[1] - 10, "Selenium WebDriver Interview Questions | Java | SDET")
        canvas.drawRightString(A4[0] - 32, A4[1] - 10, "30 Q&A")
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 7.5)
        canvas.drawCentredString(A4[0] / 2, 14, f"Page {page}")
    canvas.restoreState()


def build():
    story = []

    cover = Table([
        [P("Selenium WebDriver", "TMain")],
        [P("Top Interview Questions — Java | SDET Prep<br/><br/>"
           "Total: 30 &nbsp;|&nbsp; Commands · Waits · Locators · Windows · Framework<br/>"
           "Format: Q&amp;A with code", "TSub")],
    ], colWidths=[6.6 * inch])
    cover.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("TOPPADDING", (0, 0), (-1, -1), 26),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 20),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
    ]))
    story.append(Spacer(1, 40))
    story.append(cover)
    story.append(Spacer(1, 12))
    story.append(P(
        "Verified &amp; updated for Selenium 4 + real framework practice. "
        "Use for Week 1–2 interview prep.",
        "DBody"
    ))
    story.append(P(
        "Corrections vs older draft: get() vs navigate().to(), mixing waits, PageFactory.initElements, "
        "Actions.perform(), custom dropdowns, @BeforeMethod browser isolation, absolute upload path.",
        "DFix"
    ))
    story.append(PageBreak())

    # SECTION 1
    story.append(P("SECTION 1: WebDriver Basics", "DH1"))
    story.append(hline())

    story.append(qa(1, "What is Selenium WebDriver?", "Easy", [
        "Selenium WebDriver is a browser automation API/library that controls real browsers through "
        "browser-specific drivers (ChromeDriver, GeckoDriver, etc.) using the W3C WebDriver protocol. "
        "Unlike old Selenium RC, it does not need a separate Selenium server in the middle for basic local runs.",
    ]))

    story.append(qa(2, "What is the difference between driver.get() and driver.navigate().to()?", "Easy", [
        "Both open a URL. In modern Selenium 3/4, <b>navigate().to(url) typically behaves like get(url)</b> "
        "for page load (both wait for document ready in normal usage).",
        "The real difference: <b>Navigation</b> interface also provides <b>back(), forward(), refresh()</b> "
        "and works with browser history. get() is the simple “open this URL” convenience method.",
        code('driver.get("https://example.com");\n'
             'driver.navigate().to("https://example.com");\n'
             'driver.navigate().back();\n'
             'driver.navigate().forward();\n'
             'driver.navigate().refresh();'),
        tip("Don’t say “get waits for load but navigate doesn’t” — that is outdated and can lose marks."),
    ]))

    story.append(qa(3, "How do you get the current page title and URL?", "Easy", [
        code('String title = driver.getTitle();\nString url = driver.getCurrentUrl();'),
    ]))

    story.append(qa(4, "What does driver.close() vs driver.quit() do?", "Easy", [
        "<b>close():</b> closes the current window/tab. Session may stay open if other windows exist.",
        "<b>quit():</b> ends the entire WebDriver session and closes all windows. Prefer quit() in teardown "
        "to avoid orphaned browser processes. In method-level isolation frameworks, call quit() in @AfterMethod.",
    ]))

    story.append(qa(5, "How do you refresh a web page in Selenium?", "Easy", [
        code('driver.navigate().refresh();              // recommended\n'
             'driver.get(driver.getCurrentUrl());      // re-open same URL\n'
             '// Keys.F5 on body works but is less reliable'),
    ]))

    # SECTION 2
    story.append(P("SECTION 2: Finding Elements", "DH1"))
    story.append(hline())

    story.append(qa(6, "What are the 8 locator strategies in Selenium?", "Easy", [
        "By.id, By.name, By.className, By.tagName, By.linkText, By.partialLinkText, By.cssSelector, By.xpath.",
        "Practical preference (not a strict rule): id → name/css → xpath. Prefer stable attributes over absolute xpath.",
        "Selenium 4 also has <b>Relative Locators</b> (above/below/near) as an additional approach.",
    ]))

    story.append(qa(7, "findElement() vs findElements()?", "Medium", [
        "findElement → single WebElement; throws <b>NoSuchElementException</b> if missing.",
        "findElements → List&lt;WebElement&gt;; returns <b>empty list</b> (no exception) if missing. "
        "Use !list.isEmpty() to check presence without try/catch.",
        code('List<WebElement> els = driver.findElements(By.className("item"));\n'
             'if (!els.isEmpty()) { els.get(0).click(); }'),
    ]))

    story.append(qa(8, "When would you use cssSelector over xpath?", "Medium", [
        "CSS is often cleaner/faster enough for most lookups (id, class, attributes, hierarchy down).",
        "Use XPath when you need: text-based locate, parent/ancestor axis, following-sibling, complex DOM walks. "
        "Standard CSS cannot select “parent of this element” the way XPath can.",
        code('By.cssSelector("input#email.form-control")\n'
             'By.xpath("//label[text()=\'Email\']/following-sibling::input")'),
    ]))

    story.append(qa(9, "How do you write a dynamic xpath for changing attributes?", "Hard", [
        code('// id like btn_1234\n'
             'By.xpath("//button[contains(@id,\'btn_\')]")\n'
             'By.xpath("//button[starts-with(@id,\'btn\')]")\n'
             'By.xpath("//h1[normalize-space()=\'Accounts Overview\']")'),
        tip("Prefer data-testid / stable ids from devs over fragile dynamic xpath when possible."),
    ]))

    story.append(qa(10, "What is a relative locator (Selenium 4)?", "Hard", [
        "Find elements relative to another: above, below, toLeftOf, toRightOf, near.",
        code('import static org.openqa.selenium.support.locators.RelativeLocator.with;\n\n'
             'WebElement lbl = driver.findElement(By.id("usernameLabel"));\n'
             'WebElement input = driver.findElement(\n'
             '    with(By.tagName("input")).below(lbl));'),
    ]))

    story.append(PageBreak())

    # SECTION 3
    story.append(P("SECTION 3: Waits", "DH1"))
    story.append(hline())

    story.append(qa(11, "What are the three types of waits in Selenium?", "Easy", [
        "1) <b>Thread.sleep</b> — hard-coded pause (avoid in real frameworks).",
        "2) <b>Implicit wait</b> — global timeout for findElement polling.",
        "3) <b>Explicit wait (WebDriverWait + ExpectedConditions)</b> — condition-based, preferred.",
        "FluentWait is the flexible base; WebDriverWait is a specialized FluentWait.",
    ]))

    story.append(qa(12, "What is implicit wait and its drawback?", "Medium", [
        "Sets a global poll timeout for finding elements.",
        code('driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10));'),
        "Drawbacks: applies to all finds; slows “element should NOT be present” checks; "
        "mixing with explicit waits makes timing harder to reason about.",
    ]))

    story.append(qa(13, "Write explicit wait for element to be clickable.", "Medium", [
        code('WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(15));\n'
             'WebElement btn = wait.until(\n'
             '    ExpectedConditions.elementToBeClickable(By.id("submitBtn")));\n'
             'btn.click();'),
    ]))

    story.append(qa(14, "What is FluentWait and how is it different from WebDriverWait?", "Hard", [
        "FluentWait lets you set timeout, polling interval, and ignored exceptions. "
        "WebDriverWait extends FluentWait with defaults (commonly 500ms polling) and WebDriver-focused usage.",
        code('Wait<WebDriver> wait = new FluentWait<>(driver)\n'
             '  .withTimeout(Duration.ofSeconds(20))\n'
             '  .pollingEvery(Duration.ofMillis(500))\n'
             '  .ignoring(NoSuchElementException.class);\n'
             'WebElement el = wait.until(d -> d.findElement(By.id("result")));'),
    ]))

    story.append(qa(15, "What happens if you mix implicit and explicit waits?", "Hard", [
        "Behavior becomes <b>hard to predict</b> and can make tests slower or flaky depending on Selenium version "
        "and how findElement is used inside ExpectedConditions.",
        "Best practice in modern frameworks: prefer <b>explicit waits</b> for conditions; keep implicit wait "
        "<b>0 or a small value</b>; don’t rely on both for the same synchronization problem.",
        tip("Say “unpredictable / hard to maintain” rather than quoting a fixed 10+5=15 formula."),
    ]))

    # SECTION 4
    story.append(P("SECTION 4: Element Interactions", "DH1"))
    story.append(hline())

    story.append(qa(16, "How do you handle dropdowns in Selenium?", "Easy", [
        "For native HTML &lt;select&gt; use org.openqa.selenium.support.ui.Select:",
        code('Select dd = new Select(driver.findElement(By.id("country")));\n'
             'dd.selectByVisibleText("India");\n'
             'dd.selectByValue("IN");\n'
             'dd.selectByIndex(2);'),
        "Custom (div-based) dropdowns are NOT Select — click to open, then click option, sometimes with Actions/JS.",
    ]))

    story.append(qa(17, "How do you handle checkboxes and radio buttons?", "Easy", [
        code('WebElement chk = driver.findElement(By.id("terms"));\n'
             'if (!chk.isSelected()) { chk.click(); }\n'
             'Assert.assertTrue(chk.isSelected());'),
        "Always check isSelected() before click so you don’t accidentally uncheck.",
    ]))

    story.append(qa(18, "How do you handle file upload in Selenium?", "Medium", [
        "If the control is &lt;input type=\"file\"&gt;, use sendKeys with an <b>absolute path</b> — no OS dialog automation needed.",
        code('driver.findElement(By.id("fileInput"))\n'
             '  .sendKeys("C:\\\\testdata\\\\sample.pdf");  // absolute path'),
        "If the site only opens a native OS file dialog with no input element, then Robot/AutoIT/Sikuli-type tools may be needed.",
    ]))

    story.append(qa(19, "How do you perform mouse hover using Actions class?", "Medium", [
        code('Actions actions = new Actions(driver);\n'
             'WebElement menu = driver.findElement(By.id("navMenu"));\n'
             'actions.moveToElement(menu).perform();\n'
             '// In Selenium 3 style people used build().perform();\n'
             '// In Selenium 4, perform() is enough (it builds the chain).'),
    ]))

    story.append(qa(20, "How do you handle JavaScript alerts/popups?", "Medium", [
        code('Alert alert = driver.switchTo().alert();\n'
             'String msg = alert.getText();\n'
             'alert.accept();   // OK\n'
             '// alert.dismiss(); // Cancel\n'
             '// alert.sendKeys("text"); // prompt'),
        "These are browser JS alerts, not HTML modals. HTML modals are normal DOM elements.",
    ]))

    story.append(PageBreak())

    # SECTION 5
    story.append(P("SECTION 5: Windows, Frames &amp; Advanced", "DH1"))
    story.append(hline())

    story.append(qa(21, "How do you switch between multiple browser windows/tabs?", "Medium", [
        code('String main = driver.getWindowHandle();\n'
             'for (String h : driver.getWindowHandles()) {\n'
             '  if (!h.equals(main)) driver.switchTo().window(h);\n'
             '}\n'
             '// work in child\n'
             'driver.close();\n'
             'driver.switchTo().window(main);'),
        "Always store the parent handle before opening a new window/tab.",
    ]))

    story.append(qa(22, "How do you handle iframes in Selenium?", "Medium", [
        code('driver.switchTo().frame("frameName"); // name/id\n'
             'driver.switchTo().frame(0);         // index\n'
             'driver.switchTo().frame(frameEl);   // WebElement\n'
             'driver.switchTo().parentFrame();    // one level up\n'
             'driver.switchTo().defaultContent(); // top document'),
        "You cannot interact with elements inside a frame until you switch into it.",
    ]))

    story.append(qa(23, "How do you execute JavaScript using Selenium?", "Hard", [
        code('JavascriptExecutor js = (JavascriptExecutor) driver;\n'
             'js.executeScript("window.scrollTo(0, document.body.scrollHeight)");\n'
             'js.executeScript("arguments[0].click();", element);\n'
             'js.executeScript("arguments[0].value=\'test\';", inputEl);'),
        tip("Prefer normal WebDriver clicks/sends when possible; JS click can hide real UX issues."),
    ]))

    story.append(qa(24, "How do you take a screenshot in Selenium?", "Easy", [
        code('File src = ((TakesScreenshot) driver)\n'
             '    .getScreenshotAs(OutputType.FILE);\n'
             'Files.copy(src.toPath(), Path.of("screenshots/test.png"));\n'
             '// or FileUtils.copyFile(src, dest) with Commons IO'),
    ]))

    story.append(qa(25, "What is StaleElementReferenceException and how to fix it?", "Hard", [
        "The element was found, then DOM refreshed/re-rendered (AJAX, navigation), so the old reference is invalid.",
        "Fix: re-find the element; retry loop; or wait for a stable condition then locate again.",
        code('for (int i = 0; i < 3; i++) {\n'
             '  try {\n'
             '    driver.findElement(By.id("btn")).click();\n'
             '    break;\n'
             '  } catch (StaleElementReferenceException e) {\n'
             '    // re-find on next loop\n'
             '  }\n'
             '}'),
    ]))

    # SECTION 6
    story.append(P("SECTION 6: TestNG + Framework Questions", "DH1"))
    story.append(hline())

    story.append(qa(26, "How do you run tests in parallel in TestNG?", "Hard", [
        code('<suite parallel="methods" thread-count="3">'),
        "Use ThreadLocal&lt;WebDriver&gt; so each thread gets its own driver. Without ThreadLocal, parallel runs corrupt each other.",
    ]))

    story.append(qa(27, "What is Page Object Model (POM)?", "Medium", [
        "Design pattern: each page/screen → one class holding locators + user actions. Tests call methods only "
        "(login, transferFunds) and do assertions. Locators stay out of test classes.",
        code('public class LoginPage {\n'
             '  private By user = By.id("username");\n'
             '  private By pass = By.id("password");\n'
             '  private WebDriver driver;\n'
             '  public LoginPage(WebDriver driver) { this.driver = driver; }\n'
             '  public void login(String u, String p) {\n'
             '    driver.findElement(user).sendKeys(u);\n'
             '    driver.findElement(pass).sendKeys(p);\n'
             '  }\n'
             '}'),
        "If using @FindBy, you <b>must</b> call PageFactory.initElements(driver, this) in the constructor — "
        "otherwise fields stay null.",
    ]))

    story.append(qa(28, "What is @DataProvider in TestNG? How do you use it?", "Medium", [
        "Supplies multiple data sets to one @Test (data-driven). Returns Object[][] (or Iterator).",
        code('@DataProvider(name="credentials")\n'
             'public Object[][] getData() {\n'
             '  return new Object[][] {\n'
             '    {"user1","pass1"}, {"user2","pass2"}\n'
             '  };\n'
             '}\n'
             '@Test(dataProvider="credentials")\n'
             'public void testLogin(String u, String p) { ... }'),
    ]))

    story.append(qa(29, "What is the difference between @BeforeMethod and @BeforeClass?", "Easy", [
        "@BeforeClass: once per class. @BeforeMethod: before every @Test.",
        "In robust Selenium frameworks (including parallel-ready ones), browser setup is often in "
        "<b>@BeforeMethod</b> and quit in <b>@AfterMethod</b> for isolation. @BeforeClass is better for "
        "expensive one-time class setup (e.g., register a shared user) when methods can safely share state.",
    ]))

    story.append(qa(30, "How do you handle dynamic web tables in Selenium?", "Hard", [
        code('List<WebElement> rows = driver.findElements(\n'
             '    By.xpath("//table[@id=\'data\']//tr"));\n'
             'for (WebElement row : rows) {\n'
             '  List<WebElement> cells = row.findElements(By.tagName("td"));\n'
             '  if (!cells.isEmpty()) System.out.println(cells.get(0).getText());\n'
             '}'),
        "Use header maps, contains/text filters, or following-sibling axes to find a row by account number then read balance.",
    ]))

    story.append(PageBreak())

    # Revision
    story.append(P("Quick Revision – One-Liners", "DH1"))
    story.append(hline())
    rows = [
        ["#", "Topic", "Key point"],
        ["1", "WebDriver", "Automates real browsers via drivers / W3C protocol"],
        ["2", "get vs navigate.to", "Both open URL; navigate also back/forward/refresh"],
        ["3", "close vs quit", "One window vs end full session"],
        ["4", "findElement(s)", "Exception vs empty list"],
        ["5", "CSS vs XPath", "CSS simple/downward; XPath axes & text"],
        ["6", "Waits", "Prefer explicit; avoid sleep; careful with implicit"],
        ["7", "Select", "Only native &lt;select&gt;"],
        ["8", "File upload", "sendKeys absolute path on input[type=file]"],
        ["9", "Actions", "Hover/drag; perform() in Selenium 4"],
        ["10", "Alerts", "switchTo().alert()"],
        ["11", "Windows", "windowHandles + switchTo().window"],
        ["12", "Frames", "frame() then defaultContent()"],
        ["13", "JS Executor", "scroll/click/value when needed"],
        ["14", "Stale element", "DOM changed → re-find / retry"],
        ["15", "POM", "Locators+actions in page class; init PageFactory if @FindBy"],
        ["16", "Parallel", "testng parallel + ThreadLocal driver"],
    ]
    data = []
    for i, r in enumerate(rows):
        st = styles["DHead"] if i == 0 else styles["DCell"]
        data.append([Paragraph(c, st) for c in r])
    t = Table(data, colWidths=[0.35 * inch, 1.35 * inch, 4.85 * inch], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT]),
        ("GRID", (0, 0), (-1, -1), 0.35, SOFT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))
    story.append(P(
        "SDET Study Plan · Week 2 · Selenium WebDriver Interview Prep · 30 Questions (verified)",
        "DBody"
    ))

    doc = SimpleDocTemplate(
        str(OUT), pagesize=A4,
        leftMargin=34, rightMargin=34, topMargin=30, bottomMargin=28,
        title="Selenium WebDriver Interview Questions",
        author="SDET Interview Prep",
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print("Updated:", OUT, "bytes=", OUT.stat().st_size)


if __name__ == "__main__":
    build()
