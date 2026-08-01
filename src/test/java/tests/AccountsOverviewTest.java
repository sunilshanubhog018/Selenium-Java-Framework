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

    @BeforeMethod
    public void navigateToAccountsOverview() {
        String username = "acc_" + System.currentTimeMillis();
        String password = "Test@1234";

        getDriver().get(ConfigReader.get("base.url"));
        LoginPage loginPage = new LoginPage(getDriver());
        loginPage.clickRegister();

        RegisterPage registerPage = new RegisterPage(getDriver());
        registerPage.waitForUrl("register");
        registerPage.registerUser(
                "Account", "Tester", "789 Bank Street",
                "Mumbai", "MH", "400001",
                "9988776655", "456-78-9012",
                username, password
        );
        registerPage.waitForUrl("overview");

        accountsPage = new AccountsOverviewPage(getDriver());
        accountsPage.clickAccountsOverview();
        accountsPage.waitForUrl("overview");
    }

    @Test(priority = 1, description = "Verify Accounts Overview page title")
    @Story("Page title verification")
    public void testPageTitle() {
        Assert.assertTrue(accountsPage.isOnAccountsOverviewPage(),
                "Should be on Accounts Overview page!");
    }

    @Test(priority = 2, description = "Verify accounts table is visible")
    @Story("Accounts table visibility")
    public void testAccountsTableDisplayed() {
        Assert.assertTrue(accountsPage.isAccountsTableDisplayed(),
                "Accounts table should be visible!");
    }

    @Test(priority = 3, description = "Verify new user has at least one account")
    @Story("Account existence")
    public void testAccountExists() {
        int count = accountsPage.getAccountCount();
        Assert.assertTrue(count >= 1,
                "New user should have at least 1 account! Found: " + count);
    }

    @Test(priority = 4, description = "Verify account number is displayed")
    @Story("Account number display")
    public void testAccountNumberDisplayed() {
        String accountNumber = accountsPage.getFirstAccountNumber();
        Assert.assertFalse(accountNumber.isEmpty(),
                "Account number should not be empty!");
    }

    @Test(priority = 5, description = "Verify total balance is shown")
    @Story("Total balance display")
    public void testTotalBalanceDisplayed() {
        String total = accountsPage.getTotalBalance();
        Assert.assertTrue(total.contains("$"),
                "Total balance should contain dollar sign! Got: " + total);
    }

    @Test(priority = 6, description = "Verify Transfer Funds link navigates correctly")
    @Story("Transfer funds navigation")
    public void testTransferFundsLink() {
        accountsPage.clickTransferFunds();
        accountsPage.waitForUrl("transfer");
        Assert.assertTrue(getDriver().getCurrentUrl().contains("transfer"),
                "Should navigate to Transfer Funds page!");
    }

    @Test(priority = 7, description = "Verify logout returns to login page")
    @Story("Logout functionality")
    public void testLogOut() {
        accountsPage.clickLogOut();
        LoginPage loginPage = new LoginPage(getDriver());
        loginPage.waitForVisible(By.name("username"));
        Assert.assertTrue(loginPage.isLoginFormDisplayed(),
                "Should see login form after logout!");
    }
}
