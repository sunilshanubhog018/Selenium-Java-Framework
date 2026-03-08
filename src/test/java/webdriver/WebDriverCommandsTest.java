package webdriver;

import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.*;
import org.testng.Assert;
import org.testng.annotations.*;

import base.BaseTest;

import java.time.Duration;
import java.util.Set;

public class WebDriverCommandsTest extends BaseTest {
    // ── gap helper ────────────────────────────────────────────────────
    public void pause() {
        try {
            Thread.sleep(5000); // 5 second gap
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    // ── TEST 1: Navigate & Verify Title ──────────────────────────────
    @Test
    public void test01_NavigateAndTitle() {
        driver.get("https://www.google.com");
        String title = driver.getTitle();
        Assert.assertEquals(title, "Google", "Title mismatch!");
        pause();
    }

    // ── TEST 2: Search & Verify URL ──────────────────────────────────
    @Test
    public void test02_SearchAndVerifyURL() {
        driver.get("https://www.google.com");
        WebElement searchBox = driver.findElement(By.name("q"));
        searchBox.sendKeys("Selenium WebDriver" + Keys.ENTER);
        String url = driver.getCurrentUrl();
        Assert.assertTrue(url.contains("Selenium"), "URL does not contain 'Selenium'");
        pause();
    }

    // ── TEST 3: Back & Forward Navigation ───────────────────────────
    @Test
    public void test03_BackAndForwardNavigation() {
        driver.get("https://example.com");
        String titleA = driver.getTitle();
        driver.get("https://www.google.com");
        driver.navigate().back();
        Assert.assertEquals(driver.getTitle(), titleA, "Back navigation failed");
        driver.navigate().forward();
        Assert.assertTrue(driver.getTitle().contains("Google"), "Forward navigation failed");
        pause();
    }

    // ── TEST 4: Form Fill & Clear ────────────────────────────────────
    @Test
    public void test04_FormFillAndClear() {
        driver.get("https://the-internet.herokuapp.com/login");
        WebElement username = driver.findElement(By.id("username"));
        WebElement password = driver.findElement(By.id("password"));
        username.sendKeys("tomsmith");
        password.sendKeys("wrongpass");
        password.clear();
        password.sendKeys("SuperSecretPassword!");
        Assert.assertFalse(password.getDomProperty("value").isEmpty(), "Password field is empty");
        pause();
    }

    // ── TEST 5: Verify Element Visibility ────────────────────────────
    @Test
    public void test05_ElementVisibility() {
        driver.get("https://the-internet.herokuapp.com/dynamic_loading/1");
        WebElement result = driver.findElement(By.id("finish"));
        Assert.assertFalse(result.isDisplayed(), "Element should be hidden initially");
        driver.findElement(By.cssSelector("#start button")).click();
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        wait.until(ExpectedConditions.visibilityOf(result));
        Assert.assertTrue(result.isDisplayed(), "Element should be visible after load");
        pause();
    }

    // ── TEST 6: Implicit Wait ─────────────────────────────────────────
    @Test
    public void test06_ImplicitWait() {
        driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10));
        driver.get("https://the-internet.herokuapp.com/dynamic_loading/2");
        driver.findElement(By.cssSelector("#start button")).click();
        WebElement finish = driver.findElement(By.id("finish"));
        Assert.assertTrue(finish.isDisplayed(), "Finish element not visible");
        Assert.assertEquals(finish.getText(), "Hello World!", "Text mismatch");
        pause();
    }

    // ── TEST 7: Explicit Wait – Clickable ────────────────────────────
    @Test
    public void test07_ExplicitWaitClickable() {
        driver.get("https://the-internet.herokuapp.com/dynamic_controls");
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(15));
        driver.findElement(By.cssSelector("button[onclick='swapCheckbox()']")).click();
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("message")));
        WebElement msg = driver.findElement(By.id("message"));
        Assert.assertTrue(msg.isDisplayed(), "Message not displayed after wait");
        pause();
    }

    // ── TEST 8: Cookie Management ─────────────────────────────────────
    @Test
    public void test08_CookieManagement() {
        driver.get("https://example.com");
        driver.manage().addCookie(new Cookie("testKey", "testValue"));
        Set<Cookie> cookies = driver.manage().getCookies();
        boolean found = cookies.stream().anyMatch(c -> c.getName().equals("testKey"));
        Assert.assertTrue(found, "Cookie 'testKey' not found");
        driver.manage().deleteAllCookies();
        Assert.assertTrue(driver.manage().getCookies().isEmpty(), "Cookies not cleared");
        pause();
    }

    // ── TEST 9: Multiple Windows ──────────────────────────────────────
    @Test
    public void test09_MultipleWindows() {
        driver.get("https://the-internet.herokuapp.com/windows");
        String mainHandle = driver.getWindowHandle();
        driver.findElement(By.linkText("Click Here")).click();
        Set<String> handles = driver.getWindowHandles();
        for (String handle : handles) {
            if (!handle.equals(mainHandle)) {
                driver.switchTo().window(handle);
                break;
            }
        }
        
        wait.until(ExpectedConditions.titleIs("New Window"));
        Assert.assertEquals(driver.getTitle(), "New Window", "New window title mismatch");
        driver.close();
        driver.switchTo().window(mainHandle);
        Assert.assertEquals(driver.getTitle(), "The Internet", "Main window title mismatch");
        pause();
    }

    // ── TEST 10: Page Refresh Resets Form ────────────────────────────
    @Test
    public void test10_RefreshResetsForm() {
        driver.get("https://the-internet.herokuapp.com/login");
        WebElement username = driver.findElement(By.id("username"));
        username.sendKeys("tomsmith");
        Assert.assertEquals(username.getDomProperty("value"), "tomsmith");
        driver.navigate().refresh();
        WebElement freshUsername = driver.findElement(By.id("username"));
        Assert.assertEquals(freshUsername.getDomProperty("value"), "",
                "Field should be empty after refresh");
        pause();
    }

    @AfterMethod
    public void teardown() {
        if (driver != null) driver.quit();
    }
}