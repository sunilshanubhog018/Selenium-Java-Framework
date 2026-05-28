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

public class NavigationTest extends BaseTest {

    @Test
    public void testNavigateByLink() {
        driver.get("https://the-internet.herokuapp.com");

        driver.findElement(By.linkText("Dropdown")).click();

        String headingText = driver.findElement(By.tagName("h3")).getText();
        Assert.assertEquals(headingText, "Dropdown List");

        //driver.quit();
    }
}
