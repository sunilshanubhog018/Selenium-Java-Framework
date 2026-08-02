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
import pages.BillPayPage;
import pages.LoginPage;
import pages.RegisterPage;
import utils.ConfigReader;

@Epic("Banking Application")
@Feature("Bill Pay")
public class BillPayTest extends BaseTest {

    private static final String PASSWORD = "Test@1234";
    private static String sharedUsername;
    private BillPayPage billPayPage;
    private String accountNumber;

    @org.testng.annotations.BeforeClass
    public void registerSharedUser() throws Exception {
        setUp();
        sharedUsername = "bill_" + System.currentTimeMillis();
        getDriver().get(ConfigReader.get("base.url") + "register.htm");
        RegisterPage registerPage = new RegisterPage(getDriver());
        registerPage.registerUser(
                "Bill", "Tester", "200 Payment Road",
                "Chennai", "TN", "600001",
                "9876501234", "222-33-4444",
                sharedUsername, PASSWORD
        );
        registerPage.waitForUrl("overview");
        new AccountsOverviewPage(getDriver()).logout();
        tearDown();
    }

    @BeforeMethod
    public void navigateToBillPay() {
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

        AccountsOverviewPage accountsPage = new AccountsOverviewPage(getDriver());
        accountsPage.clickAccountsOverview();
        accountsPage.waitForUrl("overview");
        accountNumber = accountsPage.getFirstAccountNumber();

        accountsPage.clickBillPay();
        billPayPage = new BillPayPage(getDriver());
        billPayPage.waitForUrl("billpay");
    }

    @Test(priority = 1, groups = {"regression", "billpay"}, description = "Verify Bill Pay page is displayed")
    @Story("Page visibility")
    public void testBillPayPageDisplayed() {
        Assert.assertTrue(billPayPage.isOnBillPayPage(),
                "Should be on Bill Payment page!");
    }

    @Test(priority = 2, groups = {"regression", "billpay"}, description = "Verify bill pay form is displayed")
    @Story("Bill pay form visibility")
    public void testBillPayFormDisplayed() {
        Assert.assertTrue(billPayPage.isBillPayFormDisplayed(),
                "Bill pay form should be visible!");
    }

    @Test(priority = 3, groups = {"regression", "billpay"}, description = "Submit empty bill pay form shows error")
    @Story("Empty form validation")
    public void testEmptyFormSubmit() {
        billPayPage.clickSendPayment();
        billPayPage.waitForVisible(By.id("rightPanel"));
        String pageText = billPayPage.getRightPanelText();
        Assert.assertTrue(
                pageText.contains("error") || pageText.contains("Error")
                || pageText.contains("required") || pageText.contains("empty"),
                "Should show error for empty form! Got: " + pageText);
    }

    @Test(priority = 4, groups = {"regression", "billpay"}, description = "Pay bill with valid data")
    @Story("Valid bill payment")
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

    @Test(priority = 5, groups = {"regression", "billpay"}, description = "Verify payment success message details")
    @Story("Payment success message")
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

    @Test(priority = 6, groups = {"regression", "billpay"}, description = "Pay bill and verify balance still shown")
    @Story("Bill payment and balance verification")
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

    @Test(priority = 7, groups = {"regression", "billpay"}, description = "Pay bill with mismatched account numbers")
    @Story("Mismatched account validation")
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
