package utils;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import pages.AccountsOverviewPage;
import pages.RegisterPage;

import java.time.Duration;

/**
 * Shared helper to register a unique ParaBank user with retries.
 * Centralises the pattern used by multiple test classes' @BeforeClass setup.
 */
public final class UserFactory {

    private UserFactory() {
    }

    public static String registerUniqueUser(WebDriver driver, String usernamePrefix, String password) {
        Exception last = null;
        String username = usernamePrefix + System.currentTimeMillis();
        int explicitWait = Integer.parseInt(ConfigReader.get("explicit.wait"));

        for (int attempt = 1; attempt <= 3; attempt++) {
            try {
                username = usernamePrefix + System.currentTimeMillis();
                driver.get(ConfigReader.get("base.url"));
                // Prefer navigation via Register link so the form is fully initialised
                driver.findElement(By.linkText("Register")).click();

                RegisterPage registerPage = new RegisterPage(driver);
                WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(explicitWait));
                wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("customer.firstName")));

                registerPage.registerUser(
                        "Auto", "Tester", "100 Test Street",
                        "Bangalore", "KA", "560001",
                        "9876543210", "123-45-6789",
                        username, password
                );

                waitForRegistrationSuccess(driver, wait, username);

                // Best-effort logout so the next login starts clean
                try {
                    new AccountsOverviewPage(driver).logout();
                } catch (Exception logoutEx) {
                    try {
                        driver.findElement(By.linkText("Log Out")).click();
                    } catch (Exception ignored) {
                        driver.get(ConfigReader.get("base.url") + "logout.htm");
                    }
                }

                System.out.println("  ✓ Registered user: " + username);
                return username;
            } catch (Exception e) {
                last = e;
                String panel = "";
                try {
                    panel = driver.findElement(By.id("rightPanel")).getText().replace("\n", " | ");
                } catch (Exception ignored) {
                }
                System.out.println("  ⚠ Registration attempt " + attempt + " failed: " + e.getMessage());
                if (!panel.isEmpty()) {
                    System.out.println("    rightPanel=[" + panel + "]");
                }
                // Explicit wait recovery instead of Thread.sleep backoff
                try {
                    WaitHelper.recoverToRegisterForm(driver);
                } catch (Exception recoverEx) {
                    // next attempt will navigate again
                }
            }
        }
        throw new RuntimeException("Failed to register user after 3 attempts", last);
    }

    /**
     * ParaBank sometimes redirects to overview.htm after register, and sometimes keeps
     * register.htm while showing "Welcome &lt;user&gt;" with the user already logged in.
     */
    private static void waitForRegistrationSuccess(WebDriver driver, WebDriverWait wait, String username) {
        wait.until(d -> {
            String url = d.getCurrentUrl() != null ? d.getCurrentUrl() : "";
            if (url.contains("overview")) {
                return true;
            }
            try {
                String panel = d.findElement(By.id("rightPanel")).getText();
                if (panel.toLowerCase().contains("welcome")
                        || panel.contains(username)
                        || panel.toLowerCase().contains("account")) {
                    // Exclude validation-error state still on the form
                    boolean stillHasForm = !d.findElements(By.id("customer.firstName")).isEmpty()
                            && d.findElement(By.id("customer.firstName")).isDisplayed();
                    boolean hasLogout = !d.findElements(By.linkText("Log Out")).isEmpty();
                    if (hasLogout || !stillHasForm) {
                        return true;
                    }
                    if (panel.toLowerCase().contains("welcome")) {
                        return true;
                    }
                }
                if (panel.toLowerCase().contains("already exists")
                        || panel.toLowerCase().contains("error")) {
                    throw new RuntimeException("Registration rejected: " + panel.replace("\n", " | "));
                }
            } catch (RuntimeException re) {
                throw re;
            } catch (Exception ignored) {
                // keep waiting
            }
            return false;
        });
    }
}
