package tests;

import base.BaseTest;
import io.qameta.allure.Epic;
import io.qameta.allure.Feature;
import io.qameta.allure.Story;
import org.openqa.selenium.By;
import org.testng.Assert;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;
import pages.AccountsOverviewPage;
import pages.LoginPage;
import utils.ConfigReader;
import utils.UserFactory;

@Epic("Banking Application")
@Feature("Accounts Overview")
public class AccountsOverviewTest extends BaseTest {

    private AccountsOverviewPage accountsPage;
    private static final String PASSWORD = "Test@1234";
    private static String sharedUsername;

    @BeforeClass(alwaysRun = true)
    public void registerSharedUser() {
        setUp();
        try {
            sharedUsername = UserFactory.registerUniqueUser(getDriver(), "acc_", PASSWORD);
        } finally {
            tearDown();
        }
    }

    @BeforeMethod
    public void navigateToAccountsOverview() {
        loginWithRetry();
        accountsPage = new AccountsOverviewPage(getDriver());
        accountsPage.clickAccountsOverview();
        accountsPage.waitForUrl("overview");
    }

    private void loginWithRetry() {
        utils.WaitHelper.loginWithRetry(getDriver(), sharedUsername, PASSWORD);
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
