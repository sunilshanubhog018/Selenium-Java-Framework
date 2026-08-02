package utils;

import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class ExcelReader {

    /**
     * Read entire sheet as List of Maps (column header → cell value).
     * Resolves files from the filesystem first, then the test classpath
     * (so CI/packaged runs work with paths like src/test/resources/testdata/...).
     */
    public static List<Map<String, String>> readExcel(String filePath, String sheetName) {
        List<Map<String, String>> data = new ArrayList<>();

        try (InputStream file = openStream(filePath);
             Workbook workbook = new XSSFWorkbook(file)) {

            Sheet sheet = workbook.getSheet(sheetName);
            if (sheet == null) {
                throw new RuntimeException("Sheet '" + sheetName + "' not found in " + filePath);
            }

            Row headerRow = sheet.getRow(0);
            if (headerRow == null) {
                throw new RuntimeException("Header row is empty in sheet '" + sheetName + "'");
            }

            List<String> headers = new ArrayList<>();
            for (Cell cell : headerRow) {
                headers.add(getCellValue(cell));
            }

            for (int i = 1; i <= sheet.getLastRowNum(); i++) {
                Row row = sheet.getRow(i);
                if (row == null) continue;

                Map<String, String> rowData = new LinkedHashMap<>();
                for (int j = 0; j < headers.size(); j++) {
                    Cell cell = row.getCell(j);
                    String value = (cell != null) ? getCellValue(cell) : "";
                    rowData.put(headers.get(j), value);
                }
                data.add(rowData);
            }

        } catch (IOException e) {
            throw new RuntimeException("Failed to read Excel file: " + filePath + " - " + e.getMessage());
        }

        return data;
    }

    public static Object[][] readExcelAsArray(String filePath, String sheetName) {
        List<Map<String, String>> data = readExcel(filePath, sheetName);

        if (data.isEmpty()) {
            return new Object[0][0];
        }

        int cols = data.get(0).size();
        Object[][] result = new Object[data.size()][cols];

        for (int i = 0; i < data.size(); i++) {
            int j = 0;
            for (String value : data.get(i).values()) {
                result[i][j] = value;
                j++;
            }
        }

        return result;
    }

    private static InputStream openStream(String filePath) throws IOException {
        Path path = Paths.get(filePath);
        if (Files.exists(path)) {
            return new FileInputStream(path.toFile());
        }

        // Try under project root (surefire working directory)
        Path fromUserDir = Paths.get(System.getProperty("user.dir"), filePath);
        if (Files.exists(fromUserDir)) {
            return new FileInputStream(fromUserDir.toFile());
        }

        // Classpath: strip common prefixes used in tests
        String resourcePath = filePath
                .replace("\\", "/")
                .replaceFirst("^src/test/resources/", "")
                .replaceFirst("^src/main/resources/", "");
        if (resourcePath.startsWith("/")) {
            resourcePath = resourcePath.substring(1);
        }

        InputStream fromClasspath = ExcelReader.class.getClassLoader().getResourceAsStream(resourcePath);
        if (fromClasspath != null) {
            return fromClasspath;
        }

        // Last try: file name only under testdata/
        String fileName = path.getFileName() != null ? path.getFileName().toString() : filePath;
        InputStream underTestdata = ExcelReader.class.getClassLoader()
                .getResourceAsStream("testdata/" + fileName);
        if (underTestdata != null) {
            return underTestdata;
        }

        throw new IOException("Excel file not found on disk or classpath: " + filePath);
    }

    private static String getCellValue(Cell cell) {
        if (cell == null) return "";

        switch (cell.getCellType()) {
            case STRING:
                return cell.getStringCellValue().trim();
            case NUMERIC:
                double numValue = cell.getNumericCellValue();
                if (numValue == Math.floor(numValue)) {
                    return String.valueOf((long) numValue);
                }
                return String.valueOf(numValue);
            case BOOLEAN:
                return String.valueOf(cell.getBooleanCellValue());
            case FORMULA:
                try {
                    return cell.getStringCellValue().trim();
                } catch (Exception e) {
                    return String.valueOf(cell.getNumericCellValue());
                }
            case BLANK:
                return "";
            default:
                return "";
        }
    }
}
