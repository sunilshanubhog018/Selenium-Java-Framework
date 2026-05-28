package utils;

import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class ExcelReader {

    // ================================================================
    //  Read entire sheet as List of Maps
    //  Each row becomes a Map: columnHeader → cellValue
    //
    //  Example Excel:
    //  | Username  | Password  | Expected |
    //  | validuser | Test@1234 | pass     |
    //  | wronguser | wrongpass | fail     |
    //
    //  Returns:
    //  [{Username=validuser, Password=Test@1234, Expected=pass},
    //   {Username=wronguser, Password=wrongpass, Expected=fail}]
    // ================================================================

    public static List<Map<String, String>> readExcel(String filePath, String sheetName) {
        List<Map<String, String>> data = new ArrayList<>();

        try (FileInputStream file = new FileInputStream(filePath);
             Workbook workbook = new XSSFWorkbook(file)) {

            // Get the sheet by name
            Sheet sheet = workbook.getSheet(sheetName);
            if (sheet == null) {
                throw new RuntimeException("Sheet '" + sheetName + "' not found in " + filePath);
            }

            // First row is header row (column names)
            Row headerRow = sheet.getRow(0);
            if (headerRow == null) {
                throw new RuntimeException("Header row is empty in sheet '" + sheetName + "'");
            }

            // Read header names into a list
            List<String> headers = new ArrayList<>();
            for (Cell cell : headerRow) {
                headers.add(getCellValue(cell));
            }

            // Read data rows (starting from row 1, skipping header)
            for (int i = 1; i <= sheet.getLastRowNum(); i++) {
                Row row = sheet.getRow(i);
                if (row == null) continue;  // Skip empty rows

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

    // ================================================================
    //  Read Excel as 2D array — used for TestNG @DataProvider
    //
    //  Returns:
    //  [["validuser", "Test@1234", "pass"],
    //   ["wronguser", "wrongpass", "fail"]]
    // ================================================================

    public static Object[][] readExcelAsArray(String filePath, String sheetName) {
        List<Map<String, String>> data = readExcel(filePath, sheetName);

        if (data.isEmpty()) {
            return new Object[0][0];
        }

        // Get number of columns from first row
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

    // ================================================================
    //  Get cell value as String — handles different cell types
    //  Numbers, text, booleans, formulas all converted to String
    // ================================================================

    private static String getCellValue(Cell cell) {
        if (cell == null) return "";

        switch (cell.getCellType()) {
            case STRING:
                return cell.getStringCellValue().trim();
            case NUMERIC:
                // Check if it's a whole number (avoid 123.0 for 123)
                double numValue = cell.getNumericCellValue();
                if (numValue == Math.floor(numValue)) {
                    return String.valueOf((long) numValue);
                }
                return String.valueOf(numValue);
            case BOOLEAN:
                return String.valueOf(cell.getBooleanCellValue());
            case FORMULA:
                return cell.getStringCellValue().trim();
            case BLANK:
                return "";
            default:
                return "";
        }
    }
}