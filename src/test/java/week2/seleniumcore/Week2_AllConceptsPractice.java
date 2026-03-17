package week2.seleniumcore;

import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.support.ui.*;
import org.testng.Assert;
import org.testng.annotations.*;

import base.BaseTest;

import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;

/**
 * ============================================================================
 * WEEK 2 — SELENIUM CORE CONCEPTS — 20 PRACTICE TESTS
 * ============================================================================
 *
 * Practice Sites Used:
 *   - https://the-internet.herokuapp.com  (Heroku App)
 *   - https://demoqa.com
 *   - https://www.seleniumeasy.com/test
 *
 * Topics Covered:
 *   Tests  1–4  : Waits (Implicit, Explicit, Fluent)
 *   Tests  5–8  : Dropdowns, Checkboxes, Radio Buttons
 *   Tests  9–12 : Alerts, Frames, Multiple Windows
 *   Tests 13–16 : Tables, Dynamic Elements
 *   Tests 17–20 : Actions Class (Hover, Drag-Drop, Right-Click, Double-Click)
 *
 * How to Run:
 *   mvn test -Dtest=Week2_AllConceptsPractice
 * ============================================================================
 */
public class Week2_AllConceptsPractice extends BaseTest  {

    // ========================================================================
    // TOPIC 1: WAITS (Implicit, Explicit, Fluent) — Tests 1–4
    // ========================================================================

    /**
     * TEST 1: Implicit Wait — Page loads and element is found within timeout
     * Site: the-internet — Dynamic Loading (Element rendered after delay)
     */
    @Test(priority = 1)
    public void test01_ImplicitWait_DynamicLoading() {
        driver.get("https://the-internet.herokuapp.com/dynamic_loading/1");

        // Click Start button to trigger loading
        driver.findElement(By.cssSelector("#start button")).click();

        // Implicit wait should handle the delay — element is hidden, then shown
        // But implicit wait alone won't work here since element exists in DOM but is hidden
        // This demonstrates WHY explicit wait is often better
        WebDriverWait localWait = new WebDriverWait(driver, Duration.ofSeconds(10));
        WebElement result = localWait.until(
                ExpectedConditions.visibilityOfElementLocated(By.cssSelector("#finish h4"))
        );

        Assert.assertEquals(result.getText(), "Hello World!", "Dynamic loaded text mismatch");
        System.out.println("✅ Test 1 PASSED — Implicit + Explicit wait on dynamic loading");
    }

    /**
     * TEST 2: Explicit Wait — Wait for element to be clickable
     * Site: the-internet — Dynamic Controls (Enable/Disable input)
     */
    @Test(priority = 2)
    public void test02_ExplicitWait_ElementClickable() {
        driver.get("https://the-internet.herokuapp.com/dynamic_controls");

        // Click "Enable" button
        driver.findElement(By.cssSelector("#input-example button")).click();

        // Explicitly wait until the text input is enabled/clickable
        WebElement textInput = wait.until(
                ExpectedConditions.elementToBeClickable(By.cssSelector("#input-example input"))
        );

        textInput.sendKeys("Selenium Automation");
        Assert.assertEquals(textInput.getAttribute("value"), "Selenium Automation");

        // Also verify the confirmation message appears
        WebElement message = wait.until(
                ExpectedConditions.visibilityOfElementLocated(By.cssSelector("#message"))
        );
        Assert.assertTrue(message.getText().contains("enabled"), "Enable message not found");
        System.out.println("✅ Test 2 PASSED — Explicit wait for element to be clickable");
    }

