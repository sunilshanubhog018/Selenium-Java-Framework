package tests;

import base.BaseTest;
import org.testng.Assert;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;
import pages.LoginPage;
import utils.ConfigReader;

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
    @Test(priority = 1, description = "Verify login form is visible on homepage")
    public void testLoginFormDisplayed() {
        // LoginPage method returns true/false
        // Assert checks: is it true? If not, test fails with message
        Assert.assertTrue(loginPage.isLoginFormDisplayed(),
                "Login form should be visible on homepage!");
    }

    // ================================================================
    //  TEST 2: Login with empty username and password
    // ================================================================
    @Test(priority = 2, description = "Click login without entering anything")
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
    @Test(priority = 3, description = "Login with empty username")
    public void testEmptyUsername() {
        loginPage.enterPassword("Test@1234");
        loginPage.clickLogin();

        Assert.assertTrue(loginPage.isErrorDisplayed(),
                "Error should appear when username is empty!");
    }

    // ================================================================
    //  TEST 4: Login with empty password only
    // ================================================================
    @Test(priority = 4, description = "Login with empty password")
    public void testEmptyPassword() {
        loginPage.enterUsername("testuser123");
        loginPage.clickLogin();

        Assert.assertTrue(loginPage.isErrorDisplayed(),
                "Error should appear when password is empty!");
    }

    @Test(priority = 5, description = "Login with wrong username and password")
    public void testInvalidLogin() {
        loginPage.login("wronguser", "wrongpass");

        // Verify error title heading is displayed
        Assert.assertTrue(loginPage.isErrorTitleDisplayed(),
                "Error! heading should appear for invalid credentials");

        // Verify error title text
        Assert.assertEquals(loginPage.getErrorTitle(), "Error!",
                "Error title text mismatch");

        // Verify error message text
        Assert.assertEquals(loginPage.getErrorMessage(),
                "The username and password could not be verified.",
                "Error message text mismatch");
    }

    // ================================================================
    //  TEST 6: Login with invalid username, valid password
    // ================================================================
    @Test(priority = 6, description = "Login with wrong username")
    public void testInvalidUsername() {
        loginPage.login("nonexistentuser", ConfigReader.get("test.password"));

        Assert.assertTrue(loginPage.isErrorDisplayed(),
                "Error should appear for invalid username!");
    }

    // ================================================================
    //  TEST 7: Login with valid username, invalid password
    // ================================================================
    @Test(priority = 7, description = "Login with wrong password")
    public void testInvalidPassword() {
        loginPage.login(ConfigReader.get("test.username"), "WrongPass999");

        Assert.assertTrue(loginPage.isErrorDisplayed(),
                "Error should appear for invalid password!");
    }

    // ================================================================
    //  TEST 8: Verify Register link works
    // ================================================================
    @Test(priority = 8, description = "Click Register link and verify registration page")
    public void testRegisterLink() {
        loginPage.clickRegister();

        // After clicking Register, URL should contain "register"
        Assert.assertTrue(getDriver().getCurrentUrl().contains("register"),
                "Should navigate to registration page! URL: " + getDriver().getCurrentUrl());
    }

    // ================================================================
    //  TEST 9: Verify Forgot Login link works
    // ================================================================
    @Test(priority = 9, description = "Click Forgot Login and verify lookup page")
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
    @Test(priority = 10, description = "Login with valid credentials")
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
        try {
            Thread.sleep(3000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        getDriver().findElement(org.openqa.selenium.By.linkText("Log Out")).click();
    }
}