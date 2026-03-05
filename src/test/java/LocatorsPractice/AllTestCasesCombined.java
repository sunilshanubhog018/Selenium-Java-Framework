package LocatorsPractice;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.Select;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.Assert;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;

import java.time.Duration;
import java.util.List;

public class AllTestCasesCombined {

    WebDriver driver;

    @BeforeMethod
    public void setUp() {
        driver = new ChromeDriver();
        driver.manage().window().maximize();
    }

    @AfterMethod
    public void tearDown() {
        driver.quit();
    }

    // Test 1: By.id
    @Test
    public void testValidLogin() {
        driver.get("https://the-internet.herokuapp.com/login");

        driver.findElement(By.id("username")).sendKeys("tomsmith");
        driver.findElement(By.id("password")).sendKeys("SuperSecretPassword!");
        driver.findElement(By.cssSelector("button[type='submit']")).click();
        
        // Wait for flash message to appear (max 10 seconds)
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        WebElement flash = wait.until(
            ExpectedConditions.visibilityOfElementLocated(By.id("flash"))
        );

        String message = driver.findElement(By.id("flash")).getText();
        Assert.assertTrue(message.contains("You logged into a secure area!"));
    }

    // Test 2: By.cssSelector (id + class combo)
    @Test
    public void testInvalidLogin() {
        driver.get("https://the-internet.herokuapp.com/login");

        driver.findElement(By.cssSelector("input#username")).sendKeys("wronguser");
        driver.findElement(By.cssSelector("input#password")).sendKeys("wrongpass");
        driver.findElement(By.cssSelector("button.radius")).click();

        String error = driver.findElement(By.cssSelector("#flash.error")).getText();
        Assert.assertTrue(error.contains("Your username is invalid!"));
    }

    // Test 3: By.linkText
    @Test
    public void testNavigateByLink() {
        driver.get("https://the-internet.herokuapp.com");

        driver.findElement(By.linkText("Dropdown")).click();

        String heading = driver.findElement(By.tagName("h3")).getText();
        Assert.assertEquals(heading, "Dropdown List");
    }

    // Test 4: By.partialLinkText
    @Test
    public void testPartialLinkNavigation() {
        driver.get("https://the-internet.herokuapp.com");

        driver.findElement(By.partialLinkText("Drag")).click();

        String heading = driver.findElement(By.tagName("h3")).getText();
        Assert.assertEquals(heading, "Drag and Drop");
    }

    // Test 5: By.cssSelector + Select class
    @Test
    public void testDropdownSelection() {
        driver.get("https://the-internet.herokuapp.com/dropdown");

        WebElement dropdown = driver.findElement(By.cssSelector("select#dropdown"));
        Select select = new Select(dropdown);

        select.selectByVisibleText("Option 2");

        String selected = select.getFirstSelectedOption().getText();
        Assert.assertEquals(selected, "Option 2");
    }

    // Test 6: By.xpath with contains()
    @Test
    public void testCheckboxSelection() {
        driver.get("https://the-internet.herokuapp.com/checkboxes");

        List<WebElement> checkboxes = driver.findElements(
            By.xpath("//input[contains(@type,'check')]")
        );

        if (!checkboxes.get(0).isSelected()) {
            checkboxes.get(0).click();
        }

        Assert.assertTrue(checkboxes.get(0).isSelected());
    }

    // Test 7: By.xpath with index
    @Test
    public void testReadDynamicText() {
        driver.get("https://the-internet.herokuapp.com/dynamic_content");

        String text = driver.findElement(
            By.xpath("(//div[@class='large-10 columns'])[1]")
        ).getText();

        Assert.assertFalse(text.isEmpty(), "Dynamic content should not be empty");
    }

    // Test 8: By.className
    @Test
    public void testElementState() {
        driver.get("https://the-internet.herokuapp.com/login");

        WebElement loginButton = driver.findElement(By.className("radius"));

        Assert.assertTrue(loginButton.isDisplayed(), "Button should be visible");
        Assert.assertTrue(loginButton.isEnabled(), "Button should be enabled");
    }

    // Test 9: By.tagName + findElements
    @Test
    public void testCountElements() {
        driver.get("https://the-internet.herokuapp.com/checkboxes");

        List<WebElement> checkboxes = driver.findElements(By.tagName("input"));

        Assert.assertEquals(checkboxes.size(), 2, "Should have 2 checkboxes");
    }

    // Test 10: By.xpath with axes (banking pattern)
    @Test
    public void testTableNavigation() {
        driver.get("https://the-internet.herokuapp.com/tables");

        WebElement editLink = driver.findElement(
            By.xpath("//td[text()='Smith']/parent::tr//a[contains(text(),'edit')]")
        );

        Assert.assertTrue(editLink.isDisplayed());
        editLink.click();
    }
}