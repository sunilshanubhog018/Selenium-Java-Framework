package utils;

import org.openqa.selenium.io.FileHandler;
import org.openqa.selenium.support.ui.FluentWait;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.time.Duration;
import java.util.function.Function;

public final class Utils {

    private Utils() {
        // utility class - prevent instantiation
    }

    // ================================================================
    //  DIRECTORY UTILITIES
    // ================================================================

    /** Create multiple directories if they don't exist */
    public static void createDirectories(String... paths) {
        if (paths == null) return;
        for (String p : paths) {
            if (p == null) continue;
            File dir = new File(p);
            if (!dir.exists()) {
                dir.mkdirs();
            }
        }
    }

    /** Delete all files (not subdirectories) inside the given directory */
    public static void cleanDirectory(String dirPath) {
        if (dirPath == null) return;
        File dir = new File(dirPath);
        if (dir.exists() && dir.isDirectory()) {
            File[] files = dir.listFiles();
            if (files != null) {
                for (File f : files) {
                    if (f.isFile()) f.delete();
                }
            }
        }
    }

    // ================================================================
    //  FILE UPLOAD UTILITIES
    // ================================================================

    /** Create a test file with given content (for upload tests) */
    public static File createTestFile(String testDataDir, String fileName, String content) {
        File file = new File(testDataDir + File.separator + fileName);
        try (FileWriter w = new FileWriter(file)) {
            w.write(content);
        } catch (IOException e) {
            throw new RuntimeException("Failed to create test file: " + e.getMessage());
        }
        return file;
    }

    // ================================================================
    //  FILE DOWNLOAD UTILITIES
    // ================================================================

    /**
     * Wait for a downloaded file using FluentWait (condition-based), not Thread.sleep.
     * Polls until file exists, has size &gt; 0, and Chrome .crdownload is gone.
     */
    public static File waitForDownload(String downloadDir, String fileName, int timeoutSec) {
        File file = new File(downloadDir + File.separator + fileName);
        try {
            return new FluentWait<>(file)
                    .withTimeout(Duration.ofSeconds(timeoutSec))
                    .pollingEvery(Duration.ofMillis(500))
                    .ignoring(Exception.class)
                    .until((Function<File, File>) f -> {
                        if (f.exists() && f.length() > 0) {
                            File partial = new File(f.getAbsolutePath() + ".crdownload");
                            if (!partial.exists()) {
                                return f;
                            }
                        }
                        return null;
                    });
        } catch (Exception e) {
            return file.exists() ? file : null;
        }
    }

    // ================================================================
    //  SCREENSHOT UTILITIES
    // ================================================================

    /** Save screenshot to specified directory */
    public static File saveScreenshot(File src, String screenshotDir, String name) {
        File dest = new File(screenshotDir + File.separator + name);
        try {
            FileHandler.copy(src, dest);
        } catch (IOException e) {
            throw new RuntimeException("Failed to save screenshot: " + e.getMessage());
        }
        return dest;
    }
}