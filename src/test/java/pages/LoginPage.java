package pages;

import base.BasePage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

public class LoginPage extends BasePage {

    private final By usernameInput = By.name("username");
    private final By passwordInput = By.name("password");
    private final By loginButton = By.cssSelector("input[value='Log In']");
    private final By registerLink = By.linkText("Register");
    private final By forgotLoginLink = By.linkText("Forgot login info?");

    // Scope errors to the right panel so we don't match unrelated page chrome
    private final By errorTitle = By.cssSelector("#rightPanel h1.title");
    private final By errorMessage = By.cssSelector("#rightPanel p.error");
    private final By rightPanel = By.id("rightPanel");

    public LoginPage(WebDriver driver) {
        super(driver);
    }

    public LoginPage enterUsername(String username) {
        type(usernameInput, username);
        return this;
    }

    public LoginPage enterPassword(String password) {
        type(passwordInput, password);
        return this;
    }

    public void clickLogin() {
        click(loginButton);
    }

    public void login(String username, String password) {
        enterUsername(username);
        enterPassword(password);
        clickLogin();
    }

    public void clickRegister() {
        click(registerLink);
    }

    public void clickForgotLogin() {
        click(forgotLoginLink);
    }

    public boolean isErrorTitleDisplayed() {
        try {
            return wait.until(ExpectedConditions.visibilityOfElementLocated(errorTitle)).isDisplayed()
                    && getText(errorTitle).toLowerCase().contains("error");
        } catch (Exception e) {
            return false;
        }
    }

    public String getErrorTitle() {
        try {
            return getText(errorTitle);
        } catch (Exception e) {
            return "";
        }
    }

    public boolean isErrorDisplayed() {
        try {
            WebDriverWait shortWait = new WebDriverWait(driver, Duration.ofSeconds(5));
            return shortWait.until(ExpectedConditions.visibilityOfElementLocated(errorMessage)).isDisplayed();
        } catch (Exception e) {
            // Fallback: some ParaBank error pages only show title / plain text in right panel
            try {
                String panel = driver.findElement(rightPanel).getText();
                return panel.toLowerCase().contains("error")
                        || panel.toLowerCase().contains("could not be verified")
                        || panel.toLowerCase().contains("internal error");
            } catch (Exception ignored) {
                return false;
            }
        }
    }

    public String getErrorMessage() {
        try {
            WebDriverWait shortWait = new WebDriverWait(driver, Duration.ofSeconds(5));
            return shortWait.until(ExpectedConditions.visibilityOfElementLocated(errorMessage)).getText().trim();
        } catch (Exception e) {
            try {
                return driver.findElement(rightPanel).getText().trim();
            } catch (Exception ignored) {
                return "";
            }
        }
    }

    public boolean isLoginFormDisplayed() {
        return isDisplayed(usernameInput);
    }

    /**
     * Wait until login either succeeds (overview) or fails (error / still on login-ish page).
     * Returns true if redirected to accounts overview.
     */
    public boolean waitForLoginOutcome() {
        WebDriverWait outcomeWait = new WebDriverWait(driver, Duration.ofSeconds(
                Integer.parseInt(utils.ConfigReader.get("explicit.wait"))));
        try {
            outcomeWait.until(d -> {
                String url = d.getCurrentUrl();
                if (url != null && url.contains("overview")) {
                    return true;
                }
                try {
                    if (!d.findElements(errorMessage).isEmpty()
                            && d.findElement(errorMessage).isDisplayed()) {
                        return true;
                    }
                } catch (Exception ignored) {
                    // keep waiting
                }
                try {
                    String panel = d.findElement(rightPanel).getText().toLowerCase();
                    if (panel.contains("error") || panel.contains("could not be verified")
                            || panel.contains("internal error")) {
                        return true;
                    }
                } catch (Exception ignored) {
                    // keep waiting
                }
                return false;
            });
        } catch (Exception ignored) {
            // timed out — fall through with current URL check
        }
        return driver.getCurrentUrl() != null && driver.getCurrentUrl().contains("overview");
    }

    /**
     * True when ParaBank public demo accepts invalid credentials and lands on overview.
     * Observed as HTTP 302 → overview.htm for arbitrary username/password.
     */
    public boolean isAuthBypassActive() {
        return driver.getCurrentUrl() != null && driver.getCurrentUrl().contains("overview");
    }
}
