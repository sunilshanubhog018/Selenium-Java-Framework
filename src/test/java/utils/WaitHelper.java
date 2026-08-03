package utils;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import pages.LoginPage;

import java.time.Duration;

/**
 * Shared explicit-wait helpers. Prefer these over Thread.sleep for UI recovery / retries.
 */
public final class WaitHelper {

    private static final By USERNAME = By.name("username");
    private static final By REGISTER_FIRST_NAME = By.id("customer.firstName");
    private static final By REGISTER_LINK = By.linkText("Register");
    private static final By ADMIN_INIT = By.cssSelector("button[value='INIT']");

    private WaitHelper() {
    }

    private static int explicitSeconds() {
        return Integer.parseInt(ConfigReader.get("explicit.wait"));
    }

    private static WebDriverWait wait(WebDriver driver) {
        return new WebDriverWait(driver, Duration.ofSeconds(explicitSeconds()));
    }

    private static WebDriverWait wait(WebDriver driver, int seconds) {
        return new WebDriverWait(driver, Duration.ofSeconds(seconds));
    }

    /** Login form is ready (username field visible). */
    public static void waitForLoginForm(WebDriver driver) {
        wait(driver).until(ExpectedConditions.visibilityOfElementLocated(USERNAME));
    }

    /** Registration form is ready. */
    public static void waitForRegisterForm(WebDriver driver) {
        wait(driver).until(ExpectedConditions.visibilityOfElementLocated(REGISTER_FIRST_NAME));
    }

    /**
     * After a failed attempt: reload home and wait until the login form is interactive again
     * instead of Thread.sleep.
     */
    public static void recoverToLoginForm(WebDriver driver) {
        driver.get(ConfigReader.get("base.url"));
        waitForLoginForm(driver);
    }

    /**
     * After a failed registration: reload home, open Register, wait for form.
     */
    public static void recoverToRegisterForm(WebDriver driver) {
        driver.get(ConfigReader.get("base.url"));
        wait(driver).until(ExpectedConditions.elementToBeClickable(REGISTER_LINK)).click();
        waitForRegisterForm(driver);
    }

    /** Admin page INIT button is clickable. */
    public static void waitForAdminInitButton(WebDriver driver) {
        wait(driver, 20).until(ExpectedConditions.elementToBeClickable(ADMIN_INIT));
    }

    /**
     * After clicking INIT, wait until the button is usable again (page finished processing)
     * or admin content is still present — avoids fixed 3s sleep.
     */
    public static void waitForAdminInitSettled(WebDriver driver) {
        wait(driver, 20).until(ExpectedConditions.or(
                ExpectedConditions.elementToBeClickable(ADMIN_INIT),
                ExpectedConditions.presenceOfElementLocated(By.id("rightPanel")),
                ExpectedConditions.presenceOfElementLocated(By.cssSelector("#rightPanel, #leftPanel, form"))
        ));
    }

    /**
     * Login with retries. On failure, recover via explicit wait to login form (no Thread.sleep).
     */
    public static void loginWithRetry(WebDriver driver, String username, String password) {
        RuntimeException last = null;
        for (int attempt = 1; attempt <= 3; attempt++) {
            try {
                driver.get(ConfigReader.get("base.url"));
                waitForLoginForm(driver);
                LoginPage loginPage = new LoginPage(driver);
                loginPage.login(username, password);
                loginPage.waitForUrl("overview");
                return;
            } catch (RuntimeException e) {
                last = e;
                System.out.println("  ⚠ Login attempt " + attempt + " failed, recovering to login form...");
                try {
                    recoverToLoginForm(driver);
                } catch (Exception recoverEx) {
                    // next attempt will navigate again
                }
            }
        }
        throw new RuntimeException("Login failed after 3 attempts for user " + username, last);
    }
}
