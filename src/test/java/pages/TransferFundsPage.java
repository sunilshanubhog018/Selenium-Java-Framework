package pages;

import base.BasePage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.Select;

public class TransferFundsPage extends BasePage {

    // ================================================================
    //  LOCATORS — all verified from DevTools inspection
    // ================================================================

    // Page heading
    private final By pageTitle = By.cssSelector("h1.title");

    // Form fields
    private final By amountInput = By.id("amount");
    private final By fromAccountDropdown = By.id("fromAccountId");
    private final By toAccountDropdown = By.id("toAccountId");
    private final By transferButton = By.cssSelector("input[value='Transfer']");

    // Error messages (hidden by default, shown on validation failure)
    private final By amountError = By.id("amount.errors");

    // Success message (appears after successful transfer)
    private final By successMessage = By.cssSelector("#rightPanel h1.title");
    private final By transferCompleteText = By.cssSelector("#rightPanel p");

    // ================================================================
    //  CONSTRUCTOR
    // ================================================================

    public TransferFundsPage(WebDriver driver) {
        super(driver);
    }

    // ================================================================
    //  PAGE ACTIONS
    // ================================================================

    // Enter transfer amount
    public TransferFundsPage enterAmount(String amount) {
        type(amountInput, amount);
        return this;
    }

    // Select "From" account by visible text (account number)
    public TransferFundsPage selectFromAccount(String accountNumber) {
        selectByValue(fromAccountDropdown, accountNumber);
        return this;
    }

    // Select "To" account by visible text (account number)
    public TransferFundsPage selectToAccount(String accountNumber) {
        selectByValue(toAccountDropdown, accountNumber);
        return this;
    }

    // Click Transfer button
    public void clickTransfer() {
        click(transferButton);
    }

    // Convenience method — fill form and submit in one call
    public void transferFunds(String amount, String fromAccount, String toAccount) {
        enterAmount(amount);
        selectFromAccount(fromAccount);
        selectToAccount(toAccount);
        clickTransfer();
    }

    // ================================================================
    //  PAGE VERIFICATIONS
    // ================================================================

    // Get page title text
    public String getPageTitleText() {
        return getText(pageTitle);
    }

    // Check if we're on Transfer Funds page
    public boolean isOnTransferFundsPage() {
        try {
            String title = getPageTitleText();
            return title.contains("Transfer Funds");
        } catch (Exception e) {
            return false;
        }
    }

    // Check if transfer form is displayed
    public boolean isTransferFormDisplayed() {
        return isDisplayed(amountInput);
    }

    // Check if transfer was successful
    public boolean isTransferComplete() {
        try {
            String title = getPageTitleText();
            return title.contains("Transfer Complete");
        } catch (Exception e) {
            return false;
        }
    }

    // Get success/result message text
    public String getResultMessage() {
        return getText(transferCompleteText);
    }

    // Check if amount error is displayed
    public boolean isAmountErrorDisplayed() {
        try {
            WebElement error = driver.findElement(amountError);
            return error.isDisplayed();
        } catch (Exception e) {
            return false;
        }
    }

    // Get the first account number from "From" dropdown
    public String getFirstAccountNumber() {
        WebElement dropdown = driver.findElement(fromAccountDropdown);
        Select select = new Select(dropdown);
        return select.getFirstSelectedOption().getText().trim();
    }

    // Get count of accounts in "From" dropdown
    public int getFromAccountCount() {
        WebElement dropdown = driver.findElement(fromAccountDropdown);
        Select select = new Select(dropdown);
        return select.getOptions().size();
    }
}