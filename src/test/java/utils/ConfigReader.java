package utils;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.Properties;

public class ConfigReader {

    // Properties object holds all key-value pairs from config.properties
    private static Properties properties;

    // Static block - runs ONCE when class is first used
    // Loads the config.properties file into memory
    static {
        try {
            FileInputStream file = new FileInputStream("src/test/resources/config.properties");
            properties = new Properties();
            properties.load(file);
            file.close();
        } catch (IOException e) {
            throw new RuntimeException("Failed to load config.properties: " + e.getMessage());
        }
    }

    // Read any value by its key
    // Example: ConfigReader.get("base.url") returns the URL
    public static String get(String key) {
        String value = properties.getProperty(key);
        if (value == null) {
            throw new RuntimeException("Key '" + key + "' not found in config.properties!");
        }
        return value.trim();
    }
}