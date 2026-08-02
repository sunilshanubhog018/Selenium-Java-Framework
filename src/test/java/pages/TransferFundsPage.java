package pages;

import base.BasePage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.Select;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

public class TransferFundsPage extends BasePage {

    private final By pageTitle = By.cssSelector("#rightPanel h1.title");
    private final By amountInput = By.id("amount");
    private final By fromAccountDropdown = By.id("fromAccountId");
    private final By toAccountDropdown = By.id("toAccountId");
    private final By transferButton = By.cssSelector("input[value='Transfer']");
    private final By amountError = By.id("amount.errors");
    private final By transferCompleteText = By.cssSelector("#rightPanel p");

    public TransferFundsPage(WebDriver driver) {
        super(driver);
    }

    public TransferFundsPage enterAmount(String amount) {
        type(amountInput, amount);
        return this;
    }

    public TransferFundsPage selectFromAccount(String accountNumber) {
        selectByValue(fromAccountDropdown, accountNumber);
        return this;
    }

    public TransferFundsPage selectToAccount(String accountNumber) {
        selectByValue(toAccountDropdown, accountNumber);
        return this;
    }

    public void clickTransfer() {
        String titleBefore = safeTitle();
        click(transferButton);
        waitForTransferOutcome(titleBefore);
    }

    public void transferFunds(String amount, String fromAccount, String toAccount) {
        enterAmount(amount);
        selectFromAccount(fromAccount);
        selectToAccount(toAccount);
        clickTransfer();
    }

    /**
     * Wait until the form page title changes, an amount error appears, or transfer complete shows.
     * Critical: the form already has h1.title "Transfer Funds" — a plain visibility wait is a no-op.
     */
    private void waitForTransferOutcome(String titleBefore) {
        WebDriverWait outcomeWait = new WebDriverWait(driver, Duration.ofSeconds(
                Integer.parseInt(utils.ConfigReader.get("explicit.wait"))));
        try {
            outcomeWait.until(d -> {
                try {
                    if (!d.findElements(amountError).isEmpty() && d.findElement(amountError).isDisplayed()) {
                        return true;
                    }
                } catch (Exception ignored) {
                }
                try {
                    String title = d.findElement(pageTitle).getText().trim();
                    if (!title.isEmpty() && !title.equalsIgnoreCase(titleBefore)) {
                        return true;
                    }
                    if (title.toLowerCase().contains("complete") || title.toLowerCase().contains("error")) {
                        return true;
                    }
                } catch (Exception ignored) {
                }
                try {
                    String panel = d.findElement(By.id("rightPanel")).getText().toLowerCase();
                    if (panel.contains("transfer complete")
                            || panel.contains("transferred")
                            || panel.contains("error")
                            || panel.contains("invalid")) {
                        return true;
                    }
                } catch (Exception ignored) {
                }
                return false;
            });
        } catch (Exception e) {
            // leave current page state for assertions
            System.out.println("  ⚠ Transfer outcome wait timed out (title still: " + safeTitle() + ")");
        }
    }

    private String safeTitle() {
        try {
            return driver.findElement(pageTitle).getText().trim();
        } catch (Exception e) {
            return "";
        }
    }

    public String getPageTitleText() {
        return getText(pageTitle);
    }

    public boolean isOnTransferFundsPage() {
        try {
            String title = getPageTitleText();
            return title.contains("Transfer Funds") || driver.getCurrentUrl().contains("transfer");
        } catch (Exception e) {
            return driver.getCurrentUrl() != null && driver.getCurrentUrl().contains("transfer");
        }
    }

    public boolean isTransferFormDisplayed() {
        return isDisplayed(amountInput);
    }

    public boolean isTransferComplete() {
        try {
            String title = getPageTitleText();
            return title.contains("Transfer Complete");
        } catch (Exception e) {
            return false;
        }
    }

    public String getResultMessage() {
        try {
            return getText(transferCompleteText);
        } catch (Exception e) {
            return getRightPanelText();
        }
    }

    public boolean isAmountErrorDisplayed() {
        try {
            WebElement error = driver.findElement(amountError);
            return error.isDisplayed() && !error.getText().isBlank();
        } catch (Exception e) {
            return false;
        }
    }

    public String getFirstAccountNumber() {
        WebElement dropdown = wait.until(ExpectedConditions.visibilityOfElementLocated(fromAccountDropdown));
        Select select = new Select(dropdown);
        return select.getFirstSelectedOption().getText().trim();
    }

    public int getFromAccountCount() {
        try {
            WebElement dropdown = wait.until(ExpectedConditions.visibilityOfElementLocated(fromAccountDropdown));
            Select select = new Select(dropdown);
            return select.getOptions().size();
        } catch (Exception e) {
            return 0;
        }
    }

    /** Wait for AJAX-populated account dropdowns, then select first from/to option. */
    public void ensureAccountsSelected() {
        try {
            WebDriverWait accountWait = new WebDriverWait(driver, Duration.ofSeconds(
                    Integer.parseInt(utils.ConfigReader.get("explicit.wait"))));
            accountWait.until(d -> {
                try {
                    Select s = new Select(d.findElement(fromAccountDropdown));
                    return !s.getOptions().isEmpty() && !s.getOptions().get(0).getAttribute("value").isBlank();
                } catch (Exception e) {
                    return false;
                }
            });
            Select fromSelect = new Select(driver.findElement(fromAccountDropdown));
            fromSelect.selectByIndex(0);
            Select toSelect = new Select(driver.findElement(toAccountDropdown));
            if (!toSelect.getOptions().isEmpty()) {
                toSelect.selectByIndex(0);
            }
        } catch (Exception e) {
            System.out.println("  ⚠ Could not pre-select transfer accounts: " + e.getMessage());
        }
    }
}
