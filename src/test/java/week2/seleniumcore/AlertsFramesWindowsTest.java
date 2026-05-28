package week2.seleniumcore;

import base.BaseTest;
import org.openqa.selenium.Alert;
import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.WindowType;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.Assert;
import org.testng.annotations.Test;

import java.time.Duration;
import java.util.Set;

/**
 * Week 2 - Day 3: Alerts, Frames & Multiple Windows
 * 
 * All 5 tests use https://the-internet.herokuapp.com
 * Extends BaseTest.java for driver setup/teardown
 * 
 * Test Site URLs:
 *   - Alerts:  /javascript_alerts
 *   - Frames:  /iframe
 *   - Windows: /windows
 */
public class AlertsFramesWindowsTest extends BaseTest {

    // ======================== TEST 1: SIMPLE ALERT ========================
    @Test(priority = 1, description = "Trigger simple JS alert, accept it, verify result text")
    public void test01_SimpleAlert() {
        driver.get("https://the-internet.herokuapp.com/javascript_alerts");

        // Click button to trigger simple alert
        driver.findElement(By.xpath("//button[text()='Click for JS Alert']")).click();

        // Wait for alert to appear and switch to it
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        Alert alert = wait.until(ExpectedConditions.alertIsPresent());

        // Verify alert text
        String alertText = alert.getText();
        Assert.assertEquals(alertText, "I am a JS Alert", "Alert message mismatch");

        // Accept (click OK)
        alert.accept();

        // Verify result on page
        String result = driver.findElement(By.id("result")).getText();
        Assert.assertEquals(result, "You successfully clicked an alert", "Result text mismatch after accepting alert");
    }

    // ======================== TEST 2: CONFIRM ALERT — DISMISS ========================
    @Test(priority = 2, description = "Trigger confirm alert, dismiss (Cancel), verify result")
    public void test02_ConfirmAlert_Dismiss() {
        driver.get("https://the-internet.herokuapp.com/javascript_alerts");

        // Click button to trigger confirm alert
        driver.findElement(By.xpath("//button[text()='Click for JS Confirm']")).click();

        // Wait for alert
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        Alert alert = wait.until(ExpectedConditions.alertIsPresent());

        // Verify alert text
        Assert.assertEquals(alert.getText(), "I am a JS Confirm", "Confirm alert message mismatch");

        // Dismiss (click Cancel)
        alert.dismiss();

        // Verify result on page
        String result = driver.findElement(By.id("result")).getText();
        Assert.assertEquals(result, "You clicked: Cancel", "Result text mismatch after dismissing confirm");
    }

    // ======================== TEST 3: PROMPT ALERT — SEND TEXT ========================
    @Test(priority = 3, description = "Trigger prompt alert, type text, accept, verify result")
    public void test03_PromptAlert_SendKeys() {
        driver.get("https://the-internet.herokuapp.com/javascript_alerts");

        // Click button to trigger prompt alert
        driver.findElement(By.xpath("//button[text()='Click for JS Prompt']")).click();

        // Wait for alert
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        Alert alert = wait.until(ExpectedConditions.alertIsPresent());

        // Verify alert text
        Assert.assertEquals(alert.getText(), "I am a JS prompt", "Prompt alert message mismatch");

        // Type text into prompt input field
        alert.sendKeys("Selenium Automation");

        // Accept (click OK)
        alert.accept();

        // Verify result on page shows the typed text
        String result = driver.findElement(By.id("result")).getText();
        Assert.assertEquals(result, "You entered: Selenium Automation", "Result text mismatch after prompt input");
    }

    // ======================== TEST 4: IFRAME — TINYMCE EDITOR ========================
    @Test(description = "Switch to iframe, type in TinyMCE editor, switch back, verify heading")
    public void test04_FrameInteraction() {
        driver.get("https://the-internet.herokuapp.com/iframe");

        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        wait.until(ExpectedConditions.frameToBeAvailableAndSwitchToIt("mce_0_ifr"));

        // Use JavaScript to set and read content — most reliable for TinyMCE
        JavascriptExecutor js = (JavascriptExecutor) driver;
        js.executeScript("document.getElementById('tinymce').innerText = 'Hello from Selenium inside an iframe!'");

        // Verify content
        String content = (String) js.executeScript("return document.getElementById('tinymce').innerText");
        System.out.println("Editor content: [" + content + "]");
        Assert.assertTrue(content.contains("Hello from Selenium"),
                "Typed text not found. Actual content: " + content);

        // Switch back to main page
        driver.switchTo().defaultContent();

        WebElement heading = driver.findElement(By.tagName("h3"));
        Assert.assertTrue(heading.getText().contains("iFrame"),
                "Main page heading not found after switching back from frame");
    }

    // ======================== TEST 5: MULTIPLE WINDOWS ========================
    @Test(priority = 5, description = "Open new window via link, verify content, close it, return to original")
    public void test05_MultipleWindows() {
        driver.get("https://the-internet.herokuapp.com/windows");

        // Step 1: Store original window handle BEFORE clicking
        String originalWindow = driver.getWindowHandle();

        // Step 2: Click link that opens a new window
        driver.findElement(By.linkText("Click Here")).click();

        // Step 3: Wait until 2 windows are open
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        wait.until(ExpectedConditions.numberOfWindowsToBe(2));

        // Step 4: Find the new window handle and switch to it
        Set<String> allWindows = driver.getWindowHandles();
        for (String handle : allWindows) {
            if (!handle.equals(originalWindow)) {
                driver.switchTo().window(handle);
                break;
            }
        }

        // Step 5: Verify new window content
        Assert.assertEquals(driver.getTitle(), "New Window", "New window title mismatch");

        String heading = driver.findElement(By.tagName("h3")).getText();
        Assert.assertEquals(heading, "New Window", "New window heading mismatch");

        // Step 6: Close new window
        driver.close();

        // Step 7: Switch back to original window (MUST do after close)
        driver.switchTo().window(originalWindow);

        // Step 8: Verify we're back on the original page
        Assert.assertEquals(driver.getTitle(), "The Internet", "Original page title mismatch after switching back");

        WebElement link = driver.findElement(By.linkText("Click Here"));
        Assert.assertTrue(link.isDisplayed(), "Original page link not found after returning");
    }
}