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

public class PartialLinkText extends BaseTest {       
        @Test
        public void testPartialLinkNavigation() throws InterruptedException {
            driver.get("https://the-internet.herokuapp.com");
            
            Thread.sleep(3000);
            driver.findElement(By.partialLinkText("Drop")).click();
            // Matches "Drag and Drop"
            
            String heading = driver.findElement(By.tagName("h3")).getText();
            Assert.assertEquals(heading, "Drag and Drop");
        }

	}
