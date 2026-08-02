package listeners;

import org.testng.IRetryAnalyzer;
import org.testng.ITestResult;

/**
 * Retries a failed test once. Uses an instance counter (TestNG creates a new
 * RetryAnalyzer instance per test method via RetryListener).
 */
public class RetryAnalyzer implements IRetryAnalyzer {

    private static final int MAX_RETRY = 1;
    private int retryCount = 0;

    @Override
    public boolean retry(ITestResult result) {
        // Do not retry configuration failures or intentional skips
        if (result.getStatus() == ITestResult.SKIP) {
            return false;
        }
        if (result.getThrowable() instanceof org.testng.SkipException) {
            return false;
        }
        if (retryCount < MAX_RETRY) {
            retryCount++;
            System.out.println("  🔄 Retrying: " + result.getMethod().getMethodName()
                    + " (attempt " + retryCount + " of " + MAX_RETRY + ")");
            return true;
        }
        return false;
    }
}