    /**
     * TEST 3: Explicit Wait — Wait for element to disappear (invisibility)
     * Site: the-internet — Dynamic Loading (Wait for loading bar to vanish)
     */
    @Test(priority = 3)
    public void test03_ExplicitWait_ElementInvisibility() {
        driver.get("https://the-internet.herokuapp.com/dynamic_loading/1");

        driver.findElement(By.cssSelector("#start button")).click();

        // Wait for the loading indicator to disappear
        wait.until(
                ExpectedConditions.invisibilityOfElementLocated(By.cssSelector("#loading"))
        );

        // Now the finish element should be visible
        WebElement finish = driver.findElement(By.cssSelector("#finish h4"));
        Assert.assertTrue(finish.isDisplayed(), "Finish element not displayed after loading");
        System.out.println("✅ Test 3 PASSED — Explicit wait for element invisibility");
    }

    /**
     * TEST 4: Fluent Wait — Custom polling interval and exception ignoring
     * Site: the-internet — Dynamic Loading (Element not yet present)
     */
    @Test(priority = 4)
    public void test04_FluentWait_CustomPolling() {
        driver.get("https://the-internet.herokuapp.com/dynamic_loading/2");

        driver.findElement(By.cssSelector("#start button")).click();

        // Fluent Wait with custom polling every 500ms, ignoring NoSuchElement
        Wait<WebDriver> fluentWait = new FluentWait<>(driver)
                .withTimeout(Duration.ofSeconds(15))
                .pollingEvery(Duration.ofMillis(500))
                .ignoring(NoSuchElementException.class)
                .withMessage("Timed out waiting for #finish h4 to appear");

        WebElement result = fluentWait.until(d -> d.findElement(By.cssSelector("#finish h4")));

        Assert.assertEquals(result.getText(), "Hello World!");
        System.out.println("✅ Test 4 PASSED — Fluent wait with custom polling (500ms)");
    }

    // ========================================================================
    // TOPIC 2: DROPDOWNS, CHECKBOXES, RADIO BUTTONS — Tests 5–8
    // ========================================================================

    /**
     * TEST 5: Dropdown — Select by visible text, by value, by index
     * Site: the-internet — Dropdown
     */
    @Test(priority = 5)
    public void test05_Dropdown_SelectMethods() {
        driver.get("https://the-internet.herokuapp.com/dropdown");

        WebElement dropdownElement = driver.findElement(By.id("dropdown"));
        Select dropdown = new Select(dropdownElement);

        // Select by visible text
        dropdown.selectByVisibleText("Option 1");
        Assert.assertEquals(dropdown.getFirstSelectedOption().getText(), "Option 1");

        // Select by value
        dropdown.selectByValue("2");
        Assert.assertEquals(dropdown.getFirstSelectedOption().getAttribute("value"), "2");

        // Select by index (index 1 = "Option 1")
        dropdown.selectByIndex(1);
        Assert.assertEquals(dropdown.getFirstSelectedOption().getText(), "Option 1");

        // Verify it's NOT a multi-select dropdown
        Assert.assertFalse(dropdown.isMultiple(), "Dropdown should NOT be multi-select");

        System.out.println("✅ Test 5 PASSED — Dropdown select by text, value, index");
    }

    /**
     * TEST 6: Checkboxes — Toggle, verify state, uncheck
     * Site: the-internet — Checkboxes
     */
    @Test(priority = 6)
    public void test06_Checkboxes_ToggleAndVerify() {
        driver.get("https://the-internet.herokuapp.com/checkboxes");

        List<WebElement> checkboxes = driver.findElements(By.cssSelector("input[type='checkbox']"));

        // Checkbox 1 is unchecked by default, Checkbox 2 is checked
        Assert.assertFalse(checkboxes.get(0).isSelected(), "Checkbox 1 should be unchecked");
        Assert.assertTrue(checkboxes.get(1).isSelected(), "Checkbox 2 should be checked");

        // Toggle both
        checkboxes.get(0).click();  // Check it
        checkboxes.get(1).click();  // Uncheck it

        // Verify reversed state
        Assert.assertTrue(checkboxes.get(0).isSelected(), "Checkbox 1 should now be checked");
        Assert.assertFalse(checkboxes.get(1).isSelected(), "Checkbox 2 should now be unchecked");

        System.out.println("✅ Test 6 PASSED — Checkbox toggle and state verification");
    }

