package testng_basics;

import org.testng.Assert;
import org.testng.annotations.*;

public class Sedondexcersie {

    String appUrl;
    String currentUser;
    boolean isLoggedIn;

    @BeforeClass
    public void setupBrowser() {
        System.out.println("Launching browser...");
        appUrl = "https://demo-bank.com";
        isLoggedIn = false;
    }

    @BeforeMethod
    public void navigateToLogin() {
        System.out.println("Navigating to: " + appUrl + "/login");
        currentUser = null;
    }

    @Test(priority = 1, description = "Verify login with valid credentials")
    public void validLoginTest() {
        // Simulate login
        currentUser = "testuser";
        isLoggedIn = true;

        // Hard Assert — test STOPS here if it fails
        Assert.assertTrue(isLoggedIn, "User should be logged in");
        Assert.assertEquals(currentUser, "testuser", "Username mismatch");
        System.out.println("✓ Valid login successful");
    }

    @Test(priority = 2, description = "Verify login fails with wrong password")
    public void invalidPasswordTest() {
        // Simulate failed login
        currentUser = null;
        isLoggedIn = false;

        Assert.assertFalse(isLoggedIn, "User should NOT be logged in");
        Assert.assertNull(currentUser, "Username should be null on failed login");
        System.out.println("✓ Invalid password correctly rejected");
    }

    @Test(priority = 3, description = "Verify empty fields show error")
    public void emptyFieldsTest() {
        String errorMessage = "Username and password are required";

        Assert.assertNotNull(errorMessage, "Error message should be displayed");
        Assert.assertTrue(errorMessage.contains("required"), "Error should mention 'required'");
        System.out.println("✓ Empty fields validation working");
    }

    @Test(priority = 4, dependsOnMethods = "validLoginTest",
          description = "Verify account balance after login")
    public void checkBalanceTest() {
        double balance = 50000.75;

        // This runs ONLY if validLoginTest passed
        Assert.assertTrue(balance > 0, "Balance should be positive");
        Assert.assertNotEquals(balance, 0.0, "Balance should not be zero");
        System.out.println("✓ Balance check passed: ₹" + balance);
    }

    @AfterMethod
    public void logout() {
        if (isLoggedIn) {
            System.out.println("Logging out...");
            isLoggedIn = false;
        }
    }

    @AfterClass
    public void closeBrowser() {
        System.out.println("Closing browser...");
    }
}