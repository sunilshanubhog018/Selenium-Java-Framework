package pages;

import base.BasePage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.Select;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

public class BillPayPage extends BasePage {

    private final By pageTitle = By.cssSelector("#rightPanel h1.title");

    private final By payeeNameInput = By.name("payee.name");
    private final By addressInput = By.name("payee.address.street");
    private final By cityInput = By.name("payee.address.city");
    private final By stateInput = By.name("payee.address.state");
    private final By zipCodeInput = By.name("payee.address.zipCode");
    private final By phoneInput = By.name("payee.phoneNumber");

    private final By accountNumberInput = By.name("payee.accountNumber");
    private final By verifyAccountInput = By.name("verifyAccount");

    private final By amountInput = By.name("amount");
    private final By fromAccountDropdown = By.name("fromAccountId");
    private final By sendPaymentButton = By.cssSelector("input[value='Send Payment']");
    private final By billPayResult = By.id("billpayResult");

    public BillPayPage(WebDriver driver) {
        super(driver);
    }

    public BillPayPage enterPayeeName(String name) {
        type(payeeNameInput, name);
        return this;
    }

    public BillPayPage enterAddress(String address) {
        type(addressInput, address);
        return this;
    }

    public BillPayPage enterCity(String city) {
        type(cityInput, city);
        return this;
    }

    public BillPayPage enterState(String state) {
        type(stateInput, state);
        return this;
    }

    public BillPayPage enterZipCode(String zipCode) {
        type(zipCodeInput, zipCode);
        return this;
    }

    public BillPayPage enterPhone(String phone) {
        type(phoneInput, phone);
        return this;
    }

    public BillPayPage enterAccountNumber(String accountNumber) {
        type(accountNumberInput, accountNumber);
        return this;
    }

    public BillPayPage enterVerifyAccount(String accountNumber) {
        type(verifyAccountInput, accountNumber);
        return this;
    }

    public BillPayPage enterAmount(String amount) {
        type(amountInput, amount);
        return this;
    }

    public void clickSendPayment() {
        String titleBefore = safeTitle();
        click(sendPaymentButton);
        waitForBillPayOutcome(titleBefore);
    }

    public void selectFromAccount(String accountId) {
        selectByValue(fromAccountDropdown, accountId);
    }

    public void selectFirstFromAccount() {
        try {
            WebElement dropdown = wait.until(ExpectedConditions.visibilityOfElementLocated(fromAccountDropdown));
            Select select = new Select(dropdown);
            if (!select.getOptions().isEmpty()) {
                select.selectByIndex(0);
            }
        } catch (Exception e) {
            System.out.println("Warning: Could not select from-account: " + e.getMessage());
        }
    }

    public void payBill(String payeeName, String address, String city,
                        String state, String zipCode, String phone,
                        String accountNumber, String amount) {
        enterPayeeName(payeeName);
        enterAddress(address);
        enterCity(city);
        enterState(state);
        enterZipCode(zipCode);
        enterPhone(phone);
        enterAccountNumber(accountNumber);
        enterVerifyAccount(accountNumber);
        enterAmount(amount);
        selectFirstFromAccount();
        clickSendPayment();
    }

    /**
     * Form page already has h1.title "Bill Payment Service" — wait for title change or result panel.
     */
    private void waitForBillPayOutcome(String titleBefore) {
        WebDriverWait outcomeWait = new WebDriverWait(driver, Duration.ofSeconds(
                Integer.parseInt(utils.ConfigReader.get("explicit.wait"))));
        try {
            outcomeWait.until(d -> {
                try {
                    if (!d.findElements(billPayResult).isEmpty() && d.findElement(billPayResult).isDisplayed()) {
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
                    if (panel.contains("bill payment complete")
                            || panel.contains("successfully")
                            || panel.contains("error")
                            || panel.contains("required")
                            || panel.contains("match")) {
                        // still on form if only heading "bill payment service" — require more signal
                        if (panel.contains("bill payment service")
                                && !panel.contains("complete")
                                && !panel.contains("error")
                                && !panel.contains("required")
                                && !panel.contains("match")) {
                            return false;
                        }
                        return true;
                    }
                } catch (Exception ignored) {
                }
                return false;
            });
        } catch (Exception e) {
            System.out.println("  ⚠ Bill pay outcome wait timed out (title still: " + safeTitle() + ")");
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

    public boolean isOnBillPayPage() {
        try {
            String title = getPageTitleText();
            return title.contains("Bill Payment") || driver.getCurrentUrl().contains("billpay");
        } catch (Exception e) {
            return driver.getCurrentUrl() != null && driver.getCurrentUrl().contains("billpay");
        }
    }

    public boolean isBillPayFormDisplayed() {
        return isDisplayed(payeeNameInput);
    }

    public boolean isPaymentSuccessful() {
        try {
            String pageText = driver.findElement(By.id("rightPanel")).getText();
            return pageText.contains("Bill Payment Complete")
                    || pageText.toLowerCase().contains("successfully submitted")
                    || (pageText.toLowerCase().contains("payment") && pageText.toLowerCase().contains("complete"));
        } catch (Exception e) {
            return false;
        }
    }

    public String getResultText() {
        try {
            return driver.findElement(By.id("rightPanel")).getText();
        } catch (Exception e) {
            return "";
        }
    }
}
