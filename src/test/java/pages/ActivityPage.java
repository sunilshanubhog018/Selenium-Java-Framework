package pages;

import base.BasePage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import java.util.List;

public class ActivityPage extends BasePage {

    // ================================================================
    //  LOCATORS — verified from DevTools inspection
    // ================================================================
    private final By pageTitle = By.cssSelector("h1.title");
    private final By transactionTable = By.id("transactionTable");
    private final By transactionRows = By.cssSelector("#transactionTable tbody tr");
    private final By transactionDescriptions = By.cssSelector("#transactionTable tbody tr td:nth-child(2) a");
    private final By debitAmounts = By.cssSelector("#transactionTable tbody tr td:nth-child(3)");
    private final By creditAmounts = By.cssSelector("#transactionTable tbody tr td:nth-child(4)");
    private final By noTransactions = By.id("noTransactions");
    private final By accountDetails = By.id("accountDetails");

    // ================================================================
    //  CONSTRUCTOR
    // ================================================================
    public ActivityPage(WebDriver driver) {
        super(driver);
    }

    // ================================================================
    //  PAGE VERIFICATIONS
    // ================================================================

    public boolean isOnActivityPage() {
        try {
            return getText(pageTitle).contains("Account Activity");
        } catch (Exception e) {
            return false;
        }
    }

    public boolean isTransactionTableDisplayed() {
        return isDisplayed(transactionTable);
    }

    public int getTransactionCount() {
        List<WebElement> rows = driver.findElements(transactionRows);
        return rows.size();
    }

    public boolean hasTransactions() {
        return getTransactionCount() > 0;
    }

    // Get all transaction descriptions
    public List<String> getTransactionDescriptions() {
        List<WebElement> links = driver.findElements(transactionDescriptions);
        List<String> descriptions = new java.util.ArrayList<>();
        for (WebElement link : links) {
            descriptions.add(link.getText().trim());
        }
        return descriptions;
    }

    // Get all debit amounts
    public List<String> getDebitAmounts() {
        List<WebElement> debits = driver.findElements(debitAmounts);
        List<String> amounts = new java.util.ArrayList<>();
        for (WebElement debit : debits) {
            String text = debit.getText().trim();
            if (!text.isEmpty()) {
                amounts.add(text);
            }
        }
        return amounts;
    }

    // Get all credit amounts
    public List<String> getCreditAmounts() {
        List<WebElement> credits = driver.findElements(creditAmounts);
        List<String> amounts = new java.util.ArrayList<>();
        for (WebElement credit : credits) {
            String text = credit.getText().trim();
            if (!text.isEmpty()) {
                amounts.add(text);
            }
        }
        return amounts;
    }

    // Check if a specific amount appears in debit column
    public boolean hasDebitAmount(String amount) {
        return getDebitAmounts().stream()
                .anyMatch(a -> a.contains(amount));
    }

    // Check if a specific amount appears in credit column
    public boolean hasCreditAmount(String amount) {
        return getCreditAmounts().stream()
                .anyMatch(a -> a.contains(amount));
    }

    // Check if a specific description exists
    public boolean hasTransaction(String description) {
        return getTransactionDescriptions().stream()
                .anyMatch(d -> d.toLowerCase().contains(description.toLowerCase()));
    }
}