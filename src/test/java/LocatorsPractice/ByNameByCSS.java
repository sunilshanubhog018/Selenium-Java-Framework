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

public class ByNameByCSS extends BaseTest {
	
	
	@Test
	public void testDropdownSelection() {
	    driver.get("https://the-internet.herokuapp.com/dropdown");
	    
	    // Using cssSelector to find the dropdown
	    WebElement dropdown = driver.findElement(By.cssSelector("select#dropdown"));
	    Select select = new Select(dropdown);
	    
	    select.selectByVisibleText("Option 2");
	    
	    // Using cssSelector to verify selected option
	    String selected = driver.findElement(
	        By.cssSelector("select#dropdown option[selected]")
	    ).getText();
	    
	    Assert.assertEquals(selected, "Option 2");
	    //driver.quit();
	}
	}
