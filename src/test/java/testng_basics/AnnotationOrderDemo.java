package testng_basics;

import org.testng.annotations.*;

public class AnnotationOrderDemo {

    @BeforeSuite
    public void beforeSuite() {
        System.out.println("1. @BeforeSuite - Global setup");
    }

    @BeforeTest
    public void beforeTest() {
        System.out.println("2. @BeforeTest - Test-level setup");
    }

    @BeforeClass
    public void beforeClass() {
        System.out.println("3. @BeforeClass - Class-level setup");
    }

    @BeforeMethod
    public void beforeMethod() {
        System.out.println("   4. @BeforeMethod - Runs before each test");
    }

    @Test(priority = 1)
    public void testOne() {
        System.out.println("      5. @Test - testOne executing");
    }

    @Test(priority = 2)
    public void testTwo() {
        System.out.println("      5. @Test - testTwo executing");
    }

    @AfterMethod
    public void afterMethod() {
        System.out.println("   6. @AfterMethod - Runs after each test");
    }

    @AfterClass
    public void afterClass() {
        System.out.println("7. @AfterClass - Class-level teardown");
    }

    @AfterTest
    public void afterTest() {
        System.out.println("8. @AfterTest - Test-level teardown");
    }

    @AfterSuite
    public void afterSuite() {
        System.out.println("9. @AfterSuite - Global teardown");
    }
}