package week2.seleniumcore;

import org.openqa.selenium.*;
import org.openqa.selenium.support.ui.*;
import org.testng.Assert;
import org.testng.annotations.*;

import base.BaseTest;
import utils.Utils;

import java.io.File;
import java.time.Duration;
import java.util.List;


public class FileuploadDownloadScreenshots extends BaseTest {

    // Base URL - defined once, all page URLs built from this
    // If domain changes (e.g., staging), change only this one line
    private static final String BASE_URL = "https://the-internet.herokuapp.com";
    private static final String UPLOAD_URL = BASE_URL + "/upload";              // Page with file input + submit button
    private static final String DOWNLOAD_URL = BASE_URL + "/download";          // Page with list of downloadable file links
    private static final String CHALLENGING_DOM_URL = BASE_URL + "/challenging_dom"; // Complex page with table - good for screenshots
    private static final String DYNAMIC_LOAD_URL = BASE_URL + "/dynamic_loading/2"; // Page where content appears after clicking Start

    // ================================================================
    //  TEST 1: Single File Upload (sendKeys)
    //  Goal: Verify the most basic upload scenario works
    //  Banking example: Customer uploads PAN card during KYC
    // ================================================================
    @Test(priority = 1, description = "Upload single file and verify filename on success page")
    public void testSingleFileUpload() {

        // Step 1: Create a real .txt file on disk inside test-data/ directory
        // This simulates having a document ready to upload (like a scanned PAN card)
        // Utils.createTestFile() writes content to file and returns the File object
        File testFile = Utils.createTestFile(testDataDir, "sample_upload.txt", "Upload test content.");

        // Step 2: Open the upload page
        // This page has: <input type="file" id="file-upload"> and <button id="file-submit">
        driver.get(UPLOAD_URL);

        // Step 3: Find the file input element
        // This is the "Choose File" button on the page
        // HTML: <input type="file" id="file-upload">
        WebElement fileInput = driver.findElement(By.id("file-upload"));

        // Step 4: Send the absolute file path to the input element
        // IMPORTANT: Do NOT call fileInput.click() before this!
        // .click() opens the OS file dialog which Selenium CANNOT control
        // .sendKeys() bypasses the dialog entirely - sets file path directly on the element
        // testFile.getAbsolutePath() returns full path like: C:\Users\nice\...\test-data\sample_upload.txt
        fileInput.sendKeys(testFile.getAbsolutePath());

        // Step 5: Click the Upload button to submit the file
        driver.findElement(By.id("file-submit")).click();

        // Step 6: Verify the success header "File Uploaded!" appears on the result page
        Assert.assertEquals(driver.findElement(By.tagName("h3")).getText(),
                "File Uploaded!", "Success header missing!");

        // Step 7: Verify the uploaded filename matches what we sent
        // .trim() removes any leading/trailing whitespace from the text
        Assert.assertEquals(driver.findElement(By.id("uploaded-files")).getText().trim(),
                "sample_upload.txt", "Uploaded filename mismatch!");
    }

    // ================================================================
    //  TEST 2: Upload Without File (Negative Test)
    //  Goal: Verify app handles empty upload gracefully (doesn't crash)
    //  Banking example: Customer clicks Submit without attaching KYC document
    // ================================================================
    @Test(priority = 2, description = "Submit without file - verify error handling")
    public void testUploadWithoutFile() {

        // Step 1: Open the upload page
        driver.get(UPLOAD_URL);

        // Step 2: Click Submit WITHOUT selecting any file first
        // This is a negative test - testing what happens when user makes a mistake
        driver.findElement(By.id("file-submit")).click();

        // Step 3: Get the entire page source (HTML) to check for error messages
        // We check multiple possible error texts because different servers return different errors
        String pageSource = driver.getPageSource();
        boolean hasError = pageSource.contains("Internal Server Error")  // Server-side error
                || pageSource.contains("No file")                        // Validation message
                || pageSource.contains("error");                         // Generic error

        // Step 4: Assert that SOME error occurred (app didn't silently accept empty upload)
        Assert.assertTrue(hasError, "Expected error for empty upload!");

        // Step 5: Take a screenshot of the error page as evidence
        // In banking projects, screenshots serve as audit trail / proof of testing
        // (TakesScreenshot) driver - casts WebDriver to TakesScreenshot interface
        // OutputType.FILE - saves screenshot as a temporary file
        File src = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);

