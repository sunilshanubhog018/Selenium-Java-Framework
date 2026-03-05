package LocatorsPractice;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.testng.Assert;
import org.testng.annotations.Test;

public class NavigationTest {

    @Test
    public void testNavigateByLink() {

        WebDriver driver = new ChromeDriver();
        driver.get("https://the-internet.herokuapp.com");

        driver.findElement(By.linkText("Dropdown")).click();

        String headingText = driver.findElement(By.tagName("h3")).getText();
        Assert.assertEquals(headingText, "Dropdown List");

        //driver.quit();
    }
}
