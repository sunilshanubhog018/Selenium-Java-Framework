package week2.seleniumcore;

import org.openqa.selenium.*;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.Assert;
import org.testng.annotations.Test;

import base.BaseTest;

import java.time.Duration;
import java.util.List;

/**
 * Actions Class Practice Tests — Week 2
 * Covers: Hover, Drag-and-Drop, Context Click, Slider, Keyboard Shortcuts, Double-Click
 * Site: https://the-internet.herokuapp.com
 */
public class ActionsClassTest extends BaseTest {

    // ═══════════════════════════════════════════════════════════
    // TEST 1: Hover and Click Sub-Menu
    // ═══════════════════════════════════════════════════════════
    @Test(description = "Hover on avatar to reveal hidden profile info, then click profile link")
    public void testHoverRevealsUserProfile() {
        driver.get("https://the-internet.herokuapp.com/hovers");

        Actions actions = new Actions(driver);
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(5));

        // Get all figure elements, pick 1st profile (index 0)
        List<WebElement> figures = driver.findElements(By.className("figure"));
        WebElement figure = figures.get(0);

        // Hover to reveal hidden profile info
        actions.moveToElement(figure).perform();

        // Wait for caption within that specific figure (scoped search)
        WebElement caption = wait.until(
                ExpectedConditions.visibilityOf(
                        figure.findElement(By.className("figcaption"))));

        // Verify profile name is displayed
        String profileName = caption.findElement(By.tagName("h5")).getText();
        Assert.assertTrue(profileName.contains("user"),
                "Profile name should be visible after hover. Found: " + profileName);

        // Click the profile link
        WebElement profileLink = caption.findElement(By.tagName("a"));
        profileLink.click();

