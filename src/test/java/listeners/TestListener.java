package listeners;

import base.BaseTest;
import com.aventstack.extentreports.ExtentReports;
import com.aventstack.extentreports.ExtentTest;
import com.aventstack.extentreports.Status;
import com.aventstack.extentreports.MediaEntityBuilder;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;
import org.testng.ITestContext;
import org.testng.ITestListener;
import org.testng.ITestResult;
import utils.ConfigReader;
import utils.ExtentManager;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.text.SimpleDateFormat;
import java.util.Date;

public class TestListener implements ITestListener {

    private static final String SCREENSHOT_DIR = "test-output/screenshots/";
    private static final ThreadLocal<ExtentTest> extentTest = new ThreadLocal<>();
    private static ExtentReports extent;

    private static ExtentReports getExtent() {
        if (extent == null) {
            extent = ExtentManager.getInstance();
        }
        return extent;
    }

    @Override
    public void onStart(ITestContext context) {
        System.out.println("========================================");
        System.out.println("Test Suite Started: " + context.getName());
        System.out.println("========================================");
        new File(SCREENSHOT_DIR).mkdirs();
    }

    @Override
    public void onFinish(ITestContext context) {
        System.out.println("========================================");
        System.out.println("Test Suite Finished: " + context.getName());
        System.out.println("Total Tests: " + context.getAllTestMethods().length);
        System.out.println("Passed: " + context.getPassedTests().size());
        System.out.println("Failed: " + context.getFailedTests().size());
        System.out.println("Skipped: " + context.getSkippedTests().size());
        System.out.println("========================================");
        getExtent().flush();
    }

    @Override
    public void onTestStart(ITestResult result) {
        System.out.println("\n▶ Starting Test: " + result.getMethod().getMethodName());
        ExtentTest test = getExtent().createTest(
                result.getMethod().getMethodName(),
                result.getMethod().getDescription()
        );
        test.assignCategory(result.getTestClass().getName());
        extentTest.set(test);
    }

    @Override
    public void onTestSuccess(ITestResult result) {
        System.out.println("✓ Test Passed: " + result.getMethod().getMethodName());
        if (extentTest.get() != null) {
            extentTest.get().log(Status.PASS,
                    "Test passed: " + result.getMethod().getMethodName());
        }
        extentTest.remove();
    }

    @Override
    public void onTestFailure(ITestResult result) {
        // Retried failures are reported as skip first; only log final failure
        System.out.println("✗ Test Failed: " + result.getMethod().getMethodName());
        Throwable error = result.getThrowable();
        System.out.println("  Reason: " + (error != null ? error.getMessage() : "unknown"));

        if (extentTest.get() != null) {
            extentTest.get().log(Status.FAIL,
                    "Test failed: " + (error != null ? error.getMessage() : "unknown"));

            if (Boolean.parseBoolean(ConfigReader.get("screenshot.on.failure"))) {
                String screenshotPath = captureScreenshot(result);
                if (screenshotPath != null) {
                    try {
                        extentTest.get().fail("Screenshot on failure:",
                                MediaEntityBuilder.createScreenCaptureFromPath(screenshotPath).build());
                    } catch (Exception e) {
                        System.out.println("  ⚠ Could not attach screenshot to report");
                    }
                }
            }
        }
        extentTest.remove();
    }

    @Override
    public void onTestFailedButWithinSuccessPercentage(ITestResult result) {
        System.out.println("🔄 Test Retrying: " + result.getMethod().getMethodName());
        if (extentTest.get() != null) {
            extentTest.get().log(Status.WARNING,
                    "Test failed — retrying: " + result.getMethod().getMethodName());
        }
    }

    @Override
    public void onTestSkipped(ITestResult result) {
        System.out.println("⊘ Test Skipped: " + result.getMethod().getMethodName());
        // Ensure a node exists (config-method skips may never call onTestStart)
        if (extentTest.get() == null) {
            ExtentTest test = getExtent().createTest(
                    result.getMethod().getMethodName(),
                    result.getMethod().getDescription()
            );
            test.assignCategory(result.getTestClass().getName());
            extentTest.set(test);
        }
        String reason = result.getThrowable() != null
                ? result.getThrowable().getMessage()
                : "Test skipped";
        extentTest.get().log(Status.SKIP, reason);
        extentTest.remove();
    }

    private String captureScreenshot(ITestResult result) {
        try {
            WebDriver driver = BaseTest.getDriver();
            if (driver != null) {
                TakesScreenshot screenshot = (TakesScreenshot) driver;
                File srcFile = screenshot.getScreenshotAs(OutputType.FILE);

                String timestamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
                String testName = result.getMethod().getMethodName();
                String fileName = testName + "_" + timestamp + ".png";
                String destPath = System.getProperty("user.dir")
                        + File.separator + SCREENSHOT_DIR + fileName;

                new File(destPath).getParentFile().mkdirs();
                Files.copy(srcFile.toPath(), Paths.get(destPath));
                System.out.println("  📸 Screenshot saved: " + destPath);
                return destPath;
            }
        } catch (IOException e) {
            System.out.println("  ⚠ Failed to capture screenshot: " + e.getMessage());
        } catch (Exception e) {
            System.out.println("  ⚠ Error during screenshot: " + e.getMessage());
        }
        return null;
    }
}
