package tests;

import base.BaseTest;
import io.qameta.allure.Epic;
import io.qameta.allure.Feature;
import io.qameta.allure.Story;
import org.testng.Assert;
import org.testng.asserts.SoftAssert;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;
import pages.AccountsOverviewPage;
import pages.LoginPage;
import utils.ConfigReader;

@Epic("Banking Application")
@Feature("Login")
public class LoginTest extends BaseTest {

    // LoginPage object - reused across all tests
    private LoginPage loginPage;

    // Runs after BaseTest.setUp() opens the browser
    // Opens ParaBank URL and creates LoginPage object
    @BeforeMethod
    public void navigateToLoginPage() {
    	getDriver().get(ConfigReader.get("base.url"));
        loginPage = new LoginPage(getDriver());
    }

    // ================================================================
    //  TEST 1: Verify login form is displayed when site opens
    // ================================================================
    @Test(priority = 1, groups = {"smoke", "regression", "login"}, description = "Verify login form is visible on homepage")
    @Story("Login form visibility")
    public void testLoginFormDisplayed() {
        // LoginPage method returns true/false
        // Assert checks: is it true? If not, test fails with message
        Assert.assertTrue(loginPage.isLoginFormDisplayed(),
                "Login form should be visible on homepage!");
    }

    // ================================================================
    //  TEST 2: Login with empty username and password
    // ================================================================
    @Test(priority = 2, groups = {"regression", "login"}, description = "Click login without entering anything")
    @Story("Empty credentials validation")
    public void testEmptyBothFields() {
        // Click login without typing anything
        loginPage.clickLogin();

        // Error message should appear
        Assert.assertTrue(loginPage.isErrorDisplayed(),
                "Error should appear for empty credentials!");
    }

    // ================================================================
    //  TEST 3: Login with empty username only
    // ================================================================
    @Test(priority = 3, groups = {"regression", "login"}, description = "Login with empty username")
    @Story("Empty username validation")
    public void testEmptyUsername() {
        loginPage.enterPassword("Test@1234");
        loginPage.clickLogin();

        Assert.assertTrue(loginPage.isErrorDisplayed(),
                "Error should appear when username is empty!");
    }

    // ================================================================
    //  TEST 4: Login with empty password only
    // ================================================================
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
        loginPage.login("wronguser", "wrongpass");

        SoftAssert softAssert = new SoftAssert();
        softAssert.assertTrue(loginPage.isErrorTitleDisplayed(),
                "Error! heading should appear for invalid credentials");
        softAssert.assertEquals(loginPage.getErrorTitle(), "Error!",
                "Error title text mismatch");
        String errorMsg = loginPage.getErrorMessage();
        softAssert.assertTrue(
                errorMsg.contains("could not be verified") || errorMsg.contains("internal error") || errorMsg.contains("Error"),
                "Error message should indicate login failure. Got: " + errorMsg);
        softAssert.assertAll();
    }

    // ================================================================
    //  TEST 6: Login with invalid username, valid password
    // ================================================================
    @Test(priority = 6, groups = {"regression", "login"}, description = "Login with wrong username")
    @Story("Invalid username validation")
    public void testInvalidUsername() {
        loginPage.login("nonexistentuser", ConfigReader.get("test.password"));

        Assert.assertTrue(loginPage.isErrorDisplayed(),
                "Error should appear for invalid username!");
    }

    // ================================================================
    //  TEST 7: Login with valid username, invalid password
    // ================================================================
    @Test(priority = 7, groups = {"regression", "login"}, description = "Login with wrong password")
    @Story("Invalid password validation")
    public void testInvalidPassword() {
        loginPage.login(ConfigReader.get("test.username"), "WrongPass999");

        Assert.assertTrue(loginPage.isErrorDisplayed(),
                "Error should appear for invalid password!");
    }

    // ================================================================
    //  TEST 8: Verify Register link works
    // ================================================================
    @Test(priority = 8, groups = {"regression", "login"}, description = "Click Register link and verify registration page")
    @Story("Register link navigation")
    public void testRegisterLink() {
        loginPage.clickRegister();

        // After clicking Register, URL should contain "register"
        Assert.assertTrue(getDriver().getCurrentUrl().contains("register"),
                "Should navigate to registration page! URL: " + getDriver().getCurrentUrl());
    }

    // ================================================================
    //  TEST 9: Verify Forgot Login link works
    // ================================================================
    @Test(priority = 9, groups = {"regression", "login"}, description = "Click Forgot Login and verify lookup page")
    @Story("Forgot login navigation")
    public void testForgotLoginLink() {
        loginPage.clickForgotLogin();

        // After clicking, URL should contain "lookup"
        Assert.assertTrue(getDriver().getCurrentUrl().contains("lookup"),
                "Should navigate to lookup page! URL: " + getDriver().getCurrentUrl());
    }

    // ================================================================
    //  TEST 10: Valid login (needs registered user)
    //  We will create RegisterPage next to set up test user
    // ================================================================
    @Test(priority = 10, groups = {"smoke", "regression", "login"}, description = "Login with valid credentials")
    @Story("Valid login")
    public void testValidLogin() {
        // Read credentials from config.properties
        String username = ConfigReader.get("test.username");
        String password = ConfigReader.get("test.password");

        loginPage.login(username, password);

        // After successful login, URL should contain "overview"
        // and page should show "Accounts Overview"
        		Assert.assertTrue(
        		        getDriver().getCurrentUrl().contains("overview"),
        		        "Should redirect to accounts overview after login! URL: " + getDriver().getCurrentUrl());

        // Wait 3 seconds then logout
        new AccountsOverviewPage(getDriver()).waitForUrl("overview");
        new AccountsOverviewPage(getDriver()).logout();
    }
}