package tests;

import base.BaseTest;
import org.openqa.selenium.By;
import org.testng.Assert;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;
import pages.AccountsOverviewPage;
import pages.LoginPage;
import pages.RegisterPage;
import pages.TransferFundsPage;
import utils.ConfigReader;

public class TransferFundsTest extends BaseTest {

    private TransferFundsPage transferPage;
    private String firstAccountNumber;

    private void pause(int seconds) {
        try { Thread.sleep(seconds * 1000L); } catch (InterruptedException e) {}
    }

    @BeforeMethod
    public void navigateToTransferFunds() {
        String username = "tfr_" + System.currentTimeMillis();
        String password = "Test@1234";

        getDriver().get(ConfigReader.get("base.url"));
        LoginPage loginPage = new LoginPage(getDriver());
        loginPage.clickRegister();
        pause(2);

        RegisterPage registerPage = new RegisterPage(getDriver());
        registerPage.registerUser(
                "Transfer", "Tester", "100 Bank Lane",
                "Delhi", "DL", "110001",
                "9123456789", "111-22-3333",
                username, password
        );
        pause(3);

        AccountsOverviewPage accountsPage = new AccountsOverviewPage(getDriver());
        accountsPage.clickAccountsOverview();
        pause(3);

        firstAccountNumber = accountsPage.getFirstAccountNumber();

        accountsPage.clickTransferFunds();
        pause(3);

        transferPage = new TransferFundsPage(getDriver());
    }

    @Test(priority = 1, description = "Verify Transfer Funds page is displayed")
    public void testTransferPageDisplayed() {
        pause(5);
        Assert.assertTrue(transferPage.isOnTransferFundsPage(),
                "Should be on Transfer Funds page!");
    }

    @Test(priority = 2, description = "Verify transfer form is displayed")
    public void testTransferFormDisplayed() {
        pause(5);
        Assert.assertTrue(transferPage.isTransferFormDisplayed(),
                "Transfer form should be visible!");
    }

    @Test(priority = 3, description = "Verify From Account dropdown has accounts")
    public void testFromAccountHasOptions() {
        pause(5);
        int count = transferPage.getFromAccountCount();
        Assert.assertTrue(count >= 1,
                "From Account dropdown should have at least 1 option! Found: " + count);
    }

    @Test(priority = 4, description = "Transfer with empty amount shows error")
    public void testTransferEmptyAmount() {
        pause(5);
        transferPage.clickTransfer();
        pause(3);

        String pageText = getDriver().findElement(By.id("rightPanel")).getText();
        Assert.assertTrue(
                pageText.contains("Error") || pageText.contains("error")
                || pageText.contains("amount"),
                "Should show error for empty amount! Got: " + pageText);
    }

    @Test(priority = 5, description = "Transfer with invalid amount shows error")
    public void testTransferInvalidAmount() {
        pause(5);
        transferPage.enterAmount("abc");
        transferPage.clickTransfer();
        pause(3);

        String pageText = getDriver().findElement(By.id("rightPanel")).getText();
        Assert.assertTrue(
                pageText.contains("Error") || pageText.contains("error")
                || pageText.contains("amount"),
                "Should show error for invalid amount! Got: " + pageText);
    }

    @Test(priority = 7, description = "Verify transfer success message")
    public void testTransferSuccessMessage() {
        pause(5);
        transferPage.enterAmount("100");
        transferPage.clickTransfer();
        pause(5);

        String pageText = getDriver().findElement(By.id("rightPanel")).getText();
        Assert.assertTrue(
                pageText.contains("Transfer Complete") || pageText.contains("transferred")
                || pageText.contains("$100.00"),
                "Success message should mention transfer! Got: " + pageText);
    }

    @Test(priority = 8, description = "Transfer funds and verify balance")
    public void testTransferAndVerifyBalance() {
        pause(5);

        AccountsOverviewPage accountsPage = new AccountsOverviewPage(getDriver());
        accountsPage.clickAccountsOverview();
        pause(3);

        String initialBalance = accountsPage.getTotalBalance();
        String accountNumber = accountsPage.getFirstAccountNumber();
        System.out.println("Initial Balance: " + initialBalance);
        System.out.println("Account Number: " + accountNumber);

        accountsPage.clickTransferFunds();
        pause(3);

        transferPage = new TransferFundsPage(getDriver());
        transferPage.enterAmount("100");
        transferPage.clickTransfer();
        pause(5);

        String pageText = getDriver().findElement(By.id("rightPanel")).getText();
        Assert.assertTrue(
                pageText.contains("Transfer Complete") || pageText.contains("transferred"),
                "Transfer should complete! Got: " + pageText);

        accountsPage.clickAccountsOverview();
        pause(3);

        String finalBalance = accountsPage.getTotalBalance();
        System.out.println("Final Balance: " + finalBalance);

        Assert.assertEquals(finalBalance, initialBalance,
                "Balance should remain same for same-account transfer!");
    }
}