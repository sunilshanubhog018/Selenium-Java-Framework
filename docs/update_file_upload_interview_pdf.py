"""Rebuild File Upload/Download/Screenshots Interview PDF with accuracy fixes."""
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
    r"\File uploaddownload,screenshots"
    r"\File_Upload_Download_Screenshots_InterviewQA.pdf"
)

NAVY = HexColor("#0b3d5c")
TEAL = HexColor("#0f766e")
GREEN = HexColor("#166534")
LIGHT = HexColor("#f0f9ff")
SOFT = HexColor("#e2e8f0")
DARK = HexColor("#1e293b")
MUTED = HexColor("#475569")
GOLD = HexColor("#b45309")
RED = HexColor("#9f1239")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TMain", fontName="Helvetica-Bold", fontSize=14.5,
                          leading=18, textColor=white, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="TSub", fontName="Helvetica", fontSize=9,
                          leading=12, textColor=HexColor("#dbeafe"), alignment=TA_CENTER))
styles.add(ParagraphStyle(name="DH1", fontName="Helvetica-Bold", fontSize=11,
                          leading=13, textColor=NAVY, spaceBefore=7, spaceAfter=3))
styles.add(ParagraphStyle(name="DH2", fontName="Helvetica-Bold", fontSize=9.3,
                          leading=11.5, textColor=TEAL, spaceBefore=5, spaceAfter=2))
styles.add(ParagraphStyle(name="DQ", fontName="Helvetica-Bold", fontSize=8.6,
                          leading=11, textColor=NAVY, spaceBefore=4, spaceAfter=1))
styles.add(ParagraphStyle(name="DA", fontName="Helvetica", fontSize=8.1,
                          leading=10.4, textColor=DARK, alignment=TA_JUSTIFY, spaceAfter=2))
styles.add(ParagraphStyle(name="DTip", fontName="Helvetica-Oblique", fontSize=7.5,
                          leading=9.5, textColor=GOLD, leftIndent=4, spaceAfter=2))
styles.add(ParagraphStyle(name="DFix", fontName="Helvetica-Oblique", fontSize=7.4,
                          leading=9.4, textColor=GREEN, spaceAfter=3))
styles.add(ParagraphStyle(name="DBody", fontName="Helvetica", fontSize=8.4,
                          leading=10.5, textColor=DARK, spaceAfter=3))
styles.add(ParagraphStyle(name="CodeB", fontName="Courier", fontSize=6.5,
                          leading=8.4, textColor=DARK, backColor=LIGHT, spaceBefore=1, spaceAfter=2))
styles.add(ParagraphStyle(name="DCell", fontName="Helvetica", fontSize=7.1,
                          leading=9, textColor=DARK))
styles.add(ParagraphStyle(name="DHead", fontName="Helvetica-Bold", fontSize=7.1,
                          leading=9, textColor=white))
styles.add(ParagraphStyle(name="LvlB", fontName="Helvetica-Bold", fontSize=7.6,
                          textColor=HexColor("#1d4ed8"), spaceAfter=2))
styles.add(ParagraphStyle(name="LvlR", fontName="Helvetica-Bold", fontSize=7.6,
                          textColor=RED, spaceAfter=2))
