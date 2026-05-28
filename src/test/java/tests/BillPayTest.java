package tests;

import base.BaseTest;
import org.openqa.selenium.By;
import org.testng.Assert;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;
import pages.AccountsOverviewPage;
import pages.BillPayPage;
import pages.LoginPage;
import pages.RegisterPage;
import utils.ConfigReader;

public class BillPayTest extends BaseTest {

    private BillPayPage billPayPage;
    private String accountNumber;

    private void pause(int seconds) {
        try { Thread.sleep(seconds * 1000L); } catch (InterruptedException e) {}
    }

    @BeforeMethod
    public void navigateToBillPay() {
        String username = "bill_" + System.currentTimeMillis();
        String password = "Test@1234";

        getDriver().get(ConfigReader.get("base.url"));
        LoginPage loginPage = new LoginPage(getDriver());
        loginPage.clickRegister();
        pause(2);

        RegisterPage registerPage = new RegisterPage(getDriver());
        registerPage.registerUser(
                "Bill", "Tester", "200 Payment Road",
                "Chennai", "TN", "600001",
                "9876501234", "222-33-4444",
                username, password
        );
        pause(3);

        AccountsOverviewPage accountsPage = new AccountsOverviewPage(getDriver());
        accountsPage.clickAccountsOverview();
        pause(3);
        accountNumber = accountsPage.getFirstAccountNumber();

        accountsPage.clickBillPay();
        pause(3);

        billPayPage = new BillPayPage(getDriver());
    }

    @Test(priority = 1, description = "Verify Bill Pay page is displayed")
    public void testBillPayPageDisplayed() {
        pause(5);
        Assert.assertTrue(billPayPage.isOnBillPayPage(),
                "Should be on Bill Payment page!");
    }

    @Test(priority = 2, description = "Verify bill pay form is displayed")
    public void testBillPayFormDisplayed() {
        pause(5);
        Assert.assertTrue(billPayPage.isBillPayFormDisplayed(),
                "Bill pay form should be visible!");
    }

    @Test(priority = 3, description = "Submit empty bill pay form shows error")
    public void testEmptyFormSubmit() {
        pause(5);
        billPayPage.clickSendPayment();
        pause(3);

        String pageText = getDriver().findElement(By.id("rightPanel")).getText();
        Assert.assertTrue(
                pageText.contains("error") || pageText.contains("Error")
                || pageText.contains("required") || pageText.contains("empty"),
                "Should show error for empty form! Got: " + pageText);
    }

    @Test(priority = 4, description = "Pay bill with valid data")
    public void testValidBillPayment() {
        pause(5);
        billPayPage.payBill(
                "Electric Company", "100 Power Street",
                "Mumbai", "MH", "400001",
                "9876543210", "12345", "50"
        );
        pause(5);

        Assert.assertTrue(billPayPage.isPaymentSuccessful(),
                "Bill payment should complete successfully!");
    }

    @Test(priority = 5, description = "Verify payment success message details")
    public void testPaymentSuccessMessage() {
        pause(5);
        billPayPage.payBill(
                "Water Board", "200 Water Lane",
                "Delhi", "DL", "110001",
                "9988776655", "67890", "75"
        );
        pause(5);

        String resultText = billPayPage.getResultText();
        Assert.assertTrue(
                resultText.contains("$75") || resultText.contains("Water Board")
                || resultText.contains("Bill Payment Complete"),
                "Success message should contain payment details! Got: " + resultText);
    }

    @Test(priority = 6, description = "Pay bill and verify balance still shown")
    public void testPayBillAndVerifyBalance() {
        pause(5);

        AccountsOverviewPage accountsPage = new AccountsOverviewPage(getDriver());
        accountsPage.clickAccountsOverview();
        pause(3);

        String initialBalance = accountsPage.getTotalBalance();
        System.out.println("Initial Balance: " + initialBalance);

        accountsPage.clickBillPay();
        pause(3);

        billPayPage = new BillPayPage(getDriver());
        billPayPage.payBill(
                "Internet Provider", "300 Net Street",
                "Bangalore", "KA", "560001",
                "9112233445", "11111", "100"
        );
        pause(5);

        Assert.assertTrue(billPayPage.isPaymentSuccessful(),
                "Bill payment should complete!");

        accountsPage.clickAccountsOverview();
        pause(3);

        String finalBalance = accountsPage.getTotalBalance();
        System.out.println("Final Balance: " + finalBalance);

        Assert.assertTrue(finalBalance.contains("$"),
                "Balance should still be displayed after payment! Got: " + finalBalance);
    }

    @Test(priority = 7, description = "Pay bill with mismatched account numbers")
    public void testMismatchedAccountNumbers() {
        pause(5);

        billPayPage.enterPayeeName("Gas Company");
        billPayPage.enterAddress("400 Gas Road");
        billPayPage.enterCity("Pune");
        billPayPage.enterState("MH");
        billPayPage.enterZipCode("411001");
        billPayPage.enterPhone("9000000000");
        billPayPage.enterAccountNumber("12345");
        billPayPage.enterVerifyAccount("99999");
        billPayPage.enterAmount("25");
        billPayPage.clickSendPayment();
        pause(3);

        String pageText = getDriver().findElement(By.id("rightPanel")).getText();
        Assert.assertTrue(
                pageText.contains("match") || pageText.contains("Error")
                || pageText.contains("error") || pageText.contains("do not match"),
                "Should show error for mismatched accounts! Got: " + pageText);
    }
}