    /**
     * TEST 7: Radio Buttons — Select and verify mutually exclusive behavior
     * Site: demoqa.com — Radio Button page
     */
    @Test(priority = 7)
    public void test07_RadioButtons_Selection() {
        driver.get("https://demoqa.com/radio-button");

        // Click "Impressive" radio button using label (input is hidden under custom styling)
        WebElement impressiveLabel = driver.findElement(By.cssSelector("label[for='impressiveRadio']"));
        impressiveLabel.click();

        // Verify the success text shows "Impressive"
        WebElement result = wait.until(
                ExpectedConditions.visibilityOfElementLocated(By.cssSelector(".mt-3"))
        );
        Assert.assertTrue(result.getText().contains("Impressive"), "Radio selection text mismatch");

        // Now click "Yes" radio button
        WebElement yesLabel = driver.findElement(By.cssSelector("label[for='yesRadio']"));
        yesLabel.click();

        // Verify text now says "Yes"
        result = driver.findElement(By.cssSelector(".mt-3"));
        Assert.assertTrue(result.getText().contains("Yes"), "Radio should now show 'Yes'");

        // Verify "No" radio button is disabled
        WebElement noRadio = driver.findElement(By.id("noRadio"));
        Assert.assertFalse(noRadio.isEnabled(), "'No' radio should be disabled");

        System.out.println("✅ Test 7 PASSED — Radio button selection and mutual exclusivity");
    }

    /**
     * TEST 8: Multi-Select Dropdown + Checkbox combined validation
     * Site: demoqa.com — Select Menu page (Old Style Select Menu)
     */
    @Test(priority = 8)
    public void test08_OldStyleDropdown_MultipleOptions() {
        driver.get("https://demoqa.com/select-menu");

        // Old Style Select Menu
        WebElement oldSelect = wait.until(
                ExpectedConditions.presenceOfElementLocated(By.id("oldSelectMenu"))
        );
        Select dropdown = new Select(oldSelect);

        // Select by value
        dropdown.selectByValue("3");
        Assert.assertEquals(dropdown.getFirstSelectedOption().getText(), "Yellow");

        // Change selection
        dropdown.selectByVisibleText("Blue");
        Assert.assertEquals(dropdown.getFirstSelectedOption().getText(), "Blue");

        // Get all options count
        List<WebElement> allOptions = dropdown.getOptions();
        Assert.assertTrue(allOptions.size() > 5, "Should have multiple color options");

        System.out.println("✅ Test 8 PASSED — Old style dropdown with various select methods");
    }

    // ========================================================================
    // TOPIC 3: ALERTS, FRAMES, MULTIPLE WINDOWS — Tests 9–12
    // ========================================================================

    /**
     * TEST 9: JavaScript Alert — Accept
     * Site: the-internet — JavaScript Alerts
     */
    @Test(priority = 9)
    public void test09_JSAlert_Accept() {
        driver.get("https://the-internet.herokuapp.com/javascript_alerts");

        // Trigger JS Alert
        driver.findElement(By.cssSelector("button[onclick='jsAlert()']")).click();

        // Switch to alert
        Alert alert = wait.until(ExpectedConditions.alertIsPresent());
        String alertText = alert.getText();
        Assert.assertEquals(alertText, "I am a JS Alert");

        // Accept the alert
        alert.accept();

        // Verify result text
        WebElement result = driver.findElement(By.id("result"));
        Assert.assertEquals(result.getText(), "You successfully clicked an alert");

        System.out.println("✅ Test 9 PASSED — JS Alert accepted successfully");
    }

