package week2.seleniumcore;

import io.github.bonigarcia.wdm.WebDriverManager;
import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.Select;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.Assert;
import org.testng.annotations.*;

import java.time.Duration;
import java.util.List;
import org.openqa.selenium.TimeoutException;

public class Week2_DropdownCheckboxRadioTests {

    WebDriver driver;
    WebDriverWait wait;
    JavascriptExecutor js;
    Actions actions;

    @BeforeMethod
    public void setup() {
        WebDriverManager.chromedriver().setup();
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--headless");
        options.addArguments("--no-sandbox");
        options.addArguments("--disable-dev-shm-usage");
        options.addArguments("--window-size=1920,1080");
        options.addArguments("--disable-blink-features=AutomationControlled");
        driver = new ChromeDriver(options);
        wait    = new WebDriverWait(driver, Duration.ofSeconds(15));
        js      = (JavascriptExecutor) driver;
        actions = new Actions(driver);
        driver.manage().window().maximize();
        driver.manage().timeouts().pageLoadTimeout(Duration.ofSeconds(30));
    }

    @AfterMethod
    public void teardown() {
        if (driver != null) driver.quit();
    }

    // ─────────────────────────────────────────────
    // TEST 1 — passing, no changes
    // ─────────────────────────────────────────────
    @Test(description = "Verify all three selection methods on a native select dropdown")
    public void test1_NativeDropdown_AllThreeMethods() {
        driver.get("https://demoqa.com/select-menu");

        WebElement el = wait.until(ExpectedConditions
            .elementToBeClickable(By.id("oldSelectMenu")));
        js.executeScript("arguments[0].scrollIntoView(true);", el);
        Select select = new Select(el);

        select.selectByVisibleText("Yellow");
        Assert.assertEquals(select.getFirstSelectedOption().getText(), "Yellow",
            "selectByVisibleText failed");

        // value='1' = Blue (confirmed from page)
        select.selectByValue("1");
        Assert.assertEquals(select.getFirstSelectedOption().getText(), "Blue",
            "selectByValue failed");

        // index 2 = Green (confirmed from page)
        select.selectByIndex(2);
        Assert.assertEquals(select.getFirstSelectedOption().getText(), "Green",
            "selectByIndex failed");

        System.out.println("TEST 1 PASSED — All 3 selection methods verified");
    }

    // ─────────────────────────────────────────────
    // TEST 2 — passing, no changes
    // ─────────────────────────────────────────────
    @Test(description = "Verify multi-select dropdown")
    public void test2_MultiSelectDropdown() {
        driver.get("https://demoqa.com/select-menu");

        WebElement el = wait.until(ExpectedConditions
            .presenceOfElementLocated(By.id("cars")));
        js.executeScript("arguments[0].scrollIntoView(true);", el);
        Select ms = new Select(el);

        Assert.assertTrue(ms.isMultiple(), "Should support multi-select");

        ms.selectByValue("volvo");
        ms.selectByValue("saab");
        ms.selectByValue("audi");
        Assert.assertEquals(ms.getAllSelectedOptions().size(), 3);

        ms.deselectByValue("saab");
        Assert.assertEquals(ms.getAllSelectedOptions().size(), 2);

        ms.deselectAll();
        Assert.assertEquals(ms.getAllSelectedOptions().size(), 0);

        System.out.println("TEST 2 PASSED — Multi-select verified");
    }

    // ─────────────────────────────────────────────
    // TEST 3 FIX — confirmed from actual page HTML:
    //
    // DemoQA checkbox is NOT a standard <input> element.
    // It is a <span> using rc-tree library:
    //   <span class="rc-tree-checkbox"
    //         role="checkbox"
    //         aria-checked="false"
    //         aria-label="Select Home">
    //
    // - No input[id='tree-node-home'] exists
    // - isSelected() does NOT work on spans
    // - Must use aria-checked attribute instead
    // - Must click the span directly via JS
    // ─────────────────────────────────────────────
    @Test(description = "Verify checkbox check, result display, and aria-checked state")
    public void test3_Checkboxes_SafeClickPattern() {
        driver.get("https://demoqa.com/checkbox");

        // Confirmed from HTML: span.rc-tree-checkbox[aria-label='Select Home']
        WebElement homeCheckbox = wait.until(ExpectedConditions
            .presenceOfElementLocated(
                By.cssSelector("span.rc-tree-checkbox[aria-label='Select Home']")));

        js.executeScript("arguments[0].scrollIntoView({block:'center'});", homeCheckbox);

        // Verify BEFORE click — aria-checked should be false
        String beforeClick = homeCheckbox.getAttribute("aria-checked");
        System.out.println("aria-checked BEFORE click: " + beforeClick);
        Assert.assertEquals(beforeClick, "false", "Should be unchecked before clicking");

        // JS click the span checkbox
        js.executeScript("arguments[0].click();", homeCheckbox);

        // Verify result panel appears
        WebElement result = wait.until(ExpectedConditions
            .visibilityOfElementLocated(By.id("result")));
        Assert.assertTrue(result.isDisplayed(), "Result panel should be visible");
        Assert.assertTrue(result.getText().toLowerCase().contains("home"),
            "Result should mention 'home'. Actual: " + result.getText());

        // Verify AFTER click — aria-checked should now be true
        // Re-find element after DOM update
        WebElement homeCheckboxAfter = driver.findElement(
            By.cssSelector("span.rc-tree-checkbox[aria-label='Select Home']"));
        String afterClick = homeCheckboxAfter.getAttribute("aria-checked");
        System.out.println("aria-checked AFTER click: " + afterClick);
        Assert.assertEquals(afterClick, "true", "Should be checked after clicking");

        // ── isSelected() guard demo on ALL rc-tree checkboxes ──
        // Note: these are spans — use aria-checked not isSelected()
        List<WebElement> allCheckboxSpans = driver.findElements(
            By.cssSelector("span.rc-tree-checkbox"));
        System.out.println("Total rc-tree checkboxes found: " + allCheckboxSpans.size());

        for (WebElement cb : allCheckboxSpans) {
            System.out.println("  aria-label='" + cb.getAttribute("aria-label")
                + "' aria-checked=" + cb.getAttribute("aria-checked"));
        }

        System.out.println("TEST 3 PASSED — rc-tree checkbox verified via aria-checked");
    }

    // ─────────────────────────────────────────────
    // TEST 4 — passing, no changes for this
    // ─────────────────────────────────────────────
    @Test(description = "Verify radio button group behaviour")
    public void test4_RadioButtons_GroupBehaviour() {
        driver.get("https://demoqa.com/radio-button");

        driver.findElement(By.xpath("//label[@for='yesRadio']")).click();
        Assert.assertTrue(driver.findElement(By.id("yesRadio")).isSelected());

        String result = wait.until(ExpectedConditions
            .visibilityOfElementLocated(By.cssSelector(".mt-3"))).getText();
        Assert.assertTrue(result.contains("Yes"));

        driver.findElement(By.xpath("//label[@for='impressiveRadio']")).click();
        Assert.assertTrue(driver.findElement(By.id("impressiveRadio")).isSelected());
        Assert.assertFalse(driver.findElement(By.id("yesRadio")).isSelected(),
            "Yes should be auto-deselected");

        System.out.println("TEST 4 PASSED — Radio group auto-deselect verified");
    }

 }