        // Step 6: Copy the temp screenshot to our screenshots/ directory with a meaningful name
        Utils.saveScreenshot(src, screenshotDir, "test2_no_file_error.png");
    }

    // ================================================================
    //  TEST 3: Upload File With Special Characters in Filename
    //  Goal: Verify filenames with spaces, parentheses are handled correctly
    //  Banking example: Customer saves doc as "PAN Card (1).pdf" - common on Windows
    // ================================================================
    @Test(priority = 3, description = "Upload file with spaces & special chars in name")
    public void testUploadSpecialCharFilename() {

        // Step 1: Create file with spaces and parentheses in the name
        // Real users often have files like "PAN Card (1).pdf" or "Aadhaar front (copy).jpg"
        File testFile = Utils.createTestFile(testDataDir, "my document (copy 1).txt", "Special chars test.");

        // Step 2: Open upload page
        driver.get(UPLOAD_URL);

        // Step 3: Select file and submit (same sendKeys technique as Test 1)
        driver.findElement(By.id("file-upload")).sendKeys(testFile.getAbsolutePath());
        driver.findElement(By.id("file-submit")).click();

        // Step 4: Verify upload succeeded
        Assert.assertEquals(driver.findElement(By.tagName("h3")).getText(),
                "File Uploaded!", "Upload failed for special char filename!");

        // Step 5: Verify the filename with special chars was preserved exactly
        // This is the key assertion - spaces and parentheses should NOT be stripped or encoded
        Assert.assertEquals(
                driver.findElement(By.id("uploaded-files")).getText().trim(),
                "my document (copy 1).txt", "Filename not preserved!");
    }

    // ================================================================
    //  TEST 4: Hidden File Input - JS Unhide + sendKeys
    //  Goal: Handle modern UIs where file input is hidden behind styled button/drag-drop zone
    //  Banking example: Modern banking apps hide ugly default file input behind custom UI
    // ================================================================
    @Test(priority = 4, description = "JS unhide hidden input, then upload via sendKeys")
    public void testHiddenInputUpload() {

        // Step 1: Create test file
        File testFile = Utils.createTestFile(testDataDir, "hidden_test.txt", "Hidden input test.");

        // Step 2: Open upload page
        driver.get(UPLOAD_URL);

        // Step 3: Cast driver to JavascriptExecutor to run JS commands in the browser
        // We need this to manipulate CSS styles of the element
        JavascriptExecutor js = (JavascriptExecutor) driver;

        // Step 4: Find the file input element
        WebElement fileInput = driver.findElement(By.id("file-upload"));

        // Step 5: HIDE the file input using JavaScript (simulating a real-world hidden input)
        // In real apps, the input is already hidden - here we hide it ourselves to practice the technique
        // display:none = element takes no space, invisible
        // visibility:hidden = element takes space but invisible
        js.executeScript(
                "arguments[0].style.display='none';" +       // arguments[0] refers to fileInput
                "arguments[0].style.visibility='hidden';", fileInput);

        // Step 6: Verify the element is now hidden
        // .isDisplayed() returns false when element has display:none or visibility:hidden
        Assert.assertFalse(fileInput.isDisplayed(), "Input should be hidden!");

        // Step 7: UNHIDE the element using JavaScript (this is the actual framework technique)
        // We restore all CSS properties that could hide it:
        // display:block = make it visible and take space
        // visibility:visible = make it visible
        // height/width:auto = ensure it's not collapsed to 0x0 pixels
        js.executeScript(
                "arguments[0].style.display='block';" +
                "arguments[0].style.visibility='visible';" +
                "arguments[0].style.height='auto';" +
                "arguments[0].style.width='auto';", fileInput);

        // Step 8: Now that input is visible, sendKeys() works normally
        fileInput.sendKeys(testFile.getAbsolutePath());

        // Step 9: Submit the upload
        driver.findElement(By.id("file-submit")).click();

        // Step 10: Verify upload succeeded
        Assert.assertEquals(driver.findElement(By.tagName("h3")).getText(),
                "File Uploaded!", "Hidden input upload failed!");
        Assert.assertEquals(
                driver.findElement(By.id("uploaded-files")).getText().trim(),
                "hidden_test.txt", "Filename mismatch!");
    }

    // ================================================================
    //  TEST 5: Single File Download + Verification
    //  Goal: Download a file and verify it actually saved to disk
    //  Banking example: Customer downloads monthly account statement PDF
    // ================================================================
    @Test(priority = 5, description = "Download file, poll directory, verify existence & size")
    public void testFileDownload() {

        // Step 1: Open the download page (has a list of file links)
        driver.get(DOWNLOAD_URL);

        // Step 2: Find all download links on the page
        // CSS selector: a[href*='download/'] = all <a> tags whose href contains "download/"
        // findElements (plural) returns a List - even if 0 matches, no exception thrown
        List<WebElement> links = driver.findElements(By.cssSelector("a[href*='download/']"));

        // Step 3: Assert at least one download link exists
        Assert.assertTrue(links.size() > 0, "No download links found!");

        // Step 4: Get the filename from the link text (e.g., "some-file.txt")
        // .trim() removes whitespace around the text
        String fileName = links.get(0).getText().trim();

        // Step 5: Click the link to trigger download
        // Chrome will auto-download to our downloadDir (configured in BaseTest setUp)
        // No "Save As" dialog appears because we set download.prompt_for_download = false
        links.get(0).click();

        // Step 6: Wait for the file to appear in download directory
        // Utils.waitForDownload() polls every 500ms for up to 30 seconds
        // It also checks that .crdownload partial file is gone (download complete)
        // Returns the File object if found, or null if timeout
        File downloaded = Utils.waitForDownload(downloadDir, fileName, 30);

        // Step 7: Verify file downloaded successfully
        // assertNotNull - file was found within 30 seconds
        Assert.assertNotNull(downloaded, "File not downloaded: " + fileName);
        // .exists() - file is physically on disk
        Assert.assertTrue(downloaded.exists(), "File does not exist: " + fileName);
        // .length() > 0 - file is not empty (0 bytes = failed/corrupted download)
        Assert.assertTrue(downloaded.length() > 0, "File is empty: " + fileName);
    }

    // ================================================================
    //  TEST 6: Multiple File Downloads
    //  Goal: Download 2 files sequentially, verify both arrived
    //  Banking example: Download Jan statement + Feb statement in one session
    // ================================================================
    @Test(priority = 6, description = "Download 2 files and verify both exist")
    public void testMultipleFileDownloads() {

        // Step 1: Open download page
        driver.get(DOWNLOAD_URL);

        // Step 2: Find all download links
        List<WebElement> links = driver.findElements(By.cssSelector("a[href*='download/']"));

        // Step 3: Assert at least 2 links available (we need to download 2 files)
        Assert.assertTrue(links.size() >= 2, "Need at least 2 links!");

        // Step 4: Download FIRST file
        String file1Name = links.get(0).getText().trim();  // Get filename from link text
        links.get(0).click();                                // Trigger download
        File file1 = Utils.waitForDownload(downloadDir, file1Name, 30);  // Wait for it
        Assert.assertNotNull(file1, "File 1 not downloaded: " + file1Name);
        Assert.assertTrue(file1.length() > 0, "File 1 is empty!");

        // Step 5: Brief pause before second download
        // Gives Chrome a moment to finish any background cleanup from first download
        try { Thread.sleep(1000); } catch (InterruptedException ignored) {}

        // Step 6: Download SECOND file
        String file2Name = links.get(1).getText().trim();
        links.get(1).click();
        File file2 = Utils.waitForDownload(downloadDir, file2Name, 30);
        Assert.assertNotNull(file2, "File 2 not downloaded: " + file2Name);
        Assert.assertTrue(file2.length() > 0, "File 2 is empty!");

        // Step 7: Verify both files exist in the download directory
        // .listFiles() returns array of all files in the directory
        File[] allFiles = new File(downloadDir).listFiles();
        Assert.assertNotNull(allFiles);
        Assert.assertTrue(allFiles.length >= 2,
                "Expected 2+ files, found: " + allFiles.length);
    }

    // ================================================================
    //  TEST 7: Viewport Screenshot
    //  Goal: Capture what's visible in the browser window and save as PNG
    //  Banking example: Screenshot of dashboard after login for audit trail
    // ================================================================
    @Test(priority = 7, description = "Capture viewport screenshot and verify saved file")
    public void testViewportScreenshot() {

        // Step 1: Open a page with rich visual content (table, buttons, canvas)
        driver.get(CHALLENGING_DOM_URL);

        // Step 2: Cast driver to TakesScreenshot and capture the VIEWPORT (visible area only)
        // OutputType.FILE = saves as a temporary PNG file in system temp directory
        // This captures ONLY what's visible on screen - not the scrollable content below
        File src = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);

        // Step 3: Copy the temp file to our screenshots/ directory with a meaningful name
        // The temp file gets deleted when JVM exits - so we must copy it
        File saved = Utils.saveScreenshot(src, screenshotDir, "test7_viewport.png");

        // Step 4: Verify the screenshot was saved successfully
        Assert.assertTrue(saved.exists(), "Screenshot not saved!");

        // Step 5: Verify it's not an empty file (0 bytes = screenshot failed)
        Assert.assertTrue(saved.length() > 0, "Screenshot is empty!");

        // Step 6: Verify it saved as PNG format
        Assert.assertTrue(saved.getName().endsWith(".png"), "Should be PNG!");
    }

    // ================================================================
    //  TEST 8: Element-Level Screenshot (Selenium 4 feature)
    //  Goal: Capture ONLY a specific element, not the whole page
    //  Banking example: Screenshot of just the error message or account summary widget
    // ================================================================
    @Test(priority = 8, description = "Element screenshot vs viewport size comparison")
    public void testElementScreenshot() {

        // Step 1: Open page with identifiable elements
        driver.get(CHALLENGING_DOM_URL);

        // Step 2: Take VIEWPORT screenshot (full visible page) for size comparison later
        File vpSrc = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);
        File vpFile = Utils.saveScreenshot(vpSrc, screenshotDir, "test8_viewport.png");

        // Step 3: Find the table element on the page
        WebElement table = driver.findElement(By.tagName("table"));

        // Step 4: Verify table is visible (can't screenshot invisible elements)
        Assert.assertTrue(table.isDisplayed(), "Table not visible!");

        // Step 5: Take ELEMENT screenshot - Selenium 4 exclusive feature!
        // Called directly on WebElement, NOT on driver
        // Captures ONLY the table - not the header, buttons, or anything else on the page
        File elSrc = table.getScreenshotAs(OutputType.FILE);
        File elFile = Utils.saveScreenshot(elSrc, screenshotDir, "test8_table_element.png");

        // Step 6: Verify element screenshot exists and is not empty
        Assert.assertTrue(elFile.exists(), "Element screenshot missing!");
        Assert.assertTrue(elFile.length() > 0, "Element screenshot empty!");

        // Step 7: Element screenshot should be SMALLER than viewport screenshot
        // Because it captures only the table, not the entire page
        // Open both PNGs in screenshots/ folder to visually confirm the difference
        Assert.assertTrue(elFile.length() < vpFile.length(),
                "Element shot should be smaller! Element: " + elFile.length()
                + " | Viewport: " + vpFile.length());
    }

    // ================================================================
    //  TEST 9: Screenshot Before & After Dynamic Content Load
    //  Goal: Capture page state before and after an action (loading, payment, etc.)
    //  Banking example: Screenshot before fund transfer + screenshot after success
    // ================================================================
    @Test(priority = 9, description = "Before/after screenshots with dynamic loading")
    public void testScreenshotBeforeAfterDynamic() {

        // Step 1: Open the dynamic loading page
        // This page shows only a "Start" button initially
        driver.get(DYNAMIC_LOAD_URL);

        // Step 2: Take BEFORE screenshot (page shows only Start button, no content yet)
        File beforeSrc = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);
        File beforeFile = Utils.saveScreenshot(beforeSrc, screenshotDir, "test9_before.png");
        Assert.assertTrue(beforeFile.exists(), "Before screenshot missing!");

        // Step 3: Click the Start button to trigger content loading
        // After clicking, a loading bar/spinner appears for ~5 seconds
        driver.findElement(By.cssSelector("#start button")).click();

        // Step 4: Wait for the dynamic content to appear
        // ExplicitWait waits up to 15 seconds for the <h4> inside #finish to become visible
        // The page loads "Hello World!" text after the loading animation finishes
        WebDriverWait explicitWait = new WebDriverWait(driver, Duration.ofSeconds(15));
        WebElement result = explicitWait.until(
                ExpectedConditions.visibilityOfElementLocated(By.cssSelector("#finish h4")));

        // Step 5: Take AFTER screenshot (page now shows "Hello World!" text)
        File afterSrc = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);
        File afterFile = Utils.saveScreenshot(afterSrc, screenshotDir, "test9_after.png");
        Assert.assertTrue(afterFile.exists(), "After screenshot missing!");

        // Step 6: Verify the loaded content is correct
        Assert.assertEquals(result.getText(), "Hello World!", "Content mismatch!");

        // Open test9_before.png and test9_after.png side by side to see the difference!
    }

    // ================================================================
    //  TEST 10: Base64 and Bytes Screenshot Output Types
    //  Goal: Test all screenshot output formats used in CI/CD reporting
    //  Banking example: Allure reports use Base64/Bytes to embed screenshots inline
    // ================================================================
    @Test(priority = 10, description = "Test Base64 and BYTES screenshot output types")
    public void testBase64AndBytesScreenshot() {

        // Step 1: Open any page with content
        driver.get(CHALLENGING_DOM_URL);

        // ---- OUTPUT TYPE 1: Base64 String ----
        // Used for: Embedding screenshots directly inside HTML reports (Allure, ExtentReports)
        // The screenshot becomes a long text string like "iVBORw0KGgoAAAANSUh..."
        // Reports embed this string as: <img src="data:image/png;base64,iVBORw0K..." />
        String base64 = ((TakesScreenshot) driver).getScreenshotAs(OutputType.BASE64);

        // Step 2: Verify Base64 string is not null and not empty
        Assert.assertNotNull(base64, "Base64 is null!");

        // Step 3: Verify string is long enough to be a real image (not just a few characters)
        Assert.assertTrue(base64.length() > 100, "Base64 too short!");

        // Step 4: Verify it's valid Base64 by decoding it
        // If the string is corrupted/invalid, .decode() throws IllegalArgumentException
        byte[] decoded = java.util.Base64.getDecoder().decode(base64);
        Assert.assertTrue(decoded.length > 0, "Decoded Base64 empty!");

        // ---- OUTPUT TYPE 2: Byte Array ----
        // Used for: Allure @Attachment annotation which accepts byte[]
        // Example: @Attachment(value="Screenshot", type="image/png")
        //          public byte[] takeScreenshot() { return driver.getScreenshotAs(OutputType.BYTES); }
        byte[] bytes = ((TakesScreenshot) driver).getScreenshotAs(OutputType.BYTES);

        // Step 5: Verify byte array is not null and not empty
        Assert.assertNotNull(bytes, "Bytes is null!");
        Assert.assertTrue(bytes.length > 0, "Bytes empty!");

        // Step 6: Verify the bytes represent a valid PNG image
        // Every PNG file starts with the same 4 "magic number" bytes: 137 80 78 71
        // 137 = non-ASCII marker (prevents text editors from treating PNG as text)
        // 80  = letter 'P'
        // 78  = letter 'N'
        // 71  = letter 'G'
        // This is how programs detect "is this file really a PNG?"
        // bytes[0] & 0xFF converts signed byte (-128 to 127) to unsigned int (0 to 255)
        Assert.assertEquals(bytes[0] & 0xFF, 137, "Not PNG - byte 0");
        Assert.assertEquals(bytes[1] & 0xFF, 80,  "Not PNG - byte 1 (P)");
        Assert.assertEquals(bytes[2] & 0xFF, 78,  "Not PNG - byte 2 (N)");
        Assert.assertEquals(bytes[3] & 0xFF, 71,  "Not PNG - byte 3 (G)");
    }
}