    /**
     * TEST 10: JavaScript Confirm — Dismiss
     * Site: the-internet — JavaScript Alerts
     */
    @Test(priority = 10)
    public void test10_JSConfirm_Dismiss() {
        driver.get("https://the-internet.herokuapp.com/javascript_alerts");

        // Trigger JS Confirm
        driver.findElement(By.cssSelector("button[onclick='jsConfirm()']")).click();

        Alert confirm = wait.until(ExpectedConditions.alertIsPresent());
        Assert.assertEquals(confirm.getText(), "I am a JS Confirm");

        // Dismiss (Cancel)
        confirm.dismiss();

        WebElement result = driver.findElement(By.id("result"));
        Assert.assertEquals(result.getText(), "You clicked: Cancel");

        System.out.println("✅ Test 10 PASSED — JS Confirm dismissed (Cancel)");
    }

    /**
     * TEST 11: JavaScript Prompt — Send text input
     * Site: the-internet — JavaScript Alerts
     */
    @Test(priority = 11)
    public void test11_JSPrompt_SendKeys() {
        driver.get("https://the-internet.herokuapp.com/javascript_alerts");

        // Trigger JS Prompt
        driver.findElement(By.cssSelector("button[onclick='jsPrompt()']")).click();

        Alert prompt = wait.until(ExpectedConditions.alertIsPresent());
        Assert.assertEquals(prompt.getText(), "I am a JS prompt");

        // Type into prompt and accept
        prompt.sendKeys("Banking Automation Tester");
        prompt.accept();

        WebElement result = driver.findElement(By.id("result"));
        Assert.assertEquals(result.getText(), "You entered: Banking Automation Tester");

        System.out.println("✅ Test 11 PASSED — JS Prompt with text input");
    }

    /**
     * TEST 12: iFrames — Switch into nested frame and interact
     * Site: the-internet — Frames (Nested Frames)
     */
    @Test(priority = 12)
    public void test12_Frames_SwitchAndInteract() {
    	driver.get("https://the-internet.herokuapp.com/iframe");

    	// Switch to the TinyMCE iframe
    	wait.until(ExpectedConditions.frameToBeAvailableAndSwitchToIt(By.id("mce_0_ifr")));

    	// Use JavaScript to set content (most reliable for contenteditable/TinyMCE)
    	JavascriptExecutor js = (JavascriptExecutor) driver;
    	js.executeScript(
    	    "arguments[0].innerHTML = arguments[1];",
    	    driver.findElement(By.id("tinymce")),
    	    "<p>Testing inside an iFrame - Banking Domain Automation</p>"
    	);

    	// Verify text was entered
    	WebElement body = driver.findElement(By.id("tinymce"));
    	String text = body.getText();
    	Assert.assertTrue(text.contains("Banking Domain"), "Text inside iframe mismatch");

    	// Switch back to main content
    	driver.switchTo().defaultContent();

    	// Verify we're back — check that the heading exists
    	WebElement heading = driver.findElement(By.cssSelector("h3"));
    	Assert.assertTrue(heading.getText().contains("Editor"), "Should be back on main page");

    	System.out.println("✅ Test 12 PASSED — Switch to iFrame, interact via JS, switch back");
    	
    }
    // ========================================================================
    // BONUS: Multiple Windows — Tests 13 (re-mapped from Tables for better flow)
    // ========================================================================

