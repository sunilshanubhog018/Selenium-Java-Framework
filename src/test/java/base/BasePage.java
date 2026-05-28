package base;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.Select;
import org.openqa.selenium.support.ui.WebDriverWait;
import utils.ConfigReader;

import java.time.Duration;

public class BasePage {

    // Every page needs a driver to interact with browser
    // and a wait to handle slow-loading elements
    protected WebDriver driver;
    protected WebDriverWait wait;

    // Constructor - called when any page object is created
    // Example: LoginPage loginPage = new LoginPage(driver);
    public BasePage(WebDriver driver) {
        this.driver = driver;
        int explicitWait = Integer.parseInt(ConfigReader.get("explicit.wait"));
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(explicitWait));
    }

    // ================================================================
    //  COMMON METHODS - used by all page objects
    // ================================================================

    // Click on any element (waits for it to be clickable first)
    protected void click(By locator) {
        wait.until(ExpectedConditions.elementToBeClickable(locator)).click();
    }

    // Type text into any input field (clears existing text first)
    protected void type(By locator, String text) {
        WebElement element = wait.until(ExpectedConditions.visibilityOfElementLocated(locator));
        element.clear();
        element.sendKeys(text);
    }

    // Get text from any element
    protected String getText(By locator) {
        return wait.until(ExpectedConditions.visibilityOfElementLocated(locator)).getText().trim();
    }

    // Check if element is displayed on page
    protected boolean isDisplayed(By locator) {
        try {
            return wait.until(ExpectedConditions.visibilityOfElementLocated(locator)).isDisplayed();
        } catch (Exception e) {
            return false;
        }
    }

    // Select dropdown option by visible text
    protected void selectByText(By locator, String text) {
        WebElement dropdown = wait.until(ExpectedConditions.visibilityOfElementLocated(locator));
        new Select(dropdown).selectByVisibleText(text);
    }

    // Select dropdown option by value attribute
    protected void selectByValue(By locator, String value) {
        WebElement dropdown = wait.until(ExpectedConditions.visibilityOfElementLocated(locator));
        new Select(dropdown).selectByValue(value);
    }

    // Get current page title
    protected String getPageTitle() {
        return driver.getTitle();
    }

    // Get current page URL
    protected String getCurrentUrl() {
        return driver.getCurrentUrl();
    }

    // Wait for element to disappear (useful for loading spinners)
    protected void waitForElementToDisappear(By locator) {
        wait.until(ExpectedConditions.invisibilityOfElementLocated(locator));
    }
}