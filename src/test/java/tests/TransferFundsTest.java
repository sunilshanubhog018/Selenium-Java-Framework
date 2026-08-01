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
import pages.TransferFundsPage;
import utils.ConfigReader;

@Epic("Banking Application")
@Feature("Transfer Funds")
public class TransferFundsTest extends BaseTest {

    private TransferFundsPage transferPage;
    private String firstAccountNumber;

    @BeforeMethod
    public void navigateToTransferFunds() {
        String username = "tfr_" + System.currentTimeMillis();
        String password = "Test@1234";

        getDriver().get(ConfigReader.get("base.url"));
        LoginPage loginPage = new LoginPage(getDriver());
        loginPage.clickRegister();

        RegisterPage registerPage = new RegisterPage(getDriver());
        registerPage.waitForUrl("register");
        registerPage.registerUser(
                "Transfer", "Tester", "100 Bank Lane",
                "Delhi", "DL", "110001",
                "9123456789", "111-22-3333",
                username, password
        );
        registerPage.waitForUrl("overview");

        AccountsOverviewPage accountsPage = new AccountsOverviewPage(getDriver());
        accountsPage.clickAccountsOverview();
        accountsPage.waitForUrl("overview");
        firstAccountNumber = accountsPage.getFirstAccountNumber();

        accountsPage.clickTransferFunds();
        transferPage = new TransferFundsPage(getDriver());
        transferPage.waitForUrl("transfer");
    }

    @Test(priority = 1, description = "Verify Transfer Funds page is displayed")
    @Story("Page visibility")
    public void testTransferPageDisplayed() {
        Assert.assertTrue(transferPage.isOnTransferFundsPage(),
                "Should be on Transfer Funds page!");
    }

    @Test(priority = 2, description = "Verify transfer form is displayed")
    @Story("Transfer form visibility")
    public void testTransferFormDisplayed() {
        Assert.assertTrue(transferPage.isTransferFormDisplayed(),
                "Transfer form should be visible!");
    }

    @Test(priority = 3, description = "Verify From Account dropdown has accounts")
    @Story("Account dropdown population")
    public void testFromAccountHasOptions() {
        int count = transferPage.getFromAccountCount();
        Assert.assertTrue(count >= 1,
                "From Account dropdown should have at least 1 option! Found: " + count);
    }

    @Test(priority = 4, description = "Transfer with empty amount shows error")
    @Story("Empty amount validation")
    public void testTransferEmptyAmount() {
        transferPage.clickTransfer();
        transferPage.waitForVisible(By.id("rightPanel"));
        String pageText = transferPage.getRightPanelText();
        Assert.assertTrue(
                pageText.contains("Error") || pageText.contains("error")
                || pageText.contains("amount"),
                "Should show error for empty amount! Got: " + pageText);
    }

    @Test(priority = 5, description = "Transfer with invalid amount shows error")
    @Story("Invalid amount validation")
    public void testTransferInvalidAmount() {
        transferPage.enterAmount("abc");
        transferPage.clickTransfer();
        transferPage.waitForVisible(By.id("rightPanel"));
        String pageText = transferPage.getRightPanelText();
        Assert.assertTrue(
                pageText.contains("Error") || pageText.contains("error")
                || pageText.contains("amount"),
                "Should show error for invalid amount! Got: " + pageText);
    }

    @Test(priority = 7, description = "Verify transfer success message")
    @Story("Successful transfer")
    public void testTransferSuccessMessage() {
        transferPage.enterAmount("100");
        transferPage.clickTransfer();
        transferPage.waitForVisible(By.cssSelector("#rightPanel h1.title"));
        String pageText = transferPage.getRightPanelText();
        Assert.assertTrue(
                pageText.contains("Transfer Complete") || pageText.contains("transferred")
                || pageText.contains("$100.00"),
                "Success message should mention transfer! Got: " + pageText);
    }

    @Test(priority = 8, description = "Transfer funds and verify balance")
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
        transferPage.enterAmount("100");
        transferPage.clickTransfer();
        transferPage.waitForVisible(By.cssSelector("#rightPanel h1.title"));

        String pageText = transferPage.getRightPanelText();
        Assert.assertTrue(
                pageText.contains("Transfer Complete") || pageText.contains("transferred"),
                "Transfer should complete! Got: " + pageText);

        accountsPage.clickAccountsOverview();
        accountsPage.waitForUrl("overview");

        String finalBalance = accountsPage.getTotalBalance();
        System.out.println("Final Balance: " + finalBalance);
        Assert.assertEquals(finalBalance, initialBalance,
                "Balance should remain same for same-account transfer!");
    }
}