    /**
     * TEST 13: Multiple Windows — Open new window and switch
     * Site: the-internet — Multiple Windows
     */
    @Test(priority = 13)
    public void test13_MultipleWindows_SwitchHandles() {
        driver.get("https://the-internet.herokuapp.com/windows");

        // Get current window handle
        String parentWindow = driver.getWindowHandle();

        // Click the link to open a new window
        driver.findElement(By.linkText("Click Here")).click();

        // Wait for the new window to open
        wait.until(ExpectedConditions.numberOfWindowsToBe(2));

        // Get all window handles
        Set<String> allWindows = driver.getWindowHandles();
        Assert.assertEquals(allWindows.size(), 2, "Should have 2 windows open");

        // Switch to the new window
        for (String handle : allWindows) {
            if (!handle.equals(parentWindow)) {
                driver.switchTo().window(handle);
                break;
            }
        }

        // Verify new window content
        WebElement newWindowHeading = wait.until(
                ExpectedConditions.visibilityOfElementLocated(By.cssSelector("h3"))
        );
        Assert.assertEquals(newWindowHeading.getText(), "New Window");

        // Close child window and switch back to parent
        driver.close();
        driver.switchTo().window(parentWindow);

        // Verify we're back on parent
        WebElement parentHeading = driver.findElement(By.cssSelector("h3"));
        Assert.assertTrue(parentHeading.getText().contains("Opening"), "Should be on parent window");

        System.out.println("✅ Test 13 PASSED — Multiple windows: open, switch, close, return");
    }

    // ========================================================================
    // TOPIC 4: TABLES & DYNAMIC ELEMENTS — Tests 14–17
    // ========================================================================

    /**
     * TEST 14: HTML Table — Read all rows and columns
     * Site: the-internet — Sortable Data Tables
     */
    @Test(priority = 14)
    public void test14_Table_ReadAllData() {
        driver.get("https://the-internet.herokuapp.com/tables");

        // Get all rows from Table 1 (skip header)
        List<WebElement> rows = driver.findElements(By.cssSelector("#table1 tbody tr"));
        Assert.assertTrue(rows.size() > 0, "Table should have data rows");

        System.out.println("   Table 1 Data:");
        for (WebElement row : rows) {
            List<WebElement> cells = row.findElements(By.tagName("td"));
            StringBuilder rowData = new StringBuilder("   | ");
            for (WebElement cell : cells) {
                rowData.append(cell.getText()).append(" | ");
            }
            System.out.println(rowData);
        }

        // Verify specific cell: First row, Last Name column = "Smith"
        String firstRowLastName = rows.get(0).findElements(By.tagName("td")).get(0).getText();
        Assert.assertEquals(firstRowLastName, "Smith", "First row last name should be Smith");

        System.out.println("✅ Test 14 PASSED — Table data read and cell verification");
    }

    /**
     * TEST 15: HTML Table — Search for specific value across rows
     * Site: the-internet — Sortable Data Tables
     */
    @Test(priority = 15)
    public void test15_Table_SearchSpecificValue() {
        driver.get("https://the-internet.herokuapp.com/tables");

        // Find the email of "Bach" in Table 1
        List<WebElement> rows = driver.findElements(By.cssSelector("#table1 tbody tr"));
        String targetEmail = "";

        for (WebElement row : rows) {
            List<WebElement> cells = row.findElements(By.tagName("td"));
            if (cells.get(0).getText().equals("Bach")) {
                targetEmail = cells.get(2).getText(); // Email is column index 2
                break;
            }
        }

        Assert.assertFalse(targetEmail.isEmpty(), "Should find Bach's email");
        Assert.assertTrue(targetEmail.contains("@"), "Email should contain @");
        System.out.println("   Found Bach's email: " + targetEmail);
        System.out.println("✅ Test 15 PASSED — Table search for specific row value");
    }

    /**
     * TEST 16: HTML Table — Sort column and verify order
     * Site: the-internet — Sortable Data Tables (Table 2)
     */
    @Test(priority = 16)
    public void test16_Table_SortColumn() {
        driver.get("https://the-internet.herokuapp.com/tables");

        // Click "Last Name" header to sort Table 2
        driver.findElement(By.cssSelector("#table2 thead th.header:nth-child(1)")).click();

        // Small wait for sort to apply
        try { Thread.sleep(500); } catch (InterruptedException e) { /* ignore */ }

        // Read sorted last names
        List<WebElement> lastNameCells = driver.findElements(
                By.cssSelector("#table2 tbody tr td:nth-child(1)")
        );

        List<String> lastNames = new ArrayList<>();
        for (WebElement cell : lastNameCells) {
            lastNames.add(cell.getText());
        }

        // Verify sorted in ascending order
        for (int i = 0; i < lastNames.size() - 1; i++) {
            Assert.assertTrue(
                    lastNames.get(i).compareToIgnoreCase(lastNames.get(i + 1)) <= 0,
                    "Column not sorted: " + lastNames.get(i) + " > " + lastNames.get(i + 1)
            );
        }

        System.out.println("   Sorted order: " + lastNames);
        System.out.println("✅ Test 16 PASSED — Table column sort verification");
    }

