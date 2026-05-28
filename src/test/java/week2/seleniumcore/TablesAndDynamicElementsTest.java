package week2.seleniumcore;

import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.Assert;
import org.testng.annotations.Test;
import org.testng.asserts.SoftAssert;
import base.BaseTest;

import java.time.Duration;
import java.util.List;

public class TablesAndDynamicElementsTest extends BaseTest {

    // ==================== PART 1: HTML TABLES ====================

    /**
     * Test 1 - Read a specific cell value from the table
     * Target: https://the-internet.herokuapp.com/tables
     * Goal: Access row 1, column 3 (Email) and verify it contains "@"
     */
    @Test
    public void testReadSpecificCell() {
        driver.get("https://the-internet.herokuapp.com/tables");

        // Read email (column 3) of row 1 in table1
        // XPath index is 1-based: td[1]=LastName, td[2]=FirstName, td[3]=Email
        WebElement cell = driver.findElement(
                By.xpath("//table[@id='table1']//tbody/tr[1]/td[3]"));

        String email = cell.getText();
        System.out.println("Row 1 Email: " + email);
        Assert.assertTrue(email.contains("@"), "Cell should contain an email address");
    }

    /**
     * Test 2 - Iterate through all rows and print entire table data
     * Target: https://the-internet.herokuapp.com/tables
     * Goal: Read every row and cell, verify row count
     *
     * Key concept: row.findElements(By.tagName("td")) scopes search to that row only
     */
    @Test
    public void testIterateTableRows() {
        driver.get("https://the-internet.herokuapp.com/tables");

        // Get all header cells first
        List<WebElement> headers = driver.findElements(
                By.xpath("//table[@id='table1']//thead/tr/th"));

        StringBuilder headerRow = new StringBuilder("Headers: ");
        for (WebElement header : headers) {
            headerRow.append(header.getText()).append(" | ");
        }
        System.out.println(headerRow);
        System.out.println("-".repeat(60));

        // Get all data rows from tbody
        List<WebElement> rows = driver.findElements(
                By.xpath("//table[@id='table1']//tbody/tr"));

        Assert.assertTrue(rows.size() > 0, "Table should have rows");
        System.out.println("Total data rows: " + rows.size());

        // Iterate each row and print cell values
        for (int i = 0; i < rows.size(); i++) {
            // findElements on the ROW element (not driver) — scopes to children of this row
            List<WebElement> cells = rows.get(i).findElements(By.tagName("td"));
            StringBuilder rowData = new StringBuilder("Row " + (i + 1) + ": ");
            for (WebElement cell : cells) {
                rowData.append(cell.getText()).append(" | ");
            }
            System.out.println(rowData);
        }

        // Verify table has exactly 4 rows
        Assert.assertEquals(rows.size(), 4, "Table1 should have 4 data rows");
    }

    /**
     * Test 3 - Search for a specific value in the table and act on that row
     * Target: https://the-internet.herokuapp.com/tables
     * Goal: Find row where Last Name = "Bach", then click "edit" link in that row
     *
     * Key concepts:
     *   - Looping rows to find a match (like searching a transaction table)
     *   - Using RELATIVE XPath with dot: .//a (searches within current row only)
     *   - Also demonstrates the pure XPath alternative (no loop needed)
     */
    @Test
    public void testSearchAndActOnRow() {
        driver.get("https://the-internet.herokuapp.com/tables");

        String targetName = "Bach";
        List<WebElement> rows = driver.findElements(
                By.xpath("//table[@id='table1']//tbody/tr"));

        boolean found = false;
        for (WebElement row : rows) {
            List<WebElement> cells = row.findElements(By.tagName("td"));
            String lastName = cells.get(0).getText();   // Java 0-based = first column (Last Name)
            String firstName = cells.get(1).getText();
            String email = cells.get(2).getText();
            String due = cells.get(3).getText();

            if (lastName.equals(targetName)) {
                found = true;
                System.out.println("Found target row:");
                System.out.println("  Name: " + firstName + " " + lastName);
                System.out.println("  Email: " + email);
                System.out.println("  Due: " + due);

                // Click "edit" link — DOT in .//a makes XPath relative to this row
                WebElement editLink = row.findElement(
                        By.xpath(".//a[contains(text(),'edit')]"));
                editLink.click();
                System.out.println("  Clicked 'edit' link for " + targetName);
                break;
            }
        }
        Assert.assertTrue(found, "Should find row with last name: " + targetName);
    }

    // ==================== PART 2: DYNAMIC ELEMENTS ====================

