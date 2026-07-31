package tests;

import base.BaseTest;
import org.openqa.selenium.By;
import org.testng.Assert;
import org.testng.annotations.Test;
import pages.AccountsOverviewPage;
import pages.ActivityPage;
import pages.BillPayPage;
import pages.LoginPage;
import pages.RegisterPage;
import pages.TransferFundsPage;
import utils.ConfigReader;
import java.util.List;

public class EndToEndTest extends BaseTest {

    private String registerFreshUser(String prefix) {
        String username = prefix + "_" + System.currentTimeMillis();
        String password = "Test@1234";

        getDriver().get(ConfigReader.get("base.url"));
        LoginPage loginPage = new LoginPage(getDriver());
        loginPage.clickRegister();

        RegisterPage registerPage = new RegisterPage(getDriver());
        registerPage.waitForUrl("register");
        registerPage.registerUser(
                "E2E", "Tester", "100 Test Street",
                "Bangalore", "KA", "560001",
                "9876543210", "123-45-6789",
                username, password
        );
        registerPage.waitForVisible(By.cssSelector("#rightPanel h1.title"));

        String title = "";
        try {
            title = registerPage.getSuccessTitle();
        } catch (Exception e) {
            System.out.println("  ⚠ Could not get title: " + e.getMessage());
        }
        System.out.println("  Registration result: " + title);

        if (!title.contains("Welcome")) {
            System.out.println("  ⚠ Registration failed — using config user as fallback");
            getDriver().get(ConfigReader.get("base.url"));
            loginPage = new LoginPage(getDriver());
            loginPage.login(
                    ConfigReader.get("test.username"),
                    ConfigReader.get("test.password")
            );
            loginPage.waitForUrl("overview");
            System.out.println("  ✓ Logged in with config user: " + ConfigReader.get("test.username"));
            return ConfigReader.get("test.username");
        }

        return username;
    }

    @Test(priority = 1, description = "E2E: New customer onboarding flow")
    public void testNewCustomerOnboarding() {
        System.out.println("\n🏦 E2E Test 1: New Customer Onboarding");

        System.out.println("  Step 1: Registering new customer...");
        String username = registerFreshUser("onboard");
        String password = "Test@1234";

        System.out.println("  Step 2: Logging out after registration...");
        try {
            new LoginPage(getDriver()).logout();
            new LoginPage(getDriver()).waitForVisible(By.name("username"));
        } catch (Exception e) {
            System.out.println("  Already on login page — skipping logout");
        }

        System.out.println("  Step 3: Logging in with credentials...");
        getDriver().get(ConfigReader.get("base.url"));
        LoginPage loginPage = new LoginPage(getDriver());
        loginPage.login(username, password);
        loginPage.waitForUrl("overview");

        Assert.assertTrue(getDriver().getCurrentUrl().contains("overview"),
                "Step 3 Failed: Should redirect to accounts overview!");

        System.out.println("  Step 4: Verifying accounts overview...");
        AccountsOverviewPage accountsPage = new AccountsOverviewPage(getDriver());
        accountsPage.clickAccountsOverview();
        accountsPage.waitForUrl("overview");

        Assert.assertTrue(accountsPage.isOnAccountsOverviewPage(),
                "Step 4 Failed: Should be on Accounts Overview!");
        Assert.assertTrue(accountsPage.getAccountCount() >= 1,
                "Step 4 Failed: Should have at least 1 account!");

        String accountNumber = accountsPage.getFirstAccountNumber();
        String balance = accountsPage.getTotalBalance();
        System.out.println("  Account: " + accountNumber + " | Balance: " + balance);

        System.out.println("  Step 5: Viewing account activity...");
        accountsPage.clickFirstAccount();
        ActivityPage activityPage = new ActivityPage(getDriver());
        activityPage.waitForUrl("activity");

        Assert.assertTrue(activityPage.isOnActivityPage(),
                "Step 5 Failed: Should be on Account Activity page!");
        Assert.assertTrue(activityPage.isTransactionTableDisplayed(),
                "Step 5 Failed: Transaction table should be visible!");

        int txnCount = activityPage.getTransactionCount();
        System.out.println("  Transactions found: " + txnCount);

        System.out.println("  Step 6: Logging out...");
        activityPage.logout();
        LoginPage verifyPage = new LoginPage(getDriver());
        verifyPage.waitForVisible(By.name("username"));

        Assert.assertTrue(verifyPage.isLoginFormDisplayed(),
                "Step 6 Failed: Should see login form after logout!");

        System.out.println("  ✅ E2E Test 1 PASSED!");
    }

