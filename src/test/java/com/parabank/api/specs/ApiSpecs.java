package com.parabank.api.specs;

import io.restassured.builder.RequestSpecBuilder;
import io.restassured.builder.ResponseSpecBuilder;
import io.restassured.filter.log.LogDetail;
import io.restassured.http.ContentType;
import io.restassured.specification.RequestSpecification;
import io.restassured.specification.ResponseSpecification;

import utils.ConfigReader;

public class ApiSpecs {

    /**
     * The common request setup every API call reuses:
     * base URI + base path (from config), JSON content type, and request logging.
     * This is the API equivalent of BasePage - defined once, reused everywhere.
     */
    public static RequestSpecification requestSpec() {
        return new RequestSpecBuilder()
                .setBaseUri(ConfigReader.get("api.base.uri"))
                .setBasePath(ConfigReader.get("api.base.path"))
                .setContentType(ContentType.JSON)
                .setAccept(ContentType.JSON)
                .log(LogDetail.ALL)          // log every request (like your log().all())
                .build();
    }

    /**
     * A reusable response expectation for the common "success returns 200" case.
     * Tests can use this instead of repeating .statusCode(200) everywhere.
     */
    public static ResponseSpecification responseSpec200() {
        return new ResponseSpecBuilder()
                .expectStatusCode(200)
                .log(LogDetail.ALL)          // log every response
                .build();
    }
}