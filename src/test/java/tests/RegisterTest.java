package tests;

import base.BaseTest;
import io.qameta.allure.Epic;
import io.qameta.allure.Feature;
import io.qameta.allure.Story;
import org.testng.Assert;
import org.testng.asserts.SoftAssert;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;
import pages.LoginPage;
import pages.RegisterPage;
import utils.ConfigReader;

@Epic("Banking Application")
@Feature("Registration")
public class RegisterTest extends BaseTest {

    private RegisterPage registerPage;

    @BeforeMethod
    public void navigateToRegisterPage() {
        // Go to login page first, then click Register
    	getDriver().get(ConfigReader.get("base.url"));
    	LoginPage loginPage = new LoginPage(getDriver());  
        loginPage.clickRegister();
        registerPage = new RegisterPage(getDriver()); 
    }

    // ================================================================
    //  TEST 1: Verify registration form is displayed
    // ================================================================
    @Test(priority = 1, groups = {"smoke", "regression", "register"}, description = "Verify registration form loads")
    @Story("Registration form visibility")
    public void testRegisterFormDisplayed() {
        Assert.assertTrue(registerPage.isRegisterFormDisplayed(),
                "Registration form should be visible!");
    }

    // ================================================================
    //  TEST 2: Register with all fields empty
    // ================================================================
    @Test(priority = 2, groups = {"regression", "register"}, description = "Submit empty registration form")
    @Story("Empty form validation")
    public void testEmptyRegistration() {
        registerPage.clickRegister();

        SoftAssert softAssert = new SoftAssert();
        softAssert.assertTrue(registerPage.isFirstNameErrorDisplayed(), "First name error should appear!");
        softAssert.assertTrue(registerPage.isLastNameErrorDisplayed(), "Last name error should appear!");
        softAssert.assertTrue(registerPage.isUsernameErrorDisplayed(), "Username error should appear!");
        softAssert.assertTrue(registerPage.isPasswordErrorDisplayed(), "Password error should appear!");
        softAssert.assertAll();
    }

    @Test(priority = 3, groups = {"smoke", "regression", "register"}, description = "Register new user with valid data")
    @Story("Valid registration")
    public void testValidRegistration() {
        // Dynamic username — unique every run
        String username = "user_" + System.currentTimeMillis();
        String password = ConfigReader.get("test.password");

        registerPage.registerUser(
                "Test", "User", "123 Main Street",
                "New York", "NY", "10001",
                "1234567890", "123-45-6789",
                username, password
        );

        // Pause to see the result on UI
        //try { Thread.sleep(5000); } catch (InterruptedException e) {}
        
        // After successful registration, h1 shows "Welcome <username>"
        String title = registerPage.getSuccessTitle();
        Assert.assertTrue(title.contains("elcome"),
                "Should show welcome message after registration! Got: " + title);
    }
    // ================================================================
    //  TEST 4: Register with duplicate username
    // ================================================================
    @Test(priority = 4, groups = {"regression", "register"}, description = "Register with already existing username")
    @Story("Duplicate username validation")
    public void testDuplicateUsername() {
        // First register a user
        String username = "dup_" + System.currentTimeMillis();
        String password = "Test@1234";

        registerPage.registerUser(
                "Test", "User", "123 Main Street",
                "New York", "NY", "10001",
                "1234567890", "123-45-6789",
                username, password
        );

        // Now logout and go back to register page
        registerPage.logout();
        getDriver().get(ConfigReader.get("base.url"));
        LoginPage loginPage = new LoginPage(getDriver());
        loginPage.clickRegister();
        registerPage = new RegisterPage(getDriver());

        // Try same username again
        registerPage.registerUser(
                "Test", "User", "123 Main Street",
                "New York", "NY", "10001",
                "1234567890", "123-45-6789",
                username, password
        );

        // Should show error — username already taken
        Assert.assertTrue(registerPage.isUsernameErrorDisplayed(),
                "Should show error for duplicate username!");
    }

    @Test(priority = 5, groups = {"regression", "register"}, description = "Register new user then login with those credentials")
    @Story("Register then login")
    public void testRegisterThenLogin() {
        String uniqueUsername = "auto_" + System.currentTimeMillis();
        String password = "Test@1234";

        registerPage.registerUser(
                "Selenium", "Tester", "456 Test Avenue",
                "Bangalore", "KA", "560001",
                "9876543210", "987-65-4321",
                uniqueUsername, password
        );

        String title = registerPage.getSuccessTitle();
        Assert.assertTrue(title.contains("Welcome"),
                "Should show welcome message! Got: " + title);

        // Replace driver with getDriver()
        registerPage.logout();
        getDriver().get(ConfigReader.get("base.url"));

        LoginPage loginPage = new LoginPage(getDriver());   // ← fix
        loginPage.login(uniqueUsername, password);

        Assert.assertTrue(
                getDriver().getCurrentUrl().contains("overview"),
                "Should login successfully with newly registered user!");

        loginPage.logout();
    }
}