package base;

import io.github.bonigarcia.wdm.WebDriverManager;
<<<<<<< HEAD
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.firefox.FirefoxOptions;
import org.openqa.selenium.edge.EdgeDriver;
import org.openqa.selenium.edge.EdgeOptions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.BeforeSuite;
import utils.ConfigReader;

import java.time.Duration;

public class BaseTest {

    // ThreadLocal — each thread gets its OWN driver instance
    // Prevents tests from interfering with each other in parallel
    protected static ThreadLocal<WebDriver> driver = new ThreadLocal<>();
    private static ThreadLocal<WebDriverWait> wait = new ThreadLocal<>();

    // ================================================================
    //  getDriver() — used by TestListener to capture screenshots
    //  used by page objects to interact with browser
    // ================================================================
    public static WebDriver getDriver() {
        return driver.get();
    }

    public static WebDriverWait getWait() {
        return wait.get();
    }

    // ================================================================
    //  @BeforeSuite — runs ONCE before all tests
    //  Initializes ParaBank database
    // ================================================================
    @BeforeSuite
    public void initializeDatabase() {
        WebDriverManager.chromedriver().setup();
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--headless=new", "--no-sandbox", "--disable-dev-shm-usage");
        WebDriver tempDriver = new ChromeDriver(options);

        try {
            tempDriver.get("https://parabank.parasoft.com/parabank/admin.htm");
            Thread.sleep(2000);
            tempDriver.findElement(By.cssSelector("button[value='INIT']")).click();
            Thread.sleep(3000);
            System.out.println("✓ ParaBank database initialized successfully");
        } catch (Exception e) {
            System.out.println("⚠ Database initialization skipped: " + e.getMessage());
        } finally {
            tempDriver.quit();
        }
    }

    // ================================================================
    //  @BeforeMethod — runs before EVERY test
    //  Creates a NEW browser for each thread
    // ================================================================
    @BeforeMethod
    public void setUp() {
        String browser = ConfigReader.get("browser");
        boolean headless = Boolean.parseBoolean(ConfigReader.get("headless"));

        WebDriver webDriver;

        switch (browser.toLowerCase()) {
            case "chrome":
                WebDriverManager.chromedriver().setup();
                ChromeOptions chromeOptions = new ChromeOptions();
                chromeOptions.addArguments("--no-sandbox");
                chromeOptions.addArguments("--disable-dev-shm-usage");
                chromeOptions.addArguments("--window-size=1920,1080");
                if (headless) {
                    chromeOptions.addArguments("--headless=new");
                }
                webDriver = new ChromeDriver(chromeOptions);
                break;

            case "firefox":
                WebDriverManager.firefoxdriver().setup();
                FirefoxOptions firefoxOptions = new FirefoxOptions();
                if (headless) {
                    firefoxOptions.addArguments("--headless");
                }
                webDriver = new FirefoxDriver(firefoxOptions);
                break;

            case "edge":
                EdgeOptions edgeOptions = new EdgeOptions();
                edgeOptions.addArguments("--no-sandbox");
                edgeOptions.addArguments("--disable-dev-shm-usage");
                edgeOptions.addArguments("--window-size=1920,1080");
                if (headless) {
                    edgeOptions.addArguments("--headless=new");
                }
                webDriver = new EdgeDriver(edgeOptions);
                break;

            default:
                throw new RuntimeException("Browser '" + browser + "' not supported!");
        }

        int implicitWait = Integer.parseInt(ConfigReader.get("implicit.wait"));
        int pageLoadTimeout = Integer.parseInt(ConfigReader.get("page.load.timeout"));
        int explicitWait = Integer.parseInt(ConfigReader.get("explicit.wait"));

        webDriver.manage().window().maximize();
        webDriver.manage().timeouts().implicitlyWait(Duration.ofSeconds(implicitWait));
        webDriver.manage().timeouts().pageLoadTimeout(Duration.ofSeconds(pageLoadTimeout));

        // Store in ThreadLocal — this thread's own copy
        driver.set(webDriver);
        wait.set(new WebDriverWait(webDriver, Duration.ofSeconds(explicitWait)));
    }

    // ================================================================
    //  @AfterMethod — runs after EVERY test
    //  Quits browser AND removes from ThreadLocal (prevents memory leak)
    // ================================================================
    @AfterMethod
    public void tearDown() {
        if (driver.get() != null) {
            driver.get().quit();
            driver.remove(); // Critical — prevents memory leak in parallel
            wait.remove();
        }
    }
}
=======
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
>>>>>>> 127ff655b82e19ddd7b71c2cd816b0ebf70f9581
