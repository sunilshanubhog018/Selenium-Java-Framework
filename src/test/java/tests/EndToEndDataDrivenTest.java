package tests;

import base.BaseTest;
import io.qameta.allure.Epic;
import io.qameta.allure.Feature;
import io.qameta.allure.Story;
import org.openqa.selenium.By;
import org.testng.Assert;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;
import pages.AccountsOverviewPage;
import pages.ActivityPage;
import pages.BillPayPage;
import pages.LoginPage;
import pages.TransferFundsPage;
import utils.ConfigReader;
import utils.ExcelReader;
import utils.UserFactory;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Epic("Banking Application")
@Feature("End to End")
public class EndToEndDataDrivenTest extends BaseTest {

    private static final String PASSWORD = "Test@1234";
    private static String sharedUsername;

    @BeforeClass(alwaysRun = true)
    public void registerSharedUser() {
        setUp();
        try {
            sharedUsername = UserFactory.registerUniqueUser(getDriver(), "e2edd_", PASSWORD);
        } finally {
            tearDown();
        }
    }

    private void login() {
        utils.WaitHelper.loginWithRetry(getDriver(), sharedUsername, PASSWORD);
    }

    @BeforeMethod
    public void navigateToHome() {
        getDriver().get(ConfigReader.get("base.url"));
    }

    @DataProvider(name = "e2eData")
    public Object[][] getE2EData() {
        String filePath = "src/test/resources/testdata/E2ETestData.xlsx";
        List<Map<String, String>> allData = ExcelReader.readExcel(filePath, "E2ETestData");

        List<Object[]> filtered = new ArrayList<>();
        for (Map<String, String> row : allData) {
            if ("Yes".equalsIgnoreCase(row.get("Execute"))) {
                filtered.add(new Object[]{
                        row.get("TCId"),
                        row.get("ScenarioName"),
                        row.get("Description"),
                        row.get("TransferAmount"),
                        row.get("BillPayeeName"),
                        row.get("BillPayeeAddress"),
                        row.get("BillPayeeCity"),
                        row.get("BillPayeeState"),
                        row.get("BillPayeeZip"),
                        row.get("BillPayeePhone"),
                        row.get("BillAccountNumber"),
                        row.get("BillAmount"),
                        row.get("ExpectedMinTransactions")
                });
            }
        }
        return filtered.toArray(new Object[0][0]);
    }

    @Test(dataProvider = "e2eData", groups = {"e2e", "datadriven"}, description = "Data-driven E2E banking flow from Excel")
    @Story("Data-driven E2E flow")
    public void testE2EFromExcel(String tcId, String scenarioName, String description,
                                 String transferAmount, String billPayeeName,
                                 String billPayeeAddress, String billPayeeCity,
                                 String billPayeeState, String billPayeeZip,
                                 String billPayeePhone, String billAccountNumber,
                                 String billAmount, String expectedMinTxns) {

        System.out.println("\nRunning: " + tcId + " - " + scenarioName);
        System.out.println("  Description: " + description);

        login();

        if (transferAmount != null && !transferAmount.isEmpty()) {
            new AccountsOverviewPage(getDriver()).clickTransferFunds();
            TransferFundsPage transferPage = new TransferFundsPage(getDriver());
            transferPage.waitForUrl("transfer");
            transferPage.ensureAccountsSelected();
            transferPage.enterAmount(transferAmount);
            transferPage.clickTransfer();
            String result = transferPage.getRightPanelText();
            Assert.assertTrue(
                    result.contains("Transfer Complete") || result.contains("transferred")
                            || transferPage.isTransferComplete(),
                    tcId + ": Transfer should complete! Got: " + result);
            System.out.println("  Transfer $" + transferAmount + ": SUCCESS");
        }

        if (billAmount != null && !billAmount.isEmpty()) {
            new AccountsOverviewPage(getDriver()).clickBillPay();
            BillPayPage billPayPage = new BillPayPage(getDriver());
            billPayPage.waitForUrl("billpay");
            billPayPage.payBill(
                    billPayeeName, billPayeeAddress, billPayeeCity,
                    billPayeeState, billPayeeZip, billPayeePhone,
                    billAccountNumber, billAmount
            );
            String result = billPayPage.getRightPanelText();
            Assert.assertTrue(
                    billPayPage.isPaymentSuccessful()
                            || result.contains("Bill Payment Complete")
                            || result.contains("successfully"),
                    tcId + ": Bill payment should complete! Got: " + result);
            System.out.println("  Bill Pay $" + billAmount + ": SUCCESS");
        }

        int minTxns = 0;
        try {
            minTxns = Integer.parseInt(expectedMinTxns);
        } catch (Exception ignored) {
        }

        if (minTxns > 0) {
            new AccountsOverviewPage(getDriver()).clickAccountsOverview();
            AccountsOverviewPage accountsPage = new AccountsOverviewPage(getDriver());
            accountsPage.waitForUrl("overview");
            accountsPage.clickFirstAccount();
            ActivityPage activityPage = new ActivityPage(getDriver());
            activityPage.waitForUrl("activity");
            Assert.assertTrue(activityPage.isTransactionTableDisplayed(),
                    tcId + ": Transaction table should be visible!");
            int txnCount = activityPage.getTransactionCount();
            Assert.assertTrue(txnCount >= minTxns,
                    tcId + ": Expected at least " + minTxns + " transaction(s), found: " + txnCount);
            System.out.println("  Transactions verified: " + txnCount);
        }

        System.out.println("  ✅ " + tcId + " PASSED!");
    }
}
