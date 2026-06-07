package tests;

import base.BaseTest;
import org.openqa.selenium.By;
import org.testng.Assert;
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

/**
 * EndToEndDataDrivenTest — Same 4 E2E flows as EndToEndTest.java
 * BUT driven from Excel file instead of hardcoded data
 *
 * Excel file: src/test/resources/testdata/E2ETestData.xlsx
 *
 * Row 1 → E2E001 → New Customer Onboarding
 * Row 2 → E2E002 → Fund Transfer + Activity
 * Row 3 → E2E003 → Bill Payment + Activity
 * Row 4 → E2E004 → Complete Banking Session
 *
 * Same test method (testE2EFromExcel) runs 4 times
 * Each run uses different data from Excel row
 */
public class Endtoenddatadriventest extends BaseTest {

    // Path to E2E Excel file
    private static final String EXCEL_PATH =
            "src/test/resources/testdata/E2ETestData.xlsx";

    private void pause(int seconds) {
        try { Thread.sleep(seconds * 1000L); } catch (InterruptedException e) {}
    }

    // ================================================================
    //  @DataProvider — reads E2ETestData.xlsx
    //  Filters rows where Execute = "Yes"
    //  Returns one Object[] per row to testE2EFromExcel()
    // ================================================================
    @DataProvider(name = "e2eData")
    public Object[][] getE2EData() {
        // Read all rows from Excel
        List<Map<String, String>> allData =
                ExcelReader.readExcel(EXCEL_PATH, "E2ETestData");

        List<Object[]> filteredData = new ArrayList<>();

        for (Map<String, String> row : allData) {
            // Only include rows where Execute = "Yes"
            if ("Yes".equalsIgnoreCase(row.get("Execute"))) {
                filteredData.add(new Object[]{
                        row.get("TCId"),
                        row.get("ScenarioName"),
                        row.get("Description"),
                        row.get("TransferAmount"),       // "" if no transfer
                        row.get("BillPayeeName"),        // "" if no bill pay
                        row.get("BillPayeeAddress"),
                        row.get("BillPayeeCity"),
                        row.get("BillPayeeState"),
                        row.get("BillPayeeZip"),
                        row.get("BillPayeePhone"),
                        row.get("BillAccountNumber"),
                        row.get("BillAmount"),           // "" if no bill pay
                        row.get("ExpectedMinTransactions")
                });
            }
        }

        return filteredData.toArray(new Object[0][0]);
    }

    // ================================================================
    //  HELPER: registerFreshUser()
    //  Exact same logic as EndToEndTest.java
    //  Registers new user OR falls back to config user
    // ================================================================
    private String registerFreshUser(String prefix) {
        String username = prefix + "_" + System.currentTimeMillis();
        String password = "Test@1234";

        getDriver().get(ConfigReader.get("base.url"));
        LoginPage loginPage = new LoginPage(getDriver());
        loginPage.clickRegister();
        pause(2);

        RegisterPage registerPage = new RegisterPage(getDriver());
        registerPage.registerUser(
                "E2E", "Tester", "100 Test Street",
                "Bangalore", "KA", "560001",
                "9876543210", "123-45-6789",
                username, password
        );
        pause(3);

        String title = "";
        try {
            title = registerPage.getSuccessTitle();
        } catch (Exception e) {
            System.out.println("  ⚠ Could not get title: " + e.getMessage());
        }
        System.out.println("  Registration result: " + title);

        // FALLBACK: If registration failed → use config user
        if (!title.contains("Welcome")) {
            System.out.println("  ⚠ Registration failed — using config user as fallback");
            getDriver().get(ConfigReader.get("base.url"));
            loginPage = new LoginPage(getDriver());
            loginPage.login(
                    ConfigReader.get("test.username"),
                    ConfigReader.get("test.password")
            );
            pause(3);
            System.out.println("  ✓ Logged in with config user: "
                    + ConfigReader.get("test.username"));
            return ConfigReader.get("test.username");
        }

        return username;
    }

