package LocatorsPractice;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.testng.annotations.Test;
import org.testng.Assert;
public class VerfiyElemetEnabled {
	
		
		@Test
		public void testElementState() {
			WebDriver driver = new ChromeDriver();
		    driver.get("https://the-internet.herokuapp.com/login");
		    
		    WebElement loginButton = driver.findElement(By.className("radius"));
		    
		    
		    Assert.assertTrue(loginButton.isDisplayed(), "Button should be visible");
		    Assert.assertTrue(loginButton.isEnabled(), "Button should be enabled");
		    
		    System.out.println("Is button displayed? " + loginButton.isDisplayed());
		    System.out.println("Is button enabled? " + loginButton.isEnabled());


		}
	}
