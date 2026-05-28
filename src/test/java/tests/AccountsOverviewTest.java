package tests;

import base.BaseTest;
import org.openqa.selenium.By;
import org.testng.Assert;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;
import pages.AccountsOverviewPage;
import pages.LoginPage;
import pages.RegisterPage;
import utils.ConfigReader;

public class AccountsOverviewTest extends BaseTest {

    private AccountsOverviewPage accountsPage;

    private void pause(int seconds) {
        try { Thread.sleep(seconds * 1000L); } catch (InterruptedException e) {}
    }

    @BeforeMethod
    public void navigateToAccountsOverview() {
        String username = "acc_" + System.currentTimeMillis();
        String password = "Test@1234";

        getDriver().get(ConfigReader.get("base.url"));
        LoginPage loginPage = new LoginPage(getDriver());
        loginPage.clickRegister();
        pause(2);

        RegisterPage registerPage = new RegisterPage(getDriver());
        registerPage.registerUser(
                "Account", "Tester", "789 Bank Street",
                "Mumbai", "MH", "400001",
                "9988776655", "456-78-9012",
                username, password
        );
        pause(3);

        accountsPage = new AccountsOverviewPage(getDriver());
        accountsPage.clickAccountsOverview();
        pause(3);
    }

    @Test(priority = 1, description = "Verify Accounts Overview page title")
    public void testPageTitle() {
        pause(5);
        Assert.assertTrue(accountsPage.isOnAccountsOverviewPage(),
                "Should be on Accounts Overview page!");
    }

    @Test(priority = 2, description = "Verify accounts table is visible")
    public void testAccountsTableDisplayed() {
        pause(5);
        Assert.assertTrue(accountsPage.isAccountsTableDisplayed(),
                "Accounts table should be visible!");
    }

    @Test(priority = 3, description = "Verify new user has at least one account")
    public void testAccountExists() {
        pause(5);
        int count = accountsPage.getAccountCount();
        Assert.assertTrue(count >= 1,
                "New user should have at least 1 account! Found: " + count);
    }

    @Test(priority = 4, description = "Verify account number is displayed")
    public void testAccountNumberDisplayed() {
        pause(5);
        String accountNumber = accountsPage.getFirstAccountNumber();
        Assert.assertFalse(accountNumber.isEmpty(),
                "Account number should not be empty!");
    }

    @Test(priority = 5, description = "Verify total balance is shown")
    public void testTotalBalanceDisplayed() {
        pause(5);
        String total = accountsPage.getTotalBalance();
        Assert.assertTrue(total.contains("$"),
                "Total balance should contain dollar sign! Got: " + total);
    }

    @Test(priority = 6, description = "Verify Transfer Funds link navigates correctly")
    public void testTransferFundsLink() {
        pause(5);
        accountsPage.clickTransferFunds();
        pause(5);
        Assert.assertTrue(
                getDriver().getCurrentUrl().contains("transfer"),
                "Should navigate to Transfer Funds page!");
    }

    @Test(priority = 7, description = "Verify logout returns to login page")
    public void testLogOut() {
        pause(5);
        accountsPage.clickLogOut();
        pause(5);
        LoginPage loginPage = new LoginPage(getDriver());
        Assert.assertTrue(loginPage.isLoginFormDisplayed(),
                "Should see login form after logout!");
    }
}