        // Verify navigation to user profile page
        Assert.assertTrue(driver.getCurrentUrl().contains("/users/"),
                "Should navigate to user profile page. URL: " + driver.getCurrentUrl());
    }

    // ═══════════════════════════════════════════════════════════
    // TEST 2: Drag and Drop (Manual Sequence + JS Fallback)
    // ═══════════════════════════════════════════════════════════
    @Test(description = "Drag column A to column B using manual sequence, with JS fallback for HTML5 DnD")
    public void testDragAndDropManualSequence() {
        driver.get("https://the-internet.herokuapp.com/drag_and_drop");

        Actions actions = new Actions(driver);

        WebElement colA = driver.findElement(By.id("column-a"));
        WebElement colB = driver.findElement(By.id("column-b"));

        // Verify initial state
        Assert.assertEquals(colA.getText(), "A", "Column A should initially contain 'A'");
        Assert.assertEquals(colB.getText(), "B", "Column B should initially contain 'B'");

        // Attempt 1: Manual drag-and-drop (most reliable Selenium approach)
        actions.clickAndHold(colA)
                .moveToElement(colB)
                .release()
                .perform();

        // Re-locate after action
        colA = driver.findElement(By.id("column-a"));
        colB = driver.findElement(By.id("column-b"));

        // This site uses HTML5 DnD — manual Selenium approach may not trigger events.
        // If columns didn't swap, use JavaScript fallback:
        if (colA.getText().equals("A")) {
            System.out.println(">> Manual DnD didn't trigger HTML5 events. Using JS fallback...");

            String jsScript =
                    "function simulateDnD(sourceNode, destinationNode) {" +
                    "    var EVENT_TYPES = { DRAG_END: 'dragend', DRAG_START: 'dragstart'," +
                    "        DROP: 'drop', DRAG_OVER: 'dragover', DRAG_ENTER: 'dragenter' };" +
                    "    function createCustomEvent(type) {" +
                    "        var event = new CustomEvent('Event', { bubbles: true });" +
                    "        event.initEvent(type, true, true);" +
                    "        event.dataTransfer = { data: {}, setData: function(type, val) {" +
                    "            this.data[type] = val; }," +
                    "            getData: function(type) { return this.data[type]; }," +
                    "            setDragImage: function() {} };" +
                    "        return event; }" +
                    "    var ds = createCustomEvent(EVENT_TYPES.DRAG_START);" +
                    "    sourceNode.dispatchEvent(ds);" +
                    "    var de = createCustomEvent(EVENT_TYPES.DRAG_ENTER);" +
                    "    de.dataTransfer = ds.dataTransfer;" +
                    "    destinationNode.dispatchEvent(de);" +
                    "    var dov = createCustomEvent(EVENT_TYPES.DRAG_OVER);" +
                    "    dov.dataTransfer = ds.dataTransfer;" +
                    "    destinationNode.dispatchEvent(dov);" +
                    "    var dro = createCustomEvent(EVENT_TYPES.DROP);" +
                    "    dro.dataTransfer = ds.dataTransfer;" +
                    "    destinationNode.dispatchEvent(dro);" +
                    "    var den = createCustomEvent(EVENT_TYPES.DRAG_END);" +
                    "    den.dataTransfer = ds.dataTransfer;" +
                    "    sourceNode.dispatchEvent(den);" +
                    "}" +
                    "simulateDnD(arguments[0], arguments[1]);";

            ((JavascriptExecutor) driver).executeScript(jsScript, colA, colB);

            // Re-locate after JS action
            colA = driver.findElement(By.id("column-a"));
            colB = driver.findElement(By.id("column-b"));
        }

        // Verify swap occurred
        Assert.assertEquals(colA.getText(), "B",
                "Column A should now contain 'B' after drag");
        Assert.assertEquals(colB.getText(), "A",
                "Column B should now contain 'A' after drag");
    }

 // ═══════════════════════════════════════════════════════════
 // TEST 3: Context Click (Right-Click)
 // ═══════════════════════════════════════════════════════════
 @Test(description = "Right-click on hot-spot area and handle the JS alert")
 public void testContextClickTriggersAlert() {
     driver.manage().timeouts().pageLoadTimeout(Duration.ofSeconds(60));
     driver.get("https://the-internet.herokuapp.com/context_menu");

     Actions actions = new Actions(driver);
     WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));

     // Wait for hot-spot to be present (handles slow page load)
     WebElement hotSpot = wait.until(
             ExpectedConditions.presenceOfElementLocated(By.id("hot-spot")));

     // Right-click on it
     actions.contextClick(hotSpot).perform();

     // Handle the JS alert that appears
     Alert alert = wait.until(ExpectedConditions.alertIsPresent());
     String alertText = alert.getText();

     Assert.assertEquals(alertText,
             "You selected a context menu",
             "Alert text should match expected message");

     alert.accept();

     // Verify page is still intact after dismissing alert
     Assert.assertTrue(driver.findElement(By.id("hot-spot")).isDisplayed(),
             "Hot-spot should still be visible after dismissing alert");
 }
    // ═══════════════════════════════════════════════════════════
    // TEST 4: Slider (dragAndDropBy with Offset + Keyboard)
    // ═══════════════════════════════════════════════════════════
    @Test(description = "Drag horizontal slider by offset, then use arrow keys for precise control")
    public void testSliderDragByOffset() {
        driver.get("https://the-internet.herokuapp.com/horizontal_slider");

        Actions actions = new Actions(driver);

        WebElement slider = driver.findElement(
                By.cssSelector("input[type='range']"));
        WebElement output = driver.findElement(By.id("range"));

        // Verify initial value
        Assert.assertEquals(output.getText(), "0", "Slider should start at 0");

        // Approach 1: Drag by pixel offset
        actions.clickAndHold(slider)
                .moveByOffset(50, 0)
                .release()
                .perform();

        // Verify value changed from initial
        String newValue = output.getText();
        System.out.println(">> Slider value after drag: " + newValue);
        Assert.assertNotEquals(newValue, "0",
                "Slider value should change after drag");

        // Approach 2: Use keyboard arrows for precise control to reach max
        slider.click();
        for (int i = 0; i < 20; i++) {
            slider.sendKeys(Keys.ARROW_RIGHT);
        }

        // Verify slider reached max value
        String finalValue = output.getText();
        System.out.println(">> Slider value after arrow keys: " + finalValue);
        Assert.assertEquals(finalValue, "5",
                "Slider should reach max value 5 after repeated ARROW_RIGHT");
    }

    // ═══════════════════════════════════════════════════════════
    // TEST 5a: Keyboard Shortcuts & Key Detection
    // ═══════════════════════════════════════════════════════════
    @Test(description = "Verify key press detection for special keys using Actions sendKeys")
    public void testKeyboardShortcutsAndKeyDetection() {
        driver.get("https://the-internet.herokuapp.com/key_presses");

        Actions actions = new Actions(driver);

        // Test 1: Type text using Actions sendKeys
        WebElement input = driver.findElement(By.id("target"));
        actions.click(input)
                .sendKeys("Hello")
                .perform();

        Assert.assertTrue(driver.findElement(By.id("result")).getText().contains("You entered"),
                "Should detect key press event");

        // Test 2: Select All (Ctrl+A) — demonstrates modifier keys
        actions.keyDown(Keys.CONTROL)
                .sendKeys("a")
                .keyUp(Keys.CONTROL)
                .perform();

        // Test 3: Overwrite selected text
        driver.findElement(By.id("target")).sendKeys("Banking SDET");

        // Test 4: BACK_SPACE
        driver.findElement(By.id("target")).click();
        driver.findElement(By.id("target")).sendKeys(Keys.BACK_SPACE);
        String resultText = driver.findElement(By.id("result")).getText();
        System.out.println(">> After BACK_SPACE: " + resultText);
        Assert.assertTrue(resultText.contains("BACK_SPACE"),
                "Should detect BACK_SPACE. Actual: " + resultText);

        // Test 5: ESCAPE
        driver.findElement(By.id("target")).click();
        driver.findElement(By.id("target")).sendKeys(Keys.ESCAPE);
        resultText = driver.findElement(By.id("result")).getText();
        System.out.println(">> After ESCAPE: " + resultText);
        Assert.assertTrue(resultText.contains("ESCAPE"),
                "Should detect ESCAPE. Actual: " + resultText);

        // Test 6: TAB
        driver.findElement(By.id("target")).click();
        driver.findElement(By.id("target")).sendKeys(Keys.TAB);
        resultText = driver.findElement(By.id("result")).getText();
        System.out.println(">> After TAB: " + resultText);
        Assert.assertTrue(resultText.contains("TAB"),
                "Should detect TAB. Actual: " + resultText);

        // Test 7: ARROW_DOWN
        driver.findElement(By.id("target")).click();
        driver.findElement(By.id("target")).sendKeys(Keys.ARROW_DOWN);
        resultText = driver.findElement(By.id("result")).getText();
        System.out.println(">> After ARROW_DOWN: " + resultText);
        Assert.assertTrue(resultText.contains("DOWN"),
                "Should detect ARROW_DOWN. Actual: " + resultText);

        // Test 8: SPACE
        driver.findElement(By.id("target")).click();
        driver.findElement(By.id("target")).sendKeys(Keys.SPACE);
        resultText = driver.findElement(By.id("result")).getText();
        System.out.println(">> After SPACE: " + resultText);
        Assert.assertTrue(resultText.contains("SPACE"),
                "Should detect SPACE. Actual: " + resultText);
    }

    // ═══════════════════════════════════════════════════════════
    // TEST 5b: Double-Click Action
    // ═══════════════════════════════════════════════════════════
    @Test(description = "Double-click a button to trigger two add operations, then verify and cleanup")
    public void testDoubleClickAction() {
        driver.get("https://the-internet.herokuapp.com/add_remove_elements/");

        Actions actions = new Actions(driver);

        WebElement addBtn = driver.findElement(
                By.xpath("//button[text()='Add Element']"));

        // Double-click to add two elements at once
        actions.doubleClick(addBtn).perform();

        // Verify two "Delete" buttons appeared
        List<WebElement> deleteButtons = driver.findElements(
                By.cssSelector(".added-manually"));
        System.out.println(">> Elements after double-click: " + deleteButtons.size());
        Assert.assertEquals(deleteButtons.size(), 2,
                "Double-click should trigger two add operations");

        // Cleanup: click one delete button
        deleteButtons.get(0).click();

        // Verify only one element remains
        deleteButtons = driver.findElements(
                By.cssSelector(".added-manually"));
        Assert.assertEquals(deleteButtons.size(), 1,
                "One element should remain after deleting one");
    }
}