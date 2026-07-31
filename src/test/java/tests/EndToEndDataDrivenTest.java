package tests;

import base.BaseTest;
import org.openqa.selenium.By;
import org.testng.Assert;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;
import pages.AccountsOverviewPage;
import pages.ActivityPage;
import pages.BillPayPage;
import pages.LoginPage;
import pages.RegisterPage;
import pages.TransferFundsPage;
import utils.ConfigReader;
import utils.ExcelReader;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class EndToEndDataDrivenTest extends BaseTest {

    @BeforeMethod
    public void navigateToHome() {
        getDriver().get(ConfigReader.get("base.url"));
    }

    @DataProvider(name = "e2eData")
    public Object[][] getE2EData() {
        String filePath = "src/test/resources/testdata/E2ETestData.xlsx";
        List<Map<String, String>> allData = ExcelReader.readExcel(filePath, "Sheet1");

        List<Object[]> filtered = new ArrayList<>();
        for (Map<String, String> row : allData) {
            if ("Yes".equalsIgnoreCase(row.get("Execute"))) {
                filtered.add(new Object[]{
                    row.get("TestCaseID"),
                    row.get("Description"),
                    row.get("Username"),
                    row.get("Password"),
                    row.get("TransferAmount"),
                    row.get("BillAmount"),
                    row.get("ExpectedFlow")
                });
            }
        }
        return filtered.toArray(new Object[0][0]);
    }

    @Test(dataProvider = "e2eData", description = "Data-driven E2E banking flow from Excel")
    public void testE2EFromExcel(String testCaseID, String description,
                                  String username, String password,
                                  String transferAmount, String billAmount,
                                  String expectedFlow) {

        System.out.println("Running: " + testCaseID + " - " + description);

        // ---- RESOLVE USERNAME ----
        if ("CONFIG_USERNAME".equals(username)) {
            username = ConfigReader.get("test.username");
            password = ConfigReader.get("test.password");
        } else if ("REGISTER_NEW".equals(username)) {
            username = "e2e_" + System.currentTimeMillis();
            LoginPage loginPage = new LoginPage(getDriver());
            loginPage.clickRegister();
            RegisterPage registerPage = new RegisterPage(getDriver());
            registerPage.waitForUrl("register");
            registerPage.registerUser(
                    "E2E", "User", "100 Test Street",
                    "Bangalore", "KA", "560001",
                    "9876543210", "123-45-6789",
                    username, password
            );
            registerPage.waitForVisible(By.cssSelector("#rightPanel h1.title"));
        }

        // ---- LOGIN ----
        LoginPage loginPage = new LoginPage(getDriver());
        loginPage.login(username, password);
        loginPage.waitForUrl("overview");
        Assert.assertTrue(getDriver().getCurrentUrl().contains("overview"),
                testCaseID + ": Login should succeed!");

        // ---- TRANSFER ----
        if (transferAmount != null && !transferAmount.isEmpty()) {
            new AccountsOverviewPage(getDriver()).clickTransferFunds();
            TransferFundsPage transferPage = new TransferFundsPage(getDriver());
            transferPage.waitForUrl("transfer");
            transferPage.enterAmount(transferAmount);
            transferPage.clickTransfer();
            transferPage.waitForVisible(By.cssSelector("#rightPanel h1.title"));
            String result = transferPage.getRightPanelText();
            Assert.assertTrue(
                    result.contains("Transfer Complete") || result.contains("transferred"),
                    testCaseID + ": Transfer should complete! Got: " + result);
            System.out.println("  Transfer $" + transferAmount + ": SUCCESS");
        }

        // ---- BILL PAY ----
        if (billAmount != null && !billAmount.isEmpty()) {
            new AccountsOverviewPage(getDriver()).clickBillPay();
            BillPayPage billPayPage = new BillPayPage(getDriver());
            billPayPage.waitForUrl("billpay");
            billPayPage.payBill(
                    "Test Utility", "100 Bill Street",
                    "Bangalore", "KA", "560001",
                    "9876543210", "123456", billAmount
            );
            billPayPage.waitForVisible(By.cssSelector("#rightPanel h1.title"));
            String result = billPayPage.getRightPanelText();
            Assert.assertTrue(
                    result.contains("Bill Payment Complete") || result.contains("payment") || result.contains("successfully"),
                    testCaseID + ": Bill payment should complete! Got: " + result);
            System.out.println("  Bill Pay $" + billAmount + ": SUCCESS");
        }

        // ---- VERIFY ACTIVITY ----
        if ("verify_activity".equals(expectedFlow)) {
            new AccountsOverviewPage(getDriver()).clickAccountsOverview();
            AccountsOverviewPage accountsPage = new AccountsOverviewPage(getDriver());
            accountsPage.waitForUrl("overview");
            accountsPage.clickFirstAccount();
            ActivityPage activityPage = new ActivityPage(getDriver());
            activityPage.waitForUrl("activity");
            Assert.assertTrue(activityPage.isTransactionTableDisplayed(),
                    testCaseID + ": Transaction table should be visible!");
            int txnCount = activityPage.getTransactionCount();
            Assert.assertTrue(txnCount >= 1,
                    testCaseID + ": At least 1 transaction should exist!");
            System.out.println("  Transactions verified: " + txnCount);
        }

        System.out.println("  ✅ " + testCaseID + " PASSED!");
    }
}
