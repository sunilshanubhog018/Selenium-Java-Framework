package tests;

import base.BaseTest;
import org.testng.Assert;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;
import pages.LoginPage;
import pages.RegisterPage;
import utils.ConfigReader;
import org.openqa.selenium.By;

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
    @Test(priority = 1, description = "Verify registration form loads")
    public void testRegisterFormDisplayed() {
        Assert.assertTrue(registerPage.isRegisterFormDisplayed(),
                "Registration form should be visible!");
    }

    // ================================================================
    //  TEST 2: Register with all fields empty
    // ================================================================
    @Test(priority = 2, description = "Submit empty registration form")
    public void testEmptyRegistration() {
        registerPage.clickRegister();

        // Error messages should appear for required fields
        Assert.assertTrue(registerPage.isFirstNameErrorDisplayed(),
                "First name error should appear!");
        Assert.assertTrue(registerPage.isLastNameErrorDisplayed(),
                "Last name error should appear!");
        Assert.assertTrue(registerPage.isUsernameErrorDisplayed(),
                "Username error should appear!");
        Assert.assertTrue(registerPage.isPasswordErrorDisplayed(),
                "Password error should appear!");
    }

    @Test(priority = 3, description = "Register new user with valid data")
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

        // Wait 3 seconds after successful registration
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
    // ================================================================
    //  TEST 4: Register with duplicate username
    // ================================================================
    @Test(priority = 4, description = "Register with already existing username")
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
        getDriver().findElement(By.linkText("Log Out")).click();
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

    @Test(priority = 5, description = "Register new user then login with those credentials")
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
        getDriver().findElement(By.linkText("Log Out")).click();
        getDriver().get(ConfigReader.get("base.url"));

        LoginPage loginPage = new LoginPage(getDriver());   // ← fix
        loginPage.login(uniqueUsername, password);

        Assert.assertTrue(
                getDriver().getCurrentUrl().contains("overview"),
                "Should login successfully with newly registered user!");

        try { Thread.sleep(3000); } catch (InterruptedException e) { e.printStackTrace(); }

        getDriver().findElement(By.linkText("Log Out")).click();
    }
}