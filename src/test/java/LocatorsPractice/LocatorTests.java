package LocatorsPractice;

import base.BaseTest;

import java.time.Duration;
import java.util.List;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.Select;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.annotations.Test;
import org.testng.Assert;

public class LocatorTests extends BaseTest {

@Test
public void testValidLogin() {
    driver.get("https://the-internet.herokuapp.com/login");
    
    driver.findElement(By.id("username")).sendKeys("tomsmith");
    driver.findElement(By.id("password")).sendKeys("SuperSecretPassword!");
    driver.findElement(By.cssSelector("button[type='submit']")).click();
    
    WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    WebElement flashMessage = wait.until(
        ExpectedConditions.visibilityOfElementLocated(By.id("flash"))
    );
    String message = flashMessage.getText();
    Assert.assertTrue(message.contains("You logged into a secure area!"));
}
}//input[@id='username']