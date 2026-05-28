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

public class VerfiyElemetEnabled extends BaseTest {
	
		
		@Test
		public void testElementState() {
		    driver.get("https://the-internet.herokuapp.com/login");
		    
		    WebElement loginButton = driver.findElement(By.className("radius"));
		    
		    
		    Assert.assertTrue(loginButton.isDisplayed(), "Button should be visible");
		    Assert.assertTrue(loginButton.isEnabled(), "Button should be enabled");
		    
		    System.out.println("Is button displayed? " + loginButton.isDisplayed());
		    System.out.println("Is button enabled? " + loginButton.isEnabled());


		}
	}
