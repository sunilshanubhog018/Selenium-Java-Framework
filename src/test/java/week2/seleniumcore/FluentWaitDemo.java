package week2.seleniumcore;

import org.openqa.selenium.By;
import org.openqa.selenium.NoSuchElementException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.FluentWait;
import org.openqa.selenium.support.ui.Wait;
import org.testng.Assert;
import org.testng.annotations.*;

import base.BaseTest;

import java.time.Duration;

public class FluentWaitDemo extends BaseTest  {

    @Test
    public void testWithFluentWait() {

        // Step 3: Navigate to the Dynamic Loading page (Example 1)
        // Same page as WaitsDemo — used here to compare Fluent Wait behavior
        driver.get("https://the-internet.herokuapp.com/dynamic_loading/1");

        // Step 4: Configure Fluent Wait with custom settings
        // .withTimeout(20s)        → maximum time to wait before throwing TimeoutException
        // .pollingEvery(1s)        → check the condition every 1 second (vs default 500ms)
        // .ignoring(NoSuchElement) → if element is not found during polling, don't throw —
        //                            just wait and retry on the next poll cycle
        // Use Fluent Wait when: element loads slowly, appears intermittently,
        // or you need fine control over polling frequency
        Wait<WebDriver> fluentWait = new FluentWait<>(driver)
            .withTimeout(Duration.ofSeconds(20))
            .pollingEvery(Duration.ofSeconds(1))
            .ignoring(NoSuchElementException.class);

        // Step 5: Wait for Start button and click it using a lambda function
        // fluentWait.until() accepts a lambda: driver → return element or null
        // d.findElement() is called every 1 second until it finds the button
        // .click() is chained directly — no need for a separate variable
        fluentWait.until(
            d -> d.findElement(By.cssSelector("#start button"))
        ).click();

        // Step 6: Wait for the result element using a custom condition lambda
        // This is the KEY difference from Explicit Wait —
        // we write our OWN condition logic instead of using pre-built ExpectedConditions
        //
        // Logic breakdown:
        //   d.findElement(By.id("finish"))  → tries to find the element every 1 second
        //   el.isDisplayed()                → checks if it's actually visible on screen
        //   return el                       → if visible, return the element → wait STOPS
        //   return null                     → if not visible yet, return null → wait CONTINUES polling
        //
        // This pattern (return element or null) is the standard Fluent Wait custom condition pattern
        WebElement result = fluentWait.until(
            d -> {
                WebElement el = d.findElement(By.id("finish"));
                return el.isDisplayed() ? el : null;
            }
        );

        // Step 7: Assert the text content of the result element
        // Verifies the dynamic content loaded correctly
        // Test FAILS if text doesn't match, PASSES if it does
        Assert.assertEquals(result.getText(), "Hello World!");

        // Step 8: Print confirmation to console
        System.out.println("✅ Fluent Wait verified: " + result.getText());
    
    }
}