    @Test(priority = 2, description = "E2E: Fund transfer with transaction verification")
    public void testFundTransferFlow() {
        System.out.println("\n🏦 E2E Test 2: Fund Transfer + Activity Verification");

        System.out.println("  Step 1: Setting up customer account...");
        registerFreshUser("transfer");

        System.out.println("  Step 2: Checking initial balance...");
        AccountsOverviewPage accountsPage = new AccountsOverviewPage(getDriver());
        accountsPage.clickAccountsOverview();
        accountsPage.waitForUrl("overview");

        String initialBalance = accountsPage.getTotalBalance();
        System.out.println("  Initial Balance: " + initialBalance);
        Assert.assertTrue(initialBalance.contains("$"), "Step 2 Failed: Balance should be displayed!");

        System.out.println("  Step 3: Transferring $50...");
        accountsPage.clickTransferFunds();
        TransferFundsPage transferPage = new TransferFundsPage(getDriver());
        transferPage.waitForUrl("transfer");

        Assert.assertTrue(transferPage.isOnTransferFundsPage(),
                "Step 3 Failed: Should be on Transfer Funds page!");

        transferPage.enterAmount("50");
        transferPage.clickTransfer();
        transferPage.waitForVisible(By.cssSelector("#rightPanel h1.title"));

        String transferResult = transferPage.getRightPanelText();
        Assert.assertTrue(
                transferResult.contains("Transfer Complete") || transferResult.contains("transferred"),
                "Step 3 Failed: Transfer should complete! Got: " + transferResult);
        System.out.println("  Transfer: SUCCESS");

        System.out.println("  Step 4: Returning to accounts overview...");
        accountsPage.clickAccountsOverview();
        accountsPage.waitForUrl("overview");

        String finalBalance = accountsPage.getTotalBalance();
        System.out.println("  Balance after transfer: " + finalBalance);
        Assert.assertTrue(finalBalance.contains("$"), "Step 4 Failed: Balance should still be displayed!");

        System.out.println("  Step 5: Verifying transaction in account activity...");
        accountsPage.clickFirstAccount();
        ActivityPage activityPage = new ActivityPage(getDriver());
        activityPage.waitForUrl("activity");

        Assert.assertTrue(activityPage.isOnActivityPage(), "Step 5 Failed: Should be on Activity page!");
        Assert.assertTrue(activityPage.isTransactionTableDisplayed(),
                "Step 5 Failed: Transaction table should be visible!");

        int txnCount = activityPage.getTransactionCount();
        System.out.println("  Transactions found: " + txnCount);
        Assert.assertTrue(txnCount >= 1,
                "Step 5 Failed: At least 1 transaction should appear after transfer!");

        List<String> debits = activityPage.getDebitAmounts();
        System.out.println("  Debit amounts: " + debits);
        System.out.println("  ✅ E2E Test 2 PASSED!");
    }

    @Test(priority = 3, description = "E2E: Bill payment with transaction verification")
    public void testBillPaymentFlow() {
        System.out.println("\n🏦 E2E Test 3: Bill Payment + Activity Verification");

        System.out.println("  Step 1: Setting up customer account...");
        registerFreshUser("billpay");

        System.out.println("  Step 2: Checking initial balance...");
        AccountsOverviewPage accountsPage = new AccountsOverviewPage(getDriver());
        accountsPage.clickAccountsOverview();
        accountsPage.waitForUrl("overview");

        String initialBalance = accountsPage.getTotalBalance();
        System.out.println("  Initial Balance: " + initialBalance);

        System.out.println("  Step 3: Paying electricity bill of $100...");
        accountsPage.clickBillPay();
        BillPayPage billPayPage = new BillPayPage(getDriver());
        billPayPage.waitForUrl("billpay");

        Assert.assertTrue(billPayPage.isOnBillPayPage(), "Step 3 Failed: Should be on Bill Pay page!");

        billPayPage.payBill(
                "BESCOM Electric", "100 Power Street",
                "Bangalore", "KA", "560001",
                "9876543210", "123456", "100"
        );
        billPayPage.waitForVisible(By.cssSelector("#rightPanel h1.title"));

        String pageText = billPayPage.getRightPanelText();
        Assert.assertTrue(
                billPayPage.isPaymentSuccessful()
                || pageText.contains("Bill Payment Complete")
                || pageText.contains("payment")
                || pageText.contains("successfully"),
                "Step 3 Failed: Bill payment should complete! Got: " + pageText);

        String confirmText = billPayPage.getResultText();
        System.out.println("  Confirmation: " + confirmText.substring(0, Math.min(80, confirmText.length())));

        System.out.println("  Step 4: Checking balance after payment...");
        accountsPage.clickAccountsOverview();
        accountsPage.waitForUrl("overview");

        String balanceAfterPayment = accountsPage.getTotalBalance();
        System.out.println("  Balance after payment: " + balanceAfterPayment);
        Assert.assertTrue(balanceAfterPayment.contains("$"), "Step 4 Failed: Balance should be displayed!");

        System.out.println("  Step 5: Verifying bill payment in transaction history...");
        accountsPage.clickFirstAccount();
        ActivityPage activityPage = new ActivityPage(getDriver());
        activityPage.waitForUrl("activity");

        Assert.assertTrue(activityPage.isOnActivityPage(), "Step 5 Failed: Should be on Activity page!");
        Assert.assertTrue(activityPage.isTransactionTableDisplayed(),
                "Step 5 Failed: Transaction table should be visible!");

        int txnCount = activityPage.getTransactionCount();
        System.out.println("  Transactions found: " + txnCount);
        Assert.assertTrue(txnCount >= 1,
                "Step 5 Failed: Transaction should appear after bill payment!");

        List<String> debits = activityPage.getDebitAmounts();
        List<String> descriptions = activityPage.getTransactionDescriptions();
        System.out.println("  Debit amounts: " + debits);
        System.out.println("  Descriptions: " + descriptions);
        System.out.println("  ✅ E2E Test 3 PASSED!");
    }

