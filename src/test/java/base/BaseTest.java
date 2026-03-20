package base;

import io.github.bonigarcia.wdm.WebDriverManager;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;
import utils.Utils;

import java.io.File;
import java.time.Duration;
import java.util.HashMap;

public class BaseTest {

    protected WebDriver driver;
    protected WebDriverWait wait;

    // Directory paths for upload/download/screenshot tests
    protected String testDataDir;      // Files we create for upload tests
    protected String downloadDir;      // Chrome saves downloaded files here
    protected String screenshotDir;    // Screenshot evidence saved here

    @BeforeMethod
    public void setup() {

        // Create directories (thread-safe for parallel execution)
        testDataDir = System.getProperty("user.dir") + File.separator + "test-data";
        downloadDir = System.getProperty("user.dir") + File.separator + "test-downloads"
                + File.separator + Thread.currentThread().getId();
        screenshotDir = System.getProperty("user.dir") + File.separator + "screenshots";

        Utils.createDirectories(testDataDir, downloadDir, screenshotDir);

        // Clean download dir before each test (fresh start)
        Utils.cleanDirectory(downloadDir);

        WebDriverManager.chromedriver().setup();
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--headless");
        options.addArguments("--no-sandbox");
        options.addArguments("--disable-dev-shm-usage");
        options.addArguments("--window-size=1920,1080");
        options.addArguments("--disable-blink-features=AutomationControlled");

        // Download preferences (auto-download, no dialog)
        HashMap<String, Object> chromePrefs = new HashMap<>();
        chromePrefs.put("download.default_directory", downloadDir);
        chromePrefs.put("download.prompt_for_download", false);
        chromePrefs.put("download.directory_upgrade", true);
        chromePrefs.put("safebrowsing.enabled", true);
        chromePrefs.put("plugins.always_open_pdf_externally", true);
        options.setExperimentalOption("prefs", chromePrefs);

        driver = new ChromeDriver(options);
        driver.manage().window().maximize();
        driver.manage().timeouts().pageLoadTimeout(Duration.ofSeconds(30));
        wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    }

    @AfterMethod
    public void teardown() {
        if (driver != null) {
            driver.quit();
        }
    }
}
