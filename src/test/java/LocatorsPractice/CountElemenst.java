package LocatorsPractice;

import java.util.List;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.testng.annotations.Test;
import org.testng.Assert;
//import dev.failsafe.internal.util.Assert;

public class CountElemenst {
	
	@Test
	public void testCountElements() {
		WebDriver driver = new ChromeDriver();
	    driver.get("https://the-internet.herokuapp.com/checkboxes");
	    
	    List<WebElement> checkboxes = driver.findElements(By.tagName("input"));
	    
	    Assert.assertEquals(checkboxes.size(), 2, "Should have 2 checkboxes");
	}
	

}
