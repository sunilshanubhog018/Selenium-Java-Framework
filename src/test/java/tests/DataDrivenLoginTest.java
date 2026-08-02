package tests;

import base.BaseTest;
import org.openqa.selenium.By;
import org.testng.Assert;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;
import pages.AccountsOverviewPage;
import pages.BillPayPage;
import pages.LoginPage;
import pages.RegisterPage;
import pages.TransferFundsPage;
import utils.ConfigReader;
import utils.ExcelReader;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class DataDrivenLoginTest extends BaseTest {

    private LoginPage loginPage;

    @BeforeMethod
    public void navigateToLoginPage() {
        getDriver().get(ConfigReader.get("base.url"));
        loginPage = new LoginPage(getDriver());
    }

    @DataProvider(name = "loginData")
    public Object[][] getLoginData() {
        String filePath = "src/test/resources/testdata/LoginTestData.xlsx";
        List<Map<String, String>> allData = ExcelReader.readExcel(filePath, "Sheet1");

        List<Object[]> filteredData = new ArrayList<>();
        for (Map<String, String> row : allData) {
            if ("Yes".equalsIgnoreCase(row.get("Execute"))) {
                filteredData.add(new Object[]{
                    row.get("TestCaseID"),
                    row.get("Category"),
                    row.get("Description"),
                    row.get("Username"),
                    row.get("Password"),
                    row.get("Expected")
                });
            }
        }
        return filteredData.toArray(new Object[0][0]);
    }

    @Test(dataProvider = "loginData", groups = {"regression", "datadriven"}, description = "Data-driven login test from Excel")
    public void testLoginFromExcel(String testCaseID, String category,
                                    String description, String username,
                                    String password, String expected) {

        System.out.println("Running: " + testCaseID + " [" + category + "] - " + description);

        // ---- HANDLE SPECIAL USERNAMES ----
        if (username.equals("CONFIG_USERNAME")) {
            username = ConfigReader.get("test.username");
            password = ConfigReader.get("test.password");
        }

        if (username.equals("REGISTER_NEW")) {
            String newUsername = "dd_" + System.currentTimeMillis();
            loginPage.clickRegister();
            RegisterPage registerPage = new RegisterPage(getDriver());
            registerPage.waitForUrl("register");
            registerPage.registerUser(
                    "Data", "Driven", "123 Test Street",
                    "Mumbai", "MH", "400001",
                    "9876543210", "111-22-3333",
                    newUsername, password
            );
            registerPage.waitForUrl("overview");
            // Registration auto-logs in — verify directly without re-login
            Assert.assertTrue(getDriver().getCurrentUrl().contains("overview"),
                    testCaseID + ": Login should succeed!");
            System.out.println("  ✓ " + testCaseID + " PASSED!");
            return;
        }

        // ---- PERFORM LOGIN ----
        System.out.println("  Username='" + username + "' Password='" + password + "'");

        if (username != null && !username.isEmpty()) {
            loginPage.enterUsername(username);
        }
        if (password != null && !password.isEmpty()) {
            loginPage.enterPassword(password);
        }
        loginPage.clickLogin();
        // wait for page to respond — either overview (pass) or rightPanel (fail)
        try {
            loginPage.waitForUrl("overview");
        } catch (Exception e) {
            loginPage.waitForVisible(By.id("rightPanel"));
        }

        // ---- VERIFY RESULTS ----
        if (expected.equals("pass")) {
            Assert.assertTrue(getDriver().getCurrentUrl().contains("overview"),
                    testCaseID + ": Login should succeed!");

        } else if (expected.equals("pass_verify_accounts")) {
            Assert.assertTrue(getDriver().getCurrentUrl().contains("overview"),
                    testCaseID + ": Should be on accounts page!");
            String pageText = new AccountsOverviewPage(getDriver()).getRightPanelText();
            Assert.assertTrue(pageText.contains("Account"),
                    testCaseID + ": Should show account info!");

        } else if (expected.equals("pass_relogin")) {
            Assert.assertTrue(getDriver().getCurrentUrl().contains("overview"),
                    testCaseID + ": First login should succeed!");
            new AccountsOverviewPage(getDriver()).logout();
            getDriver().get(ConfigReader.get("base.url"));
            loginPage = new LoginPage(getDriver());
            loginPage.login(username, password);
            loginPage.waitForUrl("overview");
            Assert.assertTrue(getDriver().getCurrentUrl().contains("overview"),
                    testCaseID + ": Re-login should succeed!");

        } else if (expected.equals("pass_transfer")) {
            Assert.assertTrue(getDriver().getCurrentUrl().contains("overview"),
                    testCaseID + ": Login should succeed!");
            new AccountsOverviewPage(getDriver()).clickTransferFunds();
            TransferFundsPage transferPage = new TransferFundsPage(getDriver());
            transferPage.waitForUrl("transfer");
            transferPage.enterAmount("50");
            transferPage.clickTransfer();
            transferPage.waitForVisible(By.cssSelector("#rightPanel h1.title"));
            String transferText = transferPage.getRightPanelText();
            Assert.assertTrue(
                    transferText.contains("Transfer Complete") || transferText.contains("transferred"),
                    testCaseID + ": Transfer should complete! Got: " + transferText);

        } else if (expected.equals("pass_billpay")) {
            Assert.assertTrue(getDriver().getCurrentUrl().contains("overview"),
                    testCaseID + ": Login should succeed!");
            new AccountsOverviewPage(getDriver()).clickBillPay();
            BillPayPage billPayPage = new BillPayPage(getDriver());
            billPayPage.waitForUrl("billpay");
            billPayPage.payBill(
                    "Electric Company", "100 Power Street",
                    "Mumbai", "MH", "400001",
                    "9876543210", "12345", "120"
            );
            billPayPage.waitForVisible(By.cssSelector("#rightPanel h1.title"));
            String billPayText = billPayPage.getRightPanelText();
            Assert.assertTrue(
                    billPayText.contains("Bill Payment Complete") || billPayText.contains("payment")
                    || billPayText.contains("successful"),
                    testCaseID + ": Bill payment should complete! Got: " + billPayText);

        } else {
            try {
                String pageText = new AccountsOverviewPage(getDriver()).getRightPanelText();
                Assert.assertTrue(
                        pageText.contains("Error") || pageText.contains("error")
                        || getDriver().getCurrentUrl().contains("login"),
                        testCaseID + " [" + category + "]: Login should fail for '"
                        + username + "' Got: " + pageText);
            } catch (Exception e) {
                Assert.assertFalse(
                        getDriver().getCurrentUrl().contains("overview"),
                        testCaseID + ": Should not reach accounts page!");
            }
        }
    }
}