    /**
     * Test 4 - Handle dynamically loaded content (AJAX)
     * Target: https://the-internet.herokuapp.com/dynamic_loading/1
     * Scenario: Element is hidden on page, becomes visible after clicking "Start"
     *
     * Key concept: Use visibilityOfElementLocated to wait for AJAX content
     *
     * Also tests /dynamic_loading/2 where element is NOT in DOM initially
     * and gets ADDED after loading (uses presenceOfElementLocated)
     */
    @Test
    public void testDynamicLoading() {
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        SoftAssert softAssert = new SoftAssert();

        // --- Scenario A: Element hidden, then revealed ---
        driver.get("https://the-internet.herokuapp.com/dynamic_loading/1");
        System.out.println("=== Dynamic Loading Example 1: Element hidden, then shown ===");

        // Click Start button
        driver.findElement(By.xpath("//button[text()='Start']")).click();
        System.out.println("Clicked 'Start' — waiting for content to load...");

        // Wait for the finish text to become VISIBLE
        WebElement finishText = wait.until(
                ExpectedConditions.visibilityOfElementLocated(By.id("finish")));

        String loadedText = finishText.getText();
        System.out.println("Loaded text: " + loadedText);
        softAssert.assertEquals(loadedText, "Hello World!",
                "Dynamic text should appear after loading");

        // --- Scenario B: Element not in DOM, then added ---
        driver.get("https://the-internet.herokuapp.com/dynamic_loading/2");
        System.out.println("\n=== Dynamic Loading Example 2: Element added to DOM ===");

        driver.findElement(By.xpath("//button[text()='Start']")).click();
        System.out.println("Clicked 'Start' — waiting for element to be added to DOM...");

        // Wait for element to be PRESENT in DOM first, then visible
        WebElement finishText2 = wait.until(
                ExpectedConditions.visibilityOfElementLocated(By.id("finish")));

        String loadedText2 = finishText2.getText();
        System.out.println("Loaded text: " + loadedText2);
        softAssert.assertEquals(loadedText2, "Hello World!",
                "Dynamic text should appear after loading (example 2)");

        softAssert.assertAll();
    }

    /**
     * Test 5 - Handle dynamic controls (elements appearing, disappearing, enabling)
     * Target: https://the-internet.herokuapp.com/dynamic_controls
     *
     * Key concepts:
     *   - invisibilityOfElementLocated: wait for element to disappear
     *   - elementToBeClickable: wait for element to become enabled/interactable
     *   - Re-finding elements after DOM changes to avoid StaleElementReferenceException
     */
    @Test
    public void testDynamicControls() {
        driver.get("https://the-internet.herokuapp.com/dynamic_controls");
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));

        // === Part A: Remove and Add checkbox ===
        System.out.println("=== Part A: Checkbox Remove/Add ===");

        WebElement checkbox = driver.findElement(By.xpath("//input[@type='checkbox']"));
        Assert.assertTrue(checkbox.isDisplayed(), "Checkbox should be visible initially");
        System.out.println("Checkbox is displayed: " + checkbox.isDisplayed());

        // Click "Remove" button
        driver.findElement(By.xpath("//button[text()='Remove']")).click();
        System.out.println("Clicked 'Remove' — waiting for checkbox to disappear...");

        // Wait for checkbox to disappear from DOM
        wait.until(ExpectedConditions.invisibilityOfElementLocated(
                By.xpath("//input[@type='checkbox']")));
        System.out.println("Checkbox removed successfully");

        // Verify confirmation message
        WebElement message = wait.until(
                ExpectedConditions.visibilityOfElementLocated(By.id("message")));
        Assert.assertEquals(message.getText(), "It's gone!");
        System.out.println("Message: " + message.getText());

        // Now click "Add" to bring it back
        driver.findElement(By.xpath("//button[text()='Add']")).click();
        System.out.println("Clicked 'Add' — waiting for checkbox to reappear...");

        // Wait for checkbox to reappear
        WebElement readdedCheckbox = wait.until(
                ExpectedConditions.visibilityOfElementLocated(
                        By.xpath("//input[@type='checkbox']")));
        Assert.assertTrue(readdedCheckbox.isDisplayed(), "Checkbox should be back");

        WebElement addMessage = wait.until(
                ExpectedConditions.visibilityOfElementLocated(By.id("message")));
        Assert.assertEquals(addMessage.getText(), "It's back!");
        System.out.println("Message: " + addMessage.getText());

        // === Part B: Enable and Disable text input ===
        System.out.println("\n=== Part B: Input Enable/Disable ===");

        WebElement textInput = driver.findElement(By.xpath("//input[@type='text']"));
        Assert.assertFalse(textInput.isEnabled(), "Input should be enabled initially");
        System.out.println("Input enabled: " + textInput.isEnabled());

        // Click "Enable" button
        driver.findElement(By.xpath("//button[text()='Enable']")).click();
        System.out.println("Clicked 'Enable' — waiting for input to become interactable...");

        // Wait for input to become clickable (enabled + visible)
        wait.until(ExpectedConditions.elementToBeClickable(
                By.xpath("//input[@type='text']")));

        // Re-find element to avoid StaleElementReferenceException
        textInput = driver.findElement(By.xpath("//input[@type='text']"));
        Assert.assertTrue(textInput.isEnabled(), "Input should now be enabled");

        textInput.sendKeys("Banking Test Data");
        System.out.println("Typed: " + textInput.getAttribute("value"));

        WebElement enableMessage = wait.until(
                ExpectedConditions.visibilityOfElementLocated(By.id("message")));
        Assert.assertEquals(enableMessage.getText(), "It's enabled!");
        System.out.println("Message: " + enableMessage.getText());
    }
}