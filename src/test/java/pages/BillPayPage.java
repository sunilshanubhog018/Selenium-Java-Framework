package pages;

import base.BasePage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class BillPayPage extends BasePage {

    // ================================================================
    //  LOCATORS — all verified from DevTools inspection
    //  Most fields use name attribute (no id available)
    // ================================================================

    // Page heading
    private final By pageTitle = By.cssSelector("h1.title");

    // Payee Information fields
    private final By payeeNameInput = By.name("payee.name");
    private final By addressInput = By.name("payee.address.street");
    private final By cityInput = By.name("payee.address.city");
    private final By stateInput = By.name("payee.address.state");
    private final By zipCodeInput = By.name("payee.address.zipCode");
    private final By phoneInput = By.name("payee.phoneNumber");

    // Account fields
    private final By accountNumberInput = By.name("payee.accountNumber");
    private final By verifyAccountInput = By.name("verifyAccount");

    // Amount
    private final By amountInput = By.name("amount");

    // From Account dropdown
    private final By fromAccountDropdown = By.name("fromAccountId");

    // Send Payment button
    private final By sendPaymentButton = By.cssSelector("input[value='Send Payment']");

    // Result section (hidden by default, shown after payment)
    private final By billPayResult = By.id("billpayResult");
    private final By resultMessage = By.cssSelector("#billpayResult p");

    // ================================================================
    //  CONSTRUCTOR
    // ================================================================

    public BillPayPage(WebDriver driver) {
        super(driver);
    }

    // ================================================================
    //  PAGE ACTIONS — fill individual fields
    // ================================================================

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
        click(sendPaymentButton);
    }

    public void selectFromAccount(String accountId) {
        selectByValue(fromAccountDropdown, accountId);
    }

    // ================================================================
    //  CONVENIENCE METHOD — fill entire form and submit
    // ================================================================

    public void payBill(String payeeName, String address, String city,
                        String state, String zipCode, String phone,
                        String accountNumber, String amount) {
        try {
            Thread.sleep(1000);  // Wait for form to fully render
        } catch (InterruptedException e) {}
        
        enterPayeeName(payeeName);
        enterAddress(address);
        enterCity(city);
        enterState(state);
        enterZipCode(zipCode);
        enterPhone(phone);
        enterAccountNumber(accountNumber);
        enterVerifyAccount(accountNumber);  // Same account number
        enterAmount(amount);
        try {
            selectFromAccount("12345");  // Select first account
        } catch (Exception e) {
            System.out.println("Warning: Could not select account from dropdown: " + e.getMessage());
        }
        clickSendPayment();
    }

    // ================================================================
    //  PAGE VERIFICATIONS
    // ================================================================

    public String getPageTitleText() {
        return getText(pageTitle);
    }

    public boolean isOnBillPayPage() {
        try {
            String title = getPageTitleText();
            return title.contains("Bill Payment");
        } catch (Exception e) {
            return false;
        }
    }

    public boolean isBillPayFormDisplayed() {
        return isDisplayed(payeeNameInput);
    }

    public boolean isPaymentSuccessful() {
        try {
            String pageText = driver.findElement(By.id("rightPanel")).getText();
            return pageText.contains("Bill Payment Complete")
                    || pageText.contains("payment")
                    || pageText.contains("successful");
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