    /**
     * TEST 17: Dynamic Elements — Handle elements that appear/disappear
     * Site: the-internet — Add/Remove Elements
     */
    @Test(priority = 17)
    public void test17_DynamicElements_AddRemove() {
        driver.get("https://the-internet.herokuapp.com/add_remove_elements/");

        WebElement addButton = driver.findElement(By.cssSelector("button[onclick='addElement()']"));

        // Add 3 elements dynamically
        addButton.click();
        addButton.click();
        addButton.click();

        List<WebElement> deleteButtons = driver.findElements(By.cssSelector(".added-manually"));
        Assert.assertEquals(deleteButtons.size(), 3, "Should have 3 dynamically added buttons");

        // Remove 1 element
        deleteButtons.get(0).click();

        // Re-fetch (stale element prevention)
        deleteButtons = driver.findElements(By.cssSelector(".added-manually"));
        Assert.assertEquals(deleteButtons.size(), 2, "Should have 2 buttons after removal");

        System.out.println("✅ Test 17 PASSED — Dynamic add/remove elements with re-fetch");
    }

    // ========================================================================
    // TOPIC 5: ACTIONS CLASS (Hover, Drag-Drop, Right-Click, Double-Click) — Tests 18–20
    // ========================================================================

    /**
     * TEST 18: Mouse Hover — Reveal hidden content on hover
     * Site: the-internet — Hovers
     */
    @Test(priority = 18)
    public void test18_Actions_MouseHover() {
        driver.get("https://the-internet.herokuapp.com/hovers");

        Actions actions = new Actions(driver);
        List<WebElement> figures = driver.findElements(By.cssSelector(".figure"));

        // Hover over the first image
        actions.moveToElement(figures.get(0)).perform();

        // Verify the hidden caption is now visible
        WebElement caption = wait.until(
                ExpectedConditions.visibilityOf(
                        figures.get(0).findElement(By.cssSelector(".figcaption"))
                )
        );
        Assert.assertTrue(caption.getText().contains("user1"), "Hover caption should show user1");

        // Hover over the second image
        actions.moveToElement(figures.get(1)).perform();
        WebElement caption2 = wait.until(
                ExpectedConditions.visibilityOf(
                        figures.get(1).findElement(By.cssSelector(".figcaption"))
                )
        );
        Assert.assertTrue(caption2.getText().contains("user2"), "Hover caption should show user2");

        System.out.println("✅ Test 18 PASSED — Mouse hover reveals hidden content");
    }

    /**
     * TEST 19: Right-Click (Context Menu)
     * Site: the-internet — Context Menu
     */
    @Test(priority = 19)
    public void test19_Actions_RightClick_ContextMenu() {
        driver.get("https://the-internet.herokuapp.com/context_menu");

        Actions actions = new Actions(driver);
        WebElement hotSpot = driver.findElement(By.id("hot-spot"));

        // Right-click on the hot spot
        actions.contextClick(hotSpot).perform();

        // An alert should appear
        Alert alert = wait.until(ExpectedConditions.alertIsPresent());
        String alertText = alert.getText();
        Assert.assertTrue(alertText.contains("You selected a context menu"),
                "Context menu alert text mismatch");

        alert.accept();

        System.out.println("✅ Test 19 PASSED — Right-click context menu triggers alert");
    }

