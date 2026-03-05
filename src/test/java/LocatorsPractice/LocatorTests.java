package LocatorsPractice;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.Select;
import org.testng.Assert;
import org.testng.annotations.Test;
import java.util.List;

public class LocatorTests {

@Test
public void testValidLogin() {
	WebDriver driver = new ChromeDriver();
    driver.get("https://the-internet.herokuapp.com/login");
    
    driver.findElement(By.id("username")).sendKeys("tomsmith");
    driver.findElement(By.id("password")).sendKeys("SuperSecretPassword!");
    driver.findElement(By.cssSelector("button[type='submit']")).click();
    
    String message = driver.findElement(By.id("flash")).getText();
    Assert.assertTrue(message.contains("You logged into a secure area!"));
}
}//input[@id='username']