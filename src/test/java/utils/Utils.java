package utils;

import org.openqa.selenium.io.FileHandler;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

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

    /** Poll-based wait for downloaded file (checks .crdownload gone) */
    public static File waitForDownload(String downloadDir, String fileName, int timeoutSec) {
        File file = new File(downloadDir + File.separator + fileName);
        long end = System.currentTimeMillis() + (timeoutSec * 1000L);
        while (System.currentTimeMillis() < end) {
            if (file.exists() && file.length() > 0) {
                File partial = new File(file.getAbsolutePath() + ".crdownload");
                if (!partial.exists()) return file;
            }
            try { Thread.sleep(500); } catch (InterruptedException ignored) {}
        }
        return file.exists() ? file : null;
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