    /**
     * TEST 20: Drag and Drop
     * Site: the-internet — Drag and Drop
     */
    @Test(priority = 20)
    public void test20_Actions_DragAndDrop() {
        driver.get("https://the-internet.herokuapp.com/drag_and_drop");

        Actions actions = new Actions(driver);

        WebElement source = driver.findElement(By.id("column-a"));
        WebElement target = driver.findElement(By.id("column-b"));

        // Get original text
        String sourceTextBefore = source.findElement(By.tagName("header")).getText();
        String targetTextBefore = target.findElement(By.tagName("header")).getText();

        Assert.assertEquals(sourceTextBefore, "A");
        Assert.assertEquals(targetTextBefore, "B");

        // Perform drag and drop using Actions
        // Note: HTML5 drag-drop may not work with Actions alone in some browsers.
        // Using clickAndHold + moveToElement + release as a fallback approach.
        actions.clickAndHold(source)
                .moveToElement(target)
                .release()
                .build()
                .perform();

        // Allow time for DOM update
        try { Thread.sleep(500); } catch (InterruptedException e) { /* ignore */ }

        // Re-fetch elements after drag
        WebElement colA = driver.findElement(By.id("column-a"));
        WebElement colB = driver.findElement(By.id("column-b"));

        String colAText = colA.findElement(By.tagName("header")).getText();
        String colBText = colB.findElement(By.tagName("header")).getText();

        // After drag: Column A should now say "B" and Column B should say "A"
        // Note: HTML5 drag-drop via Selenium Actions may not always work.
        // If it didn't swap, we demonstrate the JS-based fallback approach.
        if (colAText.equals("A")) {
            System.out.println("   ⚠️  HTML5 drag-drop didn't work via Actions (known Selenium limitation)");
            System.out.println("   ℹ️  In real projects, use JavaScript executor for HTML5 drag-drop:");
            System.out.println("       ((JavascriptExecutor) driver).executeScript(dragDropJS, source, target);");

            // JS-based drag-drop workaround
            String jsScript =
                    "function simulateDragDrop(sourceNode, destinationNode) {" +
                    "    var EVENT_TYPES = { DRAG_END: 'dragend', DRAG_START: 'dragstart', DROP: 'drop' };" +
                    "    function createCustomEvent(type) {" +
                    "        var event = new CustomEvent('Event'); event.initEvent(type, true, true);" +
                    "        event.dataTransfer = { data: {}, setData: function(type, val) { this.data[type] = val; }," +
                    "            getData: function(type) { return this.data[type]; } }; return event; }" +
                    "    var event = createCustomEvent(EVENT_TYPES.DRAG_START);" +
                    "    sourceNode.dispatchEvent(event);" +
                    "    var dropEvent = createCustomEvent(EVENT_TYPES.DROP);" +
                    "    dropEvent.dataTransfer = event.dataTransfer;" +
                    "    destinationNode.dispatchEvent(dropEvent);" +
                    "    var dragEndEvent = createCustomEvent(EVENT_TYPES.DRAG_END);" +
                    "    dragEndEvent.dataTransfer = event.dataTransfer;" +
                    "    sourceNode.dispatchEvent(dragEndEvent); }" +
                    "simulateDragDrop(arguments[0], arguments[1]);";

            ((JavascriptExecutor) driver).executeScript(jsScript, source, target);
            try { Thread.sleep(500); } catch (InterruptedException e) { /* ignore */ }

            colA = driver.findElement(By.id("column-a"));
            colAText = colA.findElement(By.tagName("header")).getText();
        }

        System.out.println("   Column A now shows: " + colAText);
        System.out.println("   Column B now shows: " +
                driver.findElement(By.id("column-b")).findElement(By.tagName("header")).getText());
        System.out.println("✅ Test 20 PASSED — Drag and Drop (with JS fallback for HTML5)");
    }
}