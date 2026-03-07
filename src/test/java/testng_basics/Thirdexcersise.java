package testng_basics;

import org.testng.Assert;
import org.testng.annotations.Test;
import org.testng.asserts.SoftAssert;

public class Thirdexcersise {

    @Test
    public void hardAssertDemo() {
        // Hard Assert — execution STOPS at first failure
        System.out.println("Check 1");
        Assert.assertEquals("ICICI", "ICICI");  // PASS

        System.out.println("Check 2");
        Assert.assertEquals("SBI", "SBI");      // FAIL — stops here!

        System.out.println("Check 3");            // This NEVER runs
        Assert.assertEquals(100, 100);
    }

    @Test
    public void softAssertDemo() {
        SoftAssert soft = new SoftAssert();

        // Soft Assert — collects ALL failures, continues execution
        System.out.println("Check 1");
        soft.assertEquals("ICICI", "ICICI");      // PASS

        System.out.println("Check 2");
        soft.assertEquals("SBI", "SBI");          // FAIL — but continues!

        System.out.println("Check 3");
        soft.assertEquals(100, 100);               // PASS — this runs!

        System.out.println("Check 4");
        soft.assertTrue(true, "This will fail");  // FAIL — still continues

        // MANDATORY — reports all collected failures
        soft.assertAll();  // Without this, failures are silently ignored!
    }
}