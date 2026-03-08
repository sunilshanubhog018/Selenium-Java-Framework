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

public class Xpathaxes extends BaseTest {

	@Test
	public void testTableNavigation() {
	    driver.get("https://the-internet.herokuapp.com/tables");
	    
	    // Find the "edit" link for user "Smith" using XPath axes
	    WebElement editLink = driver.findElement(
	        By.xpath("//td[text()='Smith']/parent::tr//a[contains(text(),'edit')]")
	    );
	    
	    Assert.assertTrue(editLink.isDisplayed());
	    editLink.click();
	}
	
	
}
