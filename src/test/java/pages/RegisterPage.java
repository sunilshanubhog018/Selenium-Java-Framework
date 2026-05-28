package pages;

import base.BasePage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;

public class RegisterPage extends BasePage {

    // ================================================================
    //  LOCATORS - ParaBank Registration Form Fields
    //  All fields use id attribute (most reliable locator)
    // ================================================================

    // Personal Information
    private final By firstNameInput = By.id("customer.firstName");
    private final By lastNameInput = By.id("customer.lastName");
    private final By addressInput = By.id("customer.address.street");
    private final By cityInput = By.id("customer.address.city");
    private final By stateInput = By.id("customer.address.state");
    private final By zipCodeInput = By.id("customer.address.zipCode");
    private final By phoneInput = By.id("customer.phoneNumber");
    private final By ssnInput = By.id("customer.ssn");

    // Login Credentials
    private final By usernameInput = By.id("customer.username");
    private final By passwordInput = By.id("customer.password");
    private final By confirmPasswordInput = By.id("repeatedPassword");

    // Submit Button
    private final By registerButton = By.cssSelector("input[value='Register']");

    // Success Message (appears after successful registration)
    private final By successMessage = By.cssSelector("#rightPanel h1.title");
    private final By welcomeMessage = By.cssSelector("#rightPanel p");

    // Error Messages (appear when fields are empty)
    private final By firstNameError = By.id("customer.firstName.errors");
    private final By lastNameError = By.id("customer.lastName.errors");
    private final By usernameError = By.id("customer.username.errors");
    private final By passwordError = By.id("customer.password.errors");

    // ================================================================
    //  CONSTRUCTOR
    // ================================================================

    public RegisterPage(WebDriver driver) {
        super(driver);
    }

    // ================================================================
    //  PAGE ACTIONS - Fill individual fields
    // ================================================================

    public RegisterPage enterFirstName(String firstName) {
        type(firstNameInput, firstName);
        return this;
    }

    public RegisterPage enterLastName(String lastName) {
        type(lastNameInput, lastName);
        return this;
    }

    public RegisterPage enterAddress(String address) {
        type(addressInput, address);
        return this;
    }

    public RegisterPage enterCity(String city) {
        type(cityInput, city);
        return this;
    }

    public RegisterPage enterState(String state) {
        type(stateInput, state);
        return this;
    }

    public RegisterPage enterZipCode(String zipCode) {
        type(zipCodeInput, zipCode);
        return this;
    }

    public RegisterPage enterPhone(String phone) {
        type(phoneInput, phone);
        return this;
    }

    public RegisterPage enterSsn(String ssn) {
        type(ssnInput, ssn);
        return this;
    }

    public RegisterPage enterUsername(String username) {
        type(usernameInput, username);
        return this;
    }

    public RegisterPage enterPassword(String password) {
        type(passwordInput, password);
        return this;
    }

    public RegisterPage enterConfirmPassword(String confirmPassword) {
        type(confirmPasswordInput, confirmPassword);
        return this;
    }

    public void clickRegister() {
        click(registerButton);
    }

    // ================================================================
    //  CONVENIENCE METHOD - Fill entire form and submit
    //  Used when you just want to register quickly
    // ================================================================

    public void registerUser(String firstName, String lastName, String address,
                             String city, String state, String zipCode,
                             String phone, String ssn,
                             String username, String password) {
        enterFirstName(firstName);
        enterLastName(lastName);
        enterAddress(address);
        enterCity(city);
        enterState(state);
        enterZipCode(zipCode);
        enterPhone(phone);
        enterSsn(ssn);
        enterUsername(username);
        enterPassword(password);
        enterConfirmPassword(password);  // Same as password
        clickRegister();
    }

    // ================================================================
    //  PAGE VERIFICATIONS
    // ================================================================

    public String getSuccessTitle() {
        return getText(successMessage);
    }

    public String getWelcomeMessage() {
        return getText(welcomeMessage);
    }

    public boolean isRegistrationSuccessful() {
        try {
            String title = getSuccessTitle();
            return title.toLowerCase().contains("welcome");
        } catch (Exception e) {
            return false;
        }
    }

    public boolean isFirstNameErrorDisplayed() {
        return isDisplayed(firstNameError);
    }

    public boolean isLastNameErrorDisplayed() {
        return isDisplayed(lastNameError);
    }

    public boolean isUsernameErrorDisplayed() {
        return isDisplayed(usernameError);
    }

    public boolean isPasswordErrorDisplayed() {
        return isDisplayed(passwordError);
    }

    public boolean isRegisterFormDisplayed() {
        return isDisplayed(firstNameInput);
    }
}