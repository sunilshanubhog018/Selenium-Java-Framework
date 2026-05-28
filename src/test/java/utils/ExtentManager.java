package utils;

import com.aventstack.extentreports.ExtentReports;
import com.aventstack.extentreports.reporter.ExtentSparkReporter;
import com.aventstack.extentreports.reporter.configuration.Theme;

public class ExtentManager {

    // Single instance shared across all tests
    private static ExtentReports extent;

    // ================================================================
    //  getInstance() — creates ExtentReports only once (Singleton)
    //  All tests share the same report file
    // ================================================================
    public static ExtentReports getInstance() {
        if (extent == null) {
            extent = createInstance();
        }
        return extent;
    }

    private static ExtentReports createInstance() {
        // Report saved here
        String reportPath = System.getProperty("user.dir")
                + "/test-output/ExtentReport.html";

        // SparkReporter — modern HTML report
        ExtentSparkReporter sparkReporter = new ExtentSparkReporter(reportPath);

        // Report configuration
        sparkReporter.config().setTheme(Theme.DARK);
        sparkReporter.config().setDocumentTitle("ParaBank Banking Test Report");
        sparkReporter.config().setReportName("Selenium Automation Results");
        sparkReporter.config().setTimeStampFormat("dd MMM yyyy HH:mm:ss");

        ExtentReports extent = new ExtentReports();
        extent.attachReporter(sparkReporter);

        // System information shown in report
        extent.setSystemInfo("Project", "ParaBank Banking Automation");
        extent.setSystemInfo("Framework", "Selenium + TestNG + POM");
        extent.setSystemInfo("Browser", ConfigReader.get("browser"));
        extent.setSystemInfo("Environment", "QA");
        extent.setSystemInfo("Tester", "SDET Automation Engineer");

        return extent;
    }
}