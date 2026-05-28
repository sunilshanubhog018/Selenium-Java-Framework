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

public class TestInvalidLogin extends BaseTest {
	
		@Test
		public void testInvalidLogin() {
		    driver.get("https://the-internet.herokuapp.com/login");
		    
		    driver.findElement(By.id("username")).sendKeys("wronguser");
		    driver.findElement(By.id("password")).sendKeys("wrongpass");
		    driver.findElement(By.cssSelector("button.radius")).click();
		    
		    String error = driver.findElement(By.cssSelector("#flash.error")).getText();
		    Assert.assertTrue(error.contains("Your username is invalid!"));
		}

	}


