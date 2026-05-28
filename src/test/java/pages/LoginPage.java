package pages;

import base.BasePage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;

public class LoginPage extends BasePage {

    // ================================================================
    //  LOCATORS - all elements on the Login page
    //  If ParaBank changes their HTML, update ONLY these locators
    //  No test code changes needed
    // ================================================================

    private final By usernameInput = By.name("username");
    private final By passwordInput = By.name("password");
    private final By loginButton = By.cssSelector("input[value='Log In']");
    private final By registerLink = By.linkText("Register");
    private final By forgotLoginLink = By.linkText("Forgot login info?");
    // Two separate locators for better verification
    // errorTitle  → <h1 class="title">Error!</h1>
    // errorMessage → <p class="error">The username and password could not be verified.</p>
    private final By errorTitle = By.cssSelector("h1.title");
    private final By errorMessage = By.cssSelector("p.error");

    // ================================================================
    //  CONSTRUCTOR - receives driver from test class
    //  Calls BasePage constructor which sets up driver + wait
    // ================================================================

    public LoginPage(WebDriver driver) {
        super(driver);  // Passes driver to BasePage constructor
    }

    // ================================================================
    //  PAGE ACTIONS - what a user can DO on this page
    //  Each method returns a page object for method chaining
    // ================================================================

    // Enter username in the username field
    public LoginPage enterUsername(String username) {
        type(usernameInput, username);  // type() comes from BasePage
        return this;  // Returns itself for method chaining
    }

    // Enter password in the password field
    public LoginPage enterPassword(String password) {
        type(passwordInput, password);
        return this;
    }

    // Click the Log In button
    public void clickLogin() {
        click(loginButton);  // click() comes from BasePage
    }

    // Complete login in one step (username + password + click)
    // This is a convenience method - combines 3 actions into 1
    public void login(String username, String password) {
        enterUsername(username);
        enterPassword(password);
        clickLogin();
    }

    // Click "Register" link to go to registration page
    public void clickRegister() {
        click(registerLink);
    }

    // Click "Forgot login info?" link
    public void clickForgotLogin() {
        click(forgotLoginLink);
    }

    // ================================================================
    //  PAGE VERIFICATIONS - check what's visible on the page
    //  Used by test assertions to verify page state
    // ================================================================

    // Check if error title "Error!" heading is displayed
    // Used in: testInvalidLogin (Test 5)
    public boolean isErrorTitleDisplayed() {
        try {
            return wait.until(ExpectedConditions.visibilityOfElementLocated(errorTitle)).isDisplayed();
        } catch (Exception e) {
            return false;
        }
    }

    // Get error title text (e.g., "Error!")
    // Used in: testInvalidLogin (Test 5) → assertEquals("Error!")
    public String getErrorTitle() {
        return getText(errorTitle);  // getText() comes from BasePage
    }

    // Check if error message paragraph is displayed
    // Used in: testEmptyBothFields, testEmptyUsername, testEmptyPassword,
    //          testInvalidUsername, testInvalidPassword (Tests 2, 3, 4, 6, 7)
    public boolean isErrorDisplayed() {
        try {
            return wait.until(ExpectedConditions.visibilityOfElementLocated(errorMessage)).isDisplayed();
        } catch (Exception e) {
            return false;
        }
    }

    // Get error message text (e.g., "The username and password could not be verified.")
    // Used in: testInvalidLogin (Test 5) → assertEquals(expectedMessage)
    public String getErrorMessage() {
        return getText(errorMessage);  // getText() comes from BasePage
    }

    // Check if login form is displayed (verifies we're on login page)
    // Used in: testLoginFormDisplayed (Test 1)
    public boolean isLoginFormDisplayed() {
        return isDisplayed(usernameInput);
    }
}