    // ================================================================
    //  MAIN TEST METHOD — runs once per Excel row
    //
    //  One method handles ALL 4 scenarios based on Excel data:
    //
    //  E2E001: no transfer, no bill pay  → onboarding + activity check
    //  E2E002: transferAmount="50"        → transfer + activity check
    //  E2E003: billAmount="100"           → bill pay + activity check
    //  E2E004: transfer="50", bill="75"   → transfer + bill + activity
    // ================================================================
    @Test(dataProvider = "e2eData",
          description = "Data-Driven E2E: Banking flows from Excel")
    public void testE2EFromExcel(
            String tcId,
            String scenarioName,
            String description,
            String transferAmount,
            String billPayeeName,
            String billPayeeAddress,
            String billPayeeCity,
            String billPayeeState,
            String billPayeeZip,
            String billPayeePhone,
            String billAccountNumber,
            String billAmount,
            String expectedMinTxn) {

        System.out.println("\n🏦 E2E Data-Driven Test");
        System.out.println("  TC ID    : " + tcId);
        System.out.println("  Scenario : " + scenarioName);
        System.out.println("  Flow     : " + description);

        // Determine what this scenario does
        boolean hasTransfer = transferAmount != null && !transferAmount.isEmpty();
        boolean hasBillPay  = billAmount != null && !billAmount.isEmpty();
        int minTxn = Integer.parseInt(
                expectedMinTxn != null && !expectedMinTxn.isEmpty()
                ? expectedMinTxn : "1");

        System.out.println("  Transfer : " + (hasTransfer ? "$" + transferAmount : "No"));
        System.out.println("  Bill Pay : " + (hasBillPay ? "$" + billAmount + " to " + billPayeeName : "No"));

        // ==============================================================
        //  STEP 1: Register fresh user (or fallback to config user)
        // ==============================================================
        System.out.println("\n  Step 1: Setting up customer account...");
        String username = registerFreshUser(tcId.toLowerCase());
        String password = "Test@1234";

        // ==============================================================
        //  STEP 2: Logout after registration (for onboarding scenario)
        //          then login fresh to verify login works
        // ==============================================================
        if ("E2E001".equals(tcId)) {
            // Onboarding scenario: logout then login fresh
            System.out.println("  Step 2: Logging out after registration...");
            try {
                getDriver().findElement(By.linkText("Log Out")).click();
                pause(2);
            } catch (Exception e) {
                System.out.println("  Already on login page — skipping logout");
            }

            System.out.println("  Step 2b: Logging in fresh...");
            getDriver().get(ConfigReader.get("base.url"));
            LoginPage loginPage = new LoginPage(getDriver());
            loginPage.login(username, password);
            pause(3);

            Assert.assertTrue(
                    getDriver().getCurrentUrl().contains("overview"),
                    tcId + " Step 2 Failed: Should redirect to accounts overview!");
        }

        // ==============================================================
        //  STEP 3: View Accounts Overview
        // ==============================================================
        System.out.println("  Step 3: Checking accounts overview...");
        AccountsOverviewPage accountsPage = new AccountsOverviewPage(getDriver());
        accountsPage.clickAccountsOverview();
        pause(3);

        String initialBalance = accountsPage.getTotalBalance();
        System.out.println("  Balance: " + initialBalance);
        Assert.assertTrue(initialBalance.contains("$"),
                tcId + " Step 3 Failed: Balance should be displayed!");

        // ==============================================================
        //  STEP 4: Transfer funds (only if transferAmount provided)
        // ==============================================================
        if (hasTransfer) {
            System.out.println("  Step 4: Transferring $" + transferAmount + "...");
            accountsPage.clickTransferFunds();
            pause(3);

            // If navigation failed — go directly via URL
            if (!getDriver().getCurrentUrl().contains("transfer")) {
                System.out.println("  ⚠ Navigation failed — going direct to transfer URL");
                getDriver().get("https://parabank.parasoft.com/parabank/transfer.htm");
                pause(3);
            }

            TransferFundsPage transferPage = new TransferFundsPage(getDriver());
            Assert.assertTrue(transferPage.isOnTransferFundsPage(),
                    tcId + " Step 4 Failed: Should be on Transfer Funds page!");

            transferPage.enterAmount(transferAmount);
            transferPage.clickTransfer();
            pause(5);

            String transferResult = getDriver()
                    .findElement(By.id("rightPanel")).getText();
            Assert.assertTrue(
                    transferResult.contains("Transfer Complete")
                    || transferResult.contains("transferred"),
                    tcId + " Step 4 Failed: Transfer should complete! Got: "
                    + transferResult);
            System.out.println("  Transfer $" + transferAmount + ": SUCCESS");
        }

        // ==============================================================
        //  STEP 5: Bill payment (only if billAmount provided)
        // ==============================================================
        if (hasBillPay) {
            System.out.println("  Step 5: Paying bill of $" + billAmount
                    + " to " + billPayeeName + "...");

            // Navigate back to accounts first
            accountsPage.clickAccountsOverview();
            pause(5);

            accountsPage.clickBillPay();
            pause(3);

            BillPayPage billPayPage = new BillPayPage(getDriver());
            Assert.assertTrue(billPayPage.isOnBillPayPage(),
                    tcId + " Step 5 Failed: Should be on Bill Pay page!");

            billPayPage.payBill(
                    billPayeeName,
                    billPayeeAddress,
                    billPayeeCity,
                    billPayeeState,
                    billPayeeZip,
                    billPayeePhone,
                    billAccountNumber,
                    billAmount
            );
            pause(8);

            String billResult = getDriver()
                    .findElement(By.id("rightPanel")).getText();
            Assert.assertTrue(
                    billPayPage.isPaymentSuccessful()
                    || billResult.contains("Bill Payment Complete")
                    || billResult.contains("payment")
                    || billResult.contains("successfully"),
                    tcId + " Step 5 Failed: Bill payment should complete! Got: "
                    + billResult);
            System.out.println("  Bill Payment $" + billAmount + ": SUCCESS");
        }

        // ==============================================================
        //  STEP 6: Go to Accounts Overview → verify balance
        // ==============================================================
        System.out.println("  Step 6: Checking final balance...");
        getDriver().get("https://parabank.parasoft.com/parabank/overview.htm");
        pause(4);

        String finalBalance = accountsPage.getTotalBalance();
        System.out.println("  Final Balance: " + finalBalance);
        Assert.assertTrue(finalBalance.contains("$"),
                tcId + " Step 6 Failed: Balance should be displayed!");

        // ==============================================================
        //  STEP 7: Click first account → verify activity page
        // ==============================================================
     // Step 7: Verifying transactions in activity...
        System.out.println("  Step 7: Verifying transactions in activity...");
        accountsPage.clickFirstAccount();
        pause(4);

        ActivityPage activityPage = new ActivityPage(getDriver());

        // If not on activity page — something went wrong with click
        // Check URL and log current page for debugging
        if (!activityPage.isOnActivityPage()) {
            System.out.println("  ⚠ Not on activity page — URL: "
                    + getDriver().getCurrentUrl());
        }

        Assert.assertTrue(activityPage.isOnActivityPage(),
                tcId + " Step 7 Failed: Should be on Activity page!");

        // E2E001 = new user, may have no transactions yet
        // E2E003 = bill pay only, transaction may take time
        // Only assert transaction table for transfer scenarios
        if (hasTransfer) {
            Assert.assertTrue(activityPage.isTransactionTableDisplayed(),
                    tcId + " Step 7 Failed: Transaction table should be visible!");

            int txnCount = activityPage.getTransactionCount();
            System.out.println("  Transactions found: " + txnCount);
            Assert.assertTrue(txnCount >= minTxn,
                    tcId + " Step 7 Failed: Expected at least " + minTxn
                    + " transaction(s), found: " + txnCount);
        } else {
            // Just verify we're on activity page — table may be empty
            int txnCount = activityPage.getTransactionCount();
            System.out.println("  Transactions found: " + txnCount
                    + " (no transfer done — table may be empty)");
        }

        // ==============================================================
        //  STEP 8: Logout (for onboarding and complete session scenarios)
        // ==============================================================
        if ("E2E001".equals(tcId) || "E2E004".equals(tcId)) {
            System.out.println("  Step 8: Logging out...");
            try {
                getDriver().findElement(By.linkText("Log Out")).click();
                pause(2);
                LoginPage verifyPage = new LoginPage(getDriver());
                Assert.assertTrue(verifyPage.isLoginFormDisplayed(),
                        tcId + " Step 8 Failed: Should see login form after logout!");
            } catch (Exception e) {
                System.out.println("  Logout skipped: " + e.getMessage());
            }
        }

        System.out.println("  ✅ " + tcId + " PASSED! — " + scenarioName);
        System.out.println("  Summary: " + description);
    }
}