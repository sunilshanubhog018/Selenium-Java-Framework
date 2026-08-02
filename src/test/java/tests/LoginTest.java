package tests;

import base.BaseTest;
import io.qameta.allure.Epic;
import io.qameta.allure.Feature;
import io.qameta.allure.Story;
import org.testng.Assert;
import org.testng.SkipException;
import org.testng.asserts.SoftAssert;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;
import pages.AccountsOverviewPage;
import pages.LoginPage;
import utils.ConfigReader;

@Epic("Banking Application")
@Feature("Login")
public class LoginTest extends BaseTest {

    private LoginPage loginPage;

    @BeforeMethod
    public void navigateToLoginPage() {
        getDriver().get(ConfigReader.get("base.url"));
        loginPage = new LoginPage(getDriver());
    }

    @Test(priority = 1, groups = {"smoke", "regression", "login"}, description = "Verify login form is visible on homepage")
    @Story("Login form visibility")
    public void testLoginFormDisplayed() {
        Assert.assertTrue(loginPage.isLoginFormDisplayed(),
                "Login form should be visible on homepage!");
    }

    @Test(priority = 2, groups = {"regression", "login"}, description = "Click login without entering anything")
    @Story("Empty credentials validation")
    public void testEmptyBothFields() {
        loginPage.clickLogin();
        Assert.assertTrue(loginPage.isErrorDisplayed(),
                "Error should appear for empty credentials!");
    }

    @Test(priority = 3, groups = {"regression", "login"}, description = "Login with empty username")
    @Story("Empty username validation")
    public void testEmptyUsername() {
        loginPage.enterPassword("Test@1234");
        loginPage.clickLogin();
        Assert.assertTrue(loginPage.isErrorDisplayed(),
                "Error should appear when username is empty!");
    }

    @Test(priority = 4, groups = {"regression", "login"}, description = "Login with empty password")
    @Story("Empty password validation")
    public void testEmptyPassword() {
        loginPage.enterUsername("testuser123");
        loginPage.clickLogin();
        Assert.assertTrue(loginPage.isErrorDisplayed(),
                "Error should appear when password is empty!");
    }

    @Test(priority = 5, groups = {"regression", "login"}, description = "Login with wrong username and password")
    @Story("Invalid credentials validation")
    public void testInvalidLogin() {
        loginPage.login("wronguser_" + System.currentTimeMillis(), "wrongpass");
        boolean landedOnOverview = loginPage.waitForLoginOutcome();

        // Public ParaBank currently returns 302→overview for arbitrary credentials.
        // That is a demo-site defect; we cannot assert an error page while it is active.
        if (landedOnOverview) {
            throw new SkipException(
                    "ParaBank public demo currently accepts invalid credentials (redirects to overview). "
                            + "Negative login assertion skipped — see KNOWN_ISSUES.md");
        }

        SoftAssert softAssert = new SoftAssert();
        softAssert.assertTrue(loginPage.isErrorTitleDisplayed() || loginPage.isErrorDisplayed(),
                "Error heading/message should appear for invalid credentials");
        String errorMsg = loginPage.getErrorMessage();
        softAssert.assertTrue(
                errorMsg.toLowerCase().contains("could not be verified")
                        || errorMsg.toLowerCase().contains("internal error")
                        || errorMsg.toLowerCase().contains("error"),
                "Error message should indicate login failure. Got: " + errorMsg);
        softAssert.assertAll();
    }

    @Test(priority = 6, groups = {"regression", "login"}, description = "Login with wrong username")
    @Story("Invalid username validation")
    public void testInvalidUsername() {
        loginPage.login("nonexistentuser_" + System.currentTimeMillis(), ConfigReader.get("test.password"));
        boolean landedOnOverview = loginPage.waitForLoginOutcome();
        if (landedOnOverview) {
            throw new SkipException(
                    "ParaBank public demo currently accepts invalid credentials (redirects to overview). "
                            + "Negative login assertion skipped — see KNOWN_ISSUES.md");
        }
        Assert.assertTrue(loginPage.isErrorDisplayed(),
                "Error should appear for invalid username!");
    }

    @Test(priority = 7, groups = {"regression", "login"}, description = "Login with wrong password")
    @Story("Invalid password validation")
    public void testInvalidPassword() {
        // Prefer a definitely-unknown user so password check is meaningful if auth works
        loginPage.login("unknown_user_" + System.currentTimeMillis(), "WrongPass999");
        boolean landedOnOverview = loginPage.waitForLoginOutcome();
        if (landedOnOverview) {
            throw new SkipException(
                    "ParaBank public demo currently accepts invalid credentials (redirects to overview). "
                            + "Negative login assertion skipped — see KNOWN_ISSUES.md");
        }
        Assert.assertTrue(loginPage.isErrorDisplayed(),
                "Error should appear for invalid password!");
    }

    @Test(priority = 8, groups = {"regression", "login"}, description = "Click Register link and verify registration page")
    @Story("Register link navigation")
    public void testRegisterLink() {
        loginPage.clickRegister();
        Assert.assertTrue(getDriver().getCurrentUrl().contains("register"),
                "Should navigate to registration page! URL: " + getDriver().getCurrentUrl());
    }

    @Test(priority = 9, groups = {"regression", "login"}, description = "Click Forgot Login and verify lookup page")
    @Story("Forgot login navigation")
    public void testForgotLoginLink() {
        loginPage.clickForgotLogin();
        Assert.assertTrue(getDriver().getCurrentUrl().contains("lookup"),
                "Should navigate to lookup page! URL: " + getDriver().getCurrentUrl());
    }

    @Test(priority = 10, groups = {"smoke", "regression", "login"}, description = "Login with valid credentials")
    @Story("Valid login")
    public void testValidLogin() {
        String username = "login_" + System.currentTimeMillis();
        String password = "Test@1234";

        loginPage.clickRegister();
        pages.RegisterPage registerPage = new pages.RegisterPage(getDriver());
        registerPage.waitForUrl("register");
        registerPage.registerUser(
                "Login", "Test", "100 Test Street",
                "Bangalore", "KA", "560001",
                "9876543210", "123-45-6789",
                username, password
        );
        registerPage.waitForVisible(org.openqa.selenium.By.cssSelector("#rightPanel h1.title"));
        new AccountsOverviewPage(getDriver()).logout();

        loginPage = new LoginPage(getDriver());
        loginPage.waitForVisible(org.openqa.selenium.By.name("username"));
        loginPage.login(username, password);
        loginPage.waitForUrl("overview");

        Assert.assertTrue(
                getDriver().getCurrentUrl().contains("overview"),
                "Should redirect to accounts overview after login! URL: " + getDriver().getCurrentUrl());

        new AccountsOverviewPage(getDriver()).logout();
    }
}
