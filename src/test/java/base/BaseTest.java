package base;

import io.github.bonigarcia.wdm.WebDriverManager;
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
    protected static ThreadLocal<WebDriver> driver = new ThreadLocal<>();
    private static ThreadLocal<WebDriverWait> wait = new ThreadLocal<>();

    public static WebDriver getDriver() {
        return driver.get();
    }

    public static WebDriverWait getWait() {
        return wait.get();
    }

    /**
     * Optional DB reset for local debugging only.
     * NEVER enable against the public ParaBank site in CI — Initialize wipes the
     * shared demo database for every other user/job and causes mass registration/login flakiness.
     * Set -Dparabank.init.db=true (or env PARABANK_INIT_DB=true) to opt in locally.
     */
    @BeforeSuite(alwaysRun = true)
    public void initializeDatabase() {
        boolean initDb = Boolean.parseBoolean(System.getProperty("parabank.init.db",
                System.getenv().getOrDefault("PARABANK_INIT_DB", "false")));
        if (!initDb) {
            System.out.println("ℹ ParaBank DB init skipped (public shared demo). "
                    + "Set -Dparabank.init.db=true only for local isolated instances.");
            return;
        }

        WebDriverManager.chromedriver().setup();
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--headless=new", "--no-sandbox", "--disable-dev-shm-usage",
                "--window-size=1920,1080");
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

    @BeforeMethod(alwaysRun = true)
    public void setUp() {
        String browser = ConfigReader.get("browser");
        boolean headless = Boolean.parseBoolean(ConfigReader.get("headless"))
                || Boolean.parseBoolean(System.getenv("CI"))
                || Boolean.parseBoolean(System.getProperty("headless", "false"));

        WebDriver webDriver;

        switch (browser.toLowerCase()) {
            case "chrome":
                WebDriverManager.chromedriver().setup();
                ChromeOptions chromeOptions = new ChromeOptions();
                chromeOptions.addArguments("--no-sandbox");
                chromeOptions.addArguments("--disable-dev-shm-usage");
                chromeOptions.addArguments("--window-size=1920,1080");
                chromeOptions.addArguments("--disable-gpu");
                chromeOptions.addArguments("--disable-extensions");
                chromeOptions.addArguments("--disable-infobars");
                chromeOptions.addArguments("--disable-notifications");
                // Avoid port conflicts in CI when many Chrome processes start
                chromeOptions.addArguments("--remote-allow-origins=*");
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

        // maximize can fail/no-op in some headless environments — size already set via args
        try {
            if (!headless) {
                webDriver.manage().window().maximize();
            }
        } catch (Exception ignored) {
            // keep configured window size
        }
        webDriver.manage().timeouts().implicitlyWait(Duration.ofSeconds(implicitWait));
        webDriver.manage().timeouts().pageLoadTimeout(Duration.ofSeconds(pageLoadTimeout));

        driver.set(webDriver);
        wait.set(new WebDriverWait(webDriver, Duration.ofSeconds(explicitWait)));
    }

    @AfterMethod(alwaysRun = true)
    public void tearDown() {
        if (driver.get() != null) {
            try {
                driver.get().quit();
            } catch (Exception ignored) {
                // driver may already be dead after a crash
            } finally {
                driver.remove();
                wait.remove();
            }
        }
    }
}