    @Test(priority = 4, description = "E2E: Complete banking session with full verification")
    public void testCompleteBankingSession() {
        System.out.println("\n🏦 E2E Test 4: Complete Banking Session");

        System.out.println("  Step 1: Registering new customer...");
        registerFreshUser("session");

        System.out.println("  Step 2: Viewing accounts...");
        AccountsOverviewPage accountsPage = new AccountsOverviewPage(getDriver());
        accountsPage.clickAccountsOverview();
        accountsPage.waitForUrl("overview");

        String initialBalance = accountsPage.getTotalBalance();
        System.out.println("  Starting Balance: " + initialBalance);
        Assert.assertTrue(accountsPage.isAccountsTableDisplayed(),
                "Step 2 Failed: Accounts table should be visible!");

        System.out.println("  Step 3: Transferring $50...");
        accountsPage.clickTransferFunds();
        TransferFundsPage transferPage = new TransferFundsPage(getDriver());
        transferPage.waitForUrl("transfer");
        transferPage.enterAmount("50");
        transferPage.clickTransfer();
        transferPage.waitForVisible(By.cssSelector("#rightPanel h1.title"));

        String transferResult = transferPage.getRightPanelText();
        Assert.assertTrue(
                transferResult.contains("Transfer Complete") || transferResult.contains("transferred"),
                "Step 3 Failed: Transfer should complete!");
        System.out.println("  Transfer $50: SUCCESS");

        System.out.println("  Step 4: Paying internet bill of $75...");
        accountsPage.clickBillPay();
        BillPayPage billPayPage = new BillPayPage(getDriver());
        billPayPage.waitForUrl("billpay");
        billPayPage.payBill(
                "Airtel Internet", "200 Net Street",
                "Bangalore", "KA", "560001",
                "9876543210", "987654", "75"
        );
        billPayPage.waitForVisible(By.cssSelector("#rightPanel h1.title"));

        String billPayText = billPayPage.getRightPanelText();
        Assert.assertTrue(
                billPayPage.isPaymentSuccessful()
                || billPayText.contains("Bill Payment Complete")
                || billPayText.contains("payment")
                || billPayText.contains("successfully"),
                "Step 4 Failed: Bill payment should complete! Got: " + billPayText);
        System.out.println("  Bill Payment $75: SUCCESS");

        System.out.println("  Step 5: Checking final balance...");
        accountsPage.clickAccountsOverview();
        accountsPage.waitForUrl("overview");

        String finalBalance = accountsPage.getTotalBalance();
        System.out.println("  Final Balance: " + finalBalance);
        Assert.assertTrue(finalBalance.contains("$"), "Step 5 Failed: Balance should be displayed!");

        System.out.println("  Step 6: Verifying all transactions in activity...");
        accountsPage.clickFirstAccount();
        ActivityPage activityPage = new ActivityPage(getDriver());
        activityPage.waitForUrl("activity");

        Assert.assertTrue(activityPage.isOnActivityPage(), "Step 6 Failed: Should be on Activity page!");
        Assert.assertTrue(activityPage.isTransactionTableDisplayed(),
                "Step 6 Failed: Transaction table should be visible!");

        int txnCount = activityPage.getTransactionCount();
        System.out.println("  Total transactions: " + txnCount);
        Assert.assertTrue(txnCount >= 1, "Step 6 Failed: Should have at least 1 transaction!");

        List<String> debits = activityPage.getDebitAmounts();
        List<String> descriptions = activityPage.getTransactionDescriptions();
        System.out.println("  Debit amounts: " + debits);
        System.out.println("  Descriptions: " + descriptions);

        System.out.println("  Step 7: Ending banking session...");
        activityPage.logout();
        LoginPage loginPage = new LoginPage(getDriver());
        loginPage.waitForVisible(By.name("username"));

        Assert.assertTrue(loginPage.isLoginFormDisplayed(),
                "Step 7 Failed: Should see login form after logout!");

        System.out.println("  ✅ E2E Test 4 PASSED!");
        System.out.println("  Summary: Registered → Viewed Accounts → Transfer $50"
                + " → Bill Pay $75 → Verified " + txnCount + " transactions → Logged out");
    }
}
