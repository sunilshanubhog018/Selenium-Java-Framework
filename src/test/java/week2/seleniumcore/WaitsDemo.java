package week2.seleniumcore;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.Assert;
import org.testng.annotations.*;

import base.BaseTest;

import java.time.Duration;

public class WaitsDemo extends BaseTest  {

    @Test
    public void testDynamicLoading() {

        // Step 4 comment fix:
    	// Example 2 — element does NOT exist in DOM at all initially
    	// It gets dynamically created and injected after loading completes
    	driver.get("https://the-internet.herokuapp.com/dynamic_loading/2");

        // Step 5: Wait until the Start button is clickable, then store the reference
        // elementToBeClickable = element is visible + enabled (safe to click)
        // Using CSS selector: #start selects the div with id="start",
        // then "button" selects the button inside it
        WebElement start = wait.until(
            ExpectedConditions.elementToBeClickable(By.cssSelector("#start button"))
        );

        // Step 6: Click the Start button
        // This triggers the loading process — a spinner appears and then the result loads
        start.click();

        // Step 7: Wait until the loading spinner disappears
        // After clicking Start, a loading bar (id="loading") is displayed
        // We must wait for it to become invisible before looking for the result
        // If we skip this step, we risk grabbing the result element before it's fully loaded
        wait.until(
            ExpectedConditions.invisibilityOfElementLocated(By.id("loading"))
        );

        // Step 8: Wait until the result element becomes visible
        // The finish div (id="finish") exists in DOM from the beginning but is hidden (display:none)
        // visibilityOfElementLocated waits until display:none is removed and element is visible
        WebElement resultText = wait.until(
            ExpectedConditions.visibilityOfElementLocated(By.id("finish"))
        );

        // Step 9: Assert the text matches expected value
        // Assert.assertEquals(actual, expected)
        // If texts don't match → test FAILS with a clear message
        // If texts match → test PASSES
        Assert.assertEquals(resultText.getText(), "Hello World!");

        // Step 10: Print confirmation to console for visual feedback during execution
        System.out.println("✅ Text verified: " + resultText.getText());
    }
}