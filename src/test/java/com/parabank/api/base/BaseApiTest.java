package com.parabank.api.base;

import io.restassured.RestAssured;
import org.testng.annotations.BeforeClass;

public class BaseApiTest {

    /**
     * Runs once before the tests in a class.
     * API equivalent of BaseTest's driver setup - but no browser needed.
     */
    @BeforeClass(alwaysRun = true)
    public void apiSetup() {

        // The public ParaBank instance occasionally has SSL cert quirks.
        // This tells RestAssured not to fail on cert validation.
        // (Remove later if you move to a local Docker instance.)
        RestAssured.useRelaxedHTTPSValidation();
    }
}