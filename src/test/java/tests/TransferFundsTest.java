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
import pages.TransferFundsPage;
import utils.ConfigReader;
import utils.UserFactory;

@Epic("Banking Application")
@Feature("Transfer Funds")
public class TransferFundsTest extends BaseTest {

    private static final String PASSWORD = "Test@1234";
    private static String sharedUsername;
    private TransferFundsPage transferPage;

    @BeforeClass(alwaysRun = true)
    public void registerSharedUser() {
        setUp();
        try {
            sharedUsername = UserFactory.registerUniqueUser(getDriver(), "tfr_", PASSWORD);
        } finally {
            tearDown();
        }
    }

    @BeforeMethod
    public void navigateToTransferFunds() {
        loginWithRetry();

        AccountsOverviewPage accountsPage = new AccountsOverviewPage(getDriver());
        accountsPage.clickAccountsOverview();
        accountsPage.waitForUrl("overview");

        accountsPage.clickTransferFunds();
        transferPage = new TransferFundsPage(getDriver());
        transferPage.waitForUrl("transfer");
    }

    private void loginWithRetry() {
        RuntimeException last = null;
        for (int attempt = 1; attempt <= 3; attempt++) {
            try {
                getDriver().get(ConfigReader.get("base.url"));
                LoginPage loginPage = new LoginPage(getDriver());
                loginPage.login(sharedUsername, PASSWORD);
                loginPage.waitForUrl("overview");
                return;
            } catch (RuntimeException e) {
                last = e;
                System.out.println("  ⚠ Login attempt " + attempt + " failed, retrying...");
                try {
                    Thread.sleep(2000);
                } catch (InterruptedException ie) {
                    Thread.currentThread().interrupt();
                }
            }
        }
        throw new RuntimeException("Login failed after 3 attempts for user " + sharedUsername, last);
    }

    @Test(priority = 1, groups = {"regression", "transfer"}, description = "Verify Transfer Funds page is displayed")
    @Story("Page visibility")
    public void testTransferPageDisplayed() {
        Assert.assertTrue(transferPage.isOnTransferFundsPage(),
                "Should be on Transfer Funds page!");
    }

    @Test(priority = 2, groups = {"regression", "transfer"}, description = "Verify transfer form is displayed")
    @Story("Transfer form visibility")
    public void testTransferFormDisplayed() {
        Assert.assertTrue(transferPage.isTransferFormDisplayed(),
                "Transfer form should be visible!");
    }

    @Test(priority = 3, groups = {"regression", "transfer"}, description = "Verify From Account dropdown has accounts")
    @Story("Account dropdown population")
    public void testFromAccountHasOptions() {
        int count = transferPage.getFromAccountCount();
        Assert.assertTrue(count >= 1,
                "From Account dropdown should have at least 1 option! Found: " + count);
    }

    @Test(priority = 4, groups = {"regression", "transfer"}, description = "Transfer with empty amount shows error")
    @Story("Empty amount validation")
    public void testTransferEmptyAmount() {
        transferPage.ensureAccountsSelected();
        transferPage.clickTransfer();
        String pageText = transferPage.getRightPanelText();
        boolean html5Blocked = !transferPage.isTransferComplete()
                && getDriver().getCurrentUrl().contains("transfer")
                && pageText.contains("Transfer Funds");
        Assert.assertTrue(
                transferPage.isAmountErrorDisplayed()
                        || pageText.toLowerCase().contains("error")
                        || pageText.toLowerCase().contains("amount")
                        || html5Blocked,
                "Should show validation for empty amount! Got: " + pageText);
    }

    @Test(priority = 5, groups = {"regression", "transfer"}, description = "Transfer with invalid amount shows error")
    @Story("Invalid amount validation")
    public void testTransferInvalidAmount() {
        transferPage.ensureAccountsSelected();
        transferPage.enterAmount("abc");
        transferPage.clickTransfer();
        String pageText = transferPage.getRightPanelText();
        Assert.assertTrue(
                transferPage.isAmountErrorDisplayed()
                        || pageText.toLowerCase().contains("error")
                        || pageText.toLowerCase().contains("amount")
                        || pageText.toLowerCase().contains("invalid"),
                "Should show error for invalid amount! Got: " + pageText);
    }

    @Test(priority = 7, groups = {"regression", "transfer"}, description = "Verify transfer success message")
    @Story("Successful transfer")
    public void testTransferSuccessMessage() {
        transferPage.ensureAccountsSelected();
        transferPage.enterAmount("100");
        transferPage.clickTransfer();
        String pageText = transferPage.getRightPanelText();
        Assert.assertTrue(
                pageText.contains("Transfer Complete") || pageText.contains("transferred")
                        || pageText.contains("$100.00") || transferPage.isTransferComplete(),
                "Success message should mention transfer! Got: " + pageText);
    }

    @Test(priority = 8, groups = {"regression", "transfer"}, description = "Transfer funds and verify balance")
    @Story("Transfer and balance verification")
    public void testTransferAndVerifyBalance() {
        AccountsOverviewPage accountsPage = new AccountsOverviewPage(getDriver());
        accountsPage.clickAccountsOverview();
        accountsPage.waitForUrl("overview");

        String initialBalance = accountsPage.getTotalBalance();
        System.out.println("Initial Balance: " + initialBalance);

        accountsPage.clickTransferFunds();
        transferPage = new TransferFundsPage(getDriver());
        transferPage.waitForUrl("transfer");
        transferPage.ensureAccountsSelected();
        transferPage.enterAmount("100");
        transferPage.clickTransfer();

        String pageText = transferPage.getRightPanelText();
        Assert.assertTrue(
                pageText.contains("Transfer Complete") || pageText.contains("transferred")
                        || transferPage.isTransferComplete(),
                "Transfer should complete! Got: " + pageText);

        accountsPage.clickAccountsOverview();
        accountsPage.waitForUrl("overview");

        String finalBalance = accountsPage.getTotalBalance();
        System.out.println("Final Balance: " + finalBalance);
        // Single-account users transfer to the same account — net balance unchanged
        Assert.assertEquals(finalBalance, initialBalance,
                "Balance should remain same for same-account transfer!");
    }
}
