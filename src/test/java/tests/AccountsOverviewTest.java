package tests;

import base.BaseTest;
import io.qameta.allure.Epic;
import io.qameta.allure.Feature;
import io.qameta.allure.Story;
import org.openqa.selenium.By;
import org.testng.Assert;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;
import pages.AccountsOverviewPage;
import pages.LoginPage;
import pages.RegisterPage;
import utils.ConfigReader;

@Epic("Banking Application")
@Feature("Accounts Overview")
public class AccountsOverviewTest extends BaseTest {

    private AccountsOverviewPage accountsPage;

    private static final String PASSWORD = "Test@1234";
    private static String sharedUsername;

    @org.testng.annotations.BeforeClass
    public void registerSharedUser() throws Exception {
        setUp();
        sharedUsername = "acc_" + System.currentTimeMillis();
        getDriver().get(ConfigReader.get("base.url") + "register.htm");
        RegisterPage registerPage = new RegisterPage(getDriver());
        registerPage.registerUser(
                "Account", "Tester", "789 Bank Street",
                "Mumbai", "MH", "400001",
                "9988776655", "456-78-9012",
                sharedUsername, PASSWORD
        );
        registerPage.waitForUrl("overview");
        new AccountsOverviewPage(getDriver()).logout();
        tearDown();
    }

    @BeforeMethod
    public void navigateToAccountsOverview() {
        for (int attempt = 1; attempt <= 3; attempt++) {
            try {
                getDriver().get(ConfigReader.get("base.url"));
                LoginPage loginPage = new LoginPage(getDriver());
                loginPage.login(sharedUsername, PASSWORD);
                loginPage.waitForUrl("overview");
                break;
            } catch (Exception e) {
                if (attempt == 3) throw new RuntimeException("Login failed after 3 attempts", e);
                System.out.println("  ⚠ Login attempt " + attempt + " failed, retrying...");
                try { Thread.sleep(2000); } catch (InterruptedException ie) { Thread.currentThread().interrupt(); }
            }
        }

        accountsPage = new AccountsOverviewPage(getDriver());
        accountsPage.clickAccountsOverview();
        accountsPage.waitForUrl("overview");
    }

    @Test(priority = 1, groups = {"regression", "accounts"}, description = "Verify Accounts Overview page title")
    @Story("Page title verification")
    public void testPageTitle() {
        Assert.assertTrue(accountsPage.isOnAccountsOverviewPage(),
                "Should be on Accounts Overview page!");
    }

    @Test(priority = 2, groups = {"regression", "accounts"}, description = "Verify accounts table is visible")
    @Story("Accounts table visibility")
    public void testAccountsTableDisplayed() {
        Assert.assertTrue(accountsPage.isAccountsTableDisplayed(),
                "Accounts table should be visible!");
    }

    @Test(priority = 3, groups = {"regression", "accounts"}, description = "Verify new user has at least one account")
    @Story("Account existence")
    public void testAccountExists() {
        int count = accountsPage.getAccountCount();
        Assert.assertTrue(count >= 1,
                "New user should have at least 1 account! Found: " + count);
    }

    @Test(priority = 4, groups = {"regression", "accounts"}, description = "Verify account number is displayed")
    @Story("Account number display")
    public void testAccountNumberDisplayed() {
        String accountNumber = accountsPage.getFirstAccountNumber();
        Assert.assertFalse(accountNumber.isEmpty(),
                "Account number should not be empty!");
    }

    @Test(priority = 5, groups = {"regression", "accounts"}, description = "Verify total balance is shown")
    @Story("Total balance display")
    public void testTotalBalanceDisplayed() {
        String total = accountsPage.getTotalBalance();
        Assert.assertTrue(total.contains("$"),
                "Total balance should contain dollar sign! Got: " + total);
    }

    @Test(priority = 6, groups = {"regression", "accounts"}, description = "Verify Transfer Funds link navigates correctly")
    @Story("Transfer funds navigation")
    public void testTransferFundsLink() {
        accountsPage.clickTransferFunds();
        accountsPage.waitForUrl("transfer");
        Assert.assertTrue(getDriver().getCurrentUrl().contains("transfer"),
                "Should navigate to Transfer Funds page!");
    }

    @Test(priority = 7, groups = {"regression", "accounts"}, description = "Verify logout returns to login page")
    @Story("Logout functionality")
    public void testLogOut() {
        accountsPage.clickLogOut();
        LoginPage loginPage = new LoginPage(getDriver());
        loginPage.waitForVisible(By.name("username"));
        Assert.assertTrue(loginPage.isLoginFormDisplayed(),
                "Should see login form after logout!");
    }
}
