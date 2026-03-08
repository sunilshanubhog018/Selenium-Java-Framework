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

public class Byxpath extends BaseTest {
		
		@Test
		public void testCheckboxSelection() {
		    driver.get("https://the-internet.herokuapp.com/checkboxes");
		    
		    // XPath with contains()
		    List<WebElement> checkboxes = driver.findElements(
		        By.xpath("//input[contains(@type,'check')]")
		    );
		    
		    // First checkbox — click if not already selected
		    if (!checkboxes.get(0).isSelected()) {
		        checkboxes.get(0).click();
		    }
		    
		    Assert.assertTrue(checkboxes.get(0).isSelected());
		    driver.quit();
		}
		// TODO Auto-generated method stub

	}
