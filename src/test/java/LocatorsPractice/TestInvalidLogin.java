package LocatorsPractice;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.Select;
import org.testng.Assert;
import org.testng.annotations.Test;
import java.util.List;

public class TestInvalidLogin {
	
		@Test
		public void testInvalidLogin() {
			
			WebDriver driver = new ChromeDriver();
		    driver.get("https://the-internet.herokuapp.com/login");
		    
		    driver.findElement(By.id("username")).sendKeys("wronguser");
		    driver.findElement(By.id("password")).sendKeys("wrongpass");
		    driver.findElement(By.cssSelector("button.radius")).click();
		    
		    String error = driver.findElement(By.cssSelector("#flash.error")).getText();
		    Assert.assertTrue(error.contains("Your username is invalid!"));
		}

	}


