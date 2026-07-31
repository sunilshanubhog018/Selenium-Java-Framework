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

    @BeforeMethod
    public void navigateToBillPay() {
        String username = "bill_" + System.currentTimeMillis();
        String password = "Test@1234";

        getDriver().get(ConfigReader.get("base.url"));
        LoginPage loginPage = new LoginPage(getDriver());
        loginPage.clickRegister();

        RegisterPage registerPage = new RegisterPage(getDriver());
        registerPage.waitForUrl("register");
        registerPage.registerUser(
                "Bill", "Tester", "200 Payment Road",
                "Chennai", "TN", "600001",
                "9876501234", "222-33-4444",
                username, password
        );
        registerPage.waitForUrl("overview");

        AccountsOverviewPage accountsPage = new AccountsOverviewPage(getDriver());
        accountsPage.clickAccountsOverview();
        accountsPage.waitForUrl("overview");
        accountNumber = accountsPage.getFirstAccountNumber();

        accountsPage.clickBillPay();
        billPayPage = new BillPayPage(getDriver());
        billPayPage.waitForUrl("billpay");
    }

    @Test(priority = 1, description = "Verify Bill Pay page is displayed")
    public void testBillPayPageDisplayed() {
        Assert.assertTrue(billPayPage.isOnBillPayPage(),
                "Should be on Bill Payment page!");
    }

    @Test(priority = 2, description = "Verify bill pay form is displayed")
    public void testBillPayFormDisplayed() {
        Assert.assertTrue(billPayPage.isBillPayFormDisplayed(),
                "Bill pay form should be visible!");
    }

    @Test(priority = 3, description = "Submit empty bill pay form shows error")
    public void testEmptyFormSubmit() {
        billPayPage.clickSendPayment();
        billPayPage.waitForVisible(By.id("rightPanel"));
        String pageText = billPayPage.getRightPanelText();
        Assert.assertTrue(
                pageText.contains("error") || pageText.contains("Error")
                || pageText.contains("required") || pageText.contains("empty"),
                "Should show error for empty form! Got: " + pageText);
    }

    @Test(priority = 4, description = "Pay bill with valid data")
    public void testValidBillPayment() {
        billPayPage.payBill(
                "Electric Company", "100 Power Street",
                "Mumbai", "MH", "400001",
                "9876543210", "12345", "50"
        );
        billPayPage.waitForVisible(By.cssSelector("#rightPanel h1.title"));
        Assert.assertTrue(billPayPage.isPaymentSuccessful(),
                "Bill payment should complete successfully!");
    }

    @Test(priority = 5, description = "Verify payment success message details")
    public void testPaymentSuccessMessage() {
        billPayPage.payBill(
                "Water Board", "200 Water Lane",
                "Delhi", "DL", "110001",
                "9988776655", "67890", "75"
        );
        billPayPage.waitForVisible(By.cssSelector("#rightPanel h1.title"));
        String resultText = billPayPage.getResultText();
        Assert.assertTrue(
                resultText.contains("$75") || resultText.contains("Water Board")
                || resultText.contains("Bill Payment Complete"),
                "Success message should contain payment details! Got: " + resultText);
    }

    @Test(priority = 6, description = "Pay bill and verify balance still shown")
    public void testPayBillAndVerifyBalance() {
        AccountsOverviewPage accountsPage = new AccountsOverviewPage(getDriver());
        accountsPage.clickAccountsOverview();
        accountsPage.waitForUrl("overview");

        String initialBalance = accountsPage.getTotalBalance();
        System.out.println("Initial Balance: " + initialBalance);

        accountsPage.clickBillPay();
        billPayPage = new BillPayPage(getDriver());
        billPayPage.waitForUrl("billpay");
        billPayPage.payBill(
                "Internet Provider", "300 Net Street",
                "Bangalore", "KA", "560001",
                "9112233445", "11111", "100"
        );
        billPayPage.waitForVisible(By.cssSelector("#rightPanel h1.title"));
        Assert.assertTrue(billPayPage.isPaymentSuccessful(), "Bill payment should complete!");

        accountsPage.clickAccountsOverview();
        accountsPage.waitForUrl("overview");

        String finalBalance = accountsPage.getTotalBalance();
        System.out.println("Final Balance: " + finalBalance);
        Assert.assertTrue(finalBalance.contains("$"),
                "Balance should still be displayed after payment! Got: " + finalBalance);
    }

    @Test(priority = 7, description = "Pay bill with mismatched account numbers")
    public void testMismatchedAccountNumbers() {
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
        billPayPage.waitForVisible(By.id("rightPanel"));
        String pageText = billPayPage.getRightPanelText();
        Assert.assertTrue(
                pageText.contains("match") || pageText.contains("Error")
                || pageText.contains("error") || pageText.contains("do not match"),
                "Should show error for mismatched accounts! Got: " + pageText);
    }
}