styles.add(ParagraphStyle(name="LvlG", fontName="Helvetica-Bold", fontSize=7.6,
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
        canvas.drawString(28, A4[1] - 9, "File Upload · Download · Screenshots | Interview Q&A")
        canvas.drawRightString(A4[0] - 28, A4[1] - 9, "Week 2 · SDET")
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 6.8)
        canvas.drawCentredString(A4[0] / 2, 11, f"Page {page}")
    canvas.restoreState()


def build():
    story = []

    cover = Table([
        [P("File Upload, Download &amp; Screenshots", "TMain")],
        [P("Interview Q&amp;A | SDET 4+ Yrs<br/>"
           "sendKeys upload · Chrome/Firefox prefs · Grid · Allure/Extent shots<br/><br/>"
           "PART 1 Fundamentals &nbsp;·&nbsp; PART 2 Senior/Framework &nbsp;·&nbsp; PART 3 Practice Tests",
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
        "Verified for Selenium 4 interviews. Strong original content retained; technical fixes applied "
        "where answers could mislead (paths, Grid, headless downloads, partial files).",
        "DBody"
    ))
    story.append(P(
        "Fixes: absolute path; don’t open OS dialog; LocalFileDetector on RemoteWebDriver; "
        ".crdownload/.part wait; headless download enable; ThreadLocal screenshots; practice-test robustness.",
        "DFix"
    ))
    story.append(PageBreak())

    # PART 1
    story.append(P("PART 1 — FUNDAMENTALS", "DH1"))
    story.append(P("Blue | All levels — know these cold", "LvlB"))
    story.append(hline())

    story.append(qa(1, "How do you upload a file in Selenium WebDriver?", [
        "Best approach: <b>sendKeys(absolutePath)</b> on <font face='Courier'>&lt;input type=\"file\"&gt;</font>. "
        "Do not open the OS file chooser. Works local, headless, and (with LocalFileDetector) on Grid.",
        code('WebElement upload = driver.findElement(By.id("file-upload"));\n'
             'upload.sendKeys(new File("test-data/sample.pdf").getAbsolutePath());\n'
             'driver.findElement(By.id("file-submit")).click();'),
        tip("Always pass an absolute path. Relative paths often fail depending on browser CWD."),
    ]))

    story.append(qa(2, "Why NOT click the file input before sendKeys()?", [
        "Clicking opens the OS native dialog. Selenium controls the browser DOM, not the OS dialog. "
        "The test can hang. sendKeys sets the file on the input and bypasses the dialog.",
    ]))

    story.append(qa(3, "Hidden file input?", [
        "Many UIs hide the input behind a button. Options: (1) sendKeys if Selenium still accepts the element "
        "(2) JS unhide display/visibility/opacity (3) remove hidden attribute (4) as last resort Robot (not CI-friendly).",
        code("((JavascriptExecutor) driver).executeScript(\n"
             "  \"arguments[0].style.display='block';\" +\n"
             "  \"arguments[0].style.visibility='visible';\" +\n"
             "  \"arguments[0].removeAttribute('hidden');\", input);\n"
             "input.sendKeys(absPath);"),
    ]))

    story.append(qa(4, "Configure Chrome auto-download to a folder?", [
        code("ChromeOptions options = new ChromeOptions();\n"
             "Map<String, Object> prefs = new HashMap<>();\n"
             "prefs.put(\"download.default_directory\", absDownloadDir);\n"
             "prefs.put(\"download.prompt_for_download\", false);\n"
             "prefs.put(\"download.directory_upgrade\", true);\n"
             "prefs.put(\"plugins.always_open_pdf_externally\", true);\n"
             "options.setExperimentalOption(\"prefs\", prefs);\n"
             "// Selenium 4 headless: also allow downloads\n"
             "options.setEnableDownloads(true);  // when available in your version"),
        "Use an absolute download directory path.",
    ]))

    story.append(qa(5, "Verify download completed?", [
        "Poll until file exists AND length &gt; 0 AND no partial sidecar files: Chrome <b>.crdownload</b>, "
        "Firefox <b>.part</b>. Better: size stable across two polls. For critical banking docs, assert content "
        "(CSV headers / PDFBox text), not only existence.",
    ]))

    story.append(qa(6, "Screenshot types in Selenium?", [
        "OutputType.<b>FILE</b>, <b>BASE64</b>, <b>BYTES</b>. "
        "Selenium 4: WebElement.getScreenshotAs for element shots. "
        "Full page: Firefox HasFullPageScreenshot / getFullPageScreenshotAs; Chrome often needs CDP "
        "(captureBeyondViewport) or a library (AShot).",
    ]))

    story.append(qa(7, "Element-level screenshot?", [
        code("File shot = element.getScreenshotAs(OutputType.FILE);\n"
             "Files.copy(shot.toPath(), Path.of(\"shots/el.png\"));\n"
             "// or FileUtils.copyFile(...)"),
    ]))

    story.append(qa(8, "Automatic screenshot on failure?", [
        "TestNG ITestListener.onTestFailure: get driver from test instance (BaseTest.getDriver()), "
        "capture FILE/BASE64, unique name (method + timestamp + threadId), attach to Extent/Allure.",
        code("@Override\n"
             "public void onTestFailure(ITestResult r) {\n"
             "  WebDriver d = ((BaseTest) r.getInstance()).getDriver();\n"
             "  File src = ((TakesScreenshot) d).getScreenshotAs(OutputType.FILE);\n"
             "  // save under screenshots/failures/\n"
             "}"),
    ]))

    story.append(qa(9, "Robot vs sendKeys for upload?", [
        "sendKeys = DOM-level, preferred (headless/Grid). Robot = OS keyboard, brittle, fails on Linux CI/headless. "
        "Use Robot only if there is truly no file input.",
    ]))

    story.append(qa(10, "Upload multiple files?", [
        "If input has multiple attribute, join absolute paths with newline <b>\\n</b>:",
        code("input.sendKeys(abs1 + \"\\n\" + abs2 + \"\\n\" + abs3);"),
    ]))

    story.append(PageBreak())

    # PART 2
    story.append(P("PART 2 — SENIOR / FRAMEWORK LEVEL", "DH1"))
    story.append(P("Red | 4+ years · design · Grid · CI · banking", "LvlR"))
    story.append(hline())

    story.append(P("Framework design", "DH2"))
    story.append(qa(11, "Reusable file upload utility?", [
        "FileUploadUtils: validate File.exists(), resolve absolute path, find input, unhide if needed, "
        "sendKeys, log. Optional Grid LocalFileDetector setup when driver is RemoteWebDriver.",
    ]))
    story.append(qa(12, "Download verification for CI?", [
        "Per-test download dir; poll for complete file (no .crdownload); size/content checks; "
        "@BeforeMethod clean dir; headless-compatible browser prefs.",
        code("public File waitForFile(String dir, String nameContains, int timeoutSec) {\n"
             "  long end = System.currentTimeMillis() + timeoutSec * 1000L;\n"
             "  while (System.currentTimeMillis() < end) {\n"
             "    File[] files = new File(dir).listFiles();\n"
             "    if (files != null) for (File f : files) {\n"
             "      if (f.getName().endsWith(\".crdownload\") || f.getName().endsWith(\".part\")) continue;\n"
             "      if (f.getName().contains(nameContains) && f.length() > 0) return f;\n"
             "    }\n"
             "    Thread.sleep(300);\n"
             "  }\n"
             "  throw new TimeoutException(\"Download not finished\");\n"
             "}"),
    ]))

    story.append(P("Edge cases", "DH2"))
    story.append(qa(13, "Upload works local, fails on Selenium Grid?", [
        "Remote node doesn’t have your local path. Fix:",
        code("((RemoteWebDriver) driver).setFileDetector(new LocalFileDetector());\n"
             "upload.sendKeys(localAbsolutePath); // Selenium transfers file to node"),
        "Robot/AutoIT will not work on Grid. LocalFileDetector only applies to RemoteWebDriver sessions.",
    ]))
    story.append(qa(14, "Flaky downloads in CI?", [
        "Unique download dir per thread/test; wait until partial files gone; size stable twice; "
        "retry network blips; clean dir before test; absolute prefs paths.",
    ]))
    story.append(qa(15, "Upload validation negative tests?", [
        "Wrong extension, oversize, empty 0-byte, special chars in name, missing required file, "
        "duplicate upload — assert UI error messages (critical for KYC).",
    ]))
    story.append(qa(16, "Screenshots filling CI storage?", [
        "Only on failure; BASE64/BYTES into Allure/Extent; retention/delete old artifacts; "
        "optional cloud lifecycle; don’t screenshot every step in CI.",
    ]))

    story.append(P("Banking scenarios", "DH2"))
    story.append(qa(17, "E2E KYC document upload?", [
        "Login → KYC → doc type → front/back sendKeys → preview assert → submit → pending status → "
        "ops queue check. Negatives: format/size/expiry/duplicate.",
    ]))
    story.append(qa(18, "Download account statement date range?", [
        "Set download prefs → filter dates → download PDF/CSV → wait complete → assert filename → "
        "PDFBox/CSV parse for account, period, balances vs UI summary.",
    ]))

    story.append(P("Parallel", "DH2"))
    story.append(qa(19, "Downloads in parallel?", [
        "Never one shared download folder. Unique dir per method/thread when creating ChromeOptions; "
        "ThreadLocal driver; clean each dir independently.",
    ]))
    story.append(qa(20, "Screenshot captured wrong browser in parallel?", [
        "Static shared WebDriver. Use ThreadLocal; listener uses result.getInstance() driver; "
        "unique filenames with thread id / test name.",
    ]))

    story.append(P("Behavioral", "DH2"))
    story.append(qa(21, "Hard upload automation story (STAR)?", [
        "Hidden third-party dropzone → Robot failed on Linux CI → found dynamic file input → "
        "JS reveal + sendKeys → headless/Grid OK → team pattern documented.",
    ]))

    story.append(P("Rapid fire", "DH2"))
    rf = [
        ["TakesScreenshot types?", "FILE, BASE64, BYTES"],
        ["Upload headless?", "Yes with sendKeys (not Robot)"],
        ["Element screenshot since?", "Selenium 4"],
        ["Full page FF vs Chrome?", "FF native API; Chrome often CDP"],
        ["Upload on Grid?", "LocalFileDetector + sendKeys"],
        ["Chrome auto-download pref?", "download.prompt_for_download=false"],
        ["Partial Chrome file?", ".crdownload still downloading"],
        ["Parallel downloads?", "Unique directory per thread"],
        ["Failure screenshots?", "ITestListener.onTestFailure"],
        ["Path type for sendKeys?", "Absolute path"],
    ]
    data = [[Paragraph(h, styles["DHead"]) for h in ["Question", "Answer"]]]
    for a, b in rf:
        data.append([Paragraph(a, styles["DCell"]), Paragraph(b, styles["DCell"])])
    t = Table(data, colWidths=[2.4 * inch, 4.1 * inch], repeatRows=1)
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

    # PART 3
    story.append(P("PART 3 — PRACTICE TESTS", "DH1"))
    story.append(P("Green | the-internet.herokuapp.com | absolute paths + waits", "LvlG"))
    story.append(hline())

    story.append(P("Test 1 — Upload &amp; verify filename", "DH2"))
    story.append(code(
        "driver.get(\"https://the-internet.herokuapp.com/upload\");\n"
        "Path p = Path.of(\"test-data\", \"sample.txt\");\n"
        "Files.createDirectories(p.getParent());\n"
        "Files.writeString(p, \"Test upload content\");\n"
        "driver.findElement(By.id(\"file-upload\"))\n"
        "  .sendKeys(p.toAbsolutePath().toString());\n"
        "driver.findElement(By.id(\"file-submit\")).click();\n"
        "Assert.assertEquals(driver.findElement(By.id(\"uploaded-files\")).getText().trim(),\n"
        "  \"sample.txt\");\n"
        "Assert.assertEquals(driver.findElement(By.tagName(\"h3\")).getText(), \"File Uploaded!\");\n"
        "Files.deleteIfExists(p);"
    ))

    story.append(P("Test 2 — Download &amp; verify (needs Chrome download dir prefs in BaseTest)", "DH2"))
    story.append(code(
        "driver.get(\"https://the-internet.herokuapp.com/download\");\n"
        "WebElement link = driver.findElement(By.cssSelector(\".example a\"));\n"
        "String name = link.getText().trim();\n"
        "link.click();\n"
        "File f = new File(downloadDir, name);\n"
        "new WebDriverWait(driver, Duration.ofSeconds(30)).until(d ->\n"
        "  f.exists() && f.length() > 0 &&\n"
        "  !new File(downloadDir, name + \".crdownload\").exists());\n"
        "Assert.assertTrue(f.length() > 0);\n"
        "f.delete();"
    ))

    story.append(P("Test 3 — Screenshot types", "DH2"))
    story.append(code(
        "driver.get(\"https://the-internet.herokuapp.com/challenging_dom\");\n"
        "File view = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);\n"
        "Files.copy(view.toPath(), Path.of(\"screenshots/viewport.png\"),\n"
        "  StandardCopyOption.REPLACE_EXISTING);\n"
        "File el = driver.findElement(By.tagName(\"table\"))\n"
        "  .getScreenshotAs(OutputType.FILE);\n"
        "Files.copy(el.toPath(), Path.of(\"screenshots/table.png\"),\n"
        "  StandardCopyOption.REPLACE_EXISTING);\n"
        "String b64 = ((TakesScreenshot) driver).getScreenshotAs(OutputType.BASE64);\n"
        "byte[] bytes = ((TakesScreenshot) driver).getScreenshotAs(OutputType.BYTES);\n"
        "Assert.assertTrue(b64.length() > 100 && bytes.length > 0);"
    ))

    story.append(P("Test 4 — Before/after dynamic load screenshots", "DH2"))
    story.append(code(
        "driver.get(\"https://the-internet.herokuapp.com/dynamic_loading/2\");\n"
        "Files.copy(((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE).toPath(),\n"
        "  Path.of(\"screenshots/before.png\"), StandardCopyOption.REPLACE_EXISTING);\n"
        "driver.findElement(By.cssSelector(\"#start button\")).click();\n"
        "WebElement hi = new WebDriverWait(driver, Duration.ofSeconds(15)).until(\n"
        "  ExpectedConditions.visibilityOfElementLocated(By.cssSelector(\"#finish h4\")));\n"
        "Files.copy(((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE).toPath(),\n"
        "  Path.of(\"screenshots/after.png\"), StandardCopyOption.REPLACE_EXISTING);\n"
        "Assert.assertEquals(hi.getText(), \"Hello World!\");"
    ))
    story.append(P(
        "Do not assert screenshot file sizes always differ — compression can make sizes equal. "
        "Assert content text; use size difference only as a weak secondary check.",
        "DTip"
    ))

    story.append(P("Test 5 — Negative / special filename", "DH2"))
    story.append(code(
        "// Empty submit — site may return error page; assert error OR still on upload\n"
        "driver.get(\"https://the-internet.herokuapp.com/upload\");\n"
        "driver.findElement(By.id(\"file-submit\")).click();\n"
        "Assert.assertTrue(driver.getPageSource().contains(\"Internal Server Error\")\n"
        "  || driver.getCurrentUrl().contains(\"upload\"));\n\n"
        "// Spaces in filename\n"
        "Path p = Path.of(\"test-data\", \"my file (1).txt\");\n"
        "Files.createDirectories(p.getParent());\n"
        "Files.writeString(p, \"special name\");\n"
        "driver.get(\"https://the-internet.herokuapp.com/upload\");\n"
        "driver.findElement(By.id(\"file-upload\")).sendKeys(p.toAbsolutePath().toString());\n"
        "driver.findElement(By.id(\"file-submit\")).click();\n"
        "Assert.assertEquals(driver.findElement(By.id(\"uploaded-files\")).getText().trim(),\n"
        "  \"my file (1).txt\");"
    ))

    story.append(Spacer(1, 6))
    story.append(hline())
    story.append(P(
        "End of File Upload / Download / Screenshots Interview Q&amp;A — verified for Selenium 4.",
        "DBody"
    ))

    doc = SimpleDocTemplate(
        str(OUT), pagesize=A4,
        leftMargin=30, rightMargin=30, topMargin=26, bottomMargin=24,
        title="File Upload Download Screenshots Interview Q&A",
        author="SDET Week 2",
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print("Updated:", OUT, "bytes=", OUT.stat().st_size)


if __name__ == "__main__":
    build()
