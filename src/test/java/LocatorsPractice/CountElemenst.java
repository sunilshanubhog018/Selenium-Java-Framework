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

public class CountElemenst extends BaseTest {
	
	@Test
	public void testCountElements() {
	    driver.get("https://the-internet.herokuapp.com/checkboxes");
	    
	    List<WebElement> checkboxes = driver.findElements(By.tagName("input"));
	    
	    Assert.assertEquals(checkboxes.size(), 2, "Should have 2 checkboxes");
	}
	

}
