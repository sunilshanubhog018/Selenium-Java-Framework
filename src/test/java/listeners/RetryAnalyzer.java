package listeners;

import org.testng.IRetryAnalyzer;
import org.testng.ITestResult;

public class RetryAnalyzer implements IRetryAnalyzer {

    private static final int MAX_RETRY = 1;
    private int retryCount = 0;

    @Override
    public boolean retry(ITestResult result) {
        if (retryCount < MAX_RETRY) {
            retryCount++;
            System.out.println("  🔄 Retrying: " + result.getMethod().getMethodName()
                    + " (attempt " + retryCount + " of " + MAX_RETRY + ")");
            return true;
        }
        return false;
    }
}
