package pages;

import base.BasePage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

import java.util.List;

public class AccountsOverviewPage extends BasePage {

    // ================================================================
    //  LOCATORS
    // ================================================================

    // Page heading
    private final By pageTitle = By.cssSelector("#rightPanel h1.title");

    // Accounts table
    private final By accountsTable = By.id("accountTable");
    private final By accountRows = By.cssSelector("#accountTable tbody tr");
    private final By accountLinks = By.cssSelector("#accountTable tbody tr td:first-child a");
    private final By totalBalance = By.cssSelector("#accountTable tbody tr:last-child td:nth-child(2) b");

    // Left menu navigation links
    private final By openNewAccountLink = By.linkText("Open New Account");
    private final By accountsOverviewLink = By.linkText("Accounts Overview");
    private final By transferFundsLink = By.linkText("Transfer Funds");
    private final By billPayLink = By.linkText("Bill Pay");
    private final By findTransactionsLink = By.linkText("Find Transactions");
    private final By updateContactInfoLink = By.linkText("Update Contact Info");
    private final By requestLoanLink = By.linkText("Request Loan");
    private final By logOutLink = By.linkText("Log Out");

    // Welcome message (top left)
    private final By welcomeMessage = By.cssSelector("#leftPanel p.smallText");

    // ================================================================
    //  CONSTRUCTOR
    // ================================================================

    public AccountsOverviewPage(WebDriver driver) {
        super(driver);
    }

    // ================================================================
    //  PAGE VERIFICATIONS
    // ================================================================

    // Get the page title text ("Accounts Overview")
    public String getPageTitleText() {
        return getText(pageTitle);
    }

    // Check if accounts table is displayed
    public boolean isAccountsTableDisplayed() {
        return isDisplayed(accountsTable);
    }

    // Get number of accounts (rows in the table, excluding header and total)
    public int getAccountCount() {
        List<WebElement> rows = driver.findElements(accountRows);
        // Subtract 1 for the total row
        return rows.size() > 1 ? rows.size() - 1 : 0;
    }

    // Get first account number (link text)
    public String getFirstAccountNumber() {
        List<WebElement> links = driver.findElements(accountLinks);
        if (!links.isEmpty()) {
            return links.get(0).getText().trim();
        }
        return "";
    }

    // Get total balance text
    public String getTotalBalance() {
        return getText(totalBalance);
    }

    // Check if welcome message is displayed
    public boolean isWelcomeMessageDisplayed() {
        return isDisplayed(welcomeMessage);
    }

    // Get welcome message text
    public String getWelcomeMessage() {
        return getText(welcomeMessage);
    }

    // Check if we're on the correct page
    public boolean isOnAccountsOverviewPage() {
        try {
            String title = getPageTitleText();
            return title.contains("Accounts Overview");
        } catch (Exception e) {
            return false;
        }
    }

    // ================================================================
    //  NAVIGATION — click left menu links
    // ================================================================

    public void clickOpenNewAccount() {
        click(openNewAccountLink);
    }

    public void clickAccountsOverview() {
        click(accountsOverviewLink);
    }

    public void clickTransferFunds() {
        click(transferFundsLink);
    }

    public void clickBillPay() {
        click(billPayLink);
    }

    public void clickFindTransactions() {
        click(findTransactionsLink);
    }

    public void clickUpdateContactInfo() {
        click(updateContactInfoLink);
    }

    public void clickRequestLoan() {
        click(requestLoanLink);
    }

    public void clickLogOut() {
        click(logOutLink);
    }

    // ================================================================
    //  ACCOUNT ACTIONS
    // ================================================================

    // Click on the first account number link to see account details
    public void clickFirstAccount() {
        List<WebElement> links = driver.findElements(accountLinks);
        if (!links.isEmpty()) {
            links.get(0).click();
        }
    }
}