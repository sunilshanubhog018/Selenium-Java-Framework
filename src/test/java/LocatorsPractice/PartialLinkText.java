package LocatorsPractice;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.Select;
import org.testng.Assert;
import org.testng.annotations.Test;
import java.util.List;

public class PartialLinkText {       
        @Test
        public void testPartialLinkNavigation() throws InterruptedException {
    		WebDriver driver = new ChromeDriver();
            driver.get("https://the-internet.herokuapp.com");
            
            Thread.sleep(3000);
            driver.findElement(By.partialLinkText("Drop")).click();
            // Matches "Drag and Drop"
            
            String heading = driver.findElement(By.tagName("h3")).getText();
            Assert.assertEquals(heading, "Drag and Drop");
        }

	}
