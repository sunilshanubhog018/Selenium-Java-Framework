package LocatorsPractice;

import java.util.List;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.decorators.WebDriverDecorator;
import org.testng.annotations.Test;
import org.testng.Assert;

public class Byxpath {

	public class ByXpath {
		
		@Test
		public void testCheckboxSelection() {
			WebDriver driver = new ChromeDriver();
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

}
